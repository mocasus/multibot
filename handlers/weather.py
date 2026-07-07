from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode

async def cmd_cuaca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❌ <b>Usage:</b> <code>/cuaca [nama kota]</code>", parse_mode=ParseMode.HTML
        )
        return

    from config import WEATHER_API_KEY

    if not WEATHER_API_KEY:
        await update.message.reply_text(
            "❌ Weather API key belum diset. Tambahin <code>WEATHER_API_KEY</code> di .env.\n"
            "Dapetin gratis di: https://openweathermap.org/api",
            parse_mode=ParseMode.HTML,
        )
        return

    city = " ".join(context.args)
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
            await msg.edit_text(f"❌ Kota <b>{city}</b> gak ditemukan.", parse_mode=ParseMode.HTML)
            return

        weather_emojis = {
            "Clear": "☀️", "Clouds": "☁️", "Rain": "🌧", "Drizzle": "🌦",
            "Thunderstorm": "⛈", "Snow": "❄️", "Mist": "🌫", "Haze": "🌫",
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
        await msg.edit_text(text, parse_mode=ParseMode.HTML)

    except Exception as e:
        await msg.edit_text(f"❌ <b>Gagal:</b> {str(e)[:200]}", parse_mode=ParseMode.HTML)

def register(app: Application):
    app.add_handler(CommandHandler("cuaca", cmd_cuaca))
