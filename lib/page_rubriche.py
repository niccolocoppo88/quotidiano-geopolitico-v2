"""
lib/page_rubriche.py — Pagina Rubriche del Quotidiano Geopolitico v2
"""
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from config import PAGE_W, PAGE_H, MARGIN_X, MARGIN_Y, COL_WIDTH, COL_GAP
from lib.layout_engine import (
    col_x, col_span, COLOR_CARTA, COLOR_NERO, COLOR_BORDEAUX, COLOR_ORO,
    COLOR_CREMISI, COLOR_GRIGIO, font_name, draw_filetto_oro,
    draw_separator, wrap_text, LINE_H_BODY,
)

def col_w(n): return col_span(n)

def render_rubriche(content: dict, date_str: str, output_path: str):
    """Renderizza la pagina rubriche PDF."""
    c = canvas.Canvas(output_path, pagesize=(PAGE_W, PAGE_H))
    c.setFillColorRGB(*[x/255 for x in COLOR_CARTA])
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    mid_x = PAGE_W / 2
    content_w = PAGE_W - 2 * MARGIN_X

    # ── HEADER ──────────────────────────────────────────────────────────────
    header_y = PAGE_H - MARGIN_Y
    c.setStrokeColorRGB(*[x/255 for x in COLOR_ORO])
    c.setLineWidth(1)
    c.line(MARGIN_X, header_y, PAGE_W - MARGIN_X, header_y)

    c.setFillColorRGB(*[x/255 for x in COLOR_BORDEAUX])
    c.setFont(font_name("PlayfairDisplay", "bold"), 28)
    c.drawCentredString(mid_x, header_y - 30, "LE RUBRICHE")

    c.setStrokeColorRGB(*[x/255 for x in COLOR_ORO])
    c.setLineWidth(2)
    c.line(MARGIN_X, header_y - 42, PAGE_W - MARGIN_X, header_y - 42)

    # ── 3 COLONNE: MONDO, ECONOMIA, TECH ──────────────────────────────────
    col_3_w = col_w(2)  # 2 colonne ciascuna
    rubriche_y = header_y - 60

    #MONDO
    mondo_x = MARGIN_X
    c.setFillColorRGB(*[x/255 for x in COLOR_BORDEAUX])
    c.setFont(font_name("PlayfairDisplay", "bold"), 16)
    c.drawString(mondo_x, rubriche_y, "🌍 MONDO")
    c.setStrokeColorRGB(*[x/255 for x in COLOR_ORO])
    c.setLineWidth(2)
    c.line(mondo_x, rubriche_y - 6, mondo_x + col_3_w, rubriche_y - 6)

    mondo_items = content.get("mondo_items", [
        "Iran: nuove trattative a Vienna",
        "Venezuela: elezioni contestate",
        "Corea: Kim Jong-un in visita a Pechino",
        "Africa: siccità record nel Corno",
    ])
    mondo_y = rubriche_y - 20
    c.setFont(font_name("EBGaramond", "regular"), 12)
    c.setFillColorRGB(*[x/255 for x in COLOR_NERO])
    for item in mondo_items[:4]:
        lines = wrap_text("• " + item, font_name("EBGaramond", "regular"), 12, col_3_w)
        for ln in lines:
            c.drawString(mondo_x + 4, mondo_y, ln)
            mondo_y -= LINE_H_BODY
        mondo_y -= 2

    # ECONOMIA
    econ_x = col_x(2)
    c.setFillColorRGB(*[x/255 for x in COLOR_BORDEAUX])
    c.setFont(font_name("PlayfairDisplay", "bold"), 16)
    c.drawString(econ_x, rubriche_y, "💰 ECONOMIA")
    c.setStrokeColorRGB(*[x/255 for x in COLOR_ORO])
    c.setLineWidth(2)
    c.line(econ_x, rubriche_y - 6, econ_x + col_3_w, rubriche_y - 6)

    econ_items = content.get("economia_items", [
        "BCE: tassi invariati",
        "Euro in calo sul dollaro",
        "Energia: gas a livelli record",
        "Start-up: round da 50M per biotech",
    ])
    econ_y = rubriche_y - 20
    c.setFont(font_name("EBGaramond", "regular"), 12)
    c.setFillColorRGB(*[x/255 for x in COLOR_NERO])
    for item in econ_items[:4]:
        lines = wrap_text("• " + item, font_name("EBGaramond", "regular"), 12, col_3_w)
        for ln in lines:
            c.drawString(econ_x + 4, econ_y, ln)
            econ_y -= LINE_H_BODY
        econ_y -= 2

    # TECH
    tech_x = col_x(4)
    c.setFillColorRGB(*[x/255 for x in COLOR_BORDEAUX])
    c.setFont(font_name("PlayfairDisplay", "bold"), 16)
    c.drawString(tech_x, rubriche_y, "💻 TECH")
    c.setStrokeColorRGB(*[x/255 for x in COLOR_ORO])
    c.setLineWidth(2)
    c.line(tech_x, rubriche_y - 6, tech_x + col_3_w, rubriche_y - 6)

    tech_items = content.get("tech_items", [
        "Apple: Vision Pro 2 in arrivo",
        "Google: Gemini Ultra release",
        "Cybersecurity: attacco a sistemi EU",
        "AI: nuova regolamentazione UE",
    ])
    tech_y = rubriche_y - 20
    c.setFont(font_name("EBGaramond", "regular"), 12)
    c.setFillColorRGB(*[x/255 for x in COLOR_NERO])
    for item in tech_items[:4]:
        lines = wrap_text("• " + item, font_name("EBGaramond", "regular"), 12, col_3_w)
        for ln in lines:
            c.drawString(tech_x + 4, tech_y, ln)
            tech_y -= LINE_H_BODY
        tech_y -= 2

    # ── CULTURA ────────────────────────────────────────────────────────────
    cult_y = min(mondo_y, econ_y, tech_y) - 30
    cult_x = MARGIN_X
    cult_w = col_w(3)

    c.setFillColorRGB(*[x/255 for x in COLOR_BORDEAUX])
    c.setFont(font_name("PlayfairDisplay", "bold"), 16)
    c.drawCentredString(mid_x, cult_y, "🎭 CULTURA")
    c.setStrokeColorRGB(*[x/255 for x in COLOR_ORO])
    c.setLineWidth(2)
    c.line(cult_x + 100, cult_y - 6, cult_x + cult_w + 370, cult_y - 6)

    cult_items = content.get("cultura_items", [
        "Biennale di Venezia: padiglione Italia inaugurato",
        "Restauro Colosseo: nuovi ritrovamenti archeologici",
        "Musica: Sanremo 2026, ospite internazionale",
    ])
    cult_y -= 20
    c.setFont(font_name("EBGaramond", "regular"), 12)
    c.setFillColorRGB(*[x/255 for x in COLOR_NERO])
    cult_x_start = MARGIN_X + 150
    for item in cult_items:
        lines = wrap_text("• " + item, font_name("EBGaramond", "regular"), 12, cult_w)
        for ln in lines:
            c.drawCentredString(mid_x, cult_y, ln)
            cult_y -= LINE_H_BODY
        cult_y -= 2

    # ── EDITORIALE ─────────────────────────────────────────────────────────
    ed_y = cult_y - 24
    ed_h = 120
    ed_x = MARGIN_X + 50
    ed_w = content_w - 100

    # Bordo oro
    c.setStrokeColorRGB(*[x/255 for x in COLOR_ORO])
    c.setLineWidth(1)
    c.rect(ed_x, ed_y - ed_h, ed_w, ed_h, fill=0, stroke=1)

    c.setFillColorRGB(*[x/255 for x in COLOR_GRIGIO])
    c.setFont(font_name("EBGaramond", "italic"), 13)
    editoriale = content.get("editoriale", (
        "«La storia non si ripete, ma spesso rima.» Così il华尔街日报commentava la situazione "
        "geopolitica attuale. L'Europa, che aveva creduto nella fine della storia, si trova oggi "
        "a dover riscrivere il proprio futuro. Non come spettatore, ma come protagonista."
    ))
    ed_lines = wrap_text(editoriale, font_name("EBGaramond", "italic"), 13, ed_w - 24)
    ed_cur_y = ed_y - 20
    for ln in ed_lines:
        c.drawCentredString(ed_x + ed_w / 2, ed_cur_y, ln)
        ed_cur_y -= 17

    # ── CRUCIVERBA DECORATIVO ───────────────────────────────────────────────
    cw_y = ed_y - ed_h - 30
    cw_x = mid_x - 100
    cw_w = 200
    cw_h = 200
    cw_cells = 10
    cell_w = cw_w / cw_cells
    cell_h = cw_h / cw_cells

    # Schema cruciverba (1 = nero, 0 = bianco)
    schema = [
        [0,0,0,0,0,0,0,0,0,0],
        [0,1,0,0,1,0,0,0,1,0],
        [0,0,0,0,1,0,0,0,0,0],
        [0,0,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,0],
        [1,0,0,0,0,0,0,0,0,0],
        [0,0,0,1,0,0,0,0,1,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,1,0,0,0,0,0,0,0,1],
        [0,0,0,0,0,0,0,0,0,0],
    ]

    c.setStrokeColorRGB(0.2, 0.2, 0.2)
    c.setLineWidth(0.5)
    for row_i, row in enumerate(schema):
        for col_i, cell in enumerate(row):
            cx = cw_x + col_i * cell_w
            cy = cw_y - row_i * cell_h
            if cell == 1:
                c.setFillColorRGB(*[x/255 for x in COLOR_NERO])
                c.rect(cx, cy - cell_h, cell_w, cell_h, fill=1, stroke=0)
            else:
                c.setFillColorRGB(*[x/255 for x in COLOR_CARTA])
                c.rect(cx, cy - cell_h, cell_w, cell_h, fill=1, stroke=1)
                # Lettere fittizie
                c.setFillColorRGB(*[x/255 for x in COLOR_NERO])
                c.setFont(font_name("CourierPrime", "regular"), 8)
                letters = ["A","B","C","D","E","F","G","H","I","L"]
                c.drawCentredString(cx + cell_w/2, cy - cell_h + 4,
                                    letters[(row_i + col_i) % len(letters)])

    # ── FOOTER ─────────────────────────────────────────────────────────────
    footer_y = MARGIN_Y + 40
    draw_separator(c, MARGIN_X, footer_y, PAGE_W - 2 * MARGIN_X)
    c.setFillColorRGB(*[x/255 for x in COLOR_GRIGIO])
    c.setFont(font_name("CourierPrime", "regular"), 9)
    disclaimer = "QUOTIDIANO GEOPOLITICO — Anno LXXIII — Aut.Trib. Roma n. 152/2026"
    c.drawCentredString(mid_x, footer_y - 14, disclaimer)
    c.drawRightString(PAGE_W - MARGIN_X, footer_y - 26, "p. 3")
    c.drawString(MARGIN_X, footer_y - 26, "RUBRICHE")
    c.drawCentredString(mid_x, footer_y - 38, "Non è un vero giornale 🗞")

    c.save()
    print(f"[page_rubriche] Salvato: {output_path}")
