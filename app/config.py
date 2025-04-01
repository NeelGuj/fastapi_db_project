from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

# .env because .env is file in root directory of the project.
# ./app/.env if the file .env is in same directory as config.py i.e app.
settings = Settings()
# To know if env variables are set or not.
# print(settings.model_dump())