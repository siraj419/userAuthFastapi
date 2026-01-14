from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    # App settings
    APP_NAME : str = "User Management API"
    APP_DESCRIPTION : str = "API for managing users with registration, authentication, and user info retrieval functionalities."
    APP_POSRT : int = 9090
    APP_HOST : str = "0.0.0.0"
    APP_DEBUG : bool = True
    
    
    # JWT settings
    JWT_SECRET_KEY : str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    JWT_ALGORITHM : str = "HS256"
    
    # Database settings
    DATABASE_URL : str = "sqlite:///./database.db"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
    

settings = Settings()