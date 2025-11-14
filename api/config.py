from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    secret_key: str = "super-secret-change-me"
    database_url: str = "sqlite:///tasks.db"
    access_token_expire_minutes: int = 60

settings = Settings()
