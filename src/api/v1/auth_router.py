from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from src.di import Container
from src.repositories.auth_repository import AuthRepository, pwd_context
from src.schemas.auth import (GetRefreshToken, RefreshTokenRead, UserCreate,
                              UserLogin)

router = APIRouter(prefix="/auth")


@router.post("/", response_model=RefreshTokenRead)
@inject
async def login_for_access_token(
        user_auth: UserLogin,
        auth: Annotated[AuthRepository, Depends(Provide[Container.auth_repository])]
):
    user = await auth.authenticate_user(user_auth.email, user_auth.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = await auth.create_access_token(data={"sub": str(user.id)})
    refresh_token = await auth.create_refresh_token(user.id)

    await auth.auth_service.create(user_id=user.id, refresh_token=refresh_token)

    return RefreshTokenRead(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/register")
@inject
async def register_user(
        user: UserCreate,
        auth: Annotated[AuthRepository, Depends(Provide[Container.auth_repository])]
):
    stmt = await auth.user_service.get(email=user.email)

    if stmt:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    new_user = await auth.user_service.create(
        email=user.email,
        hashed_password=pwd_context.hash(user.password)
    )

    access_token = await auth.create_access_token(data={"sub": str(new_user.id)})
    refresh_token = await auth.create_refresh_token(new_user.id)

    await auth.auth_service.create(user_id=new_user.id, refresh_token=refresh_token)

    return RefreshTokenRead(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/token/refresh", response_model=RefreshTokenRead)
@inject
async def refresh_access_token(
        rt: GetRefreshToken,
        auth: Annotated[AuthRepository, Depends(Provide[Container.auth_repository])]
):
    user_id = await auth.verify_refresh_token(rt.refresh_token)

    await auth.auth_service.mark_denied(refresh_token=rt.refresh_token)
    user = await auth.user_service.get(user_id=user_id)

    new_access_token = await auth.create_access_token(data={"sub": str(user_id)})
    new_refresh_token = await auth.create_refresh_token(user_id=user_id)

    await auth.auth_service.create(user_id=user.id, refresh_token=new_refresh_token)
    return RefreshTokenRead(access_token=new_access_token, refresh_token=new_refresh_token, token_type="bearer")
