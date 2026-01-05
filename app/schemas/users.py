from pydantic import BaseModel, UUID4, EmailStr
from enum import Enum
from typing import List, Optional

class UserRole(Enum):
    ADMIN = 'admin'
    USER = 'user'


class User(BaseModel):
    id: UUID4
    name: str
    email: EmailStr
    role: UserRole
    password: str

class UserRegitserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserSiginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID4
    name: str
    email: EmailStr
    role: UserRole

class UserPaginatedResponse(BaseModel):
    users: List[UserResponse]
    total: int
    offset: Optional[int] = None
    limit: Optional[int] = None

class UserTokenResponse(BaseModel):
    access_token: str
    expires_in: int