import logging, sys
from config import BOT_TOKEN
from telegram.ext import Application

# Setup logging
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN kosong! Set di .env")
        sys.exit(1)

    app = Application.builder().token(BOT_TOKEN).build()

    # Register all modules
    from handlers import start, download, qr, shorten, sticker, weather, calc
    start.register(app)
    download.register(app)
    qr.register(app)
    shorten.register(app)
    sticker.register(app)
    weather.register(app)
    calc.register(app)

    # Verify
    total = len(app.handlers[0]) if app.handlers else 0
    logger.info(f"Registered {total} handlers")

    logger.info("Bot mulai polling...")
    app.run_polling(allowed_updates=["message", "callback_query"])

if __name__ == "__main__":
    main()
