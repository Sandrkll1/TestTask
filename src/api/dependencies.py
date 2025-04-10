from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Security, status

from src.di import Container
from src.models.user import User
from src.repositories.auth_repository import AuthRepository, oauth2_scheme


@inject
async def get_current_user(
        token: str = Security(oauth2_scheme),
        auth_repository: AuthRepository = Depends(Provide[Container.auth_repository])
) -> User:
    user_id = await auth_repository.verify_token(token)
    user = await auth_repository.user_service.get(user_id=user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    return user
