"""Multi-platform downloader — video, audio, playlist"""
import os, tempfile, shutil
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode

MAX_SIZE = 50 * 1024 * 1024  # 50MB


def back_button(target="menu_dl"):
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data=target)]])


async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str = None):
    if url is None and context.args:
        url = context.args[0]
    if not url:
        await update.message.reply_text("❌ Kirim URL video.", reply_markup=back_button())
        return

    msg = await update.message.reply_text("⏳ Download video...")
    tmpdir = tempfile.mkdtemp()

    try:
        import yt_dlp
        opts = {
            "outtmpl": f"{tmpdir}/%(title).100s.%(ext)s",
            "quiet": True, "no_warnings": True,
            "format_sort": ["res:1080", "res:720", "res:480"],
            "format": "best[filesize<50M]/best[height<=720][filesize<50M]/best",
            "max_filesize": MAX_SIZE,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            ydl.prepare_filename(info)

        actual = None
        for f in os.listdir(tmpdir):
            actual = os.path.join(tmpdir, f)
            break

        if actual and os.path.exists(actual):
            fsize = os.path.getsize(actual)
            if fsize > MAX_SIZE:
                await msg.edit_text("❌ File kegedean (>50MB).", reply_markup=back_button())
                return

            title = info.get("title", "Video")[:100]
            dur = info.get("duration", 0) or 0
            dur_str = f"{int(dur)//60}:{int(dur)%60:02d}" if dur else "?"
            ext = info.get("extractor_key", "").lower()
            platform = {
                "tiktok": "TikTok", "instagram": "IG", "youtube": "YT",
                "twitter": "X", "facebook": "FB", "reddit": "Reddit",
                "soundcloud": "SoundCloud",
            }.get(ext, ext.upper())

            caption = f"🎬 <b>{title}</b>\n📱 {platform} · ⏱ {dur_str}"
            if len(caption) > 1024:
                caption = caption[:1021] + "..."

            ext_lower = os.path.splitext(actual)[1].lower()
            with open(actual, "rb") as vf:
                if ext_lower in (".mp4", ".webm", ".mov"):
                    await update.message.reply_video(
                        vf, caption=caption, parse_mode=ParseMode.HTML,
                        supports_streaming=True,
                    )
                else:
                    await update.message.reply_document(
                        vf, caption=caption, parse_mode=ParseMode.HTML,
                    )
            await msg.delete()
        else:
            await msg.edit_text("❌ Gak nemu video — mungkin post teks/foto aja?", reply_markup=back_button())

    except Exception as e:
        err = str(e)
        if "No video" in err or "no video" in err.lower():
            friendly = "❌ Gak ada video di link itu — mungkin post teks/foto, bukan video."
        elif "HTTP Error 404" in err:
            friendly = "❌ URL gak ditemukan (404)."
        elif "HTTP Error 403" in err:
            friendly = "❌ Akses ditolak — mungkin video private."
        elif "Login" in err or "age" in err.lower():
            friendly = "❌ Butuh login — video age-restricted atau private."
        elif "File is larger" in err:
            friendly = "❌ Video kegedean (>50MB), gabisa dikirim."
        else:
            friendly = f"❌ Gagal: {err[:200]}"
        await msg.edit_text(friendly, reply_markup=back_button(), parse_mode=ParseMode.HTML)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str = None):
    if url is None and context.args:
        url = context.args[0]
    if not url:
        await update.message.reply_text("❌ Kirim URL.", reply_markup=back_button())
        return

    msg = await update.message.reply_text("⏳ Download audio (MP3)...")
    tmpdir = tempfile.mkdtemp()

    try:
        import yt_dlp
        opts = {
            "outtmpl": f"{tmpdir}/%(title).100s.%(ext)s",
            "quiet": True, "no_warnings": True,
            "format": "bestaudio/best",
            "max_filesize": MAX_SIZE,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)

        actual = None
        for f in os.listdir(tmpdir):
            actual = os.path.join(tmpdir, f)
            break

        if actual and os.path.exists(actual):
            fsize = os.path.getsize(actual)
            if fsize > MAX_SIZE:
                await msg.edit_text("❌ Audio >50MB.", reply_markup=back_button())
                return

            title = info.get("title", "Audio")[:100]
            dur = info.get("duration", 0) or 0
            dur_str = f"{int(dur)//60}:{int(dur)%60:02d}" if dur else "?"

            with open(actual, "rb") as af:
                await update.message.reply_audio(
                    af, title=title[:64],
                    performer=info.get("uploader", "")[:64],
                    duration=int(dur),
                    caption=f"🎵 <b>{title}</b>\n⏱ {dur_str}",
                    parse_mode=ParseMode.HTML,
                )
            await msg.delete()
        else:
            await msg.edit_text("❌ Gagal ekstrak audio.", reply_markup=back_button())

    except Exception as e:
        err = str(e)
        await msg.edit_text(f"❌ Gagal: {err[:200]}", reply_markup=back_button())
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


async def show_playlist(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str = None):
    if url is None and context.args:
        url = context.args[0]
    if not url:
        await update.message.reply_text("❌ Kirim URL playlist YouTube.", reply_markup=back_button())
        return

    msg = await update.message.reply_text("📋 Ambil info playlist...")

    try:
        import yt_dlp
        opts = {"quiet": True, "no_warnings": True, "extract_flat": True, "playlistend": 30}
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)

        title = info.get("title", "Playlist")
        count = info.get("playlist_count", 0) or len(info.get("entries", []))
        entries = info.get("entries", [])[:20]

        text = f"📋 <b>{title}</b>\n📊 Total: {count} video\n\n"
        for i, entry in enumerate(entries, 1):
            t = (entry.get("title") or "???")[:60]
            d = entry.get("duration", 0) or 0
            ds = f"{int(d)//60}:{int(d)%60:02d}" if d else "?"
            text += f"{i}. <b>{t}</b> · ⏱{ds}\n"

        if count > 20:
            text += f"\n...dan {count - 20} video lainnya"

        await msg.edit_text(text[:4000], parse_mode=ParseMode.HTML, reply_markup=back_button())

    except Exception as e:
        await msg.edit_text(f"❌ Gagal: {str(e)[:200]}", reply_markup=back_button())


async def cmd_dl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "📥 <b>Downloader</b>\n\n"
            "🎬 <code>/dl [url]</code> — Download video\n"
            "🎵 <code>/mp3 [url]</code> — Download audio\n"
            "📋 <code>/pl [url]</code> — Info playlist\n\n"
            "Atau klik /menu buat tampilan button.",
            parse_mode="HTML",
        )
        return
    await download_video(update, context)


async def cmd_mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ <b>Usage:</b> <code>/mp3 [url]</code>", parse_mode="HTML")
        return
    await download_audio(update, context)


async def cmd_pl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ <b>Usage:</b> <code>/pl [url playlist]</code>", parse_mode="HTML")
        return
    await show_playlist(update, context)


def register(app: Application):
    app.add_handler(CommandHandler("dl", cmd_dl))
    app.add_handler(CommandHandler("mp3", cmd_mp3))
    app.add_handler(CommandHandler("pl", cmd_pl))
