from app.repositories.content_repository import ContentRepository
from app.repositories.author_repository import AuthorRepository

from app.services.linkedin import LinkedInService


class PublishPostsJob:

    def __init__(self):

        self.content_repo = ContentRepository()
        self.author_repo = AuthorRepository()

        self.linkedin = LinkedInService()

    def run(self):

        posts = self.content_repo.get_posts_ready_to_publish()

        if not posts:
            print("No posts to publish.")
            return

        for post in posts:

            print(f"Publishing: {post.topic}")

            self.content_repo.update_status(
                post.id,
                "Publishing"
            )

            try:

                author = self.author_repo.get_author(
                    post.author_id
                )

                self.linkedin.publish_post(
                    author,
                    post.draft,
                    post.image_url
                )

                self.content_repo.mark_published(
                    post.id
                )

                print("Published.\n")

            except Exception as e:

                self.content_repo.update_error(
                    post.id,
                    str(e)
                )

                self.content_repo.update_status(
                    post.id,
                    "Approved"
                )

                print(e)
