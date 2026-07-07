from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode
import math

ALLOWED_NAMES = {
    "pi": math.pi, "e": math.e, "tau": math.tau,
    "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
    "tan": math.tan, "log": math.log, "log10": math.log10,
    "log2": math.log2, "abs": abs, "round": round,
    "pow": pow, "min": min, "max": max,
    "ceil": math.ceil, "floor": math.floor,
    "radians": math.radians, "degrees": math.degrees,
}

async def cmd_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❌ <b>Usage:</b> <code>/calc [ekspresi]</code>\n\n"
            "Contoh:\n"
            "<code>/calc 2 + 2 * 3</code>\n"
            "<code>/calc sqrt(144)</code>\n"
            "<code>/calc sin(pi / 2)</code>",
            parse_mode=ParseMode.HTML,
        )
        return

    expr = " ".join(context.args)

    # Security: only allow safe chars
    safe_chars = set("0123456789+-*/().,%^ ")
    for c in expr:
        if c.isalpha() or c == "_":
            continue
        if c not in safe_chars:
            await update.message.reply_text(
                f"❌ Karakter gaboleh: <code>{c}</code>", parse_mode=ParseMode.HTML
            )
            return

    try:
        result = eval(expr, {"__builtins__": {}}, ALLOWED_NAMES)
        # Format result
        if isinstance(result, float):
            if abs(result) < 1e10 and abs(result) > 1e-10:
                result_str = f"{result:,.6f}".rstrip("0").rstrip(".")
            else:
                result_str = f"{result:.6e}"
        else:
            result_str = f"{result:,}"

        await update.message.reply_text(
            f"🧮 <code>{expr}</code>\n<b>= {result_str}</b>", parse_mode=ParseMode.HTML
        )

    except Exception as e:
        await update.message.reply_text(
            f"❌ <b>Error:</b> {str(e)[:200]}", parse_mode=ParseMode.HTML
        )

def register(app: Application):
    app.add_handler(CommandHandler("calc", cmd_calc))
