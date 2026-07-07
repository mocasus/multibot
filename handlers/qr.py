"""QR Code generator"""
import io
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode


def back_button(target="menu_tools"):
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data=target)]])


async def generate_qr(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str = None):
    if text is None and context.args:
        text = " ".join(context.args)
    if not text:
        await update.message.reply_text("❌ Kirim teks/URL buat QR.", reply_markup=back_button())
        return
    if len(text) > 2000:
        await update.message.reply_text("❌ Teks kepanjangan (max 2000).", reply_markup=back_button())
        return

    msg = await update.message.reply_text("🔳 Bikin QR...")

    try:
        import qrcode
        from qrcode.image.styledpil import StyledPilImage
        from qrcode.image.styles.moduledrawers import RoundedModuleDrawer

        qr = qrcode.QRCode(box_size=12, border=2)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            fill_color="black", back_color="white",
        )
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        preview = text if len(text) <= 50 else text[:47] + "..."
        await update.message.reply_photo(
            buf, caption=f"🔳 QR: <code>{preview}</code>", parse_mode=ParseMode.HTML,
        )
        await msg.delete()
    except Exception as e:
        await msg.edit_text(f"❌ Gagal: {str(e)[:200]}", reply_markup=back_button())


async def cmd_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "🔳 <b>Usage:</b> <code>/qr [teks/URL]</code>\nAtau klik /menu.", parse_mode="HTML",
        )
        return
    await generate_qr(update, context)


def register(app: Application):
    app.add_handler(CommandHandler("qr", cmd_qr))
