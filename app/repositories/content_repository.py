from app.config import Config
from app.models.post import Post
from app.services.notion import notion


class ContentRepository:

    def _page_to_post(self, page):

        properties = page["properties"]

        topic = ""
        if properties["Topic"]["title"]:
            topic = properties["Topic"]["title"][0]["plain_text"]

        additional_information = "".join(
            block["plain_text"]
            for block in properties["Additional Information"]["rich_text"]
        )

        draft = "".join(
            block["plain_text"]
            for block in properties["Draft"]["rich_text"]
        )

        author_id = ""
        if properties["Author"]["relation"]:
            author_id = properties["Author"]["relation"][0]["id"]

        publish_date = None
        if properties["Post On Date"]["date"]:
            publish_date = properties["Post On Date"]["date"]["start"]

        regenerate = properties["Regenerate Draft"]["checkbox"]

        image_url = None

        if "Image" in properties and properties["Image"]["files"]:
            image_file = properties["Image"]["files"][0]

            if image_file["type"] == "file":
                image_url = image_file["file"]["url"]

            elif image_file["type"] == "external":
                image_url = image_file["external"]["url"]

        return Post(
            id=page["id"],
            topic=topic,
            additional_information=additional_information,
            status=properties["Status"]["status"]["name"],
            draft=draft,
            publish_date=publish_date,
            author_id=author_id,
            regenerate_draft=regenerate,
            image_url=image_url,
        )

    def get_posts_by_status(self, status: str):

        response = notion.data_sources.query(
            data_source_id=Config.CONTENT_DB_ID,
            filter={
                "property": "Status",
                "status": {
                    "equals": status
                }
            }
        )

        return [self._page_to_post(page) for page in response["results"]]

    def get_regeneration_requests(self):

        response = notion.data_sources.query(
            data_source_id=Config.CONTENT_DB_ID,
            filter={
                "and": [
                    {
                        "property": "Status",
                        "status": {
                            "equals": "Ready for review"
                        }
                    },
                    {
                        "property": "Regenerate Draft",
                        "checkbox": {
                            "equals": True
                        }
                    }
                ]
            }
        )

        return [self._page_to_post(page) for page in response["results"]]

    def update_status(self, page_id: str, status: str):
        notion.pages.update(
            page_id=page_id,
            properties={
                "Status": {
                    "status": {
                        "name": status
                    }
                }
            }
        )

    def update_draft(self, page_id: str, draft: str):

        chunks = [
            draft[i:i + 2000]
            for i in range(0, len(draft), 2000)
        ]

        notion.pages.update(
            page_id=page_id,
            properties={
                "Draft": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": chunk
                            }
                        }
                        for chunk in chunks
                    ]
                }
            }
        )

    def update_error(self, page_id: str, error: str):
        notion.pages.update(
            page_id=page_id,
            properties={
                "Error Message(if any)": {
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

    def clear_error(self, page_id: str):
        notion.pages.update(
            page_id=page_id,
            properties={
                "Error Message(if any)": {
                    "rich_text": []
                }
            }
        )

    def clear_regenerate_checkbox(self, page_id: str):
        notion.pages.update(
            page_id=page_id,
            properties={
                "Regenerate Draft": {
                    "checkbox": False
                }
            }
        )

    def mark_ready_for_review(self, page_id: str):
        self.clear_error(page_id)
        self.clear_regenerate_checkbox(page_id)
        self.update_status(page_id, "Ready for review")

    def mark_published(self, page_id: str):
        self.clear_error(page_id)
        self.update_status(page_id, "Published")

    def get_posts_ready_to_publish(self):
        return self.get_posts_by_status("Approved")
