"""
page.py — Assemblatore pagina per Quotidiano Geopolitico V3
Disegna la pagina completa secondo Design Spec e Mockup
"""
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from styles import *
from components import (
    draw_filetto_oro, draw_double_filetto_oro, draw_separator,
    draw_masthead, draw_flash_bar, draw_flash_box,
    draw_section_header, draw_mini_news, wrap_text, draw_footer
)


def draw_capolettera_dropcap(c, x, y, letter, font_size=52):
    """
    Capolettera 'drop cap' professionale:
    - Lettera grande (3 linee) a sinistra
    - Rispettato da wrap_text per le righe successive
    """
    c.setFillColorRGB(*COLOR_BORDEAUX)
    c.setFont(font_name('Playfair', 'bold'), font_size)
    c.drawString(x, y, letter.upper())
    # Altezza in pt (linea ~0.73 * font_size per Playfair)
    return int(font_size * 0.73)  # 3 linee ~ 3 * 14pt ≈ 42pt

def render_page(content: dict, date_str: str, output_path: str):
    """
    Renderizza una pagina del giornale.
    
    Args:
        content: dict con chiavi per ogni sezione
        date_str: stringa data formattata (es. "18 Apr 2026")
        output_path: percorso output PDF
    """
    c = canvas.Canvas(output_path, pagesize=(PAGE_W, PAGE_H))
    
    # Background carta
    c.setFillColorRGB(*COLOR_CARTA)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    
    # ── MASTHEAD ────────────────────────────────────────────────────────────
    masthead_y = draw_masthead(c, date_str)
    
    # ── FLASH BAR ───────────────────────────────────────────────────────────
    flash_text = content.get('flash_text', 'Tensioni in Mar Rosso: la NATO convoca vertice straordinario')
    flash_y = draw_flash_bar(c, flash_text, masthead_y)
    
    # ── ARTICOLO PRINCIPALE (colonne 0-3) ──────────────────────────────────
    main_y = flash_y - 16
    
    # Occhiello
    occhiello = content.get('occhiello', 'GEOPOLITICA').upper()
    c.setFillColorRGB(*COLOR_BORDEAUX)
    c.setFont(font_name('Playfair', 'italic'), FONT_SIZES['occhiello'])
    c.drawString(MARGIN_X, main_y, f"// {occhiello}")
    main_y -= 20
    
    # Titolo principale
    titolo = content.get('main_title', 'Il G20 di Johannesburg apre i giochi: emergenza clima al centro del dibattito mondiale')
    c.setFillColorRGB(*COLOR_NERO)
    c.setFont(font_name('Playfair', 'bold'), FONT_SIZES['title_main'])
    title_lines = wrap_text(titolo, font_name('Playfair', 'bold'), FONT_SIZES['title_main'], col_span(4))
    for line in title_lines:
        c.drawString(MARGIN_X, main_y, line)
        main_y -= LINE_H_TITLE
    
    main_y -= 4
    
    # Sommario
    sommario = content.get('sommario', 'I leader delle principali economie globali si ritrovano oggi nel capoluogo sudafricano per un vertice che potrebbe segnare una svolta.')
    c.setFillColorRGB(*COLOR_GRIGIO)
    c.setFont(font_name('EBGaramond', 'italic'), 13)
    sommario_lines = wrap_text(sommario, font_name('EBGaramond', 'italic'), 13, col_span(4))
    for line in sommario_lines:
        c.drawString(MARGIN_X, main_y, line)
        main_y -= 16
    
    main_y -= 12
    
    # Corpo in 2 colonne
    corpo = content.get('body_text', 
        "Il vertice del G20 di Johannesburg rappresenta oggi il principale appuntamento della diplomazia climatica mondiale. "
        "Alla vigilia dell'incontro, fonti vicine alla delegazione dell'Unione Europea riferiscono che il testo finale del comunicato è ancora oggetto di negoziati serrati, "
        "in particolare sui meccanismi di finanziamento per i paesi in via di sviluppo più vulnerabili agli effetti del riscaldamento globale. "
        "Secondo fonti diplomatiche citate dall'agenzia Reuters, il nodo centrale resta la definizione di un fondo di adattamento che garantisca risorse certe ai paesi del Sud del mondo.")
    
    c.setFillColorRGB(*COLOR_NERO)
    c.setFont(font_name('EBGaramond', 'regular'), FONT_SIZES['body'])
    
    # ── CORPO IN 2 COLONNE CON CAPOLETTERA ───────────────────────────
    col0_x = MARGIN_X
    col1_x = MARGIN_X + col_span(2)  # metà destra del corpo (col 0+1 divise a metà)
    col_w = col_span(2)  # 2 colonne per il corpo principale
    
    # Capolettera drop cap — grande, a sinistra della prima colonna
    first_letter = corpo[0].upper()
    cap_height = draw_capolettera_dropcap(c, col0_x, main_y, first_letter, 52)
    cap_line_count = 3  # quante righe "occupa" il capolettera
    cap_right_edge = col0_x + 42  # quanto spazio occupa a destra il capolettera
    
    # Prima porzione: righe che "wrapparono" attorno al capolettera
    wrap_lines_text = corpo[1:80]  # ~3 parole che stanno a destra del drop cap
    c.setFillColorRGB(*COLOR_NERO)
    c.setFont(font_name('EBGaramond', 'regular'), FONT_SIZES['body'])
    
    # Disegna le prime 2 righe ravvicinate a destra del capolettera
    wrap_w = col_span(1) - 50  # larghezza disponibile a destra del cap
    wrap_lines = wrap_text(corpo[1:], font_name('EBGaramond', 'regular'), 
                          FONT_SIZES['body'], wrap_w)
    
    # Riga 1: a fianco del capolettera
    if wrap_lines:
        c.drawString(cap_right_edge, main_y, wrap_lines[0])
    # Riga 2: sotto, ancora a fianco del cap
    if len(wrap_lines) > 1:
        c.drawString(cap_right_edge, main_y - LINE_H_BODY, wrap_lines[1])
    
    # Dopo le 2 righe "wrap, scendiamo sotto il capolettera
    body_start_y = main_y - cap_height  # sotto il cap
    
    # Corpo completo in 2 colonne: testo rimanente
    remaining_text = ' '.join(wrap_lines[2:]) if len(wrap_lines) > 2 else ''
    if not remaining_text:
        remaining_text = corpo[50:]  # fallback
    
    # Colonna sinistra (col 0-1)
    left_lines = wrap_text(remaining_text, font_name('EBGaramond', 'regular'),
                           FONT_SIZES['body'], col_span(2))
    line_y = body_start_y
    mid_col = len(left_lines) // 2
    for i, line in enumerate(left_lines[:mid_col]):
        c.drawString(col0_x, line_y, line)
        line_y -= LINE_H_BODY
    
    # Colonna destra (col 2-3, ma serve x diverso)
    # right side è la continuazione... ma abbiamo 4 colonne totali
    # Colonne 0-1 = corpo principale, colonne 2-3 = TODO
    # Per ora riempiamo la 2a metà delle righe left_lines nella stessa area
    # "col1_x" in realtà è l'inizio della 3a colonna
    line_y = body_start_y
    for i, line in enumerate(left_lines[mid_col:]):
        c.drawString(col1_x, line_y, line)
        line_y -= LINE_H_BODY
    
    # ── SIDEBAR (colonne 4-5) ────────────────────────────────────────────────
    sidebar_x = col_x(4)
    sidebar_w = col_span(2)
    sidebar_y = flash_y - 16
    
    # Flash box 1
    flash1_title = content.get('flash1_title', 'ECONOMIA')
    flash1_text = content.get('flash1_text', 'Borsa di Tokyo +1.8% dopo annuncio stimoli fiscali. Petrolio stabile a $74/barile')
    draw_flash_box(c, sidebar_x, sidebar_y, sidebar_w, 60, flash1_title, flash1_text)
    
    # Flash box 2
    flash2_title = content.get('flash2_title', 'TECNOLOGIA')
    flash2_text = content.get('flash2_text', 'OpenAI presenta GPT-5: "Intelligenza generale a portata di mano"')
    draw_flash_box(c, sidebar_x, sidebar_y - 76, sidebar_w, 60, flash2_title, flash2_text)
    
    # Flash box 3
    flash3_title = content.get('flash3_title', 'GEOPOLITICA')
    flash3_text = content.get('flash3_text', 'Taiwan: elezioni legislative, opposizione conquista maggioranza')
    draw_flash_box(c, sidebar_x, sidebar_y - 152, sidebar_w, 60, flash3_title, flash3_text)
    
    # Sezione ECONOMIA (sotto ai flash box)
    econ_y = sidebar_y - 180
    draw_section_header(c, sidebar_x, econ_y, 'ECONOMIA', sidebar_w)
    econ_y -= 24
    
    econ_items = content.get('economia_items', [
        ('Eurotower: tassi confermati, Lagarde apre a taglio a giugno', ''),
        ('Cina: export oltre attese, surplus record', ''),
    ])
    for title, text in econ_items[:3]:
        econ_y = draw_mini_news(c, sidebar_x + 4, econ_y, title, text, sidebar_w - 8)
        econ_y -= 8
    
    # Sezione TECNOLOGIA
    tech_y = econ_y - 16
    draw_section_header(c, sidebar_x, tech_y, 'TECNOLOGIA', sidebar_w)
    tech_y -= 24
    
    tech_items = content.get('tech_items', [
        ('Chip AI: nuove restrizioni USA verso la Cina', ''),
        ('Apple: presentazione iPhone 17 slitta a settembre', ''),
    ])
    for title, text in tech_items[:3]:
        tech_y = draw_mini_news(c, sidebar_x + 4, tech_y, title, text, sidebar_w - 8)
        tech_y -= 8
    
    # ── SEPARATORE ORO ──────────────────────────────────────────────────────
    sep_y = min(main_y - 100, sidebar_y - 300)
    draw_separator(c, MARGIN_X, sep_y, PAGE_W - MARGIN_X, COLOR_ORO, 1)
    
    # ── FOOTER ─────────────────────────────────────────────────────────────
    draw_footer(c, page_num=1)
    
    # Save
    c.save()
    print(f"[page] Salvato: {output_path}")