from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.security import verify_token
from app.schemas.users import UserResponse

from app.db.base import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request) -> any: # type: ignore
    from app.db.user import users
    
    user_id = verify_token(request)
    
    with SessionLocal() as db:
        user = db.execute(text(""" 
            select * from users where id=:id
        """), {

            "id": user_id,
        }).first()
    
    if (not user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found in the token'
        )
    
    return user

