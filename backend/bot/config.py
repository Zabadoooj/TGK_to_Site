from dotenv import load_dotenv
import os

load_dotenv()

# Telegram
BOT_TOKEN = os.getenv("TG_BOT_KEY")
CHANNEL_ID = os.getenv("TG_CHANNEL")
YOUR_USER_ID = int(os.getenv("USER_ID"))


# CORS — какие адреса фронта допускаются
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
]