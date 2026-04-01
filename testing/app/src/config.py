"""Configuration settings"""
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App settings
    app_name: str = "DevOps Automation"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"
    
    # API settings
    api_prefix: str = "/api/v1"
    
    # Database settings
    database_url: str = "sqlite:///./test.db"
    
    # Security settings
    secret_key: str = "dev-secret-key-change-in-production"
    
    # AWS settings
    aws_region: str = "us-east-1"
    aws_s3_bucket: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
