import os
from typing import Optional

class Settings:
    """Application settings and configuration."""
    
    def __init__(self):
        self.openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
        self.tavily_api_key: Optional[str] = os.getenv("TAVILY_API_KEY")
        # self.frontend_host: str = os.getenv("FRONTEND_HOST", "0.0.0.0")
        # self.frontend_port: int = int(os.getenv("FRONTEND_PORT", "7819"))
        self.model_name: str = os.getenv("MODEL_NAME", "gpt-4")
        self.temperature: float = float(os.getenv("TEMPERATURE", "0.3"))

settings = Settings()

