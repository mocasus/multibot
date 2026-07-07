from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode

async def cmd_short(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❌ <b>Usage:</b> <code>/short [url]</code>", parse_mode=ParseMode.HTML
        )
        return

    url = context.args[0]
    if not url.startswith("http"):
        url = "https://" + url

    msg = await update.message.reply_text("⏳ Mendein URL...")

    try:
        import requests
        # Use tinyurl as fallback
        r = requests.get(f"https://tinyurl.com/api-create.php?url={url}", timeout=10)
        if r.status_code == 200 and r.text and "Error" not in r.text:
            short = r.text.strip()
            await msg.edit_text(
                f"🔗 <b>Short URL:</b>\n<code>{short}</code>\n\n📎 Original: {url}",
                parse_mode=ParseMode.HTML,
            )
        else:
            # Try is.gd
            r2 = requests.get(
                f"https://is.gd/create.php?format=simple&url={url}", timeout=10
            )
            if r2.status_code == 200 and r2.text:
                await msg.edit_text(
                    f"🔗 <b>Short URL:</b>\n<code>{r2.text.strip()}</code>\n\n📎 Original: {url}",
                    parse_mode=ParseMode.HTML,
                )
            else:
                await msg.edit_text("❌ Gagal mendein URL, coba lagi nanti.")
    except Exception as e:
        await msg.edit_text(f"❌ <b>Gagal:</b> {str(e)[:200]}", parse_mode=ParseMode.HTML)

def register(app: Application):
    app.add_handler(CommandHandler("short", cmd_short))
