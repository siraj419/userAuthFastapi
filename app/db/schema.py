
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import Depends

from app.db.base import SessionLocal

user_schema = """
    Create table if not exists users (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL,
        role TEXT NOT NULL
    );
"""

tasks_schema = """
    Create table if not exists tasks (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        owner_id TEXT NOT NULL,
        FOREIGN KEY (owner_id) REFERENCES users (id)
    );
"""

def create_tables():
    with SessionLocal() as db:
        db.execute(text(user_schema))
        db.execute(text(tasks_schema))
        db.commit()