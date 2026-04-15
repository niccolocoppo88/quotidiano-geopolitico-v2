"""
lib/page_deepdive.py — Pagina Approfondimento del Quotidiano Geopolitico v2
"""
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from config import PAGE_W, PAGE_H, MARGIN_X, MARGIN_Y, COL_WIDTH, COL_GAP
from lib.layout_engine import (
    col_x, col_span, COLOR_CARTA, COLOR_NERO, COLOR_BORDEAUX, COLOR_ORO,
    COLOR_CREMISI, COLOR_GRIGIO, font_name, draw_filetto_oro,
    draw_double_filetto_oro, draw_separator, wrap_text, LINE_H_BODY,
    LINE_H_TITLE,
)

def col_w(n): return col_span(n)

def render_deepdive(content: dict, date_str: str, output_path: str):
    """Renderizza la pagina approfondimento PDF."""
    c = canvas.Canvas(output_path, pagesize=(PAGE_W, PAGE_H))
    c.setFillColorRGB(*[x/255 for x in COLOR_CARTA])
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    mid_x = PAGE_W / 2
    content_w = PAGE_W - 2 * MARGIN_X

    # ── HEADER APPROFONDIMENTO ──────────────────────────────────────────────
    header_center_y = PAGE_H - MARGIN_Y

    c.setStrokeColorRGB(*[x/255 for x in COLOR_ORO])
    c.setLineWidth(4)
    c.line(MARGIN_X, header_center_y, PAGE_W - MARGIN_X, header_center_y)
    c.setLineWidth(1)
    c.line(MARGIN_X, header_center_y - 6, PAGE_W - MARGIN_X, header_center_y - 6)

    c.setFillColorRGB(*[x/255 for x in COLOR_BORDEAUX])
    c.setFont(font_name("PlayfairDisplay", "bold"), 24)
    c.drawCentredString(mid_x, header_center_y - 28, "APPROFONDIMENTO")

    c.setStrokeColorRGB(*[x/255 for x in COLOR_ORO])
    c.setLineWidth(4)
    c.line(MARGIN_X, header_center_y - 38, PAGE_W - MARGIN_X, header_center_y - 38)
    c.setLineWidth(1)
    c.line(MARGIN_X, header_center_y - 44, PAGE_W - MARGIN_X, header_center_y - 44)

    # ── TITOLO ARTICOLO ────────────────────────────────────────────────────
    main = content.get("main_article", {})
    titolo = main.get("titolo", "La Nuova Guerra Fredda: Come l'Europa sta Ripensando la sua Difesa")
    articolo_text = main.get("articolo", "")

    titolo_y = header_center_y - 60
    c.setFillColorRGB(*[x/255 for x in COLOR_NERO])
    c.setFont(font_name("PlayfairDisplay", "bold"), 28)
    title_lines = wrap_text(titolo, font_name("PlayfairDisplay", "bold"), 28, content_w)
    for line in title_lines:
        c.drawString(MARGIN_X, titolo_y, line)
        titolo_y -= LINE_H_TITLE

    # ── GRIGLIA: FOTO + CORPO ───────────────────────────────────────────────
    grid_top = titolo_y - 20
    grid_h = 400

    # Foto a sinistra (col 0-1)
    foto_x = MARGIN_X
    foto_w = col_w(2)
    foto_h = 280
    foto_y = grid_top

    c.setFillColorRGB(0.6, 0.6, 0.6)
    c.rect(foto_x, foto_y - foto_h, foto_w, foto_h, fill=1, stroke=0)
    c.setStrokeColorRGB(*[x/255 for x in COLOR_GRIGIO])
    c.setLineWidth(1)
    c.rect(foto_x, foto_y - foto_h, foto_w, foto_h, fill=0, stroke=1)
    c.setFillColorRGB(0.4, 0.4, 0.4)
    c.setFont(font_name("CourierPrime", "regular"), 10)
    c.drawCentredString(foto_x + foto_w / 2, foto_y - foto_h / 2 - 4, "📷 Foto B/N — AFP")

    # Didascalia sotto foto
    c.setFont(font_name("EBGaramond", "italic"), 10)
    c.setFillColorRGB(*[x/255 for x in COLOR_GRIGIO])
    c.drawCentredString(foto_x + foto_w / 2, foto_y - foto_h - 14, "Il Segretario NATO durante la conferenza stampa")

    # Corpo testo a destra (col 2-5)
    corpo_x = col_x(2)
    corpo_w = col_w(4)
    corpo_y = grid_top

    # Usa il testo dell'articolo o fallback
    if not articolo_text:
        articolo_text = (
            "Dopo decenni di disimpegno, l'Europa si trova oggi a dover affrontare una realtà "
            "che aveva creduto di aver superato: la possibilità di un conflitto su larga scala "
            "sul proprio continente. L'invasione dell'Ucraina ha risvegliato antiche paure e, "
            "soprattutto, una nuova consapevolezza strategica.\n\n"
            "«Non possiamo più permetterci di delegare la nostra sicurezza agli altri» ha "
            "dichiarato il Segretario Generale della NATO. «L'Europa deve imparare a camminare "
            "con le proprie gambe.»\n\n"
            "I numeri parlano chiaro: la spesa militare europea è cresciuta del 18% nell'ultimo "
            "anno, con la Germania che guida la classifica, seguita da Polonia e Paesi Baltici. "
            "Ma la vera sfida non è solo economica — è culturale e politica."
        )

    # Dividi in due colonne
    paragraphs = articolo_text.split("\n\n")

    c.setFont(font_name("EBGaramond", "regular"), 13)
    c.setFillColorRGB(*[x/255 for x in COLOR_NERO])

    cur_y = corpo_y
    col_height = foto_h
    line_h = 17

    for para in paragraphs:
        if not para.strip():
            cur_y -= 10
            continue

        # Capolettera per il primo paragrafo
        if paragraphs.index(para) == 0:
            first_letter = para[0]
            rest = para[1:].strip()

            # Disegna capolettera
            c.setFont(font_name("PlayfairDisplay", "bold"), 52)
            c.setFillColorRGB(*[x/255 for x in COLOR_BORDEAUX])
            c.drawString(corpo_x, cur_y, first_letter)
            cur_y -= 52

            # Resto del testo impaginato
            c.setFont(font_name("EBGaramond", "regular"), 13)
            c.setFillColorRGB(*[x/255 for x in COLOR_NERO])
            # Prima riga accanto al capolettera
            first_line = first_letter + rest
            wrapped = wrap_text(rest, font_name("EBGaramond", "regular"), 13, corpo_w)
            # La prima riga include il resto dopo la prima lettera
            char_w = stringWidth("M", font_name("EBGaramond", "regular"), 13)
            x_offset = corpo_x + 38  # spazio per capolettera
            wrapped_rest = wrap_text(rest, font_name("EBGaramond", "regular"), 13, corpo_w - 38)
            for i, line in enumerate(wrapped_rest):
                if i == 0:
                    # Prima riga accanto al capolettera
                    c.drawString(x_offset, cur_y, line)
                    cur_y -= line_h
                else:
                    c.drawString(corpo_x, cur_y, line)
                    cur_y -= line_h
            cur_y -= 8  # Spazio tra paragrafi
        else:
            wrapped = wrap_text(para, font_name("EBGaramond", "regular"), 13, corpo_w)
            for line in wrapped:
                c.drawString(corpo_x, cur_y, line)
                cur_y -= line_h
            cur_y -= 8

    # ── BOX CONTESTO STORICO ────────────────────────────────────────────────
    box_y = min(cur_y - 20, foto_y - foto_h - 40)
    box_h = 80
    box_x = MARGIN_X
    box_w = content_w

    # Bordo bordeaux
    c.setStrokeColorRGB(*[x/255 for x in COLOR_BORDEAUX])
    c.setLineWidth(2)
    c.rect(box_x, box_y - box_h, box_w, box_h, fill=0, stroke=1)

    # Sfondo leggermente più chiaro (già è carta)
    c.setFillColorRGB(*[x/255 for x in COLOR_CARTA])

    # Icona + titolo
    c.setFillColorRGB(*[x/255 for x in COLOR_BORDEAUX])
    c.setFont(font_name("PlayfairDisplay", "bold"), 13)
    c.drawString(box_x + 12, box_y - 16, "📜 CONTESTO STORICO")

    # Testo contesto
    contesto = (
        "L'ultima volta che l'Europa ha affrontato una crisi di queste proporzioni era il 1945. "
        "Da allora, il continente ha costruito la sua identità sul soft power e sull'integrazione "
        "economica. Oggi, per la prima volta, deve ridefinire il proprio posto nel mondo."
    )
    c.setFillColorRGB(*[x/255 for x in COLOR_GRIGIO])
    c.setFont(font_name("EBGaramond", "italic"), 12)
    contesto_lines = wrap_text(contesto, font_name("EBGaramond", "italic"), 12, box_w - 24)
    cy = box_y - 34
    for line in contesto_lines:
        c.drawString(box_x + 12, cy, line)
        cy -= 15

    # ── FOOTER ──────────────────────────────────────────────────────────────
    footer_y = MARGIN_Y + 40
    draw_separator(c, MARGIN_X, footer_y, PAGE_W - 2 * MARGIN_X)
    c.setFillColorRGB(*[x/255 for x in COLOR_GRIGIO])
    c.setFont(font_name("CourierPrime", "regular"), 9)
    disclaimer = "QUOTIDIANO GEOPOLITICO — Anno LXXIII — Aut.Trib. Roma n. 152/2026"
    c.drawCentredString(mid_x, footer_y - 14, disclaimer)
    c.drawRightString(PAGE_W - MARGIN_X, footer_y - 26, "p. 2")
    c.drawString(MARGIN_X, footer_y - 26, "APPROFONDIMENTO")

    c.save()
    print(f"[page_deepdive] Salvato: {output_path}")
