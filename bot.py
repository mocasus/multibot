import logging, sys
from config import BOT_TOKEN
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN kosong! Set di .env")
        sys.exit(1)

    app = Application.builder().token(BOT_TOKEN).build()

    # Register all handlers
    from handlers import start, download, notebook, qr, shorten, weather, calc, sticker, menu

    start.register(app)
    menu.register(app)
    download.register(app)
    notebook.register(app)
    qr.register(app)
    shorten.register(app)
    weather.register(app)
    calc.register(app)
    sticker.register(app)

    total = len(app.handlers[0]) if app.handlers else 0
    logger.info(f"Registered {total} handlers")
    logger.info("Bot mulai polling...")
    app.run_polling(allowed_updates=["message", "callback_query"])

if __name__ == "__main__":
    main()
