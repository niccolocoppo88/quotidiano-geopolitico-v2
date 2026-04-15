# ARCHITECTURE_LOCK.md — Il Tuo Quotidiano Geopolitico v2

**Versione:** 1.0  
**Data:** 2026-04-15  
**Autori:** Thomas (Coder) + Piotr (Architect) — Architecture Review congiunta  
**Progetto:** quotidiano-geopolitico-v2  
**GitHub:** https://github.com/niccolocoppo88/quotidiano-geopolitico-v2  

---

## 1. STACK SCELTO — ReportLab + Pillow

**Decisione presa:** ReportLab + Pillow (lo stack esistente del v1)

**Motivazione:**
- ReportLab è già installato e funzionante (v4.4.10)
- Il v1 ha già un pipeline completo funzionante con questo stack
- Pillow è presente per l'image export
- NON si implementa Jinja2/imgkit in parallelo — scelta univoca
- Il v2 è un miglioramento incrementale, non una riscrittura totale

**Struttura tecnologica:**
```
ReportLab (layout PDF) + Pillow (image export)
    ↓
3 PDF → 3 PNG → Telegram
```

**Dipendenze (requirements.txt):**
```
Pillow>=10.0.0
reportlab>=4.0.0
requests>=2.31.0
feedparser>=6.0.0
python-dateutil>=2.8.0
python-telegram-bot>=20.0
python-dotenv>=1.0
```

---

## 2. FONT SOLUTION — Download da Google Fonts

**Problema risolto:** I fallback DejaVu non sono accettabili per un giornale di qualità.

**Soluzione:** Google Fonts scaricati e bundled nel progetto.

**Font necessari:**
| Font | File | Uso |
|------|------|-----|
| Playfair Display | `PlayfairDisplay-Regular.ttf`, `PlayfairDisplay-Bold.ttf` | Titoli, masthead |
| EB Garamond | `EBGaramond-Regular.ttf`, `EBGaramond-Italic.ttf` | Corpo testo, sommari |
| Courier Prime | `CourierPrime-Regular.ttf`, `CourierPrime-Bold.ttf` | Numeri di pagina, date |

**Script:** `scripts/download_fonts.sh`
- Scarica i font dai release GitHub ufficiali di Google Fonts
- Li mette in `assets/fonts/`
- Da eseguire una tantum o quando i font mancano

**Integrazione con font_manager.py:**
```python
FONT_DIR = os.path.join(BASE_DIR, "assets", "fonts")
# Registra i font reali da assets/fonts, non più DejaVu
```

---

## 3. STRUTTURA DIRECTORY

```
quotidiano-geopolitico-v2/
├── .git/
├── .gitignore
├── ARCHITECTURE_LOCK.md          ← questo file (lock architettura)
├── README.md
├── requirements.txt
├── config.py                     # configurazione centralizzata
├── main.py                       # orchestrator (entry point)
├── assets/
│   ├── fonts/                   # Google Fonts scaricati
│   │   ├── PlayfairDisplay-Regular.ttf
│   │   ├── PlayfairDisplay-Bold.ttf
│   │   ├── EBGaramond-Regular.ttf
│   │   ├── EBGaramond-Italic.ttf
│   │   ├── CourierPrime-Regular.ttf
│   │   └── CourierPrime-Bold.ttf
│   └── textures/
│       └── paper_texture.png     # texture overlay leggera
├── scripts/
│   ├── download_fonts.sh         # scarica font da Google Fonts
│   └── setup_cron.sh             # setup cron job
├── lib/
│   ├── __init__.py
│   ├── font_manager.py           # registrazione font (da assets/fonts)
│   ├── news_fetcher.py           # fetch da RSS + NewsAPI
│   ├── content_generator.py      # generazione titoli/sommari con MiniMax
│   ├── layout_engine.py          # costanti griglia (1200×1650, 6 col)
│   ├── page_frontpage.py         # Pagina 1
│   ├── page_deepdive.py          # Pagina 2
│   ├── page_rubriche.py          # Pagina 3
│   ├── image_exporter.py         # PDF → PNG (PyMuPDF/pdftoppm)
│   └── telegram_sender.py        # invio Telegram (openclaw message tool)
├── output/                       # PNG/PDF temporanei (gitignored)
└── logs/                         # log esecuzioni (gitignored)
```

---

## 4. MODULI — RESPONSABILITÀ

### `fetcher` — Raccolta notizie
- **Input:** URL RSS (Reuters, BBC, ANSA) + optional NewsAPI
- **Output:** `dict[category, list[Article]]`
- **Sorgenti RSS:**
  - Geopolitica: Reuters World, BBC World, ANSA
  - Economia: Reuters Business, FT
  - Tech: BBC Tech, Ars Technica

