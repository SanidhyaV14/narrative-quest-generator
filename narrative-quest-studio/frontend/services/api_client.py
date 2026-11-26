import requests
import streamlit as st
from typing import Optional, Dict, Any, List
try:
    from frontend.config import BACKEND_URL
except (ModuleNotFoundError, ImportError):
    from config import BACKEND_URL


class APIClient:
    """Client for communicating with the Narrative Studio FastAPI backend."""

    def __init__(self, base_url: str = BACKEND_URL):
        self.base_url = base_url.rstrip("/")

    def _get_headers(self, is_json: bool = True) -> Dict[str, str]:
        headers = {}
        if is_json:
            headers["Content-Type"] = "application/json"
        token = st.session_state.get("token")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    def register(self, username: str, email: str, password: str, confirm_password: str) -> Dict[str, Any]:
        url = f"{self.base_url}/api/auth/register"
        payload = {
            "username": username,
            "email": email,
            "password": password,
            "confirm_password": confirm_password
        }
        resp = requests.post(url, json=payload, headers=self._get_headers())
        if not resp.ok:
            detail = resp.json().get("detail", "Registration failed.")
            raise Exception(detail)
        return resp.json()

    def login(self, email: str, password: str) -> Dict[str, Any]:
        url = f"{self.base_url}/api/auth/login"
        payload = {"email": email, "password": password}
        resp = requests.post(url, json=payload, headers=self._get_headers())
        if not resp.ok:
            detail = resp.json().get("detail", "Login failed. Check your credentials.")
            raise Exception(detail)
        return resp.json()

    def get_me(self) -> Dict[str, Any]:
        url = f"{self.base_url}/api/auth/me"
        resp = requests.get(url, headers=self._get_headers())
        if not resp.ok:
            raise Exception("Session expired or invalid. Please log in.")
        return resp.json()

    def generate_story(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/api/generate/story"
        resp = requests.post(url, json=payload, headers=self._get_headers(), timeout=120)
        if not resp.ok:
            detail = resp.json().get("detail", "Story generation failed.")
            raise Exception(detail)
        return resp.json()

    def generate_quest(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/api/generate/quest"
        resp = requests.post(url, json=payload, headers=self._get_headers(), timeout=120)
        if not resp.ok:
            detail = resp.json().get("detail", "Quest generation failed.")
            raise Exception(detail)
        return resp.json()

    def upload_image(self, uploaded_file, category: str = "reference") -> Dict[str, Any]:
        """Uploads a reference image file, runs analysis, and returns the saved paths."""
        file_bytes = uploaded_file.getvalue() if hasattr(uploaded_file, "getvalue") else uploaded_file.read()
        filename = getattr(uploaded_file, "name", "image.png")
        analysis = self.analyze_image(file_bytes=file_bytes, filename=filename)
        path = analysis.get("image_path") or analysis.get("file_path")
        return {"success": True, "image_path": path, "file_path": path, "analysis": analysis}

    def analyze_image(
        self,
        file_bytes: Optional[bytes] = None,
        filename: Optional[str] = None,
        question: Optional[str] = None,
        image_path: Optional[str] = None
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/api/images/analyze"
        headers = self._get_headers(is_json=False)

        if file_bytes is None and image_path:
            import os
            if os.path.exists(image_path):
                with open(image_path, "rb") as f:
                    file_bytes = f.read()
                filename = os.path.basename(image_path)
            else:
                raise Exception(f"Image not found at {image_path}")

        actual_filename = filename or "image.png"
        files = {"file": (actual_filename, file_bytes or b"", "image/png" if actual_filename.endswith(".png") else "image/jpeg")}
        data = {"question": question} if question else {}
        resp = requests.post(url, files=files, data=data, headers=headers, timeout=60)
        if not resp.ok:
            detail = resp.json().get("detail", "Image analysis failed.")
            raise Exception(detail)
        return resp.json()

    def generate_image(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/api/images/generate"
        resp = requests.post(url, json=payload, headers=self._get_headers(), timeout=120)
        if not resp.ok:
            detail = resp.json().get("detail", "Image generation failed.")
            raise Exception(detail)
        return resp.json()

    def save_project(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/api/projects"
        resp = requests.post(url, json=payload, headers=self._get_headers())
        if not resp.ok:
            detail = resp.json().get("detail", "Failed to save project.")
            raise Exception(detail)
        return resp.json()

    def list_projects(self, project_type: Optional[str] = None) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/api/projects"
        params = {"project_type": project_type} if project_type else {}
        resp = requests.get(url, params=params, headers=self._get_headers())
        if not resp.ok:
            detail = resp.json().get("detail", "Failed to fetch projects.")
            raise Exception(detail)
        return resp.json().get("projects", [])

    def get_project(self, project_id: int) -> Dict[str, Any]:
        url = f"{self.base_url}/api/projects/{project_id}"
        resp = requests.get(url, headers=self._get_headers())
        if not resp.ok:
            detail = resp.json().get("detail", "Failed to fetch project details.")
            raise Exception(detail)
        return resp.json()

    def delete_project(self, project_id: int) -> Dict[str, Any]:
        url = f"{self.base_url}/api/projects/{project_id}"
        resp = requests.delete(url, headers=self._get_headers())
        if not resp.ok:
            detail = resp.json().get("detail", "Failed to delete project.")
            raise Exception(detail)
        return resp.json()

    def export_project_txt(self, project_id: int) -> str:
        url = f"{self.base_url}/api/projects/{project_id}/export"
        resp = requests.get(url, headers=self._get_headers())
        if not resp.ok:
            detail = resp.json().get("detail", "Failed to export project.")
            raise Exception(detail)
        return resp.text

    def submit_feedback(self, project_id: int, rating: int, comments: Optional[str] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/api/feedback"
        payload = {"project_id": project_id, "rating": rating, "comments": comments}
        resp = requests.post(url, json=payload, headers=self._get_headers())
        if not resp.ok:
            detail = resp.json().get("detail", "Failed to submit feedback.")
            raise Exception(detail)
        return resp.json()


api_client = APIClient()
