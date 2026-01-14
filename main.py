from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers.users import router as user_router
from app.core.config import settings
from app.db.schema import create_tables
from app.utils.create_admin import create_admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    
    print("Creating database tables if not exist...")
    create_tables()
    create_admin()
    
    print("Startup complete.")
    yield
    
    # Shutdown code
    print("Shutting down...")
    

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    lifespan=lifespan,
)


# 
app.include_router(user_router, prefix='/users', tags=['Users'])


if __name__ == '__main__':
    from uvicorn import run
    run(
        'main:app',
        reload=settings.APP_DEBUG,
        port=settings.APP_POSRT,
        host=settings.APP_HOST,
    )