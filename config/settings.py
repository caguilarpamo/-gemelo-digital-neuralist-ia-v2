import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    # Updated to the latest stable version
    #MODEL = "claude-3-5-sonnet-20241022"
    MODEL = "claude-sonnet-4-5"
    MAX_TOKENS = 1500

    # Stitch MCP (Google) - para el agente DesarrolladorFrontEnd
    STITCH_API_KEY = os.getenv("STITCH_API_KEY")
    STITCH_MCP_URL = os.getenv("STITCH_MCP_URL", "https://stitch.googleapis.com/mcp")

    # Vercel - para el agente Despliegue (deploy automático)
    VERCEL_TOKEN = os.getenv("VERCEL_TOKEN")
    VERCEL_PROJECT_NAME = os.getenv("VERCEL_PROJECT_NAME", "gemelo-digital-demo")
