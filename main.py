#!/usr/bin/env python3
"""
main.py — Il Tuo Quotidiano Geopolitico v2
Orchestratore: fetch → generate → render → export → send
"""
import os
import sys
from datetime import datetime

# Aggiungi la directory del progetto al path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from config import OUTPUT_DIR, FONTS_DIR
from lib.font_manager import register_fonts
from lib.news_fetcher import fetch_with_fallback
from lib.content_generator import generate_mock_content
from lib.page_frontpage import render_frontpage
from lib.page_deepdive import render_deepdive
from lib.page_rubriche import render_rubriche
from lib.image_exporter import export_all
from lib.telegram_sender import send_all, send_text

def main():
    print("=" * 60)
    print("  QUOTIDIANO GEOPOLITICO v2 — Generazione")
    print("=" * 60)

    # 1. Registra font
    print("\n[1/6] Registrazione font...")
    register_fonts()

    # 2. Fetch notizie
    print("[2/6] Fetch notizie...")
    articles = fetch_with_fallback()
    print(f"  → {sum(len(v) for v in articles.values())} articoli raccolti")

    # 3. Genera contenuti (mock per ora — MiniMax opzionale)
    print("[3/6] Generazione contenuti...")
    content = generate_mock_content(articles)
    print("  → Contenuti pronti")

    # Data formattata
    date_str = datetime.now().strftime("%d %B %Y").replace(" 0", " ").title()
    date_str = date_str.replace("April", "Aprile").replace("May", "Maggio").replace("June", "Giugno")
    date_str = date_str.replace("January", "Gennaio").replace("February", "Febbraio").replace("March", "Marzo")
    date_str = date_str.replace("July", "Luglio").replace("August", "Agosto").replace("September", "Settembre")
    date_str = date_str.replace("October", "Ottobre").replace("November", "Novembre").replace("December", "Dicembre")

    # 4. Render PDF
    print("[4/6] Rendering PDF...")
    timestamp = datetime.now().strftime("%H%M%S")
    output_base = os.path.join(OUTPUT_DIR, f"quotidiano_{timestamp}")

    fp_path = f"{output_base}_fp.pdf"
    dd_path = f"{output_base}_dd.pdf"
    rb_path = f"{output_base}_rb.pdf"

    render_frontpage(content, date_str, fp_path)
    render_deepdive(content, date_str, dd_path)
    render_rubriche(content, date_str, rb_path)

    pdf_paths = [fp_path, dd_path, rb_path]
    print(f"  → 3 PDF generati in {OUTPUT_DIR}")

    # 5. Converti in PNG
    print("[5/6] Conversione PDF → PNG...")
    png_paths = export_all(pdf_paths)
    print(f"  → {len(png_paths)} PNG create")

    if not png_paths:
        print("[5/6] ERRORE: nessuna PNG convertita, skip invio")
        return

    # 6. Invia a Nico
    print("[6/6] Invio a Nico via Telegram...")
    page_labels = ["Prima Pagina", "Approfondimento", "Rubriche"]
    captions = [f"📰 {label} — {date_str}" for label in page_labels]

    ok = send_all(png_paths, captions)
    if ok:
        send_text("8336585509", f"✅ Quotidiano Geopolitico del {date_str} completato!")
        print("\n" + "=" * 60)
        print("  ✅ COMPLETATO — Nico ha ricevuto il giornale!")
        print("=" * 60)
    else:
        print("\n⚠️  Invio Telegram fallito — controlla i log")

if __name__ == "__main__":
    main()
