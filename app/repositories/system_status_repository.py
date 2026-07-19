from app.config import Config
from app.services.notion import notion


class SystemStatusRepository:

    def __init__(self):

        response = notion.data_sources.query(
            data_source_id=Config.SYSTEM_STATUS_DB_ID
        )

        if not response["results"]:
            raise Exception("System Status row not found.")

        self.page = response["results"][0]
        self.page_id = self.page["id"]

    def set_online(self):

        notion.pages.update(
            page_id=self.page_id,
            properties={
                "Status": {
                    "status": {
                        "name": "Online"
                    }
                }
            }
        )

    def set_offline(self):

        notion.pages.update(
            page_id=self.page_id,
            properties={
                "Status": {
                    "status": {
                        "name": "Offline"
                    }
                }
            }
        )

    def increment_posts_generated(self):

        page = notion.pages.retrieve(self.page_id)

        current = page["properties"]["Total Posts Generated"]["number"] or 0

        notion.pages.update(
            page_id=self.page_id,
            properties={
                "Total Posts Generated": {
                    "number": current + 1
                }
            }
        )

    def set_error(self, error: str):

        notion.pages.update(
            page_id=self.page_id,
            properties={
                "Error (if any)": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": error
                            }
                        }
                    ]
                }
            }
        )

    def clear_error(self):

        notion.pages.update(
            page_id=self.page_id,
            properties={
                "Error (if any)": {
                    "rich_text": []
                }
            }
        )