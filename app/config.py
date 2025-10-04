import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL", "gpt-4o-mini")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8080"))
# If NANDA adapter requires a specific secret or handshake, add here:
NANDA_SHARED_SECRET = os.getenv("NANDA_SHARED_SECRET", None)
