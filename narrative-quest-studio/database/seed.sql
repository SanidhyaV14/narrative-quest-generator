-- ====================================================================
-- Narrative Studio - Seed Data
-- ====================================================================

USE narrative_studio;

-- Insert a default demo user (password is "password123", hashed with bcrypt)
-- $2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW is bcrypt for "password123"
INSERT INTO users (id, username, email, password_hash, created_at)
VALUES 
(1, 'demo_writer', 'demo@narrativestudio.ai', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', NOW())
ON DUPLICATE KEY UPDATE id=id;

-- Sample Story Project
INSERT INTO projects (id, user_id, title, project_type, input_data, generated_content, created_at, updated_at)
VALUES (
    1,
    1,
    'Whispers of the Obsidian Spire',
    'STORY',
    JSON_OBJECT(
        'genre', 'Fantasy',
        'theme', 'Betrayal',
        'setting', 'The floating spires of Aethelgard',
        'character', 'Kaelen, a rogue archivist',
        'tone', 'Suspenseful',
        'length', 'Medium'
    ),
    JSON_OBJECT(
        'title', 'Whispers of the Obsidian Spire',
        'genre', 'Fantasy',
        'introduction', 'High above the mist-cloaked chasms of Aethelgard, the Obsidian Spire hummed with forbidden celestial energy.',
        'main_characters', 'Kaelen (a rogue archivist seeking forbidden scrolls), Master Vane (the spire overseer harboring an ancient secret).',
        'setting', 'Aethelgard, a fragmented realm connected by floating crystalline bridges and ancient obsidian watchtowers.',
        'conflict', 'Kaelen discovers the spire does not preserve lost histories—it feeds upon them.',
        'complete_story', 'Kaelen stepped carefully across the bridge of humming quartz. The wind whispered of forgotten names. Inside the archives, the glyphs pulsed an eerie violet. When Master Vane blocked the vault door, cold iron met shimmering sorcery...',
        'ending', 'Kaelen shattered the core crystal, plunging the spire into silence, escaping into the dawn with the final true chronicle of their world.',
        'suggested_image_description', 'A rogue cloaked archivist looking up at a towering floating obsidian spire glowing with violet celestial energy, fantasy digital painting, dramatic clouds.'
    ),
    NOW(),
    NOW()
)
ON DUPLICATE KEY UPDATE id=id;

-- Sample Quest Project
INSERT INTO projects (id, user_id, title, project_type, input_data, generated_content, created_at, updated_at)
VALUES (
    2,
    1,
    'The Sunken Relic of Eldoria',
    'GAME_QUEST',
    JSON_OBJECT(
        'game_genre', 'RPG',
        'theme', 'Treasure Hunt',
        'setting', 'Submerged ruins of an ancient coastal cathedral',
        'difficulty', 'Medium',
        'character', 'Aria the Tide Hunter',
        'missions', 3,
        'ending_preference', 'Victory'
    ),
    JSON_OBJECT(
        'title', 'The Sunken Relic of Eldoria',
        'quest_description', 'Recover the legendary Coral Heart from the drowned crypts of the Cathedral of Eldoria before the abyssal cult awakens the Leviathan.',
        'background_story', 'A century ago, Eldoria fell into the sea after an alchemical ritual went awry. Now, its sacred relics pulse under the tides.',
        'main_character', 'Aria the Tide Hunter, armed with a runic harpoon and breath-holding charms.',
        'npcs', 'Elder Marcus (the harbor keeper who provides underwater maps), Silas the Deep Trader (sells protective sea-glass charms).',
        'objectives', '1. Infiltrate the Drowned Nave.\n2. Disable the three Abyssal Ward stones.\n3. Retrieve the Coral Heart and defeat the Deep Warden.',
        'challenges', 'Submerged labyrinth navigation, limited oxygen timer, hostile Abyssal Lurkers, and puzzle runes on the sanctuary gates.',
        'dialogue', 'Aria: "The tide is turning, Marcus. If that heart pulses once more, the bay will drown."\nMarcus: "Then take this ward-breaker. Don\'t look directly into the coral\'s light."',
        'rewards', '500 Gold Coins, Coral Heart Trinket (+20% Water Resistance), Tide Hunter Crest.',
        'ending', 'With the Deep Warden pacified, Aria surfaces under the moonlight, the Coral Heart glowing safely inside her runic satchel.',
        'suggested_illustration_description', 'An underwater fantasy RPG quest scene, a brave hunter with a glowing runic spear inside a submerged gothic cathedral illuminated by bioluminescent coral.'
    ),
    NOW(),
    NOW()
)
ON DUPLICATE KEY UPDATE id=id;
