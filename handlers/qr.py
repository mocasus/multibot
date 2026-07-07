import io
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode

async def cmd_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❌ <b>Usage:</b> <code>/qr [teks atau URL]</code>", parse_mode=ParseMode.HTML
        )
        return

    text = " ".join(context.args)
    if len(text) > 2000:
        await update.message.reply_text("❌ Teks kepanjangan (max 2000 karakter).")
        return

    msg = await update.message.reply_text("🔳 Bikin QR...")

    try:
        import qrcode
        from qrcode.image.styledpil import StyledPilImage
        from qrcode.image.styles.moduledrawers import RoundedModuleDrawer

        qr = qrcode.QRCode(box_size=10, border=2)
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            fill_color="black",
            back_color="white",
        )

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        preview = text if len(text) <= 50 else text[:47] + "..."
        await update.message.reply_photo(
            buf,
            caption=f"🔳 QR untuk: <code>{preview}</code>",
            parse_mode=ParseMode.HTML,
        )
        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"❌ <b>Gagal:</b> {str(e)[:200]}", parse_mode=ParseMode.HTML)

def register(app: Application):
    app.add_handler(CommandHandler("qr", cmd_qr))
