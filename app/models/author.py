from dataclasses import dataclass


@dataclass
class Author:

    id: str
    name: str
    style_card: str
    linkedin_url: str

    linkedin_connected: bool
    linkedin_person_id: str
    linkedin_access_token: str
    linkedin_refresh_token: str