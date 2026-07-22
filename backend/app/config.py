from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    supabase_url: str
    supabase_service_key: str
    r2_account_id: str
    r2_access_key: str
    r2_secret_key: str
    r2_bucket_name: str = "datasanity-files"
    openrouter_api_key: str
    groq_api_key: str = ""
    environment: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
