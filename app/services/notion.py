from notion_client import Client

from app.config import Config

notion = Client(auth=Config.NOTION_API_KEY)