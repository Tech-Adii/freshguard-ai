import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from root directory
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings:
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")
    
    # Bifrost AI Gateway Configuration (Maxim AI)
    BIFROST_BASE_URL: str = os.getenv("BIFROST_BASE_URL", "http://localhost:8080/v1")
    USE_BIFROST_GATEWAY: bool = os.getenv("USE_BIFROST_GATEWAY", "true").lower() in ("true", "1", "yes")
    
    # Gemini Models
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    GEMINI_FALLBACK_MODEL: str = os.getenv("GEMINI_FALLBACK_MODEL", "gemini-3.5-flash")
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Verification thresholds
    STALE_THRESHOLD: float = 0.50  # Freshness below 50% considered stale
    HIGH_VOLATILITY_THRESHOLD: float = 0.70

settings = Settings()
