from fastapi import FastAPI
from fastapi.responses import RedirectResponse

import requests
import jwt

CLIENT_ID = "8682iill2o22nr"
CLIENT_SECRET = "WPL_AP1.5yo6LJjmhTna8oEY.P5uoMA=="

REDIRECT_URI = "http://localhost:8000/callback"

app = FastAPI()


@app.get("/")
def login():

    auth_url = (
        "https://www.linkedin.com/oauth/v2/authorization"
        "?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        "&scope=openid%20profile%20email%20w_member_social"
    )

    return RedirectResponse(auth_url)


@app.get("/callback")
def callback(code: str):

    token = requests.post(
        "https://www.linkedin.com/oauth/v2/accessToken",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    ).json()

    print("\nTOKEN")
    print(token)

    claims = jwt.decode(
        token["id_token"],
        options={"verify_signature": False},
    )

    print("\nID TOKEN CLAIMS")
    print(claims)

    return {
        "access_token": token["access_token"],
        "claims": claims,
    }   