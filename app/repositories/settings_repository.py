from app.config import Config
from app.models.settings import AISettings
from app.services.notion import notion


class SettingsRepository:

    def get_settings(self) -> AISettings:

        response = notion.data_sources.query(
            data_source_id=Config.AI_SETTINGS_DB_ID
        )

        if not response["results"]:
            raise Exception("AI Settings page not found.")

        page = response["results"][0]

        prompt = "".join(
            block["plain_text"]
            for block in page["properties"]["System Default Prompt"]["rich_text"]
        )

        return AISettings(
            system_prompt=prompt
        )