from authlib.integrations.starlette_client import OAuthError
from fastapi import APIRouter, Request

from src.api.dependencies import GoogleOAuthDep, SessionDep
from src.crud.user import UserCRUD
from src.models.user import User, UserCreate

router = APIRouter()


@router.post("/register")
async def register(user_creation_data: UserCreate, session: SessionDep) -> User:
    crud = UserCRUD(session)
    user = await crud.create(user_creation_data)
    return user


# @router.post("/login")
# async def login(user_creation_data: UserLogin, session: SessionDep) -> User:
#     crud = UserCRUD(session)
#     user = await crud.create(user_creation_data)
#     return user


@router.get("/login/google")
async def login_google(request: Request, oauth: GoogleOAuthDep) -> None:
    redirect_uri = request.url_for("auth_google")
    return await oauth.authorize_redirect(request, redirect_uri)


@router.get("/auth/google")
async def auth_google(
    request: Request, oauth: GoogleOAuthDep, session: SessionDep
) -> dict:
    # provider = "google"
    try:
        token = await oauth.authorize_access_token(request)
        userinfo = token.get("userinfo")

        # service = UserService(session)
        # if service.is_user_exist_by_account(provider=provider, id=userinfo["sub"]):
        #     user = service.register_user_with_account(provider=provider, info=userinfo)
        # else:
        #     user = service.get_user_with_account_account(provider=provider, id=userinfo["sub"])

        # access_token = service.login(user)
        return {"userinfo": userinfo}

    except OAuthError as e:
        print(e)
        return {"error": "Something went wrong"}
