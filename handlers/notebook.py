"""Notebook — save text as .txt files"""
import re, io
from datetime import datetime
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode
from config import NOTEBOOK_DIR


def back_button(target="menu_note"):
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data=target)]])


def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name.strip())[:50]


def list_notes():
    return sorted(
        [f.name for f in NOTEBOOK_DIR.glob("*.txt")],
        key=lambda x: NOTEBOOK_DIR.joinpath(x).stat().st_mtime, reverse=True,
    )


def delete_note(filename):
    f = NOTEBOOK_DIR / filename
    if f.exists():
        f.unlink()
        return True
    return False


async def save_note(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str = None):
    if text is None and context.args:
        text = " ".join(context.args)

    if not text:
        await update.message.reply_text(
            "✍️ Kirim teks catatan.\nBaris pertama = judul file.",
            reply_markup=back_button(),
        )
        return

    lines = text.split("\n", 1)
    title = sanitize_filename(lines[0])
    content = lines[1] if len(lines) > 1 else lines[0]

    filename = f"{title}.txt"
    filepath = NOTEBOOK_DIR / filename

    if filepath.exists():
        ts = datetime.now().strftime("\n\n--- %Y-%m-%d %H:%M ---\n")
        with open(filepath, "a") as f:
            f.write(ts + content)
    else:
        with open(filepath, "w") as f:
            f.write(content)

    await update.message.reply_text(
        f"✅ Catatan disimpan: <code>{filename}</code>\n📏 {len(content)} karakter",
        parse_mode=ParseMode.HTML,
        reply_markup=back_button(),
    )


async def view_note_file(update: Update, context: ContextTypes.DEFAULT_TYPE, filename: str = None):
    if filename is None and context.args:
        filename = context.args[0]
    if not filename:
        notes = list_notes()
        if notes:
            text = "📄 <b>Catatan:</b>\n\n" + "\n".join(f"• <code>{n}</code>" for n in notes)
        else:
            text = "📄 Belum ada catatan."
        await update.message.reply_text(text, parse_mode=ParseMode.HTML)
        return

    filepath = NOTEBOOK_DIR / filename
    if not filepath.exists():
        await update.message.reply_text(
            f"❌ Catatan <code>{filename}</code> gak ditemukan.", parse_mode=ParseMode.HTML,
        )
        return

    with open(filepath) as f:
        content = f.read()

    buf = io.BytesIO(content.encode("utf-8"))
    await update.message.reply_document(
        buf, filename=filename,
        caption=f"📄 <b>{filename}</b> · {len(content)} karakter",
        parse_mode=ParseMode.HTML,
    )


async def cmd_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "📝 <b>Notebook</b>\n\n"
            "<code>/note [judul] [isi]</code> — Simpan catatan\n"
            "<code>/notes</code> — Lihat daftar catatan\n"
            "<code>/view [file]</code> — Buka catatan\n\n"
            "Atau klik /menu buat tampilan button.",
            parse_mode="HTML",
        )
        return
    await save_note(update, context)


async def cmd_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await view_note_file(update, context)


async def cmd_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        await view_note_file(update, context, filename=context.args[0])
    else:
        await update.message.reply_text("❌ <b>Usage:</b> <code>/view [filename.txt]</code>", parse_mode="HTML")


def register(app: Application):
    app.add_handler(CommandHandler("note", cmd_note))
    app.add_handler(CommandHandler("notes", cmd_notes))
    app.add_handler(CommandHandler("view", cmd_view))