### `generator` — Generazione contenuti con AI
- **Input:** Notizie grezze
- **Output:** `{titolo, sommario, body, categoria, priorità}`
- **API:** MiniMax (già nel workspace)

### `renderer` — Rendering PDF con ReportLab
- **Input:** Contenuti generati
- **Output:** 3 PDF (frontpage, deepdive, rubriche)
- **Canvas:** 1200×1650 px, 6 colonne, griglia 170px + gutter 20px
- **Palette:** Carta #F5F0E8, Nero #1A1A1A, Bordeaux #8B1A1A, Oro #B8860B

### `sender` — Invio Telegram
- **Input:** 3 PNG
- **Output:** 3 messaggi Telegram a Nico
- **Tool:** `openclaw message` (canale Telegram)

### `scheduler` — Automazione giornaliera
- **Cron:** `30 7 * * *` (Europe/Rome)
- **Orario:** 07:30 ogni giorno
- **Tool:** `openclaw cron`

---

## 5. FLUSSO END-TO-END

```
06:00 ────────────────────────────────────────────────────────┐
                                                           │
                                                           ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐
│ 1. FETCH     │───▶│ 2. GENERATE  │───▶│ 3. RENDER PDF         │
│ news_fetcher │    │ content_     │    │ page_frontpage.py     │
│ (RSS/NewsAPI)│    │ generator     │    │ page_deepdive.py      │
│              │    │ (MiniMax AI) │    │ page_rubriche.py      │
└──────────────┘    └──────────────┘    └───────────────────────┘
                                                  │
                                                  ▼
                                         ┌──────────────────────┐
                                         │ 4. EXPORT PNG        │
                                         │ image_exporter.py    │
                                         │ PDF → PNG 1200×1650  │
                                         └───────────────────────┘
                                                  │
                           ┌──────────────────────┼──────────────────────┐
                           │                      │                      │
                           ▼                      ▼                      ▼
                    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
                    │ quotidiano_  │    │ quotidiano_  │    │ quotidiano_  │
                    │ fp_HHMMSS.   │    │ dd_HHMMSS.   │    │ rb_HHMMSS.   │
                    │ png          │    │ png          │    │ png          │
                    └──────────────┘    └──────────────┘    └──────────────┘
                           │                      │                      │
                           └──────────────────────┼──────────────────────┘
                                                  ▼
                                         ┌──────────────────────┐
                                         │ 5. SEND TELEGRAM     │
                                         │ telegram_sender.py   │
                                         │ (openclaw message)   │
                                         └───────────────────────┘
                                                  │
                                                  ▼
                                              ✅ COMPLETO
                                              (07:30 circa)
```

---

## 6. CRON CONFIGURATION

```bash
# Orario: 07:30 Europe/Rome ogni giorno
# Job: python3 /path/to/quotidiano-v2/main.py

30 7 * * * /usr/bin/python3 /Users/niccolocoppo/.openclaw/workspace/quotidiano-v2/main.py >> /Users/niccolocoppo/.openclaw/workspace/quotidiano-v2/logs/cron.log 2>&1
```

**Via OpenClaw CLI:**
```bash
openclaw cron create \
  --name "quotidiano-geopolitico-v2" \
  --schedule "30 7 * * *" \
  --timezone "Europe/Rome" \
  --command "python3 /Users/niccolocoppo/.openclaw/workspace/quotidiano-v2/main.py"
```

---

## 7. CONFIGURAZIONE (config.py)

```python
# Impostazioni chiave (il resto in config.py esistente)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Canvas
PAGE_W, PAGE_H = 1200, 1650
DPI = 72

# Palette
COL_CARTA   = (245, 240, 232)   # #F5F0E8
COL_NERO     = (26, 26, 26)     # #1A1A1A
COL_BORDEAUX = (139, 26, 26)    # #8B1A1A
COL_ORO      = (184, 134, 11)   # #B8860B

# Cron
CRON_SCHEDULE = "30 7 * * *"
CRON_TZ = "Europe/Rome"
```

---

## 8. ALTERNATIVE SCARTATE

| Alternativa | Motivo scarto |
|-------------|--------------|
| Jinja2 + imgkit | Troppo complesso per ora; ReportLab già funzionante |
| WeasyPrint | Dipendenza esterna aggiuntiva, non necessaria |
| wkhtmltopdf | Non installato nell'ambiente |

---

**Lock status:** ✅ ARCHITETTURA CONGELATA — si procede con implementazione

**Firmato:**  
Thomas (Coder)  
Piotr (Architect)  
Data: 2026-04-15