import os, tempfile, shutil
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode

MAX_SIZE = 50 * 1024 * 1024  # 50MB Telegram limit

async def cmd_dl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❌ <b>Usage:</b> <code>/dl [url]</code>", parse_mode=ParseMode.HTML
        )
        return

    url = context.args[0]
    msg = await update.message.reply_text("⏳ Lagi download...")

    tmpdir = tempfile.mkdtemp()
    try:
        import yt_dlp
        opts = {
            "outtmpl": f"{tmpdir}/%(title).100s.%(ext)s",
            "quiet": True,
            "no_warnings": True,
            "format": "best[filesize<50M]/best",
            "max_filesize": MAX_SIZE,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # yt-dlp might change extension
            actual = None
            for f in os.listdir(tmpdir):
                actual = os.path.join(tmpdir, f)
                break

        if actual:
            fsize = os.path.getsize(actual)
            if fsize > MAX_SIZE:
                await msg.edit_text("❌ File kegedean (>50MB), gabisa dikirim.")
                return

            title = info.get("title", "Video")[:100]
            dur = info.get("duration", 0)
            dur_str = f"{dur // 60}:{dur % 60:02d}" if dur else "?"
            caption = f"🎬 <b>{title}</b>\n⏱ {dur_str}"
            if len(caption) > 1024:
                caption = caption[:1021] + "..."

            with open(actual, "rb") as vf:
                await update.message.reply_video(
                    vf, caption=caption, parse_mode=ParseMode.HTML
                )
            await msg.delete()
        else:
            await msg.edit_text("❌ Gagal nemuin file hasil download.")

    except Exception as e:
        await msg.edit_text(f"❌ <b>Gagal:</b> {str(e)[:200]}", parse_mode=ParseMode.HTML)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

def register(app: Application):
    app.add_handler(CommandHandler("dl", cmd_dl))
