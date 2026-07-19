from app.repositories.content_repository import ContentRepository
from app.repositories.author_repository import AuthorRepository
from app.repositories.settings_repository import SettingsRepository
from app.repositories.system_status_repository import SystemStatusRepository

from app.services.claude import ClaudeService


class GenerateDraftsJob:

    def __init__(self):

        self.content_repo = ContentRepository()
        self.author_repo = AuthorRepository()
        self.settings_repo = SettingsRepository()
        self.system_repo = SystemStatusRepository()
        self.claude = ClaudeService()

    def run(self):

        self.system_repo.set_online()
        self.system_repo.clear_error()

        posts = (
            self.content_repo.get_posts_by_status("Not started")
            +
            self.content_repo.get_regeneration_requests()
        )

        if not posts:
            print("No posts to generate.")
            return

        settings = self.settings_repo.get_settings()

        for post in posts:

            print(f"Generating draft for: {post.topic}")

            self.content_repo.update_status(
                post.id,
                "In progress"
            )

            author = self.author_repo.get_author(
                post.author_id
            )

            draft = self.claude.generate_post(
                post,
                author,
                settings
            )

            self.content_repo.update_draft(
                post.id,
                draft
            )

            self.content_repo.mark_ready_for_review(
                post.id
            )

            self.system_repo.increment_posts_generated()

            print("Done.\n")