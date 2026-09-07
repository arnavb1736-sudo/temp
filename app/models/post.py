from dataclasses import dataclass
from datetime import datetime


@dataclass
class Post:
    id: str
    topic: str
    additional_information: str
    status: str
    draft: str
    publish_date: datetime | None
    author_id: str
    regenerate_draft: bool
    image_url: str | None = None
