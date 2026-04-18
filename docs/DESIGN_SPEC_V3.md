# Design Spec — Quotidiani Geopolitico V3

**Versione:** 2.0  
**Data:** 2026-04-18  
**Architect:** Piotr  
**Status:** IN IMPLEMENTAZIONE

---

## 1. Riferimento Visivo — Stile Corriere della Sera

**Stile:** Corriere della Sera — prima pagina anni '70/'80  
**Carattere:** Autoritario, cartaceo, eleganza sobria. Non è un blog. È un giornale vero.

### Struttura Pagina V3 (1 pagina sola)

```
┌──────────────────────────────────────────────────────────────────┐
│  ════════════════════════════════════════════════════════════   │
│                                                                   │
│              Q U O T I D I A N O   G E O P O L I T I C O        │
│              ────────────────────────────────────────           │
│              18 Aprile 2026          Anno XX, Num. 107           │
│  ─────────────────────────────────────────────────────────────  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ ⚑ CRONACA ESTERA — FLASH — ULTIM'ORA                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────┐  ┌──────┐  ┌──────┐          │
│  │                             │  │      │  │      │          │
│  │  TITOLONE PRINCIPALE        │  │FLASH │  │FLASH │          │
│  │  (col 1-4)                  │  │  5   │  │  6   │          │
│  │  ┌───────────────────┐      │  │      │  │      │          │
│  │  │  foto B/N         │      │  ├──────┴──┴──────┤          │
│  │  │  750×420           │      │  │ ECONOMIA │ TECH │          │
│  │  └───────────────────┘      │  │  col1-3  │col4-6│          │
│  │  Sommario + corpo           │  └──────────┴──────┘          │
│  └─────────────────────────────┘                                │
│  ─────────────────────────────────────────────────────────────  │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐              │
│  │ MONDO   │ │ AFRICA  │ │ EUROPA  │ │ ASIA    │              │
│  │ 2 col   │ │  2 col  │ │  1 col  │ │  1 col  │              │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘              │
│  ═══════════════════════════════════════════════════════════   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. Specifiche Pagina

| Parametro | Valore |
|-----------|--------|
| Larghezza | 1200 px |
| Altezza | 1650 px |
| DPI | 72 |
| Sfondo | `#F5F0E8` (carta) |
| Margine X | 30 px |
| Margine Y | 30 px |

---

## 3. Palette Colori

| Nome | Hex | RGB | Uso |
|------|-----|-----|-----|
| Carta | `#F5F0E8` | (245, 240, 232) | Sfondo pagina |
| Nero | `#1A1A1A` | (26, 26, 26) | Titoli, corpo testo |
| Bordeaux | `#8B1A1A` | (139, 26, 26) | Header, accenti, titoli sezione |
| Oro | `#B8860B` | (184, 134, 11) | Filetti, separatori, dettagli premium |
| Cremisi | `#C0392B` | (192, 57, 43) | Box flash, breaking news |
| Grigio | `#4A4A4A` | (74, 74, 74) | Didascalie, testo secondario |

---

## 4. Tipografia

### 4.1 Font — Playfair Display (Titoli)
- **File:** `PlayfairDisplay-Regular.ttf`, `PlayfairDisplay-Bold.ttf`
- **CDN:** `https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap`
- **Uso:** Masthead, titoli articoli, titoli sezione

### 4.2 Font — EB Garamond (Corpo)
- **File:** `EBGaramond-Regular.ttf`, `EBGaramond-Italic.ttf`
- **CDN:** `https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&display=swap`
- **Uso:** Corpo articoli, sommari, box contesto

### 4.3 Font — Courier Prime (Data/Numeri)
- **File:** `CourierPrime-Regular.ttf`, `CourierPrime-Bold.ttf`
- **CDN:** `https://fonts.googleapis.com/css2?family=Courier+Prime:ital,wght@0,400;0,700;1,400&display=swap`
- **Uso:** Data, numeri pagina, etichette flash, filetti

---

## 5. Layout — Griglia 6 Colonne

```
Larghezza disponibile: 1200 - 60 (margini) = 1140 px
6 col × 170 px + 5 gap × 20 px = 1020 + 100 = 1120 px
(Resta 20 px di buffer per lato — OK)

Colonna: 170 px
Gap: 20 px

[Col1][Gap][Col2][Gap][Col3][Gap][Col4][Gap][Col5][Gap][Col6]
 170    20   170    20   170    20   170    20   170    20   170
```

### Assegnazione Colonne

