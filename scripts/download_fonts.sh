#!/bin/bash
#
# download_fonts.sh — Scarica i Google Fonts necessari per Il Quotidiano Geopolitico
# Autore: Thomas (Coder)
# Data: 2026-04-15
#
# Font scaricati:
#   - Playfair Display (Regular, Bold)
#   - EB Garamond (Regular, Italic)
#   - Courier Prime (Regular)
#
# I font vengono scaricati dai release GitHub ufficiali di Google Fonts.
#

set -e

ASSETS_DIR="$(cd "$(dirname "$0")/.." && pwd)/assets/fonts"
FONTS_DIR="$ASSETS_DIR"

echo "📥 Download Google Fonts per Il Tuo Quotidiano Geopolitico"
echo "══════════════════════════════════════════════════════════"
echo ""

# Crea la directory dei font se non esiste
mkdir -p "$FONTS_DIR"

# ── Playfair Display ──────────────────────────────────────────────────────────
PLAYFAIR_REGULAR="https://github.com/google/fonts/raw/main/ofl/playfairdisplay/PlayfairDisplay-Regular.ttf"
PLAYFAIR_BOLD="https://github.com/google/fonts/raw/main/ofl/playfairdisplay/PlayfairDisplay-Bold.ttf"
PLAYFAIR_ITALIC="https://github.com/google/fonts/raw/main/ofl/playfairdisplay/PlayfairDisplay-Italic.ttf"
PLAYFAIR_BOLDITALIC="https://github.com/google/fonts/raw/main/ofl/playfairdisplay/PlayfairDisplay-BoldItalic.ttf"

# ── EB Garamond ───────────────────────────────────────────────────────────────
GARAMOND_REGULAR="https://github.com/google/fonts/raw/main/ofl/ebgaramond/EBGaramond-Regular.ttf"
GARAMOND_ITALIC="https://github.com/google/fonts/raw/main/ofl/ebgaramond/EBGaramond-Italic.ttf"
GARAMOND_MEDIUM="https://github.com/google/fonts/raw/main/ofl/ebgaramond/EBGaramond-Medium.ttf"
GARAMOND_MEDIUMITALIC="https://github.com/google/fonts/raw/main/ofl/ebgaramond/EBGaramond-MediumItalic.ttf"

# ── Courier Prime ─────────────────────────────────────────────────────────────
COURIER_REGULAR="https://github.com/google/fonts/raw/main/ofl/courierprime/CourierPrime-Regular.ttf"
COURIER_BOLD="https://github.com/google/fonts/raw/main/ofl/courierprime/CourierPrime-Bold.ttf"
COURIER_ITALIC="https://github.com/google/fonts/raw/main/ofl/courierprime/CourierPrime-Italic.ttf"
COURIER_BOLDITALIC="https://github.com/google/fonts/raw/main/ofl/courierprime/CourierPrime-BoldItalic.ttf"

download_font() {
    local url="$1"
    local dest="$2"
    local name=$(basename "$dest" .ttf)

    if [ -f "$dest" ]; then
        echo "  ✓ $name (già presente)"
    else
        echo "  ⬇ $name..."
        curl -sL "$url" -o "$dest"
        if [ -f "$dest" ] && [ -s "$dest" ]; then
            echo "  ✓ $name scaricato"
        else
            echo "  ✗ ERRORE: $name non scaricato"
            return 1
        fi
    fi
}

echo "📁 Directory: $FONTS_DIR"
echo ""

# Playfair Display
echo "🎩 Playfair Display"
download_font "$PLAYFAIR_REGULAR" "$FONTS_DIR/PlayfairDisplay-Regular.ttf"
download_font "$PLAYFAIR_BOLD" "$FONTS_DIR/PlayfairDisplay-Bold.ttf"
download_font "$PLAYFAIR_ITALIC" "$FONTS_DIR/PlayfairDisplay-Italic.ttf"
download_font "$PLAYFAIR_BOLDITALIC" "$FONTS_DIR/PlayfairDisplay-BoldItalic.ttf"
echo ""

# EB Garamond
echo "📜 EB Garamond"
download_font "$GARAMOND_REGULAR" "$FONTS_DIR/EBGaramond-Regular.ttf"
download_font "$GARAMOND_ITALIC" "$FONTS_DIR/EBGaramond-Italic.ttf"
download_font "$GARAMOND_MEDIUM" "$FONTS_DIR/EBGaramond-Medium.ttf"
download_font "$GARAMOND_MEDIUMITALIC" "$FONTS_DIR/EBGaramond-MediumItalic.ttf"
echo ""

# Courier Prime
echo "🔤 Courier Prime"
download_font "$COURIER_REGULAR" "$FONTS_DIR/CourierPrime-Regular.ttf"
download_font "$COURIER_BOLD" "$FONTS_DIR/CourierPrime-Bold.ttf"
download_font "$COURIER_ITALIC" "$FONTS_DIR/CourierPrime-Italic.ttf"
download_font "$COURIER_BOLDITALIC" "$FONTS_DIR/CourierPrime-BoldItalic.ttf"
echo ""

# Verifica finale
echo "══════════════════════════════════════════════════════════"
echo "✅ Font installati:"
ls -la "$FONTS_DIR"/*.ttf 2>/dev/null | awk '{print "   " $9 " (" $5 " bytes)"}' || echo "   (nessun file trovato)"
echo ""
echo "Totale: $(ls -1 $FONTS_DIR/*.ttf 2>/dev/null | wc -l | tr -d ' ') font"