from fastapi import HTTPException, status
from typing import List, Optional
from uuid import uuid4
from datetime import timedelta
from pydantic import UUID4
from sqlalchemy.orm import Session
from sqlalchemy import text


from app.core.security import hash_password, verify_password

from app.schemas.users import (
    User,
    UserRegitserRequest,
    UserSiginRequest,
    UserResponse,
    UserPaginatedResponse,
    UserTokenResponse,
    UserRole
)
from app.db.user import users
from app.core.security import create_access_token

class UserService:
    def __init__(self, db:Session) -> None:
        self.db = db
    
    def regitser(self, request: UserRegitserRequest) -> UserTokenResponse:

        user = self.db.execute(
            text("SELECT * FROM users WHERE email = :email"),
            {"email": request.email.strip().lower()}
        ).first()
        
        if(user):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User's email already exists"
            )
        
        user_id = str(uuid4())
        self.db.execute(
            text("""
                INSERT INTO users (id, name, email, hashed_password, role)
                VALUES (:id, :name, :email, :hashed_password, :role)
            """),
            {
                "id": user_id,
                "name": request.name.strip().lower(),
                "email": request.email.strip().lower(),
                "hashed_password": hash_password(request.password),
                "role": UserRole.USER.value
            }
        )
        self.db.commit()
        
        token = create_access_token({
            'user_id': user_id
        }, expires_delta=timedelta(minutes=30))
        
        
        return UserTokenResponse(
            access_token=token,
            expires_in=30 * 60,
        )
    
    def sigin(self, request: UserSiginRequest):
        
        user = self.db.execute(
            text("SELECT * FROM users WHERE email = :email"),
            {"email": request.email.strip().lower()}
        ).first() 
                
        if(not user):     
            raise HTTPException( 
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='User email not found'
            )
        
        
        if not verify_password(request.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid User Password'
            )
        
        
        token = create_access_token({
            'user_id': str(user.id)
        }, expires_delta=timedelta(minutes=30))
        
        return UserTokenResponse(
            access_token=token,
            expires_in=30 * 60,
        )
    
    def get_users(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> UserPaginatedResponse:
        
        paginated_users = self.db.execute(
            text("""
                SELECT * FROM users LIMIT :limit OFFSET :offset
            """),
            {
                "limit": limit if limit else 999999999,
                "offset": offset if offset else 0,
            }
        ).fetchall()
        
        users_list = []
        for user in paginated_users:
            users_list.append(
                UserResponse(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    role=user.role,
                )
            )
        
        return UserPaginatedResponse(
            users=users_list,
            total=len(users),
            offset=offset,
            limit=limit,
        )
    
    def get_user_by_id(self, user_id: UUID4) -> UserResponse:
        
        user = self.db.execute(text("""
                
                Select * from users where id = :id                
        """),
            {
                "id": str(user_id)
            }
        ).first()
        
        
        if (not user):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User email not found'
            )
        
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role
        )