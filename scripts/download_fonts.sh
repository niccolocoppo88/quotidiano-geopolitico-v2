#!/bin/bash
#
# download_fonts.sh — Scarica i Google Fonts necessari per Il Quotidiano Geopolitico
# Autore: Thomas (Coder)
# Data: 2026-04-15
#
# Font scaricati dai CDN Google Fonts (fonts.gstatic.com)
#   - Playfair Display (Regular, Bold, Italic) — BoldItalic non disponibile
#   - EB Garamond (Regular, Italic, Medium) — MediumItalic non disponibile
#   - Courier Prime (Regular, Bold, Italic, BoldItalic)
#
set -e

ASSETS_DIR="$(cd "$(dirname "$0")/.." && pwd)/assets/fonts"
FONTS_DIR="$ASSETS_DIR"

echo "📥 Download Google Fonts per Il Tuo Quotidiano Geopolitico"
echo "══════════════════════════════════════════════════════════"
echo ""

mkdir -p "$FONTS_DIR"

# Helper: scarica un font se non esiste o è corrotto
download_font() {
    local url="$1"
    local dest="$2"
    local name=$(basename "$dest")

    # Verifica esistenza e validità
    if [ -f "$dest" ] && [ -s "$dest" ]; then
        # Check magic bytes (TTF = 00 01 00 00)
        magic=$(head -c 4 "$dest" | od -An -tx1 | tr -d ' ')
        if [ "$magic" = "00010000" ] || [ "$magic" = "4f54544f" ]; then
            echo "  ✓ $name (già valido)"
            return 0
        fi
        echo "  ⚠ $name (corrotto, riscarico)"
        rm "$dest"
    fi

    echo "  ⬇ $name..."
    curl -sL --max-time 30 -A "Mozilla/5.0" "$url" -o "$dest"
    if [ -f "$dest" ] && [ -s "$dest" ]; then
        magic=$(head -c 4 "$dest" | od -An -tx1 | tr -d ' ')
        if [ "$magic" = "00010000" ] || [ "$magic" = "4f54544f" ]; then
            echo "  ✓ $name scaricato ($(wc -c < "$dest") bytes)"
        else
            echo "  ✗ ERRORE: $name non è un TTF valido"
            rm "$dest"
            return 1
        fi
    else
        echo "  ✗ ERRORE: $name non scaricato"
        return 1
    fi
}

# ── Playfair Display ──────────────────────────────────────────────────────────
echo "🎩 Playfair Display"
download_font "https://fonts.gstatic.com/s/playfairdisplay/v40/nuFvD-vYSZviVYUb_rj3ij__anPXJzDwcbmjWBN2PKdFvUDQ.ttf" \
    "$FONTS_DIR/PlayfairDisplay-Regular.ttf"
download_font "https://fonts.gstatic.com/s/playfairdisplay/v40/nuFvD-vYSZviVYUb_rj3ij__anPXJzDwcbmjWBN2PKeiukDQ.ttf" \
    "$FONTS_DIR/PlayfairDisplay-Bold.ttf"
download_font "https://fonts.gstatic.com/s/playfairdisplay/v40/nuFRD-vYSZviVYUb_rj3ij__anPXDTnCjmHKM4nYO7KN_qiTbtY.ttf" \
    "$FONTS_DIR/PlayfairDisplay-Italic.ttf"
echo ""

# ── EB Garamond ───────────────────────────────────────────────────────────────
echo "📜 EB Garamond"
download_font "https://fonts.gstatic.com/s/ebgaramond/v32/SlGDmQSNjdsmc35JDF1K5E55YMjF_7DPuGi-6_RUAw.ttf" \
    "$FONTS_DIR/EBGaramond-Regular.ttf"
download_font "https://fonts.gstatic.com/s/ebgaramond/v32/SlGFmQSNjdsmc35JDF1K5GRwUjcdlttVFm-rI7e8QI96.ttf" \
    "$FONTS_DIR/EBGaramond-Italic.ttf"
download_font "https://fonts.gstatic.com/s/ebgaramond/v32/SlGDmQSNjdsmc35JDF1K5E55YMjF_7DPuGi-2fRUAw.ttf" \
    "$FONTS_DIR/EBGaramond-Medium.ttf"
echo ""

# ── Courier Prime ─────────────────────────────────────────────────────────────
echo "🔤 Courier Prime"
download_font "https://fonts.gstatic.com/s/courierprime/v11/u-4n0q2lgwslOqpF_6gQ8kELawRpXw.ttf" \
    "$FONTS_DIR/CourierPrime-Regular.ttf"
download_font "https://fonts.gstatic.com/s/courierprime/v11/u-450q2lgwslOqpF_6gQ8kELWwY.ttf" \
    "$FONTS_DIR/CourierPrime-Bold.ttf"
download_font "https://fonts.gstatic.com/s/courierprime/v11/u-4k0q2lgwslOqpF_6gQ8kELY7pMf-c.ttf" \
    "$FONTS_DIR/CourierPrime-Italic.ttf"
download_font "https://fonts.gstatic.com/s/courierprime/v11/u-4k0q2lgwslOqpF_6gQ8kELZ7pMf-c.ttf" \
    "$FONTS_DIR/CourierPrime-BoldItalic.ttf"
echo ""

# Verifica finale
echo "══════════════════════════════════════════════════════════"
echo "✅ Font installati:"
for f in "$FONTS_DIR"/*.ttf; do
    if [ -f "$f" ]; then
        size=$(wc -c < "$f")
        echo "   $(basename $f) ($((size/1024))KB)"
    fi
done
