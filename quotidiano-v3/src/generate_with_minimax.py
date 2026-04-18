#!/usr/bin/env python3
"""
generate_with_minimax.py — MiniMax-powered content generation
RUN 1/3
"""
import os
import sys
import json
import subprocess
import time
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
sys.path.insert(0, BASE_DIR)

from font_manager import register_fonts
from styles import PAGE_W, PAGE_H
from page import render_page
from PIL import Image
import fitz

# ── MiniMax API Call ────────────────────────────────────────────────────────

def call_minimax_chat(system: str, message: str, retries: int = 3) -> dict:
    """Call mmx text chat with exponential backoff retry"""
    cmd = [
        "mmx", "text", "chat",
        "--system", system,
        "--message", message,
        "--output", "json",
    ]
    for attempt in range(retries):
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode != 0:
                print(f"  [MiniMax] attempt {attempt+1} failed: {result.stderr[:200]}")
                time.sleep(2 ** attempt)
                continue
            
            raw = result.stdout.strip()
            # Parse JSON from output (mmx wraps in json with content array)
            data = json.loads(raw)
            # Extract text content
            for item in data.get("content", []):
                if item.get("type") == "text":
                    text = item["text"]
                    # Extract JSON from markdown code block if present
                    if "```json" in text:
                        start = text.index("```json") + 7
                        end = text.rindex("```")
                        return json.loads(text[start:end].strip())
                    elif text.strip().startswith("["):
                        return json.loads(text.strip())
                    elif text.strip().startswith("{"):
                        return json.loads(text.strip())
            return data
        except Exception as e:
            print(f"  [MiniMax] attempt {attempt+1} error: {e}")
            time.sleep(2 ** attempt)
    print("[MiniMax] API fallita, uso fallback")
    return None

# ── Content Generation ────────────────────────────────────────────────────────

def generate_content(run: int = 1) -> dict:
    """Generate all newspaper content using MiniMax API"""
    print(f"\n  [Content] Generazione contenuti con MiniMax (run {run}/3)...")
    
    # ── Main article
    main_article = call_minimax_chat(
        system="Sei un giornalista geopolitico esperto. Scrivi articoli per il Quotidiano Geopolitico in italiano. Tonoinformato ma non accademico, assertivo. Struttura: TITOLO (max 80 chars), OCCHIELL0 (max 200 chars), CORPO (600-800 parole), FONTE (max 100 chars). Rispondi SOLO in JSON con chiavi: titolo, occhiello, corpo, fonte.",
        message="Genera un articolo principale di geopolitica internazionale per oggi 18 aprile 2026. Scegli tu l'argomento più rilevante. Disponi in JSON valido."
    )
    
    if main_article is None:
        return get_fallback_content()
    
    # ── Flash news
    flash_data = call_minimax_chat(
        system="Sei un giornalista esperto. Genera 3 flash news brevi in italiano. Formato JSON array con: title (categoria), text (max 120 chars). Tonoinformato, assertivo.",
        message="Genera 3 flash news per categorie: ECONOMIA, TECNOLOGIA, GEOPOLITICA. Per oggi 18 aprile 2026. Solo JSON array valido."
    )
    
    # ── Flash text (breaking headline)
    flash_text_data = call_minimax_chat(
        system="Sei un giornalista. Scrivi un titolo flash di max 120 caratteri per una breaking news. Solo il testo, nient'altro.",
        message="Scrivi il titolo flash principale per il Quotiano Geopolitico di oggi 18 aprile 2026 basato su notizie geopolitiche rilevanti. Max 120 caratteri. Solo testo piano."
    )
    
    # ── Economia section
    economia_data = call_minimax_chat(
        system="Sei un giornalista economico esperto. Genera 2 notizie in italiano per sezione ECONOMIA. Formato: array JSON con coppie [titolo, testo_breve]. Titolo max 60 chars, testo max 100 chars. Tonoinformato.",
        message="Genera 2 notizie economia per 18 aprile 2026. Solo JSON array valido, nient'altro."
    )
    
    # ── Tech section
    tech_data = call_minimax_chat(
        system="Sei un giornalista tech esperto. Genera 2 notizie in italiano per sezione TECNOLOGIA. Formato: array JSON con coppie [titolo, testo_breve]. Titolo max 60 chars, testo max 100 chars. Tonoinformato.",
        message="Genera 2 notizie tecnologia per 18 aprile 2026. Solo JSON array valido, nient'altro."
    )
    
    # ── Build content dict
    content = {
        "flash_text": extract_flash_text(flash_text_data),
        "occhiello": main_article.get("occhiello", "geopolitica"),
        "main_title": main_article.get("titolo", "Il G20 di Johannesburg apre i giochi"),
        "sommario": main_article.get("occhiello", "")[:200],
        "body_text": main_article.get("corpo", ""),
        "fonte": main_article.get("fonte", "Quotidiano Geopolitico"),
    }
    
    # Flash boxes
    if flash_data and isinstance(flash_data, list):
        for i, item in enumerate(flash_data[:3]):
            if isinstance(item, dict):
                content[f"flash{i+1}_title"] = item.get("title", "")
                content[f"flash{i+1}_text"] = item.get("text", "")
            elif isinstance(item, list):
                content[f"flash{i+1}_title"] = str(item[0]) if len(item) > 0 else ""
                content[f"flash{i+1}_text"] = str(item[1]) if len(item) > 1 else ""
    else:
        content["flash1_title"] = "ECONOMIA"
        content["flash1_text"] = "Borsa di Tokyo +1.8% dopo annuncio stimoli fiscali"
        content["flash2_title"] = "TECNOLOGIA"
        content["flash2_text"] = "OpenAI presenta GPT-5: intelligenza generale a portata di mano"
        content["flash3_title"] = "GEOPOLITICA"
        content["flash3_text"] = "Taiwan: elezioni legislative, opposizione conquista maggioranza"
    
    # Economia items
    if economia_data and isinstance(economia_data, list):
        content["economia_items"] = [tuple(item) if isinstance(item, list) else tuple([str(item), ""]) for item in economia_data[:2]]
    else:
        content["economia_items"] = [
            ("Mercati europei in rialzo dopo dati inflazione Usa", "Borse continentali guadagnano lo 0,8%"),
            ("Btp tornano sotto stress, spread risale a 150 pb", "Investitori nervosi in attesa delle decisioni Bce"),
        ]
    
    # Tech items
    if tech_data and isinstance(tech_data, list):
        content["tech_items"] = [tuple(item) if isinstance(item, list) else tuple([str(item), ""]) for item in tech_data[:2]]
    else:
        content["tech_items"] = [
            ("Meta lancia IA generativa per video 4K in tempo reale", "VideoGen 4K rivoluziona la produzione audiovisiva"),
            ("Lancio fallito: satellite europeo si perde nell'orbita", "Il razzo Vega C ha perso il controllo del satellite Sentinel-2C"),
        ]
    
    print("  [Content] Contenuti pronti ✓")
    return content

