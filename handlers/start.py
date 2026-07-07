from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode

START_TEXT = """🤖 <b>MultiBot v1.0</b>

Bot utility serbaguna. Langsung aja:

📥 <b>Download</b>
<code>/dl [url]</code> — TikTok / YouTube / IG

📱 <b>QR Code</b>
<code>/qr [teks]</code> — Generate QR code

🔗 <b>URL Shortener</b>
<code>/short [url]</code> — Pendein URL

🖼 <b>Sticker</b>
Kirim foto → <code>/sticker</code> — Jadiin stiker
Kirim stiker → <code>/toimg</code> — Jadiin foto

🌤 <b>Cuaca</b>
<code>/cuaca [kota]</code> — Info cuaca

🧮 <b>Kalkulator</b>
<code>/calc [ekspresi]</code> — Hitung

Ketik /help buat lihat lagi."""

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_TEXT, parse_mode=ParseMode.HTML)

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_TEXT, parse_mode=ParseMode.HTML)

def register(app: Application):
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
