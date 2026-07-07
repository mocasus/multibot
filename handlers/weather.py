"""Weather checker"""
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode
from config import WEATHER_API_KEY


def back_button(target="menu_tools"):
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data=target)]])


async def do_cuaca(update: Update, context: ContextTypes.DEFAULT_TYPE, city: str = None):
    if city is None and context.args:
        city = " ".join(context.args)
    if not city:
        await update.message.reply_text("❌ Kirim nama kota.", reply_markup=back_button())
        return

    if not WEATHER_API_KEY:
        await update.message.reply_text(
            "❌ Weather API key belum diset.\n"
            "Tambahin <code>WEATHER_API_KEY</code> di .env.\n"
            "Dapetin di: openweathermap.org/api",
            parse_mode=ParseMode.HTML, reply_markup=back_button(),
        )
        return

    msg = await update.message.reply_text(f"🌤 Cek cuaca <b>{city}</b>...", parse_mode=ParseMode.HTML)

    try:
        import requests
        r = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": WEATHER_API_KEY, "units": "metric", "lang": "id"},
            timeout=10,
        )
        data = r.json()
        if r.status_code != 200:
            await msg.edit_text(
                f"❌ Kota <b>{city}</b> gak ditemukan.", parse_mode=ParseMode.HTML,
                reply_markup=back_button(),
            )
            return

        weather_emojis = {
            "Clear": "☀️", "Clouds": "☁️", "Rain": "🌧",
            "Drizzle": "🌦", "Thunderstorm": "⛈", "Snow": "❄️",
            "Mist": "🌫", "Haze": "🌫",
        }
        w_main = data["weather"][0]["main"]
        emoji = weather_emojis.get(w_main, "🌡")

        text = (
            f"{emoji} <b>Cuaca {data['name']}, {data['sys']['country']}</b>\n\n"
            f"🌡 Suhu: <b>{data['main']['temp']}°C</b> (terasa {data['main']['feels_like']}°C)\n"
            f"💧 Kelembaban: <b>{data['main']['humidity']}%</b>\n"
            f"🌬 Angin: <b>{data['wind']['speed']} m/s</b>\n"
            f"📊 Kondisi: <b>{data['weather'][0]['description'].title()}</b>"
        )
        await msg.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=back_button())
    except Exception as e:
        await msg.edit_text(f"❌ Gagal: {str(e)[:200]}", reply_markup=back_button())


async def cmd_cuaca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "🌤 <b>Usage:</b> <code>/cuaca [kota]</code>\nAtau /menu.", parse_mode="HTML",
        )
        return
    await do_cuaca(update, context)


def register(app: Application):
    app.add_handler(CommandHandler("cuaca", cmd_cuaca))
