from fastapi import HTTPException, status
from typing import List, Optional
from uuid import uuid4
from datetime import timedelta
from pydantic import UUID4

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
    def __init__(self) -> None:
        pass
    
    
    def regitser(self, request: UserRegitserRequest) -> UserTokenResponse:
        
        for user in users:
            if user.email == request.email:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User's email alreday exists"
                )

        new_user  = User(
                        id=uuid4(),
                        name=request.name.strip().lower(),
                        email=request.email.strip().lower(),
                        role=UserRole.USER,
                        password=request.password
                    )

        users.append(new_user)
        
        token = create_access_token({
            'user_id': str(new_user.id)
        }, expires_delta=timedelta(minutes=30))
        
        
        return UserTokenResponse(
            access_token=token,
            expires_in=30 * 60,
        )
    
    def sigin(self, request: UserSiginRequest):
        for user in users:
            if user.email == request.email:
                if user.password != request.password:
                    raise HTTPException(
                                status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Invalid User Password'
                            )
                
                token = create_access_token({
                    'user_id': str(user.id)
                }, expires_delta=timedelta(minutes=30))
                
                
                return UserTokenResponse(
                    access_token=token,
                    expires_in=30 * 60,
                )
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User email not found'
        )
    
    def get_users(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> UserPaginatedResponse:
        
        paginated_users = users
        if offset:
            paginated_users = paginated_users[offset:]
        if limit:
            paginated_users = paginated_users[:limit]
        
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
        for user in users:
            if str(user.id) == str(user_id):
                return UserResponse(
                    id=user_id,
                    name=user.name,
                    email=user.email,
                    role=user.role,
                )
            
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User email not found'
        )