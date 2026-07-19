from app.jobs.generate_drafts import GenerateDraftsJob
from app.jobs.publish_posts import PublishPostsJob


GenerateDraftsJob().run()
PublishPostsJob().run()