# src/config/settings.py
from dataclasses import dataclass
from typing import Optional
import os

try:
    # Only needed in local/dev; harmless in prod/CI where env vars are set
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


@dataclass(frozen=True)
class Settings:
    default_agent_name: str = "hello-agent"
    google_api_key: Optional[str] = None

    @staticmethod
    def from_env() -> "Settings":
        return Settings(
            default_agent_name=os.getenv("DEFAULT_AGENT_NAME", "hello-agent"),
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )

settings = Settings.from_env()