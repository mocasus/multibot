"""URL Shortener"""
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode


def back_button(target="menu_tools"):
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data=target)]])


async def shorten_url(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str = None):
    if url is None and context.args:
        url = context.args[0]
    if not url:
        await update.message.reply_text("❌ Kirim URL.", reply_markup=back_button())
        return
    if not url.startswith("http"):
        url = "https://" + url

    msg = await update.message.reply_text("⏳ Mendein URL...")

    try:
        import requests
        for svc, api in [
            ("is.gd", f"https://is.gd/create.php?format=simple&url={url}"),
            ("tinyurl", f"https://tinyurl.com/api-create.php?url={url}"),
        ]:
            r = requests.get(api, timeout=10)
            if r.status_code == 200 and r.text.strip() and "Error" not in r.text:
                short = r.text.strip()
                await msg.edit_text(
                    f"🔗 <b>Short URL:</b>\n<code>{short}</code>\n\n📎 Original: {url[:60]}...",
                    parse_mode=ParseMode.HTML, reply_markup=back_button(),
                )
                return
        await msg.edit_text("❌ Semua service gagal.", reply_markup=back_button())
    except Exception as e:
        await msg.edit_text(f"❌ Gagal: {str(e)[:200]}", reply_markup=back_button())


async def cmd_short(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "🔗 <b>Usage:</b> <code>/short [url]</code>\nAtau klik /menu.", parse_mode="HTML",
        )
        return
    await shorten_url(update, context)


def register(app: Application):
    app.add_handler(CommandHandler("short", cmd_short))
