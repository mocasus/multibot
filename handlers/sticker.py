"""Sticker tools — foto↔stiker"""
import io, os, tempfile
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.constants import ParseMode


async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Only process photo if user is in sticker_photo state"""
    state = context.user_data.get("state", "")
    if state == "sticker_photo":
        await photo_to_sticker(update, context)


async def sticker_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Only process sticker if user is in sticker_toimg state"""
    state = context.user_data.get("state", "")
    if state == "sticker_toimg":
        await sticker_to_img(update, context)


async def photo_to_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("🖼 Konversi ke stiker...")
    try:
        from PIL import Image
        photo = update.message.photo[-1]
        f = await photo.get_file()
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            await f.download_to_memory(tmp)
            tmp.flush()
            img = Image.open(tmp.name)
            img.thumbnail((512, 512), Image.LANCZOS)
            buf = io.BytesIO()
            img.convert("RGBA").save(buf, format="PNG")
            buf.seek(0)
            os.unlink(tmp.name)
        await update.message.reply_sticker(buf)
        await msg.delete()
        context.user_data["state"] = None
    except Exception as e:
        await msg.edit_text(f"❌ Gagal: {str(e)[:200]}")


async def sticker_to_img(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("🖼 Konversi ke foto...")
    try:
        from PIL import Image
        sticker = update.message.sticker
        f = await sticker.get_file()
        with tempfile.NamedTemporaryFile(suffix=".webp", delete=False) as tmp:
            await f.download_to_memory(tmp)
            tmp.flush()
            img = Image.open(tmp.name)
            buf = io.BytesIO()
            img.convert("RGBA").save(buf, format="PNG")
            buf.seek(0)
            os.unlink(tmp.name)
        await update.message.reply_document(buf, filename="sticker.png", caption="🖼 Stiker → PNG")
        await msg.delete()
        context.user_data["state"] = None
    except Exception as e:
        await msg.edit_text(f"❌ Gagal: {str(e)[:200]}")


async def cmd_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        await update.message.reply_text(
            "❌ Reply foto + <code>/sticker</code>\nAtau /menu → Stiker Tools.", parse_mode="HTML",
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
            img.thumbnail((512, 512), Image.LANCZOS)
            buf = io.BytesIO()
            img.convert("RGBA").save(buf, format="PNG")
            buf.seek(0)
            os.unlink(tmp.name)
        await update.message.reply_sticker(buf)
        await msg.delete()
    except Exception as e:
        await msg.edit_text(f"❌ Gagal: {str(e)[:200]}", parse_mode="HTML")


async def cmd_toimg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.sticker:
        await update.message.reply_text(
            "❌ Reply stiker + <code>/toimg</code>\nAtau /menu → Stiker Tools.", parse_mode="HTML",
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
        await update.message.reply_document(buf, filename="sticker.png", caption="🖼 Stiker → PNG")
        await msg.delete()
    except Exception as e:
        await msg.edit_text(f"❌ Gagal: {str(e)[:200]}", parse_mode="HTML")


def register(app: Application):
    app.add_handler(CommandHandler("sticker", cmd_sticker))
    app.add_handler(CommandHandler("toimg", cmd_toimg))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    app.add_handler(MessageHandler(filters.Sticker.ALL, sticker_handler))
