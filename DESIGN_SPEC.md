# Design Spec — Quotidiano Geopolitico V2

## Stile

- **Riferimento:** Corriere della Sera anni '70
- **Carattere:** Eleganza autorevole, stile cartaceo, sobrietà giornalistica
- **Tono:** Serio, colto, senza fronzoli — il peso della carta stampata

---

## Palette Colori (hex esatti)

| Nome | Hex | Uso |
|------|-----|-----|
| Carta | `#F5F0E8` | Sfondo pagina, aree lectura |
| Nero | `#1A1A1A` | Testo principale, titoli |
| Bordeaux | `#8B1A1A` | Header, accent, titoli sezione |
| Oro | `#B8860B` | Filetti, separatori, dettagli premium |
| Cremisi | `#C0392B` | Box flash, breaking news, emergenze |

---

## Tipografia (Google Fonts CDN)

### Font Titoli — `Playfair Display`
- **Peso:** 700 (Bold)
- **Varianti:** Regular 400, Bold 700, Italic 400
- **CDN:** `https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap`
- **Uso:** Titoli articoli, masthead, titoli di sezione

### Font Corpo — `EB Garamond`
- **Peso:** 400 (Regular)
- **Varianti:** Regular 400, Italic 400, Medium 500
- **CDN:** `https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&display=swap`
- **Uso:** Corpo testo, sommari, box contesto

### Font Data/Numeri — `Courier Prime`
- **Peso:** 400 (Regular)
- **Varianti:** Regular 400, Italic 400, Bold 700
- **CDN:** `https://fonts.googleapis.com/css2?family=Courier+Prime:ital,wght@0,400;0,700;1,400&display=swap`
- **Uso:** Data in cima alla pagina, numeri di pagina, prezzi, statistiche

---

## Layout — 3 Pagine

### Pagina 1 — Prima Pagina

**Dimensioni:** 1200×1650 px (proporzione A4 portrait)

**Struttura:**
```
┌─────────────────────────────────────────────────────────────┐
│  ══════════════ FILO ORO (2px) ══════════════              │
│                                                             │
│  [MASTHEAD: QUOTIDIANO GEOPOLITICO]     [Data: 15 Apr 2026] │
│  ════════════════════════════════════════════════════════   │
│                                                             │
│  [OCCHIELLO: flash/breaking news — cremisi]                 │
│                                                             │
│  ┌───────────────────────────────┐ ┌─────────┬─────────┐  │
│  │                               │ │         │         │  │
│  │     ARTICOLO PRINCIPALE       │ │  FLASH  │  FLASH  │  │
│  │     (colonne 1-4)             │ │   5     │   6     │  │
│  │     Titolone + sommario       │ │         │         │  │
│  │     + foto B/N                │ │         │         │  │
│  │                               │ ├─────────┼─────────┤  │
│  │                               │ │ ECONOMIA│  TECH   │  │
│  │                               │ │  (1-3)  │  (4-6)  │  │
│  └───────────────────────────────┘ └─────────┴─────────┘  │
│                                                             │
│  [Filetto oro separatore]                                  │
│  [Altre notizie in griglia 6 col]                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Griglia 6 colonne:** ~170px ciascuna, gap 20px

---

### Pagina 2 — Approfondimento

**Header:** "APPROFONDIMENTO" centrato, font Playfair Display Bold, colore bordeaux `#8B1A1A`, sottolineato con filetto oro doppio.

**Struttura:**
```
┌─────────────────────────────────────────────────────────────┐
│              ══ APPROFONDIMENTO ══                         │
│                                                             │
│  Titolo Lungo dell'Articolo di Approfondimento            │
│  che occupa 2-3 righe                                      │
│                                                             │
│  ┌──────────────────────┐  ┌───────────────────────────── │
│  │                      │  │                              │
│  │   FOTO B/N           │  │  Corpo testo 2 colonne       │
│  │   (formato ritratto) │  │  con capolettera             │
│  │                      │  │                              │
│  │   Didascalia         │  │  Lorem ipsum dolor sit      │
│  └──────────────────────┘  │  amet, consectetur...       │
│                             │                              │
│                             └───────────────────────────── │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ 📜 BOX CONTESTO STORICO                                ││
│  │ Citazione o contesto storico con bordo bordeaux       ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Capolettera:** Prima lettera del primo paragrafo — Playfair Display Bold, ~4 righe di altezza, colore bordeaux.

---

### Pagina 3 — Rubriche

**Struttura:**
```
┌─────────────────────────────────────────────────────────────┐
│  [Header filetto oro]                                       │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   MONDO     │  │  ECONOMIA   │  │    TECH     │         │
│  │  [notizie]  │  │  [notizie]  │  │  [notizie]  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                             │
│              ┌─────────────────────┐                        │
│              │    CULTURA         │                        │
│              │   [rubriche]        │                        │
│              └─────────────────────┘                        │
│                                                             │
│        ┌───────────────────────────────────┐               │
│        │         EDITORIALE                │               │
│        │    (centrato, corsivo, lungo)     │               │
│        └───────────────────────────────────┘               │
│                                                             │
│  ─────────────────────────────────────────────────────     │
│  [FOOTER: disclaimer, copyright, data stampa]             │
│  [Cruciverba decorativo — element SVG]                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Grid Dettagliato — ASCII Art

