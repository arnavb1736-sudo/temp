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
Author Style Card:
{author.style_card}

Topic:
{post.topic}

Additional Information:
{post.additional_information}
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

        # Claude 5 may return ThinkingBlocks before TextBlocks.
        # Extract only the text blocks.
        output = []

        for block in response.content:
            if getattr(block, "type", None) == "text":
                output.append(block.text)

        if not output:
            raise Exception("Claude returned no text.")

        return "\n".join(output).strip()