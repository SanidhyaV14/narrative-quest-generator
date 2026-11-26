import os
import json
import re
import logging
from typing import Dict, Any, Optional
import httpx
from fastapi import HTTPException, status
from backend.config import settings

logger = logging.getLogger("nemotron_client")


class NemotronClient:
    """Client for NVIDIA Nemotron text and vision-language endpoints via NVIDIA Build API."""

    def __init__(self):
        self.api_key = settings.NVIDIA_API_KEY
        self.base_url = settings.NEMOTRON_BASE_URL.rstrip("/")
        self.text_model = settings.NEMOTRON_MODEL
        self.vl_model = settings.NEMOTRON_VL_MODEL
        self.timeout = 120.0  # seconds

    def _extract_json(self, raw_text: str) -> Dict[str, Any]:
        """Extracts and parses JSON object from model response, handling markdown blocks, unescaped chars, and truncation."""
        text = raw_text.strip()
        # Remove markdown code fences if present
        if "```json" in text:
            match = re.search(r"```json\s*(.*?)\s*(?:```|$)", text, re.DOTALL)
            if match:
                text = match.group(1).strip()
        elif "```" in text:
            match = re.search(r"```\s*(.*?)\s*(?:```|$)", text, re.DOTALL)
            if match:
                text = match.group(1).strip()

        # Find first '{'
        start = text.find("{")
        if start != -1:
            text = text[start:]

        # 1. Direct parse attempt with strict=False (allows literal newlines/control characters)
        try:
            return json.loads(text, strict=False)
        except Exception:
            pass

        # 2. Attempt outermost curly braces
        end = text.rfind("}")
        if end != -1 and end > 0:
            try:
                return json.loads(text[: end + 1], strict=False)
            except Exception:
                pass

        # 3. Auto-repair truncated JSON (e.g. cut off by max_tokens)
        in_string = False
        escape = False
        stack = []
        repaired_chars = []

        for char in text:
            repaired_chars.append(char)
            if in_string:
                if escape:
                    escape = False
                elif char == '\\':
                    escape = True
                elif char == '"':
                    in_string = False
            else:
                if char == '"':
                    in_string = True
                elif char in '{[':
                    stack.append('}' if char == '{' else ']')
                elif char in '}]':
                    if stack and stack[-1] == char:
                        stack.pop()

        if in_string:
            repaired_chars.append('"')
        while stack:
            repaired_chars.append(stack.pop())

        repaired_text = "".join(repaired_chars)
        try:
            return json.loads(repaired_text, strict=False)
        except Exception:
            pass

        # 4. Fallback: Key-value pattern extraction for narrative schemas
        fallback_dict: Dict[str, Any] = {}
        pattern = r'"([a-zA-Z0-9_]+)"\s*:\s*(?:"([^"\\]*(?:\\.[^"\\]*)*)"|([\d\.]+|true|false|null))'
        for match in re.finditer(pattern, text):
            k = match.group(1)
            v = match.group(2) if match.group(2) is not None else match.group(3)
            fallback_dict[k] = v

        if "complete_story" not in fallback_dict:
            story_match = re.search(r'"complete_story"\s*:\s*"(.*)', text, re.DOTALL)
            if story_match:
                raw_story = story_match.group(1).rstrip('"} \n\r\t')
                fallback_dict["complete_story"] = raw_story

        if fallback_dict and ("title" in fallback_dict or "complete_story" in fallback_dict or "quest_description" in fallback_dict):
            logger.warning("Recovered narrative content using structured regex extraction.")
            return fallback_dict

        logger.error(f"Failed to parse JSON response: {raw_text[:500]}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The AI model returned an incomplete response. Please try generating again with shorter length or more specific prompt."
        )

    async def generate_chat_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 8192,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """Sends chat completion request to NVIDIA-hosted OpenAI-compatible endpoint."""
        target_model = model or self.text_model

        if not self.api_key:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="NVIDIA API key is not configured. Please set NVIDIA_API_KEY in the .env file."
            )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        payload = {
            "model": target_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": 0.95
        }

        url = f"{self.base_url}/chat/completions"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, headers=headers, json=payload)

            if response.status_code == 401:
                logger.error("NVIDIA API authentication failure.")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="NVIDIA API key is invalid or unauthorized."
                )
            elif response.status_code == 429:
                logger.error("NVIDIA API rate limit reached.")
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="NVIDIA API rate limit exceeded. Please wait a moment and try again."
                )
            elif response.status_code >= 400:
                logger.error(f"NVIDIA API error ({response.status_code}): {response.text}")
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"NVIDIA AI service error ({response.status_code}): {response.text[:200]}"
                )

            data = response.json()
            message = data["choices"][0]["message"]
            content = message.get("content") or message.get("reasoning_content") or ""
            parsed_json = self._extract_json(content)
            
            prompt_tokens = data.get("usage", {}).get("prompt_tokens")
            return {
                "data": parsed_json,
                "model_used": target_model,
                "prompt_tokens": prompt_tokens
            }

        except httpx.TimeoutException:
            logger.error("NVIDIA API request timed out.")
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="The request to NVIDIA AI service timed out. Please try again."
            )
        except httpx.RequestError as e:
            logger.error(f"NVIDIA API connection error: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Could not connect to NVIDIA AI service: {str(e)}"
            )

    async def analyze_image_with_vision(
        self,
        base64_image: str,
        user_question: Optional[str] = None,
        image_mime: str = "image/jpeg"
    ) -> Dict[str, Any]:
        """Analyzes an image using NVIDIA vision-language model with base64 data URL."""
        if not self.api_key:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="NVIDIA API key is not configured. Please set NVIDIA_API_KEY in .env."
            )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        from backend.ai.prompt_templates import VISION_ANALYSIS_SYSTEM_PROMPT

        user_content = [
            {
                "type": "text",
                "text": user_question or "Analyze this image in detail for creative storytelling inspiration. Return strictly the requested JSON structure."
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{image_mime};base64,{base64_image}"
                }
            }
        ]

        payload = {
            "model": self.vl_model,
            "messages": [
                {"role": "system", "content": VISION_ANALYSIS_SYSTEM_PROMPT},
                {"role": "user", "content": user_content}
            ],
            "max_tokens": 4096,
            "temperature": 0.3
        }

        url = f"{self.base_url}/chat/completions"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, headers=headers, json=payload)

            if response.status_code >= 400:
                logger.error(f"Vision API error ({response.status_code}): {response.text}")
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"Vision model error ({response.status_code}): {response.text[:200]}"
                )

            data = response.json()
            message = data["choices"][0]["message"]
            content = message.get("content") or message.get("reasoning_content") or ""
            parsed = self._extract_json(content)
            return {
                "data": parsed,
                "model_used": self.vl_model
            }

        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Vision analysis request timed out."
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Vision analysis connection failure: {str(e)}"
            )


nemotron_client = NemotronClient()
