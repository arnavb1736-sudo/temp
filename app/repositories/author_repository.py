from app.models.author import Author
from app.services.notion import notion


class AuthorRepository:

    def get_author(self, page_id: str) -> Author:

        page = notion.pages.retrieve(page_id=page_id)

        properties = page["properties"]

        name = properties["Author"]["title"][0]["plain_text"]

        style = "".join(
            block["plain_text"]
            for block in properties["Author Style Card"]["rich_text"]
        )

        linkedin = properties["Linkedin URL"]["url"] or ""

        linkedin_connected = properties["Linkedin Connected"]["checkbox"]

        linkedin_person_id = "".join(
            block["plain_text"]
            for block in properties["Linkedin Person ID"]["rich_text"]
        )

        linkedin_access_token = "".join(
            block["plain_text"]
            for block in properties["Linkedin Access Token"]["rich_text"]
        )

        linkedin_refresh_token = "".join(
            block["plain_text"]
            for block in properties["Linkedin Refresh Token"]["rich_text"]
        )

        return Author(
            id=page["id"],
            name=name,
            style_card=style,
            linkedin_url=linkedin,
            linkedin_connected=linkedin_connected,
            linkedin_person_id=linkedin_person_id,
            linkedin_access_token=linkedin_access_token,
            linkedin_refresh_token=linkedin_refresh_token,
        )