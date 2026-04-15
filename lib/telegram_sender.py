"""
lib/telegram_sender.py — Invio PNG a Nico via Telegram
"""
import os
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

def send_photo(chat_id: str, photo_path: str, caption: str = "") -> bool:
    """Invia una foto a un chat Telegram."""
    if not os.path.exists(photo_path):
        print(f"[telegram_sender] ERRORE: file non trovato: {photo_path}")
        return False

    url = f"{TELEGRAM_API}/sendPhoto"
    with open(photo_path, "rb") as f:
        files = {"photo": f}
        data = {
            "chat_id": chat_id,
            "caption": caption,
        }
        try:
            resp = requests.post(url, data=data, files=files, timeout=60)
            result = resp.json()
            if result.get("ok"):
                print(f"[telegram_sender] ✓ Inviato: {os.path.basename(photo_path)}")
                return True
            else:
                print(f"[telegram_sender] ERRORE Telegram: {result}")
                return False
        except Exception as e:
            print(f"[telegram_sender] ERRORE invio: {e}")
            return False

def send_all(png_paths: list[str], captions: list[str] = None) -> bool:
    """Invia tutti i PNG a Nico."""
    if captions is None:
        page_names = ["Prima Pagina", "Approfondimento", "Rubriche"]
        captions = [f"📰 {name} — Il Quotidiano Geopolitico" for name in page_names]

    all_ok = True
    for i, png_path in enumerate(png_paths):
        caption = captions[i] if i < len(captions) else ""
        if not send_photo(TELEGRAM_CHAT_ID, png_path, caption):
            all_ok = False
        else:
            print(f"[telegram_sender] Inviato ({i+1}/{len(png_paths)}): {os.path.basename(png_path)}")

    return all_ok

def send_text(chat_id: str, text: str) -> bool:
    """Invia un messaggio di testo."""
    url = f"{TELEGRAM_API}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    try:
        resp = requests.post(url, data=data, timeout=15)
        result = resp.json()
        if result.get("ok"):
            print(f"[telegram_sender] ✓ Messaggio inviato")
            return True
        else:
            print(f"[telegram_sender] ERRORE: {result}")
            return False
    except Exception as e:
        print(f"[telegram_sender] ERRORE: {e}")
        return False