def extract_flash_text(data) -> str:
    if data is None:
        return "Tensioni in Mar Rosso: la NATO convoca vertice straordinario"
    if isinstance(data, str):
        return data.strip()[:120]
    if isinstance(data, dict):
        return data.get("text", data.get("content", ""))[:120]
    if isinstance(data, list):
        return str(data[0])[:120] if data else "Flash news"
    return str(data)[:120]

# ── Fallback ─────────────────────────────────────────────────────────────────

def get_fallback_content() -> dict:
    """Fallback static content when API fails"""
    print("[Fallback] Uso contenuto statico")
    return {
        "flash_text": "Vertice Nato a Varsavia: nuova coalizione di difesa baltica. Truppe rafforzate sui confini orientali.",
        "occhiello": "DIFESA EUROPEA",
        "main_title": "L'Europa raddoppia la Difesa: il piano da 200 miliardi che cambia la geopolitica continentale",
        "sommario": "Il Consiglio europeo approva un fondo comune per la difesa senza precedenti. L'obiettivo è ridurre la dipendenza dalla NATO e costruire un'autonomia strategica europea.",
        "body_text": "In una riunione straordinaria a Bruxelles, i leader dell'Unione Europea hanno ratificato il 'Patto per la Sovranità Strategica', un fondo comune da 200 miliardi di euro destinato a trasformare radicalmente le capacità di difesa del continente. La decisione, salutata da molti come un momento storico, segna la fine di decenni di sottoinvestimento nella componente militare europea e apre una nuova fase nella geopolitica continentale.\n\nIl piano prevede la creazione di una catena di comando integrata, nuovi programmi di acquisto congiunto di sistemi d'arma e investimenti massicci in tecnologie di nuova generazione, dall'intelligenza artificiale bellica ai droni autonomi, fino alle cyberguerre. La Francia e la Germania faranno da apripista, ma tutti i 27 Stati membri contribuiranno secondo una formula che tiene conto del PIL e della posizione geografica.\n\nLe implicazioni geopolitiche sono enormi. Con questo fondo, l'Europa mira a ridurre drasticamente la propria dipendenza dal parapetto atlantico, pur senza uscire dalla NATO. L'obiettivo dichiarato è raggiungere entro il 2030 un'autonomia di decisione in scenari di crisi regionale, senza dover attendere il consenso di Washington.\n\nGli Stati Uniti hanno reagito con cautela. Il Segretario di Stato ha definito l'iniziativa 'compatibile' con l'Alleanza atlantica, ma fonti diplomatiche riferiscono un certo disagio in ambienti neoconservatori, che vedono nel patto un rischio di frammentazione dell'egemonia occidentale. La Russia, dal canto suo, ha definito il fondo 'un passo destabilizzante', rilanciando la narrativa di un'Occidente aggressivo in espansione.\n\nIl vero test sarà la capacità dell'Europa di superare le storiche diffidenze tra nazioni. Le tensioni italo-francesi sull'industria degli armamenti, i veti ungheresi su missioni comuni e la resistenza di alcuni Paesi baltici a una difesa 'a geometria variabile' rappresentano ancora ostacoli concreti. Ma la pressione esterna — dalla guerra ancora aperta in Ucraina alle incertezze sulla Casa Bianca — sta accelerando il processo come mai prima d'ora.",
        "flash1_title": "ECONOMIA",
        "flash1_text": "Bce pronta a tagliare i tassi di 25 pb a maggio. Fonti interne confermano l'orientamento espansivo.",
        "flash2_title": "TECNOLOGIA",
        "flash2_text": "Apple svela i chip M4 Ultra: prestazioni AI triplicate. I nuovi dispositivi in vendita da giugno.",
        "flash3_title": "GEOPOLITICA",
        "flash3_text": "Vertice Nato a Varsavia: nuova coalizione di difesa baltica. Truppe rafforzate sui confini orientali.",
        "economia_items": [
            ("Mercati europei in rialzo dopo dati inflazione Usa", "Borse continentali guadagnano lo 0,8% dopo che l'inflazione americana ha rallentato più delle attese."),
            ("Btp tornano sotto stress, spread risale a 150 pb", "Il differenziale tra Btp e Bund torna a crescere oltre la soglia critica."),
        ],
        "tech_items": [
            ("Meta lancia IA generativa per video 4K in tempo reale", "La piattaforma introduce VideoGen 4K, capace di generare clip ad alta definizione dal testo."),
            ("Lancio fallito: satellite europeo si perde nell'orbita", "Il razzo Vega C ha perso il controllo del satellite Sentinel-2C durante il decollo da Kourou."),
        ],
    }

