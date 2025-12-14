"""
Configuration for the application - Python 3.6 compatible
"""
import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    # API Keys
    deepseek_api_key: str = ""
    deepseek_api_url: str = "https://api.deepseek.com/v1/chat/completions"
    
    yandex_vision_api_key: str = ""
    yandex_vision_folder_id: str = ""
    yandex_vision_endpoint: str = "https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze"
    
    # Server settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Application settings
    app_title: str = "MotionCraft AI Analyzer"
    app_version: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

