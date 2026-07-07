"""Welcome handler — 3 varied /start + /help with styled buttons"""
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode
from handlers.rich import (rich_send, rich_edit, btn, copy_btn, url_btn, rows)


# ── Welcome Variants ──────────────────────────────────────────────

def _welcome_md(variant: int) -> str:
    return VARIANTS.get(variant, VARIANTS[1])


VARIANTS = {
    1: (
        "# 🤖 MultiBot\n\n"
        "Bot serbaguna — *download*, *tools*, *notebook*.\n\n"
        "---\n\n"
        "## Fitur\n"
        "- 🎬 **Downloader** — TikTok, IG, YT, X, FB, Reddit\n"
        "- 📝 **Notebook** — Catatan pribadi `.txt`\n"
        "- 🧮 **Kalkulator** — Hitung ekspresi matematika\n"
        "- 🔳 **QR Code** — Generate QR code\n"
        "- 🔗 **URL Shortener** — TinyURL & is.gd\n"
        "- 🌤 **Cuaca** — Info cuaca real-time\n"
        "- 🖼 **Stiker** — Konversi foto ↔ stiker\n\n"
        "Pilih menu di bawah ↓"
    ),
    2: (
        "# 🎯 Selamat Datang!\n\n"
        "MultiBot siap bantu kebutuhan digital kamu.\n\n"
        "<details>\n"
        "<summary>📥 Downloader</summary>\n\n"
        "Download video dari TikTok, IG, YT, X, FB, Reddit.\n"
        "Support MP4 & MP3. Kirim URL, bot auto-detect.\n"
        "</details>\n\n"
        "<details>\n"
        "<summary>🧰 Tools</summary>\n\n"
        "- Kalkulator (math parser)\n"
        "- QR Code generator\n"
        "- URL shortener (TinyURL/is.gd)\n"
        "- Cek cuaca (OpenWeatherMap)\n"
        "- Stiker ↔ Foto converter\n"
        "</details>\n\n"
        "<details>\n"
        "<summary>📝 Notebook</summary>\n\n"
        "Simpan catatan langsung ke `.txt`.\n"
        "Multi-append + auto-timestamp.\n"
        "</details>\n\n"
        "Gunakan tombol di bawah ↓"
    ),
    3: (
        "# ⚡ MultiBot\n\n"
        "```\n"
        "Status  : Online\n"
        "Mode   : Inline Button\n"
        "Handler: 9 modul\n"
        "```\n\n"
        "| Fitur      | Command    |\n"
        "|------------|------------|\n"
        "| Download   | `/dl url`  |\n"
        "| QR Code    | `/qr text` |\n"
        "| Shortlink  | `/short u` |\n"
        "| Kalkulator | `/calc x`  |\n"
        "| Cuaca      | `/cuaca k` |\n"
        "| Stiker     | `/sticker` |\n"
        "| Notebook   | `/note`    |\n\n"
        "Pilih fitur ↓"
    ),
}


def _menu_buttons() -> list:
    """Styled inline keyboard — success green for primary action"""
    return rows(
        [btn("🎬 Download", "menu_dl", "primary"),
         btn("📝 Notebook", "menu_note", "primary")],
        [btn("🧮 Kalkulator", "menu_calc"),
         btn("🔳 QR Code", "menu_qr")],
        [btn("🔗 Shortlink", "menu_short"),
         btn("🌤 Cuaca", "menu_weather")],
        [btn("🖼 Stiker", "menu_sticker"),
         btn("ℹ️ Bantuan", "menu_help")],
        [copy_btn("📋 @moyxpremium_bot", "@moyxpremium_bot")],
    )


# ── Commands ───────────────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    variant = random.randint(1, 3)
    md = _welcome_md(variant)
    try:
        await rich_send(chat.id, md, _menu_buttons())
    except Exception:
        # Fallback HTML — simpler but works everywhere
        from telegram import InlineKeyboardMarkup, InlineKeyboardButton
        await update.message.reply_text(
            f"🤖 <b>MultiBot v2.0</b>\n\nPilih fitur:",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🎬 Downloader", callback_data="menu_dl")],
                [InlineKeyboardButton("📝 Notebook", callback_data="menu_note")],
                [InlineKeyboardButton("🧰 Tools", callback_data="menu_tools")],
                [InlineKeyboardButton("ℹ️ Bantuan", callback_data="menu_help")],
            ]),
        )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    md = (
        "# ❓ Bantuan\n\n"
        "### Downloader\n"
        "Kirim URL atau `/dl <url>` — bot auto-detect.\n"
        "Platform: TikTok, IG, YT, X, FB, Reddit.\n\n"
        "### Notebook\n"
        "`/note <teks>` — simpan ke `.txt` + timestamp.\n\n"
        "### Tools\n"
        "- `/qr <teks>` — generate QR code\n"
        "- `/short <url>` — pendekin URL\n"
        "- `/calc <ekspresi>` — kalkulator\n"
        "- `/cuaca <kota>` — info cuaca\n"
        "- `/sticker` — foto → stiker (reply foto)\n"
        "- `/toimg` — stiker → foto (reply stiker)\n\n"
        "---\n"
        "💡 Ketik `/menu` kapan aja buat balik ke menu utama."
    )
    try:
        await rich_send(chat.id, md)
    except Exception:
        from telegram import InlineKeyboardMarkup, InlineKeyboardButton
        await update.message.reply_text(
            "<b>❓ Bantuan</b>\n\n"
            "📥 <b>Downloader</b> — kirim URL atau /dl\n"
            "📝 <b>Notebook</b> — /note teks\n"
            "🧮 <b>Kalkulator</b> — /calc ekspresi\n"
            "🔳 <b>QR Code</b> — /qr teks\n"
            "🔗 <b>Shortlink</b> — /short url\n"
            "🌤 <b>Cuaca</b> — /cuaca kota\n"
            "🖼 <b>Stiker</b> — /sticker (reply foto)",
            parse_mode=ParseMode.HTML,
        )


# ── Callback Handlers ──────────────────────────────────────────────

async def cb_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback dari menu_help balik ke welcome"""
    query = update.callback_query
    await query.answer()
    variant = random.randint(1, 3)
    md = _welcome_md(variant)
    try:
        await rich_edit(query.message.chat_id, query.message.message_id, md, _menu_buttons())
    except Exception:
        await query.edit_message_text(
            "🤖 <b>MultiBot v2.0</b>\n\nPilih fitur:",
            parse_mode=ParseMode.HTML,
            reply_markup=None,
        )


def register(app: Application):
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CallbackQueryHandler(cb_welcome, pattern=r"^menu_help$"))