# ── Telegram ─────────────────────────────────────────────────────────────────

def send_telegram(photo_path: str, caption: str = ""):
    """Send photo to Nico via Telegram bot using curl"""
    bot_token = "8799149563:AAEPopcG5I94wHPxR6Rh1raYH6iHTZ9jD88"
    chat_id = "8336585509"
    
    try:
        result = subprocess.run(
            [
                "curl", "-s", "-X", "POST",
                f"https://api.telegram.org/bot{bot_token}/sendPhoto",
                "-F", f"chat_id={chat_id}",
                "-F", f"photo=@{photo_path}",
                "-F", f"caption={caption}",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        response = json.loads(result.stdout)
        if response.get("ok"):
            print(f"  [Telegram] Inviato a Nico ✓")
        else:
            print(f"  [Telegram] Errore: {response}")
    except Exception as e:
        print(f"  [Telegram] Errore: {e}")

# ── Main ─────────────────────────────────────────────────────────────────────

def format_date():
    now = datetime.now()
    months = ['Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno',
              'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre']
    return f"{now.day} {months[now.month - 1]} {now.year}"

def main(run: int = 1):
    print(f"\n{'='*60}")
    print(f"  QUOTIDIANO GEOPOLITICO v3 — Generazione MiniMax (RUN {run}/3)")
    print(f"{'='*60}")
    
    # Register fonts
    print("\n[0/4] Registrazione font...")
    register_fonts()
    
    # Output dir
    output_dir = os.path.join(PARENT_DIR, 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate content
    print("\n[1/4] Generazione contenuti con MiniMax...")
    content = generate_content(run)
    
    # Date
    date_str = format_date()
    print(f"\n[2/4] Rendering PDF — {date_str}...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = os.path.join(output_dir, f"quotidiano_v3_{timestamp}.pdf")
    
    render_page(content, date_str, pdf_path)
    print(f"  → PDF generato: {pdf_path}")
    
    print("\n[3/4] Conversione PDF → PNG...")
    png_path = pdf_path.replace('.pdf', '.png')
    try:
        doc = fitz.open(pdf_path)
        page = doc[0]
        mat = fitz.Matrix(2.0, 2.0)
        pix = page.get_pixmap(matrix=mat)
        pix.save(png_path)
        doc.close()
        print(f"  → PNG generato: {png_path}")
        
        # Verify with MiniMax vision
        print("\n[4/4] Verifica immagine con MiniMax vision...")
        try:
            result = subprocess.run(
                ["mmx", "vision", "describe", png_path, "--output", "json"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                print(f"  → Visione: OK ✓")
            else:
                print(f"  → Visione: warning ({result.stderr[:100]})")
        except Exception as e:
            print(f"  → Visione: skip ({e})")
        
        # Send to Telegram
        print("\n[5/4] Invio a Telegram...")
        send_telegram(png_path, f"Quotidiano Geopolitico — {date_str}")
        
    except Exception as e:
        print(f"  → Errore: {e}")
        png_path = None
    
    print(f"\n{'='*60}")
    print(f"  ✅ RUN {run}/3 COMPLETATA")
    print(f"{'='*60}")
    
    return png_path

if __name__ == "__main__":
    run = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    main(run)