| Colonne | Uso | Larghezza |
|---------|-----|-----------|
| 1-4 | Articolo principale + foto | 710 px (4 col + 3 gap) |
| 5 | Flash box 1 | 170 px |
| 6 | Flash box 2 | 170 px |
| 1-3 (seconda fila) | Articoli secondari (Mondo, Africa) | 560 px |
| 4-6 (seconda fila) | Articoli secondari (Europa, Asia) | 560 px |

---

## 6. Struttura Sezioni — Prima Pagina V3

### 6.1 Masthead (Mastro)

```
╔══════════════════════════════════════════════════════════════════╗
║  ═══════════════════════════════════════════════════════════════ ║
║                                                                   ║
║         Q  U  O  T  I  D  I  A  N  O    G  E  O  P  O  L  I  T  I  C  O  ║
║         ───────────────────────────────────────────────────      ║
║         18 Aprile 2026         Anno XX, Num. 107                 ║
║                                                                   ║
║  ─────────────────────────────────────────────────────────────  ║
╚══════════════════════════════════════════════════════════════════╝
```

- **Sfondo:** Carta `#F5F0E8`
- **Titolo:** Playfair Display Bold, 48px, Nero `#1A1A1A`, letter-spacing 0.08em
- **Filetto superiore:** 3px, Oro `#B8860B`
- **Filetto sotto titolo:** doppia linea — 2px Oro + 4px spazio + 1px Nero
- **Data/Anno:** Courier Prime, 12px, Grigio `#4A4A4A`
- **Linea separatrice footer mastro:** 1px, Nero `#1A1A1A`

### 6.2 Barra Flash / Etichetta Sezione

- **Background:** Cremisi `#C0392B`
- **Testo:** Courier Prime Bold, 11px, Bianco, "⚑ CRONACA ESTERA — FLASH — ULTIM'ORA"
- **Border-left:** 4px, Oro `#B8860B`
- **Padding:** 6px 14px
- **Maiuscolo** con letter-spacing 0.05em

### 6.3 Articolo Principale (Colonne 1-4)

- **Occhiello:** Playfair Display Italic, 13px, Bordeaux, maiuscolo, letter-spacing 0.1em
- **Titolo:** Playfair Display Bold, 32px, Nero, leading 36px
- **Foto:** B/N, 750×420 px, bordi 0, didascalia Courier Prime Italic 10px Grigio
- **Sommario:** EB Garamond Italic, 14px, Nero
- **Corpo:** EB Garamond Regular, 11px, interlinea 14px, Nero
- **Box Citazione:** border-left 3px Bordeaux, padding 12px, EB Garamond Italic 13px

### 6.4 Flash Box (Colonne 5-6)

- **Background flash header:** Cremisi `#C0392B`
- **Testo header:** Courier Prime Bold 10px, Bianco, "⚑ FLASH"
- **Titolo:** Playfair Display Bold, 14px, Nero
- **Corpo:** EB Garamond Regular, 10px, Nero
- **Fonte:** Courier Prime Italic, 9px, Grigio `#4A4A4A`
- **Separatore tra flash e contenuto:** 1px Oro `#B8860B`

### 6.5 Griglia Articoli Secondari (Seconda Riga — Col 1-6)

- **Titolo sezione:** Playfair Display Bold, 16px, Bordeaux, sottolineato con filetto Oro 1px
- **Titolo articolo:** Playfair Display Bold, 13px, Nero
- **Corpo:** EB Garamond Regular, 10px, Nero, interlinea 13px
- **Fonte:** Courier Prime Italic, 9px, Grigio
- **Gap tra articoli secondari:** 20px

### 6.6 Footer Giornale

- **Filetto superiore:** 2px, Oro `#B8860B`
- **Testo:** Courier Prime, 10px, Grigio `#4A4A4A`
- **Contenuto:** `Quotidiani Geopolitico — Anno XX, Num. 107 — 18 Aprile 2026 | Editore: Nico | Powered by MiniMax AI`

---

## 7. Componenti UI — Riepilogo Dimensionale

