import requests

from app.models.author import Author


class LinkedInService:

    API_URL = "https://api.linkedin.com/rest/posts"

    def publish_post(self, author: Author, content: str):

        if not author.linkedin_connected:
            raise Exception("LinkedIn account not connected.")

        if not author.linkedin_access_token:
            raise Exception("Missing LinkedIn access token.")

        if not author.linkedin_person_id:
            raise Exception("Missing LinkedIn Person ID.")

        headers = {
            "Authorization": f"Bearer {author.linkedin_access_token}",
            "LinkedIn-Version": "202507",
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json",
        }

        payload = {
            "author": f"urn:li:person:{author.linkedin_person_id}",
            "commentary": content,
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": []
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False
        }

        response = requests.post(
            self.API_URL,
            headers=headers,
            json=payload
        )

        if response.status_code not in (200, 201):
            raise Exception(response.text)

        return response.json() if response.text else {}