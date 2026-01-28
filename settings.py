import os
from typing import Literal, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings with env variable support and validation"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # SPEECH-TO-TEXT SETTINGS
    DEEPGRAM_API_KEY: Optional[str] = Field(default=None, description="Deepgram API key for STT service")


    # LLM SETTINGS FOR AGENT
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API key for LLM access")
    LLM_MODEL_NAME: str = Field(default="gpt-4.1", description="LLM model name to use")



settings = Settings()
