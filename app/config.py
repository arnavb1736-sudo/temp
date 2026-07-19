import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from the project root
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Config:
    # API Keys
    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

    # Notion Data Source IDs
    CONTENT_DB_ID = os.getenv("NOTION_CONTENT_DB_ID")
    AUTHOR_DB_ID = os.getenv("NOTION_AUTHOR_DB_ID")
    AI_SETTINGS_DB_ID = os.getenv("NOTION_AI_SETTINGS_DB_ID")
    SYSTEM_STATUS_DB_ID = os.getenv("NOTION_SYSTEM_STATUS_DB_ID")

    # Default publish time
    DEFAULT_PUBLISH_HOUR = 10
    DEFAULT_PUBLISH_MINUTE = 0