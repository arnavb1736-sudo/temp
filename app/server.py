from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse

from app.config import Config
from app.scheduler import start_scheduler
from app.services.linkedin_oauth import LinkedInOAuthService


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield


app = FastAPI(
    title="Elevastra LinkedIn Agent",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {
        "message": "Elevastra LinkedIn Agent Running"
    }


@app.get("/health")
def health():
    return {
        "status": "online"
    }


@app.get("/status")
def status():
    return {
        "scheduler": "running",
        "draft_interval": Config.DRAFT_CHECK_INTERVAL,
        "publish_interval": Config.PUBLISH_CHECK_INTERVAL,
        "auto_generation": Config.ENABLE_AUTO_GENERATION,
        "auto_publish": Config.ENABLE_AUTO_PUBLISH,
    }


@app.get("/auth/linkedin")
def linkedin_login(author_id: str):

    if not Config.LINKEDIN_CLIENT_ID:
        raise HTTPException(
            status_code=500,
            detail="LinkedIn Client ID is not configured."
        )

    if not Config.LINKEDIN_CLIENT_SECRET:
        raise HTTPException(
            status_code=500,
            detail="LinkedIn Client Secret is not configured."
        )

    if not Config.LINKEDIN_REDIRECT_URI:
        raise HTTPException(
            status_code=500,
            detail="LinkedIn Redirect URI is not configured."
        )

    oauth = LinkedInOAuthService()

    authorization_url = oauth.get_authorization_url(
        author_id
    )

    return RedirectResponse(
        authorization_url
    )


@app.get("/auth/linkedin/callback")
def linkedin_callback(
    code: str,
    state: str,
):

    try:

        oauth = LinkedInOAuthService()

        result = oauth.handle_callback(
            code=code,
            state=state,
        )

        return HTMLResponse(
            """
            <!DOCTYPE html>
            <html>
            <head>
                <title>LinkedIn Connected</title>
            </head>
            <body>
                <h2>LinkedIn connected successfully.</h2>
                <p>You can close this window.</p>
            </body>
            </html>
            """
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=f"LinkedIn connection failed: {str(e)}"
        )
