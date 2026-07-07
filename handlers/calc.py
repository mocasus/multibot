"""Calculator"""
import math
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode

ALLOWED_NAMES = {
    "pi": math.pi, "e": math.e, "tau": math.tau,
    "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
    "tan": math.tan, "log": math.log, "log10": math.log10,
    "log2": math.log2, "abs": abs, "round": round,
    "pow": pow, "min": min, "max": max,
    "ceil": math.ceil, "floor": math.floor,
    "radians": math.radians, "degrees": math.degrees,
}


def back_button(target="menu_tools"):
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data=target)]])


async def do_calc(update: Update, context: ContextTypes.DEFAULT_TYPE, expr: str = None):
    if expr is None and context.args:
        expr = " ".join(context.args)
    if not expr:
        await update.message.reply_text("❌ Kirim ekspresi.", reply_markup=back_button())
        return

    safe_chars = set("0123456789+-*/().,%^ ")
    for c in expr:
        if c.isalpha() or c == "_":
            continue
        if c not in safe_chars:
            await update.message.reply_text(
                f"❌ Karakter gaboleh: <code>{c}</code>", parse_mode=ParseMode.HTML,
                reply_markup=back_button(),
            )
            return

    try:
        result = eval(expr, {"__builtins__": {}}, ALLOWED_NAMES)
        if isinstance(result, float):
            if abs(result) < 1e10 and abs(result) > 1e-10:
                result_str = f"{result:,.6f}".rstrip("0").rstrip(".")
            else:
                result_str = f"{result:.6e}"
        else:
            result_str = f"{result:,}"

        await update.message.reply_text(
            f"🧮 <code>{expr}</code>\n<b>= {result_str}</b>",
            parse_mode=ParseMode.HTML, reply_markup=back_button(),
        )
    except Exception as e:
        await update.message.reply_text(
            f"❌ Error: {str(e)[:200]}", reply_markup=back_button(),
        )


async def cmd_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "🧮 <b>Usage:</b> <code>/calc [ekspresi]</code>\n"
            "Contoh: <code>/calc sqrt(144)</code>\nAtau /menu.",
            parse_mode="HTML",
        )
        return
    await do_calc(update, context)


def register(app: Application):
    app.add_handler(CommandHandler("calc", cmd_calc))
