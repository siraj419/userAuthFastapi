from fastapi import APIRouter, Query, Depends, HTTPException, status
from typing import Optional
from pydantic import UUID4

from app.schemas.users import (
    UserRegitserRequest,
    UserSiginRequest,
    UserResponse,
    UserPaginatedResponse,
    UserTokenResponse,
    UserRole
)
from app.services.users import UserService
from app.core.security import get_current_user

router = APIRouter()

@router.post('/register', response_model=UserTokenResponse)
def register_user(
    request: UserRegitserRequest,
):
    """
        Registers a new user (create acccount)
    """
    
    user_service = UserService()
    return user_service.regitser(request)

@router.post('/signin', response_model=UserTokenResponse)
def signin(
    request: UserSiginRequest,
):
    """
        Signin to the account
    """
    
    user_service = UserService()
    return user_service.sigin(request)

@router.get('/me', response_model=UserResponse)
def get_me(
    user : UserResponse = Depends(get_current_user)
):
    """
        Get currently logged in user infromation.
    """
    
    return user

@router.get('/', response_model=UserPaginatedResponse)
def get_users(
    offset: Optional[int] = Query(None, ge=0),
    limit: Optional[int] = Query(None, ge=1),
    user : UserResponse = Depends(get_current_user),
):
    """
        Get all users info.
    """
    
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only admin can access this resource'
        )
    
    user_service = UserService()
    return user_service.get_users(
        offset=offset,
        limit=limit
    )

@router.get('/{user_id}', response_model=UserResponse)
def get_user(
    user_id: UUID4,
    user : UserResponse = Depends(get_current_user)
):
    """
        Get a specific user info by id
    """
    
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only admin can access this resource'
        )
    
    user_service = UserService()
    return user_service.get_user_by_id(user_id)

def delete_user():
    """
        - Only admin can delete any user.
        - Admin cannot delete himself.
    """
    
    pass

def update_user():
    """
        Any user can update the information of it.
        Admin can update the information of any user.
    """
    pass

def change_role():
    """
        Only admin can change the user role
    """
    pass

def change_password():
    """
        Any user can  change it's password.
        Admin can change the password of any user.
    """
    pass

