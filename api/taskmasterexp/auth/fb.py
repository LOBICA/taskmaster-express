from authlib.integrations.httpx_client import AsyncOAuth2Client
from pydantic import BaseModel

from taskmasterexp.settings import FB_CLIENT_ID, FB_CLIENT_SECRET, FB_REDIRECT

authorization_base_url = "https://www.facebook.com/dialog/oauth"
token_endpoint = "https://graph.facebook.com/oauth/access_token"


class FbInfo(BaseModel):
    token: str
    fb_user_id: str
    name: str
    email: str


async def get_authorization_url() -> str:
    # Initialize the OAuth2 client
    client = AsyncOAuth2Client(
        client_id=FB_CLIENT_ID, redirect_uri=FB_REDIRECT, scope="email"
    )

    # Get the authorization URL
    authorization_url, _ = client.create_authorization_url(authorization_base_url)

    # Redirect the user to the authorization URL and obtain the authorization code
    return authorization_url


async def get_fb_info(response_url: str) -> FbInfo:
    client = AsyncOAuth2Client(
        client_id=FB_CLIENT_ID, client_secret=FB_CLIENT_SECRET, redirect_uri=FB_REDIRECT
    )
    # Exchange the authorization code for an access token
    token = await client.fetch_token(
        token_endpoint, authorization_response=response_url
    )
    user_info_response = await client.get(
        "https://graph.facebook.com/me?fields=id,name,email"
    )
    user_info_response.raise_for_status()

    user_info = user_info_response.json()

    return FbInfo(
        token=token["access_token"],
        fb_user_id=user_info["id"],
        name=user_info["name"],
        email=user_info["email"],
    )


async def get_fb_info_from_token(token: str) -> FbInfo:
    client = AsyncOAuth2Client(
        client_id=FB_CLIENT_ID,
        client_secret=FB_CLIENT_SECRET,
    )
    client.token = {
        "access_token": token,
        "token_type": "Bearer",
    }
    user_info_response = await client.get(
        "https://graph.facebook.com/me?fields=id,name,email"
    )
    user_info_response.raise_for_status()

    user_info = user_info_response.json()

    return FbInfo(
        token=token,
        fb_user_id=user_info["id"],
        name=user_info["name"],
        email=user_info["email"],
    )
