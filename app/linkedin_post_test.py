import requests

ACCESS_TOKEN = "AQWeBoXAlBbwN-XE2wE9CDJdi7P3kGsjLzs9dMWaodu_i-mi-X0rJikrUmEAL1JusSnkmeyY0AYyTkXljECRaq10cnajCKzFhbTPseJYtvo8UQlMlYRTEv2P_r8a2cPJRFJIJhESfxpVYdI79bo7RYnHC8lD3lO204ieJHRLE3YkNar2r7U7NNKIe8UKbXdV5Vj1Lgn88M0ClL5eoTZPvly1Ksi0MnKuMIusEIodEdgHeUpInLg5dlnQMiyme-2QnRQzkftD8AZk3evjtt2kNfx7aki_RljWPgnFIq42-iwHdNQekI-yz7aaEFcccnYkAx5Ai9Xa24tGpRPZppwpYFJY4ml8Iw"

PERSON_ID = "mZYVy6Rq1O"

url = "https://api.linkedin.com/rest/posts"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "LinkedIn-Version": "202507",
    "X-Restli-Protocol-Version": "2.0.0",
    "Content-Type": "application/json",
}

payload = {
    "author": f"urn:li:person:{PERSON_ID}",
    "commentary": "Hello from my Python LinkedIn automation 🚀",
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
    url,
    headers=headers,
    json=payload,
)

print(response.status_code)
print(response.text)