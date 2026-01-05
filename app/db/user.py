from app.schemas.users import User
from app.schemas.users import UserRole
from uuid import uuid4

users : list[User] = [
    User(
        id=uuid4(),
        name='admin',
        email='admin@gmail.com',
        password='admin',
        role=UserRole.ADMIN
    )
]