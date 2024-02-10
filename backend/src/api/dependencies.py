from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.oauth import OAuth, StarletteOAuth2App, create_client_dep, get_oauth
from src.core.config import Settings, get_settings
from src.db import get_session

SettingsDep = Annotated[Settings, Depends(get_settings)]
SessionDep = Annotated[AsyncSession, Depends(get_session)]
OAuthDep = Annotated[OAuth, Depends(get_oauth)]
GoogleOAuthDep = Annotated[StarletteOAuth2App, Depends(create_client_dep("google"))]
