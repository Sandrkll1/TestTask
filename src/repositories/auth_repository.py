from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from src.models.user import User
from src.services.user import AuthService, UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthRepository:

    def __init__(self,
                 access_token_expire_minutes: int,
                 refresh_token_expire_days: int,
                 secrete_key: str,
                 algorithm: str,
                 user_service: UserService,
                 auth_service: AuthService):
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days
        self.secrete_key = secrete_key
        self.algorithm = algorithm

        self.user_service = user_service
        self.auth_service = auth_service

    async def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secrete_key, algorithm=self.algorithm)

    async def create_refresh_token(self, user_id: int) -> str:
        to_encode = {"sub": str(user_id)}
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secrete_key, algorithm=self.algorithm)

    async def verify_token(self, token: str) -> int:
        try:
            payload = jwt.decode(token, self.secrete_key, algorithms=[self.algorithm])
            user_id = self._extract_user_id_from_payload(payload)
            return user_id
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    async def verify_refresh_token(self, token: str) -> int:
        try:
            payload = jwt.decode(token, self.secrete_key, algorithms=[self.algorithm])
            user_id = self._extract_user_id_from_payload(payload)

            auth_record = await self.auth_service.get(user_id=user_id, refresh_token=token)
            if auth_record is None or auth_record.denied:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Refresh token not found or revoked"
                )

            return user_id
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

    def _extract_user_id_from_payload(self, payload: dict) -> int:
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        try:
            return int(user_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user ID in token"
            )

    async def authenticate_user(self, email: str, password: str) -> User | None:
        user = await self.user_service.get(email=email)
        if not user:
            return None
        if not pwd_context.verify(password, user.hashed_password):
            return None
        return user
