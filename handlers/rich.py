"""Rich message helpers — sendRichMessage + styled inline buttons via httpx"""
import httpx
from config import BOT_TOKEN


BTN_STYLES = {"primary": "primary", "success": "success", "danger": "danger"}


def btn(text: str, callback: str, style: str = None) -> dict:
    """Build inline button dict. style: 'primary'|'success'|'danger'|None"""
    b = {"text": text, "callback_data": callback}
    if style:
        b["style"] = style
    return b


def copy_btn(text: str, value: str) -> dict:
    """Copy-to-clipboard button"""
    return {"text": text, "copy_text": {"text": value}}


def url_btn(text: str, href: str) -> dict:
    return {"text": text, "url": href}


def rows(*row_list: list) -> list:
    return list(row_list)


async def rich_send(chat_id: int, markdown: str, buttons: list = None, reply_to: int = None) -> dict:
    """Send rich message via Bot API sendRichMessage (bypass aiogram)"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendRichMessage"
    body = {"chat_id": chat_id, "rich_message": {"markdown": markdown}}
    if buttons:
        body["reply_markup"] = {"inline_keyboard": buttons}
    if reply_to:
        body["reply_parameters"] = {"message_id": reply_to}
    async with httpx.AsyncClient(timeout=15) as c:
        r = await c.post(url, json=body)
        return r.json()


async def rich_edit(chat_id: int, msg_id: int, markdown: str, buttons: list = None) -> dict:
    """Edit existing message with rich content"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
    body = {"chat_id": chat_id, "message_id": msg_id, "rich_message": {"markdown": markdown}}
    if buttons:
        body["reply_markup"] = {"inline_keyboard": buttons}
    async with httpx.AsyncClient(timeout=15) as c:
        r = await c.post(url, json=body)
        return r.json()
