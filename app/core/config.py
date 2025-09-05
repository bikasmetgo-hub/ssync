from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str
    env: str
    debug: bool
    
    database_url: str
    redis_url: str
    
    jwt_secret: str
    jwt_algorithm: str
    jwt_expire_minutes: int
    
    class Config:
        env_file = '.env'
        

settings = Settings()
