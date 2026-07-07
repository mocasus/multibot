from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode

HELP_TEXT = (
    "🤖 <b>MultiBot v2.0</b>\n\n"
    "Bot utility serbaguna dengan inline button.\n\n"
    "📥 <b>Downloader</b>\n"
    "• Video: TikTok, YT, IG, X, FB, Reddit\n"
    "• Audio: Ekstrak MP3\n"
    "• Playlist: Info playlist YT\n\n"
    "📝 <b>Notebook</b>\n"
    "• Simpan catatan auto .txt\n"
    "• Multi-append + timestamp\n\n"
    "🧰 <b>Tools</b>\n"
    "• Kalkulator\n"
    "• QR Code\n"
    "• URL Shortener\n"
    "• Cek Cuaca\n"
    "• Stiker ↔ Foto\n\n"
    "Ketik /menu atau /start buat mulai."
)

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎬 Downloader", callback_data="menu_dl")],
        [InlineKeyboardButton("📝 Notebook", callback_data="menu_note")],
        [InlineKeyboardButton("🧰 Tools", callback_data="menu_tools")],
        [InlineKeyboardButton("ℹ️ Bantuan", callback_data="menu_help")],
    ])

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 <b>MultiBot v2.0</b>\n\nPilih fitur:",
        parse_mode=ParseMode.HTML, reply_markup=main_menu()
    )

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT, parse_mode=ParseMode.HTML, reply_markup=main_menu())

def register(app: Application):
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
