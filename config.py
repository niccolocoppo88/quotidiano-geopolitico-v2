"""
config.py — Il Tuo Quotidiano Geopolitico v2
Configuration centralizzata per il progetto.
"""
import os
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.resolve()
ASSETS_DIR = BASE_DIR / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# ── Canvas ────────────────────────────────────────────────────────────────────
PAGE_W = 1200
PAGE_H = 1650
DPI = 72

# ── Layout ────────────────────────────────────────────────────────────────────
MARGIN_X  = 30   # px margine sinistro/destro
MARGIN_Y  = 30   # px margine alto/basso
COL_WIDTH = 170  # px per colonna
COL_GAP   = 20   # px tra colonne

# ── Palette ───────────────────────────────────────────────────────────────────
COL_CARTA   = (245, 240, 232)   # #F5F0E8
COL_NERO     = (26, 26, 26)     # #1A1A1A
COL_BORDEAUX = (139, 26, 26)    # #8B1A1A
COL_ORO      = (184, 134, 11)   # #B8860B
COL_CREMISI  = (192, 57, 43)    # #C0392B
COL_GRIGIO   = (74, 74, 74)     # #4A4A4A

# ── Font families (Google Fonts bundled in assets/fonts/) ───────────────────
FONT_PLAYFAIR   = "PlayfairDisplay-Regular.ttf"
FONT_PLAYFAIR_B = "PlayfairDisplay-Bold.ttf"
FONT_GARAMOND   = "EBGaramond-Regular.ttf"
FONT_GARAMOND_I = "EBGaramond-Italic.ttf"
FONT_COURIER    = "CourierPrime-Regular.ttf"
FONT_COURIER_B  = "CourierPrime-Bold.ttf"

FONT_MAP = {
    "Playfair": (str(FONTS_DIR / FONT_PLAYFAIR), str(FONTS_DIR / FONT_PLAYFAIR_B)),
    "Garamond": (str(FONTS_DIR / FONT_GARAMOND), str(FONTS_DIR / FONT_GARAMOND_I)),
    "Courier":  (str(FONTS_DIR / FONT_COURIER), str(FONTS_DIR / FONT_COURIER_B)),
}

# ── News sources ──────────────────────────────────────────────────────────────
RSS_FEEDS = {
    "geopolitica": [
        "https://feeds.reuters.com/reuters/worldnews",
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://www.ansa.it/sito/ansait_rss.xml",
    ],
    "economia": [
        "https://feeds.reuters.com/reuters/businessNews",
        "https://feeds.bbci.co.uk/news/business/rss.xml",
    ],
    "tech": [
        "https://feeds.bbci.co.uk/news/technology/rss.xml",
        "https://techcrunch.com/feed/",
    ],
}

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

# ── MiniMax ───────────────────────────────────────────────────────────────────
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "")
MINIMAX_BASE_URL = "https://api.minimax.io/v1/text/chatcompletion_v2"

# ── Telegram ──────────────────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8799149563:AAEPopcG5I94wHPxR6Rh1raYH6iHTZ9jD88")
TELEGRAM_CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID", "8336585509")

# ── Cron ──────────────────────────────────────────────────────────────────────
CRON_SCHEDULE = "30 7 * * *"
CRON_TZ = "Europe/Rome"

# ── Date ──────────────────────────────────────────────────────────────────────
from datetime import datetime
TODAY = datetime.now().strftime("%d %B %Y").lower()