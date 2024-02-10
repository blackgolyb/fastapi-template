from functools import lru_cache
from typing import Callable

from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client.apps import StarletteOAuth2App

from src.core.config import get_settings


@lru_cache
def get_oauth() -> OAuth:
    settings = get_settings()
    oauth = OAuth()
    oauth.register(
        name="google",
        client_id=settings.auth.google.client_id,
        client_secret=settings.auth.google.client_secret,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

    return oauth


def create_client_dep(client_name: str) -> Callable[[], StarletteOAuth2App]:
    def create_client() -> StarletteOAuth2App:
        oauth = get_oauth()
        client = oauth.create_client(client_name)

        return client

    return create_client
