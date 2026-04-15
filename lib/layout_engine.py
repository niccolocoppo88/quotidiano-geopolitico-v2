"""
lib/layout_engine.py — Griglia 6 colonne e costanti di design
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from config import PAGE_W, PAGE_H, DPI, COL_CARTA, COL_NERO, COL_BORDEAUX, COL_ORO, COL_CREMISI, COL_GRIGIO

# ── Griglia ──────────────────────────────────────────────────────────────────
# Page: 1200 x 1650 px @72dpi
# 6 colonne + 5 gutter
COL_WIDTH = 170       # px per colonna
COL_GAP   = 20        # px tra colonne
MARGIN_X  = 30        # px margine sinistro/destro
MARGIN_Y  = 30        # px margine alto/basso
HEADER_H  = 100       # px riservati all'header
FOOTER_H  = 60        # px riservati al footer

CONTENT_W = PAGE_W - 2 * MARGIN_X
CONTENT_H = PAGE_H - HEADER_H - FOOTER_H - 2 * MARGIN_Y

# Posizioni X di ogni colonna
def col_x(n: int) -> int:  # n: 0-5
    return MARGIN_X + n * (COL_WIDTH + COL_GAP)

# Larghezza per n colonne contigue (es. 4 col = 4*170 + 3*20)
def col_span(n: int) -> int:
    return n * COL_WIDTH + (n - 1) * COL_GAP

# ── Colori ───────────────────────────────────────────────────────────────────
COLOR_CARTA   = COL_CARTA    # (245, 240, 232)
COLOR_NERO    = COL_NERO     # (26, 26, 26)
COLOR_BORDEAUX = COL_BORDEAUX # (139, 26, 26)
COLOR_ORO     = COL_ORO      # (184, 134, 11)
COLOR_CREMISI = COL_CREMISI  # (192, 57, 43)
COLOR_GRIGIO  = COL_GRIGIO   # (74, 74, 74)

def hex_to_rgb(hex_str: str):
    h = hex_str.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# ── Font helper ───────────────────────────────────────────────────────────────
def font_name(family: str, variant: str = "regular") -> str:
    from lib.font_manager import get_font
    variants = {
        "regular": "regular",
        "bold": "bold",
        "italic": "italic",
        "bolditalic": "bolditalic",
    }
    return get_font(family, variants.get(variant, "regular"))

# ── Layout constants ───────────────────────────────────────────────────────────
LINE_H_SMALL = 14
LINE_H_BODY  = 18
LINE_H_TITLE = 24
LINE_H_MAST  = 48

# Colonna singola = ~60 caratteri EB Garamond 12pt
CHARS_PER_COL = 60

# ── Drawing helpers ───────────────────────────────────────────────────────────
def draw_filetto_oro(c, x, y, w, thickness=1):
    """Disegna una linea orizzontale oro."""
    c.setStrokeColorRGB(*[x/255 for x in COL_ORO])
    c.setLineWidth(thickness)
    c.line(x, y, x + w, y)

def draw_double_filetto_oro(c, x, y, w, t1=2, t2=1, gap=4):
    """Disegna doppio filetto oro (per header importanti)."""
    c.setStrokeColorRGB(*[x/255 for x in COL_ORO])
    c.setLineWidth(t1)
    c.line(x, y, x + w, y)
    c.setLineWidth(t2)
    c.line(x, y - t1 - gap, x + w, y - t1 - gap)

def draw_flash_box(c, x, y, w, h, text, font_size=11):
    """Box flash cremisi con bordo oro."""
    c.setFillColorRGB(*[x/255 for x in COL_CREMISI])
    c.rect(x, y - h, w, h, fill=1, stroke=0)
    # Bordo oro a sinistra
    c.setStrokeColorRGB(*[x/255 for x in COL_ORO])
    c.setLineWidth(4)
    c.line(x, y, x, y - h)
    # Testo
    c.setFillColorRGB(1, 1, 1)
    c.setFont(font_name("CourierPrime", "bold"), font_size)
    c.drawString(x + 8, y - h/2 - font_size/3, text)

def draw_separator(c, x, y, w):
    """Separatore oro singolo."""
    draw_filetto_oro(c, x, y, w, thickness=1)

def draw_masthead(c, title: str, date_str: str):
    """Disegna il masthead del giornale."""
    mid_x = PAGE_W / 2
    y_top = PAGE_H - MARGIN_Y

    # Titolo centrato
    c.setFillColorRGB(*[x/255 for x in COL_NERO])
    c.setFont(font_name("PlayfairDisplay", "bold"), 48)
    c.drawCentredString(mid_x, y_top - 48, title)

    # Doppio filetto oro
    double_y = y_top - 56
    draw_double_filetto_oro(c, MARGIN_X, double_y, PAGE_W - 2 * MARGIN_X)

    # Data a destra
    c.setFillColorRGB(*[x/255 for x in COL_GRIGIO])
    c.setFont(font_name("CourierPrime", "regular"), 11)
    c.drawRightString(PAGE_W - MARGIN_X, double_y - 16, date_str)

def draw_footer(c, page_label: str, page_num: int):
    """Disegna il footer della pagina."""
    y = MARGIN_Y
    c.setStrokeColorRGB(*[x/255 for x in COL_ORO])
    c.setLineWidth(1)
    c.line(MARGIN_X, y + 30, PAGE_W - MARGIN_X, y + 30)

    c.setFillColorRGB(*[x/255 for x in COL_GRIGIO])
    c.setFont(font_name("CourierPrime", "regular"), 9)
    disclaimer = "QUOTIDIANO GEOPOLITICO — Anno LXXIII — Aut.Trib. Roma n. 152/2026"
    c.drawCentredString(PAGE_W / 2, y + 16, disclaimer)
    c.drawRightString(PAGE_W - MARGIN_X, y + 6, f"p. {page_num}")
    c.drawString(MARGIN_X, y + 6, page_label)

def wrap_text(text: str, font_name_str: str, font_size: float, max_width: float) -> list:
    """Wrap text into lines that fit within max_width."""
    from reportlab.pdfbase.pdfmetrics import stringWidth
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        if stringWidth(test, font_name_str, font_size) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def draw_text_block(c, x, y, text: str, font_name_str: str, font_size: float,
                    max_width: float, line_height: float, color=None, align="left"):
    """Draw a block of text with word wrap, returns new y position."""
    from reportlab.pdfbase.pdfmetrics import stringWidth
    if color:
        c.setFillColorRGB(*[x/255 for x in color] if isinstance(color, str) else color)
    else:
        c.setFillColorRGB(*[x/255 for x in COL_NERO])

    c.setFont(font_name_str, font_size)
    lines = wrap_text(text, font_name_str, font_size, max_width)
    cur_y = y
    for line in lines:
        if align == "center":
            c.drawCentredString(x + max_width / 2, cur_y, line)
        elif align == "right":
            c.drawRightString(x + max_width, cur_y, line)
        else:
            c.drawString(x, cur_y, line)
        cur_y -= line_height
    return cur_y

def draw_capolettera(c, x, y, font_size: float, line_height: float, color=None):
    """Draws the initial letter for a drop cap, returns y after cap."""
    # This is handled in the text drawing — just position the first letter
    pass
