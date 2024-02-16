from pydantic import BaseSettings

class Settings(BaseSettings):

    DB_USERNAME: str
    DB_PASSWORD: int
    DB_NAME: str
    DB_HOST: str
    DB_PORT=3306

class Config:
    env_file = ".env"