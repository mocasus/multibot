import io, os, tempfile
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.constants import ParseMode

async def cmd_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Convert replied photo to sticker"""
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        await update.message.reply_text(
            "❌ <b>Usage:</b> Reply foto + <code>/sticker</code>",
            parse_mode=ParseMode.HTML,
        )
        return

    msg = await update.message.reply_text("🖼 Konversi ke stiker...")

    try:
        from PIL import Image

        photo = update.message.reply_to_message.photo[-1]
        f = await photo.get_file()

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            await f.download_to_memory(tmp)
            tmp.flush()
            img = Image.open(tmp.name)
            # Resize to sticker dimensions (512x512 max)
            img.thumbnail((512, 512), Image.LANCZOS)
            # Convert to PNG with transparent bg
            buf = io.BytesIO()
            img.convert("RGBA").save(buf, format="PNG")
            buf.seek(0)
            os.unlink(tmp.name)

        await update.message.reply_sticker(buf)
        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"❌ <b>Gagal:</b> {str(e)[:200]}", parse_mode=ParseMode.HTML)

async def cmd_toimg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Convert replied sticker to image"""
    if not update.message.reply_to_message or not update.message.reply_to_message.sticker:
        await update.message.reply_text(
            "❌ <b>Usage:</b> Reply stiker + <code>/toimg</code>",
            parse_mode=ParseMode.HTML,
        )
        return

    msg = await update.message.reply_text("🖼 Konversi ke foto...")

    try:
        from PIL import Image

        sticker = update.message.reply_to_message.sticker
        f = await sticker.get_file()

        with tempfile.NamedTemporaryFile(suffix=".webp", delete=False) as tmp:
            await f.download_to_memory(tmp)
            tmp.flush()
            img = Image.open(tmp.name)

            buf = io.BytesIO()
            img.convert("RGBA").save(buf, format="PNG")
            buf.seek(0)
            os.unlink(tmp.name)

        await update.message.reply_document(
            buf, filename="sticker.png", caption="🖼 Stiker → PNG"
        )
        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"❌ <b>Gagal:</b> {str(e)[:200]}", parse_mode=ParseMode.HTML)

def register(app: Application):
    app.add_handler(CommandHandler("sticker", cmd_sticker))
    app.add_handler(CommandHandler("toimg", cmd_toimg))
