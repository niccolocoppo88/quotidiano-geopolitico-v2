"""
lib/page_frontpage.py — Prima pagina del Quotidiano Geopolitico v2
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape
from reportlab.pdfbase.pdfmetrics import stringWidth
from config import PAGE_W, PAGE_H, MARGIN_X, MARGIN_Y, COL_WIDTH, COL_GAP
from lib.layout_engine import (
    col_x, col_span, COLOR_CARTA, COLOR_NERO, COLOR_BORDEAUX, COLOR_ORO,
    COLOR_CREMISI, COLOR_GRIGIO, font_name, draw_filetto_oro,
    draw_double_filetto_oro, draw_separator, draw_masthead, draw_footer,
    draw_text_block, wrap_text, LINE_H_BODY, LINE_H_TITLE, HEADER_H, FOOTER_H,
)
from datetime import datetime

def col_c(n): return col_x(n)
def col_w(n): return col_span(n)

def render_frontpage(content: dict, date_str: str, output_path: str):
    """Renderizza la prima pagina PDF."""
    c = canvas.Canvas(output_path, pagesize=(PAGE_W, PAGE_H))
    c.setFillColorRGB(*[x/255 for x in COLOR_CARTA])
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    mid_x = PAGE_W / 2

    # ── MASTHEAD ────────────────────────────────────────────────────────────
    y_top = PAGE_H - MARGIN_Y
    c.setFillColorRGB(*[x/255 for x in COLOR_NERO])
    c.setFont(font_name("PlayfairDisplay", "bold"), 48)
    c.drawCentredString(mid_x, y_top - 48, "QUOTIDIANO GEOPOLITICO")

    double_y = y_top - 56
    # Doppio filetto oro
    c.setStrokeColorRGB(*[x/255 for x in COLOR_ORO])
    c.setLineWidth(2)
    c.line(MARGIN_X, double_y, PAGE_W - MARGIN_X, double_y)
    c.setLineWidth(1)
    c.line(MARGIN_X, double_y - 6, PAGE_W - MARGIN_X, double_y - 6)

    # Data a destra
    c.setFillColorRGB(*[x/255 for x in COLOR_GRIGIO])
    c.setFont(font_name("CourierPrime", "regular"), 11)
    c.drawRightString(PAGE_W - MARGIN_X, double_y - 18, date_str)

    # ── FLASH BAR ───────────────────────────────────────────────────────────
    flash_text = content.get("flash_news", ["⚡ ULTIM'ORA — VERTICE NATO A BRUXELLES"])[0]
    flash_bar_h = 32
    flash_bar_y = double_y - 30

    c.setFillColorRGB(*[x/255 for x in COLOR_CREMISI])
    c.rect(MARGIN_X, flash_bar_y - flash_bar_h, PAGE_W - 2 * MARGIN_X, flash_bar_h, fill=1, stroke=0)
    # Bordo oro a sinistra
    c.setStrokeColorRGB(*[x/255 for x in COLOR_ORO])
    c.setLineWidth(4)
    c.line(MARGIN_X, flash_bar_y, MARGIN_X, flash_bar_y - flash_bar_h)

    c.setFillColorRGB(1, 1, 1)
    c.setFont(font_name("CourierPrime", "bold"), 12)
    c.drawString(MARGIN_X + 10, flash_bar_y - flash_bar_h / 2 - 6, f"⚡ ULTIM'ORA — {flash_text[:70]}")

    # ── ARTICOLO PRINCIPALE (col 0-3) ───────────────────────────────────────
    main = content.get("main_article", {})
    main_x = MARGIN_X
    main_w = col_w(4)
    main_y = flash_bar_y - flash_bar_h - 20

    # Occhiello
    occhiello = main.get("occhiello", "geopolitica").upper()
    c.setFillColorRGB(*[x/255 for x in COLOR_BORDEAUX])
    c.setFont(font_name("PlayfairDisplay", "italic"), 14)
    c.drawString(main_x, main_y, f"// {occhiello}")

    # Titolo
    titolo = main.get("titolo", "Titolo non disponibile")
    main_y -= 20
    c.setFillColorRGB(*[x/255 for x in COLOR_NERO])
    c.setFont(font_name("PlayfairDisplay", "bold"), 30)
    # Wrap lungo titolo
    title_lines = wrap_text(titolo, font_name("PlayfairDisplay", "bold"), 30, main_w)
    for line in title_lines:
        c.drawString(main_x, main_y, line)
        main_y -= LINE_H_TITLE

    # Sommario
    main_y -= 4
    sommario = main.get("sommario", "")
    c.setFillColorRGB(*[x/255 for x in COLOR_GRIGIO])
    c.setFont(font_name("EBGaramond", "italic"), 14)
    sommario_lines = wrap_text(sommario, font_name("EBGaramond", "italic"), 14, main_w)
    for line in sommario_lines:
        c.drawString(main_x, main_y, line)
        main_y -= 16

    # Foto placeholder (rettangolo grigio con didascalia)
    main_y -= 12
    foto_h = 160
    c.setFillColorRGB(0.6, 0.6, 0.6)
    c.rect(main_x, main_y - foto_h, main_w, foto_h, fill=1, stroke=0)
    c.setStrokeColorRGB(*[x/255 for x in COLOR_GRIGIO])
    c.setLineWidth(1)
    c.rect(main_x, main_y - foto_h, main_w, foto_h, fill=0, stroke=1)
    c.setFillColorRGB(0.4, 0.4, 0.4)
    c.setFont(font_name("CourierPrime", "regular"), 10)
    c.drawCentredString(main_x + main_w / 2, main_y - foto_h / 2 - 4, "📷 Foto B/N — Reuters")

    # ── SIDEBAR (col 4-5) ────────────────────────────────────────────────────
    sidebar_x = col_x(4)
    sidebar_w = col_w(2)
    sidebar_y = flash_bar_y - flash_bar_h - 20

    # Flash box 1
    flash1_text = content.get("flash_news", [""])[1] if len(content.get("flash_news", [])) > 1 else "Flash 2"
    flash1_h = 60
    c.setFillColorRGB(*[x/255 for x in COLOR_CREMISI])
    c.rect(sidebar_x, sidebar_y - flash1_h, sidebar_w, flash1_h, fill=1, stroke=0)
    c.setStrokeColorRGB(*[x/255 for x in COLOR_ORO])
    c.setLineWidth(4)
    c.line(sidebar_x, sidebar_y, sidebar_x, sidebar_y - flash1_h)
    c.setFillColorRGB(1, 1, 1)
    c.setFont(font_name("CourierPrime", "bold"), 10)
    c.drawString(sidebar_x + 8, sidebar_y - 14, "⚡ FLASH")
    c.setFont(font_name("CourierPrime", "regular"), 11)
    # Wrap flash text
    flash_lines = wrap_text(flash1_text[:60], font_name("CourierPrime", "regular"), 11, sidebar_w - 16)
    fy = sidebar_y - 28
    for fl in flash_lines:
        c.drawString(sidebar_x + 8, fy, fl)
        fy -= 13

    # Sezione ECONOMIA
    econ_y = sidebar_y - flash1_h - 16
    c.setStrokeColorRGB(*[x/255 for x in COLOR_ORO])
    c.setLineWidth(2)
    c.line(sidebar_x, econ_y, sidebar_x + sidebar_w, econ_y)

    c.setFillColorRGB(*[x/255 for x in COLOR_BORDEAUX])
    c.setFont(font_name("PlayfairDisplay", "bold"), 14)
    c.drawString(sidebar_x, econ_y - 16, "ECONOMIA")

    econ_items = content.get("economia_items", ["Borsa Milano: +1.2%", "Spread BTP-Bund a 98", "Inflazione: +2.1%"])
    econ_y -= 30
    for item in econ_items[:3]:
        c.setFillColorRGB(*[x/255 for x in COLOR_NERO])
        c.setFont(font_name("EBGaramond", "regular"), 12)
        c.drawString(sidebar_x + 6, econ_y, "• " + item[:30])
        econ_y -= LINE_H_BODY

    # Sezione TECH
    tech_y = econ_y - 16
    c.setStrokeColorRGB(*[x/255 for x in COLOR_ORO])
    c.setLineWidth(2)
    c.line(sidebar_x, tech_y, sidebar_x + sidebar_w, tech_y)

    c.setFillColorRGB(*[x/255 for x in COLOR_BORDEAUX])
    c.setFont(font_name("PlayfairDisplay", "bold"), 14)
    c.drawString(sidebar_x, tech_y - 16, "TECH")

    tech_items = content.get("tech_items", ["OpenAI lancia GPT-5", "Apple: evento il 23", "Meta: tagli in Europa"])
    tech_y -= 30
    for item in tech_items[:3]:
        c.setFillColorRGB(*[x/255 for x in COLOR_NERO])
        c.setFont(font_name("EBGaramond", "regular"), 12)
        c.drawString(sidebar_x + 6, tech_y, "• " + item[:30])
        tech_y -= LINE_H_BODY

    # ── COLONNE INFERIORI (6 col grid) ──────────────────────────────────────
    bottom_y = min(sidebar_y - LINE_H_BODY * 4 - 20, main_y - foto_h - 20)
    draw_separator(c, MARGIN_X, bottom_y, PAGE_W - 2 * MARGIN_X)

    # Mondo
    mondo_x = col_x(0)
    mondo_w = col_w(3)
    mondo_y = bottom_y - 16
    c.setFillColorRGB(*[x/255 for x in COLOR_BORDEAUX])
    c.setFont(font_name("PlayfairDisplay", "bold"), 14)
    c.drawString(mondo_x, mondo_y, "MONDO")
    mondo_y -= 20

    mondo_items = content.get("mondo_items", ["Iran: negoziati nucleare ripresi", "Francia: riforma pensioni contestata", "India: elections in corso"])
    c.setFont(font_name("EBGaramond", "regular"), 12)
    for item in mondo_items[:3]:
        c.setFillColorRGB(*[x/255 for x in COLOR_NERO])
        item_lines = wrap_text("• " + item, font_name("EBGaramond", "regular"), 12, mondo_w)
        for il in item_lines:
            c.drawString(mondo_x + 4, mondo_y, il)
            mondo_y -= LINE_H_BODY
        mondo_y -= 2

    # Analisi (col 3-5)
    analisi_x = col_x(3)
    analisi_w = col_w(3)
    analisi_y = bottom_y - 16
    c.setFillColorRGB(*[x/255 for x in COLOR_BORDEAUX])
    c.setFont(font_name("PlayfairDisplay", "bold"), 14)
    c.drawString(analisi_x, analisi_y, "ANALISI")
    analisi_y -= 20

    analisi_items = ["Il ruolo dell'Italia nel nuovo ordine mondiale", "Clima: vertice COP32 a Dubai"]
    c.setFont(font_name("EBGaramond", "regular"), 12)
    for item in analisi_items:
        c.setFillColorRGB(*[x/255 for x in COLOR_NERO])
        item_lines = wrap_text("• " + item, font_name("EBGaramond", "regular"), 12, analisi_w)
        for il in item_lines:
            c.drawString(analisi_x + 4, analisi_y, il)
            analisi_y -= LINE_H_BODY
        analisi_y -= 2

    # ── FOOTER ───────────────────────────────────────────────────────────────
    footer_y = MARGIN_Y + 40
    draw_separator(c, MARGIN_X, footer_y, PAGE_W - 2 * MARGIN_X)
    c.setFillColorRGB(*[x/255 for x in COLOR_GRIGIO])
    c.setFont(font_name("CourierPrime", "regular"), 9)
    disclaimer = "QUOTIDIANO GEOPOLITICO — Anno LXXIII — Aut.Trib. Roma n. 152/2026"
    c.drawCentredString(mid_x, footer_y - 14, disclaimer)
    c.drawRightString(PAGE_W - MARGIN_X, footer_y - 26, "p. 1")
    c.drawString(MARGIN_X, footer_y - 26, "PRIMA PAGINA")
    c.drawString(mid_x - stringWidth("Stampa: Tipografia Nazionale, Roma", font_name("CourierPrime", "regular"), 9) / 2,
                 footer_y - 26, "Stampa: Tipografia Nazionale, Roma")

    c.save()
    print(f"[page_frontpage] Salvato: {output_path}")
