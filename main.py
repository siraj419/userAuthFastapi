from fastapi import FastAPI

from app.routers.users import router as user_router


app = FastAPI()

# 
app.include_router(user_router, prefix='/users', tags=['Users'])


if __name__ == '__main__':
    from uvicorn import run
    run(
        'main:app',
        reload=True,
        port=9090,
        host='0.0.0.0'
    )