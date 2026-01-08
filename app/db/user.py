from app.schemas.users import User
from app.schemas.users import UserRole
from uuid import uuid4

from app.core.security import hash_password

users : list[User] = [
    User(
        id=uuid4(),
        name='admin',
        email='admin@gmail.com',
        password=hash_password('admin'),
        role=UserRole.ADMIN
    )
]


# db = {
#     'users': users,
#     'tasks': [
#         {
#             'id': uuid4(),
#             'title': 'Sample Task 1',
#             'description': 'This is a sample task description',
#             'owner_id': users[0].id
#         }
#     ]
# }