### Prima Pagina
```
╔════════════════════════════════════════════════════════════════════╗
║════════════════════════════════════════════════════════════════════║
║  QUOTIDIANO GEOPOLITICO                          15 Aprile 2026   ║
║───────────────────────────────────────────────────────────────────║
║                                                                    ║
║  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ FLASH — Cremisi ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ║
║                                                                    ║
║  ┌─────────────────────────────┐ ┌──────────┬──────────┐          ║
║  │                             │ │          │          │          ║
║  │     ARTICOLO PRINCIPALE     │ │  FLASH   │  FLASH   │          ║
║  │     Titolone su 4 col.      │ │   col 5   │   col 6  │          ║
║  │                             │ │          │          │          ║
║  │     ┌─────────────────┐     │ ├──────────┼──────────┤          ║
║  │     │   foto B/N     │     │ │ ECONOMIA │   TECH   │          ║
║  │     └─────────────────┘     │ │  col 1-3 │  col 4-6 │          ║
║  │                             │ │          │          │          ║
║  └─────────────────────────────┘ └──────────┴──────────┘          ║
║                                                                    ║
║════════════════════════════════════════════════════════════════════║
╚════════════════════════════════════════════════════════════════════╝
```

### Griglia 6 Colonne
```
Col 1   Col 2   Col 3   Col 4   Col 5   Col 6
│170px  │170px  │170px  │170px  │170px  │170px  │
│←—————— 6 col = 1040px + 5 gap×20px = 1140px ——————→
```

---

## Componenti UI

### 1. Masthead
- Logo/testata "QUOTIDIANO GEOPOLITICO"
- Font: Playfair Display Bold, 48px
- Colore: Nero `#1A1A1A`
- Sottolineato da doppio filetto oro `#B8860B` (2px + 4px spazio + 1px)

### 2. Titoli Occhiello
- Font: Playfair Display Italic, 14px
- Colore: Bordeaux `#8B1A1A`
- Maiuscolo, letter-spacing: 0.1em

### 3. Box Flash / Breaking News
- Background: Cremisi `#C0392B`
- Testo: Bianco `#FFFFFF`
- Font: Courier Prime Bold, 12px
- Padding: 8px 12px
- Border-left: 4px oro `#B8860B`

### 4. Separatori Oro
- Linea orizzontale: 1px, colore Oro `#B8860B`
- Utilizzati tra sezioni
- Doppia linea per header importanti

### 5. Cruciverba (decorativo)
- Elemento SVG posizionato nel footer
- Reticolo grigio scuro `#333333`
- Caselle nere: Nero `#1A1A1A`
- Lettere: Courier Prime, 10px

### 6. Box Contesto Storico
- Bordo: 2px Bordeaux `#8B1A1A`
- Background: Carta `#F5F0E8`
- Padding: 16px
- Font: EB Garamond Italic, 14px
- Icona: 📜 (o SVG equivalente)

### 7. Capolettera
- Font: Playfair Display Bold
- Dimensione: 4 righe di testo
- Colore: Bordeaux `#8B1A1A`
- Float: left

---

## Font Solution

**Google Fonts CDN — nessun fallback locale:**

```html
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Courier+Prime:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
```

**Usage in CSS:**
```css
--font-titles: 'Playfair Display', Georgia, serif;
--font-body: 'EB Garamond', Georgia, serif;
--font-data: 'Courier Prime', 'Courier New', monospace;
```

**Regola:** nessun fallback a DejaVu, Liberation, o altri font di sistema. Se Google Fonts non carica, il fallback accettabile è `Georgia, serif` per i titoli/corpo e `monospace` per data/numeri.

---

## Responsive Strategy

- **Desktop (>1200px):** Layout nativo 1200px centrato
- **Tablet (768-1199px):** Griglia 4 colonne, prima pagina adattata
- **Mobile (<768px):** Layout single-column, sezioni impilate

---

## Checklist Implementazione

- [ ] Google Fonts CDN caricati
- [ ] Palette colori applicata con CSS variables
- [ ] Griglia 6 colonne CSS Grid
- [ ] Masthead con filetti oro
- [ ] Box flash cremisi
- [ ] Capolettera CSS
- [ ] Box contesto storico
- [ ] Cruciverba SVG decorativo
- [ ] Footer con disclaimer
- [ ] Responsive breakpoints