| Componente | Font | Size | Colore | Background |
|------------|------|------|--------|------------|
| Masthead | Playfair Bold | 48px | Nero | Carta |
| Dateline | Courier Prime | 12px | Grigio | — |
| Barra Flash | Courier Prime Bold | 11px | Bianco | Cremisi |
| Occhiello | Playfair Italic | 13px | Bordeaux | — |
| Titolo Principale | Playfair Bold | 32px | Nero | — |
| Sommario | EB Garamond Italic | 14px | Nero | — |
| Corpo Principale | EB Garamond Regular | 11px | Nero | — |
| Box Citazione | EB Garamond Italic | 13px | Nero | Carta + bordo Bordeaux |
| Titoli Flash | Playfair Bold | 14px | Nero | — |
| Corpo Flash | EB Garamond Regular | 10px | Nero | — |
| Titoli Sezione | Playfair Bold | 16px | Bordeaux | — |
| Titoli Articoli Secondari | Playfair Bold | 13px | Nero | — |
| Corpo Secondario | EB Garamond Regular | 10px | Nero | — |
| Didascalie | Courier Prime Italic | 10px | Grigio | — |
| Footer | Courier Prime | 10px | Grigio | — |

---

## 8. Regole di Impaginazione

1. **Mai mandare il testo in overflow** — calcolare l'altezza disponibile PRIMA di impaginare
2. **Tagliare i titoli** se superano 4 righe — meglio un titolo breve che un overflow
3. **Foto sempre B/N** — nessuna eccezione (stile cartaceo)
4. **Almeno 2px tra elementi** — il vuoto è elegante, l'affollamento no
5. **Filetti oro** ovunque ci sia una separazione di sezione
6. **Maiuscolo bianco** su sfondo colorato — solo Courier Prime Bold

---

## 9. Architecture Review — Flusso Thomas + Piotr

```
Thomas genera immagine PNG
        ↓
Thomas condivide PNG con Piotr
        ↓
Piotr fa Image Recognition verify:
  - I colori corrispondono alla palette?
  - I font si vedono correttamente?
  - La struttura 6 colonne è rispettata?
  - Il masthead è conforme?
        ↓
Se OK → si passa al Text layer
Se NO → Thomas rigenera con fix specifici
```

**Criteri di accettazione visiva (Piotr verify):**
- [ ] Sfondo `#F5F0E8` (carta) — NON bianco puro
- [ ] Titoli Playfair Display — serif, non sans-serif
- [ ] Filetti Oro `#B8860B` visibili
- [ ] Box Flash Cremisi `#C0392B` con bordo oro
- [ ] Nessun elemento che trabocca fuori pagina
- [ ] 6 colonne distinte e allineate

---

## 10. Font Test Pre-Implementation (Thomas)

**OBBLIGATORIO prima di implementare il layout:**

```python
from PIL import Image, ImageDraw, ImageFont

fonts = {
    "Playfair": "./assets/fonts/PlayfairDisplay-Bold.ttf",
    "Garamond": "./assets/fonts/EBGaramond-Regular.ttf",
    "Courier": "./assets/fonts/CourierPrime-Regular.ttf",
}

for name, path in fonts.items():
    try:
        font = ImageFont.truetype(path, 48)
        print(f"✅ {name}: caricato OK")
    except Exception as e:
        print(f"❌ {name}: ERRORE — {e}")
        # Fallback: Georgia/monospace MA documenta l'issue
```

Se un font non carica → fallback a Georgia/monospace MA documentare l'issue prima di procedere.

---

## 11. Processo di Review V3

### Flusso Articolo

```
1. Thomas scrive bozza articolo (basato su issue Linear con criteria)
2. Thomas apre PR su GitHub con bozza PNG
3. Goksu fa QA visivo + criteria check
4. Se Goksu dice "non va" → Thomas riscrive → torna a step 2
5. Se Goksu dice "ok" → articolo approvato per pubblicazione
6. Thomas pubblica su Telegram
```

### Criteri per articolo (in issue Linear)

Ogni issue deve contenere:
- Titolo esatto dell'articolo
- Fonti (link o note)
- Lunghezza target (parole o caratteri)
- Tono (formale/informale/analitico)
- Deadline
- Acceptance criteria specifici

### Backlog Scarti

Per ogni edizione, Thomas documenta in `logs/backlog-<data>.md`:
- Notizia considerata ma scartata
- Motivo della scelta

---

## 12. Checklist Implementazione

- [ ] Font test OK (Thomas)
- [ ] Palette applicata in config
- [ ] Griglia 6 colonne calcolata
- [ ] Masthead impaginato
- [ ] Barra flash Cremisi
- [ ] Articolo principale (col 1-4)
- [ ] 2 Flash box (col 5-6)
- [ ] Griglia articoli secondari (riga 2)
- [ ] Footer con disclaimer
- [ ] Image generation + verify (Thomas + Piotr)
- [ ] 3 run end-to-end consecutive OK

---

**Creato:** 2026-04-18  
**Aggiornato:** 2026-04-18  
**Architect:** Piotr
