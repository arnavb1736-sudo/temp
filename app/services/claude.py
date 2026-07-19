from anthropic import Anthropic

from app.config import Config
from app.models.author import Author
from app.models.post import Post
from app.models.settings import AISettings


class ClaudeService:

    def __init__(self):
        self.client = Anthropic(
            api_key=Config.CLAUDE_API_KEY
        )

    def generate_post(
        self,
        post: Post,
        author: Author,
        settings: AISettings
    ) -> str:

        user_prompt = f"""
Topic:
{post.topic}

Additional Information:
{post.additional_information}

Author Style Card:
{author.style_card}
"""

        response = self.client.messages.create(
            model="claude-sonnet-5",
            max_tokens=2500,
            system=settings.system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

        return response.content[0].text.strip()