from fastapi import FastAPI

from app.routers.users import router as user_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
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