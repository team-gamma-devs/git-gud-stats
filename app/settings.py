from pydantic_settings import BaseSettings
import os

class BaseSettingsClass(BaseSettings):
    github_token: str
    # URLs with default vaules.
    github_api_url: str = "https://api.github.com/users/"
    github_graphql_url: str = "https://api.github.com/graphql"
    client_id: str
    client_secret: str

    class Config:
        env_file = ".env"
        case_sensitive = False

class DevelopmentSettings(BaseSettingsClass):
    debug: bool = True

class ProductionSettings(BaseSettingsClass):
    debug: bool = False

# Select class depends of the env.
env = os.getenv("ENV", "development")
settings = DevelopmentSettings() if env == "development" else ProductionSettings()
