import requests

from app.models.author import Author


class LinkedInService:

    API_URL = "https://api.linkedin.com/rest/posts"
    IMAGE_API_URL = "https://api.linkedin.com/rest/images"

    LINKEDIN_VERSION = "202607"

    def _get_headers(self, access_token: str, content_type: str = "application/json"):
        return {
            "Authorization": f"Bearer {access_token}",
            "LinkedIn-Version": self.LINKEDIN_VERSION,
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": content_type,
        }

    def _upload_image(self, author: Author, image_url: str):
        """
        Download the image from the URL stored in Notion,
        initialize a LinkedIn image upload, and upload the image.
        """

        # Download image from Notion/external URL
        image_response = requests.get(image_url, timeout=30)

        if image_response.status_code != 200:
            raise Exception(
                f"Failed to download image: "
                f"{image_response.status_code} {image_response.text}"
            )

        image_data = image_response.content

        if not image_data:
            raise Exception("Downloaded image is empty.")

        # The current implementation publishes as the LinkedIn member.
        owner = f"urn:li:person:{author.linkedin_person_id}"

        # Step 1: Initialize LinkedIn image upload
        initialize_payload = {
            "initializeUploadRequest": {
                "owner": owner
            }
        }

        initialize_response = requests.post(
            f"{self.IMAGE_API_URL}?action=initializeUpload",
            headers=self._get_headers(author.linkedin_access_token),
            json=initialize_payload,
            timeout=30,
        )

        if initialize_response.status_code not in (200, 201):
            raise Exception(
                f"LinkedIn image initialization failed: "
                f"{initialize_response.status_code} "
                f"{initialize_response.text}"
            )

        initialize_data = initialize_response.json()

        try:
            upload_url = initialize_data["value"]["uploadUrl"]
            image_urn = initialize_data["value"]["image"]
        except (KeyError, TypeError):
            raise Exception(
                f"LinkedIn image initialization returned an unexpected response: "
                f"{initialize_response.text}"
            )

        # Step 2: Upload the actual image bytes
        upload_response = requests.put(
            upload_url,
            data=image_data,
            headers={
                "Content-Type": image_response.headers.get(
                    "Content-Type",
                    "application/octet-stream"
                )
            },
            timeout=60,
        )

        if upload_response.status_code not in (200, 201):
            raise Exception(
                f"LinkedIn image upload failed: "
                f"{upload_response.status_code} "
                f"{upload_response.text}"
            )

        return image_urn

    def publish_post(
        self,
        author: Author,
        content: str,
        image_url: str | None = None
    ):

        if not author.linkedin_connected:
            raise Exception("LinkedIn account not connected.")

        if not author.linkedin_access_token:
            raise Exception("Missing LinkedIn access token.")

        if not author.linkedin_person_id:
            raise Exception("Missing LinkedIn Person ID.")

        headers = self._get_headers(author.linkedin_access_token)

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

        # If an image exists, upload it first and attach the
        # resulting LinkedIn image URN to the post.
        if image_url:
            image_urn = self._upload_image(
                author,
                image_url
            )

            payload["content"] = {
                "media": {
                    "id": image_urn
                }
            }

        response = requests.post(
            self.API_URL,
            headers=headers,
            json=payload,
            timeout=30,
        )

        if response.status_code not in (200, 201):
            raise Exception(response.text)

        return response.json() if response.text else {}
