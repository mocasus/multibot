import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "").strip()
ADMIN_IDS = set(
    int(x.strip())
    for x in os.getenv("ADMIN_IDS", "").split(",")
    if x.strip().isdigit()
)
NOTEBOOK_DIR = Path(__file__).parent / "notebooks"
NOTEBOOK_DIR.mkdir(exist_ok=True)
