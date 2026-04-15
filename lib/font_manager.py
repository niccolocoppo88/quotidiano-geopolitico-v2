"""
lib/font_manager.py — Registrazione font bundled in assets/fonts/
"""
import os
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from config import FONTS_DIR

# Registra i font Google Fonts bundled
FONTS_REGISTERED = False

def register_fonts():
    global FONTS_REGISTERED
    if FONTS_REGISTERED:
        return

    font_files = {
        "PlayfairDisplay": {
            "regular": "PlayfairDisplay-Regular.ttf",
            "bold": "PlayfairDisplay-Bold.ttf",
            "italic": "PlayfairDisplay-Italic.ttf",
            "bolditalic": "PlayfairDisplay-BoldItalic.ttf",
        },
        "EBGaramond": {
            "regular": "EBGaramond-Regular.ttf",
            "italic": "EBGaramond-Italic.ttf",
            "medium": "EBGaramond-Medium.ttf",
        },
        "CourierPrime": {
            "regular": "CourierPrime-Regular.ttf",
            "bold": "CourierPrime-Bold.ttf",
            "italic": "CourierPrime-Italic.ttf",
            "bolditalic": "CourierPrime-BoldItalic.ttf",
        },
    }

    for family, variants in font_files.items():
        for variant, filename in variants.items():
            font_path = FONTS_DIR / filename
            if font_path.exists():
                pdfmetrics.registerFont(TTFont(f"{family}-{variant}", str(font_path)))
            else:
                print(f"[font_manager] ATTENZIONE: font non trovato {font_path}")

    FONTS_REGISTERED = True
    print(f"[font_manager] {len(font_files)} famiglie registrate")


def get_font(name: str, variant: str = "regular"):
    """Restituisce il nome del font registrato per ReportLab."""
    return f"{name}-{variant}"
