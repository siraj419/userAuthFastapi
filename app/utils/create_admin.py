from sqlalchemy import text
from uuid import uuid4

from app.db.base import SessionLocal
from app.schemas.users import UserRole
from app.core.security import hash_password

def create_admin():
    try:
        with SessionLocal() as db:
            db.execute(text("""
                Insert into users (id, name, email, hashed_password, role)
                values (:id, :name, :email, :hashed_password, :role)
            """),
                {
                    "id": str(uuid4()),
                    "name": "admin",
                    "email": "admin@app.com",
                    "hashed_password": hash_password("admin"),
                    "role": UserRole.ADMIN.value
                }
            )
            db.commit()
        print("Admin user created successfully")
    except:
        print("Admin user already exits")