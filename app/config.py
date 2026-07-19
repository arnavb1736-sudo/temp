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

    # Scheduler
    DRAFT_CHECK_INTERVAL = int(
        os.getenv("DRAFT_CHECK_INTERVAL", 1)
    )

    PUBLISH_CHECK_INTERVAL = int(
        os.getenv("PUBLISH_CHECK_INTERVAL", 5)
    )

    ENABLE_AUTO_GENERATION = (
        os.getenv("ENABLE_AUTO_GENERATION", "true").lower()
        == "true"
    )

    ENABLE_AUTO_PUBLISH = (
        os.getenv("ENABLE_AUTO_PUBLISH", "true").lower()
        == "true"
    )

    # Default publish time
    DEFAULT_PUBLISH_HOUR = 10
    DEFAULT_PUBLISH_MINUTE = 0