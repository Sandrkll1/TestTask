from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class GetRefreshToken(BaseModel):
    refresh_token: str


class RefreshTokenRead(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
