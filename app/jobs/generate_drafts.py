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

        print("Checking Notion for posts...")

        posts = (
            self.content_repo.get_posts_by_status("Not started")
            +
            self.content_repo.get_regeneration_requests()
        )

        print(f"Posts found: {len(posts)}")

        if not posts:
            print("No posts to generate.")
            return

        settings = self.settings_repo.get_settings()

        for post in posts:

            print("--------------------------------------")
            print(f"Topic : {post.topic}")
            print(f"Author: {post.author_id}")
            print("--------------------------------------")

            self.content_repo.update_status(
                post.id,
                "In progress"
            )

            try:

                author = self.author_repo.get_author(
                    post.author_id
                )

                print("Author loaded.")

                draft = self.claude.generate_post(
                    post,
                    author,
                    settings
                )

                print("Claude generation successful.")

                self.content_repo.update_draft(
                    post.id,
                    draft
                )

                print("Draft written to Notion.")

                self.content_repo.mark_ready_for_review(
                    post.id
                )

                self.system_repo.increment_posts_generated()
                self.system_repo.set_online()
                self.system_repo.clear_error()

                print("Finished successfully.")

            except Exception as e:

                print("ERROR")
                print(e)

                self.content_repo.update_error(
                    post.id,
                    str(e)
                )

                self.content_repo.update_status(
                    post.id,
                    "Ready for review"
                )

                self.system_repo.set_error(
                    str(e)
                )