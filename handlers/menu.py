"""Menu navigation with inline keyboards + state routing"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, MessageHandler, CommandHandler, ContextTypes, filters

STATE_IDLE = None
STATE_DL_URL = "dl_url"
STATE_DL_AUDIO = "dl_audio"
STATE_NOTE_WRITE = "note_write"
STATE_QR_TEXT = "qr_text"
STATE_SHORT_URL = "short_url"
STATE_CALC_EXPR = "calc_expr"
STATE_CUACA_KOTA = "cuaca_kota"


def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎬 Downloader", callback_data="menu_dl")],
        [InlineKeyboardButton("📝 Notebook", callback_data="menu_note")],
        [InlineKeyboardButton("🧰 Tools", callback_data="menu_tools")],
        [InlineKeyboardButton("ℹ️ Bantuan", callback_data="menu_help")],
    ])


def dl_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎬 Download Video", callback_data="dl_video")],
        [InlineKeyboardButton("🎵 Download Audio", callback_data="dl_audio")],
        [InlineKeyboardButton("📋 Playlist Info", callback_data="dl_playlist")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="menu_back")],
    ])


def note_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✍️ Tulis Catatan", callback_data="note_write")],
        [InlineKeyboardButton("📄 Lihat Catatan", callback_data="note_view")],
        [InlineKeyboardButton("🗑 Hapus Catatan", callback_data="note_delete")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="menu_back")],
    ])


def tools_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🧮 Kalkulator", callback_data="tool_calc"),
         InlineKeyboardButton("🔳 QR Code", callback_data="tool_qr")],
        [InlineKeyboardButton("🔗 Short URL", callback_data="tool_short"),
         InlineKeyboardButton("🌤 Cuaca", callback_data="tool_cuaca")],
        [InlineKeyboardButton("🖼 Stiker Tools", callback_data="tool_sticker")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="menu_back")],
    ])


def sticker_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🖼 Foto → Stiker", callback_data="sticker_photo")],
        [InlineKeyboardButton("📸 Stiker → Foto", callback_data="sticker_toimg")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="menu_tools")],
    ])


def back_button(target="menu_back"):
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data=target)]])


async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu_back":
        await query.edit_message_text(
            "🤖 <b>MultiBot v2.0</b>\n\nPilih fitur:",
            parse_mode="HTML", reply_markup=main_menu()
        )
        context.user_data["state"] = STATE_IDLE

    elif data == "menu_dl":
        await query.edit_message_text(
            "📥 <b>Downloader</b>\n\nPilih mode download:",
            parse_mode="HTML", reply_markup=dl_menu()
        )

    elif data == "menu_note":
        await query.edit_message_text(
            "📝 <b>Notebook</b>\n\nCatatan pribadi auto-save ke .txt:",
            parse_mode="HTML", reply_markup=note_menu()
        )

    elif data == "menu_tools":
        await query.edit_message_text(
            "🧰 <b>Tools</b>\n\nPilih tool:",
            parse_mode="HTML", reply_markup=tools_menu()
        )

    elif data == "tool_calc":
        context.user_data["state"] = STATE_CALC_EXPR
        await query.edit_message_text(
            "🧮 <b>Kalkulator</b>\n\nKirim ekspresi matematika:\n"
            "<code>2 + 2 * 3</code>\n<code>sqrt(144)</code>\n<code>sin(pi/2)</code>",
            parse_mode="HTML", reply_markup=back_button("menu_tools")
        )

    elif data == "tool_qr":
        context.user_data["state"] = STATE_QR_TEXT
        await query.edit_message_text(
            "🔳 <b>QR Code Generator</b>\n\nKirim teks atau URL yang mau dijadiin QR:",
            parse_mode="HTML", reply_markup=back_button("menu_tools")
        )

    elif data == "tool_short":
        context.user_data["state"] = STATE_SHORT_URL
        await query.edit_message_text(
            "🔗 <b>URL Shortener</b>\n\nKirim URL yang mau dipendein:",
            parse_mode="HTML", reply_markup=back_button("menu_tools")
        )

    elif data == "tool_cuaca":
        context.user_data["state"] = STATE_CUACA_KOTA
        await query.edit_message_text(
            "🌤 <b>Cek Cuaca</b>\n\nKirim nama kota:",
            parse_mode="HTML", reply_markup=back_button("menu_tools")
        )

    elif data == "tool_sticker":
        await query.edit_message_text(
            "🖼 <b>Stiker Tools</b>\n\nPilih aksi:",
            parse_mode="HTML", reply_markup=sticker_menu()
        )

    elif data == "sticker_photo":
        context.user_data["state"] = "sticker_photo"
        await query.edit_message_text(
            "🖼 <b>Foto → Stiker</b>\n\nKirim foto, nanti aku jadiin stiker.",
            parse_mode="HTML", reply_markup=back_button("tool_sticker")
        )

    elif data == "sticker_toimg":
        context.user_data["state"] = "sticker_toimg"
        await query.edit_message_text(
            "📸 <b>Stiker → Foto</b>\n\nKirim stiker, nanti aku jadiin foto PNG.",
            parse_mode="HTML", reply_markup=back_button("tool_sticker")
        )

    elif data == "dl_video":
        context.user_data["state"] = STATE_DL_URL
        await query.edit_message_text(
            "🎬 <b>Download Video</b>\n\n"
            "🟢 TikTok · YouTube · Instagram · Twitter/X · Facebook · Reddit\n\n"
            "Kirim URL video:",
            parse_mode="HTML", reply_markup=back_button("menu_dl")
        )

    elif data == "dl_audio":
        context.user_data["state"] = STATE_DL_AUDIO
        await query.edit_message_text(
            "🎵 <b>Download Audio (MP3)</b>\n\n"
            "🟢 YouTube · TikTok · SoundCloud · Instagram\n\n"
            "Kirim URL:",
            parse_mode="HTML", reply_markup=back_button("menu_dl")
        )

    elif data == "dl_playlist":
        context.user_data["state"] = "dl_playlist"
        await query.edit_message_text(
            "📋 <b>Playlist Info</b>\n\n"
            "Lihat isi playlist YouTube.\nKirim URL playlist:",
            parse_mode="HTML", reply_markup=back_button("menu_dl")
        )

    elif data == "note_write":
        context.user_data["state"] = STATE_NOTE_WRITE
        await query.edit_message_text(
            "✍️ <b>Tulis Catatan</b>\n\n"
            "Kirim teks, nanti aku simpan jadi file .txt.\n"
            "Format: baris pertama = judul file",
            parse_mode="HTML", reply_markup=back_button("menu_note")
        )

    elif data == "note_view":
        from .notebook import list_notes
        notes = list_notes()
        if notes:
            text = "📄 <b>Catatan kamu:</b>\n\n" + "\n".join(f"• <code>{n}</code>" for n in notes)
        else:
            text = "📄 Belum ada catatan."
        await query.edit_message_text(text, parse_mode="HTML", reply_markup=note_menu())

    elif data == "note_delete":
        from .notebook import list_notes
        notes = list_notes()
        if not notes:
            await query.edit_message_text("📄 Belum ada catatan.", reply_markup=note_menu())
            return
        btns = []
        for n in notes:
            btns.append([InlineKeyboardButton(f"🗑 {n}", callback_data=f"note_del_{n}")])
        btns.append([InlineKeyboardButton("🔙 Kembali", callback_data="menu_note")])
        await query.edit_message_text(
            "🗑 <b>Hapus Catatan</b>\n\nPilih yang mau dihapus:",
            parse_mode="HTML", reply_markup=InlineKeyboardMarkup(btns)
        )

    elif data.startswith("note_del_"):
        filename = data[9:]
        from .notebook import delete_note
        if delete_note(filename):
            await query.edit_message_text(
                f"✅ Catatan <code>{filename}</code> dihapus.",
                parse_mode="HTML", reply_markup=note_menu()
            )
        else:
            await query.edit_message_text("❌ Gagal hapus.", reply_markup=note_menu())


async def text_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get("state", STATE_IDLE)
    text = update.message.text.strip()

    if state == STATE_DL_URL:
        from .download import download_video
        await download_video(update, context, text)
    elif state == STATE_DL_AUDIO:
        from .download import download_audio
        await download_audio(update, context, text)
    elif state == "dl_playlist":
        from .download import show_playlist
        await show_playlist(update, context, text)
    elif state == STATE_QR_TEXT:
        from .qr import generate_qr
        await generate_qr(update, context, text)
    elif state == STATE_SHORT_URL:
        from .shorten import shorten_url
        await shorten_url(update, context, text)
    elif state == STATE_CALC_EXPR:
        from .calc import do_calc
        await do_calc(update, context, text)
    elif state == STATE_CUACA_KOTA:
        from .weather import do_cuaca
        await do_cuaca(update, context, text)
    elif state == STATE_NOTE_WRITE:
        from .notebook import save_note
        await save_note(update, context, text)
    else:
        await update.message.reply_text(
            "🤖 <b>MultiBot v2.0</b>\n\nPilih fitur atau ketik /start:",
            parse_mode="HTML", reply_markup=main_menu()
        )

    context.user_data["state"] = STATE_IDLE


def register(app: Application):
    app.add_handler(CallbackQueryHandler(callback_router))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_router))
    app.add_handler(CommandHandler("menu", lambda u, c: u.message.reply_text(
        "🤖 <b>MultiBot v2.0</b>\n\nPilih fitur:", parse_mode="HTML", reply_markup=main_menu()
    )))
