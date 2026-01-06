from fastapi import Request, HTTPException, status
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

from app.schemas.users import UserResponse
from app.db.user import users

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def verify_token(request: Request):
    authorization_header = request.headers.get('Authorization', None)
    if not authorization_header:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Please provide Authorization header'
            )
    token_type, token = authorization_header.split(' ')
    
    if token_type != 'Bearer' or not token:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid auth token'
            )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid auth token'
            )
    except InvalidTokenError:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid auth token'
            )
        
    return user_id

def get_current_user(request: Request) -> UserResponse:
    user_id = verify_token(request)

    for user in users:
        if str(user.id) == str(user_id):
            return UserResponse(
                id=user_id,
                name=user.name,
                email=user.email,
                role=user.role
            )
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='User not found in the token'
    )

def hash_password(password: str):
    return password_hash.hash(password)

def verify_password(txt_password:str, hash_password:str):
    return password_hash.verify(txt_password, hash_password)