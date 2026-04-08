import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    # Updated to the latest stable version
    #MODEL = "claude-3-5-sonnet-20241022"
    MODEL = "claude-sonnet-4-5"
    MAX_TOKENS = 1500