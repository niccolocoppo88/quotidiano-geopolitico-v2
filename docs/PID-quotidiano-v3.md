# PID — QUOTIDIANO GEOPOLITICO V3

**Versione:** 1.0  
**Data:** 2026-04-16  
**PM:** Elisa  
**Approvato da:** Nico  
**Status:** IN REVISIONE

---

## 1. Product Vision

**Problema che risolviamo:**
Nico ha bisogno di un quotidiano geopolitico automatico che arrivi ogni sera alle 22:00 — elegante, autorevole, leggibile in 5 minuti. Un giornale vero, non un aggregatore di link.

**Utenti concreti:**
- **Nico** — lettore finale. Vuole svegliarsi la mattina e in 5 minuti capire cosa è successo nel mondo. Non vuole pensare.
- **Il lettore finale** (che è Nico che condivide) — riceve il prodotto finito su Telegram.

**Cosa succede se non lo facciamo:**
Nico perde 30 minuti ogni mattina a cercare notizie disparate. Il quotidiano V2 era instabile e senza review.

**Criterio di successo misurabile:**
- Il giornale arriva entro le 22:00 (buffer 1h)
- 3 run end-to-end consecutive funzionano PRIMA di considerare delivery completata
- Goksu approva ogni articolo con criteria scritti

---

## 2. Scope

**✅ DENTRO (in scope):**
- Generazione automatica PDF-style PNG (stesso formato elegante V2)
- Invio automatico su Telegram
- Review strutturata PRIMA di pubblicazione
- Issue con criteri misurabili per ogni articolo
- Backlog notizie scartate documentato

**❌ FUORI (out of scope):**
- Nuova grafica o redesign del layout
- Multi-pagina (restiamo 1 pagina come V2)
- Supporto ad altre piattaforme (solo Telegram)
- Beta reader esterni (almeno per ora)

**Vincoli hard:**
- Pubblicazione: entro le 22:00 (non le 23:00 — buffer 1h)
- Stack: ReportLab + Pillow (mantenuto da V2)
- Font: Playfair Display, EB Garamond, Courier Prime (già scaricati)

---

## 3. Feature Priority

| Priorità | Feature | Descrizione | Criterio di accettazione |
|----------|---------|-------------|--------------------------|
| **P0** | Run stabile end-to-end | Genera → invia su Telegram senza errori | 3 run consecutive OK |
| **P0** | Review strutturata | Bozza → Goksu review → riscrittura → ok | Nessun articolo pubblicato senza ok esplicito |
| **P0** | Issue con criteria | Ogni articolo: titolo esatto, fonti, lunghezza, tono, deadline | Issue in Linear con tutti i campi compilati |
| **P1** | Buffer notizie scartate | Backlog documentato per ogni edizione | File `logs/backlog-<data>.md` |
| **P1** | End-to-end testato 3x | Verifica completa prima di annunciare delivery | 3 PNG ricevuti su Telegram di fila |
| **P2** | Funzionalità nuova | Qualcosa che differenzia V3 da V2 | Da definire con Nico |

---

## 4. Decisioni già prese

- [x] **Stack: ReportLab + Pillow** — funziona, mantenuto da V2
- [x] **Font: Playfair + Garamond + Courier Prime** — già scaricati in `assets/fonts/`
- [x] **Palette colori: Carta #F5F0E8, Nero #1A1A1A, Bordeaux #8B1A1A, Oro #B8860B, Cremisi #C0392B** — mantenuta da V2
- [x] **Orario pubblicazione: 22:00** (non più 23:00)
- [x] **Invio: Telegram bot** — mantenuto da V2

**Questo è Fermo — Non si tocca:**
1. Il formato elegante stile Corriere anni '70
2. La struttura a 6 colonne
3. L'invio automatico su Telegram (non cambia piattaforma)

---

## 5. Edge Case Principali

1. **Se una notizia API fallisce** → fallback a contenuto statico pre-scritto, retry 3x con backoff
2. **Se il font non si carica in ReportLab** → test precoce PRIMA del layout, fallback a font di sistema
3. **Se MiniMax API timeout** → Thomas logga "API fallita, uso fallback", continua senza bloccare
4. **Se Goksu dice "non va"** → articolo torna in bozza, Thomas riscrive, non si pubblica
5. **Se Run fallisce a metà** → notifica a Elisa, si investigate prima di provare ancora

---

## 6. Architettura Rough (per Thomas)

**Frontend:** PNG (stesso formato V2)  
**Backend/Servizi:** Python script con ReportLab + Pillow  
**Database:** File system (`output/`, `assets/`, `logs/`)  
**Invio:** Telegram Bot API  

**Mappa flusso:**
```
API News → Content Generator → PDF Renderer (ReportLab) → PNG Exporter → Telegram Sender → Goksu QA → Pubblicazione
```

**Note per Thomas:**
- Font test PRIMA di implementare layout — verifica che Playfair si veda come Playfair
- Timeout AI strategy con retry/backoff esponenziale (3 tentativi)
- Fallback a contenuto statico se API fallisce

---

## 7. Milestone

| Data | Milestone | Deliverable |
|------|-----------|-------------|
| 2026-04-16 | PID approvato | Questo documento approvato da Nico |
| 2026-04-16 | Linear + GitHub V3 | Repo, progetto, issue pronte |
| 2026-04-17 | End-to-end test #1 | Prima run completa |
| 2026-04-17 | End-to-end test #2 | Seconda run |
| 2026-04-18 | End-to-end test #3 | Terza run — se OK, delivery |
| 2026-04-18 | Delivery V3 | Annuncio a Nico |

**Decision Maker:** Nico — per ogni decisione ambigua, escalation a Nico.

---

## 8. Sprint Review — Cosa è andato storto in V2

**Goksu:**
- Deadline troppo stretta (23:00) → risolto con pubblicazione 22:00
- QA dopo pubblicazione → risolto con gate Goksu PRIMA

**Thomas:**
- Ha scritto senza criteri → risolto con issue Linear dettagliate
- Nessuna review → risolto con bozza → feedback → riscrittura
- Nessun gate → risolto con "nessun ok, nessuna pubblicazione"

**Piotr:**
- Due stack in parallelo → risolto con Architecture Review obbligatoria
- Font mai verificati → risolto con test font precoce
- Nessun end-to-end → risolto con 3 run consecutive

---

## 9. Ricerca Competitiva

Non applicabile per ora — il formato è già definito da V2. Se Nico vuole evolvere il formato, ne parliamo.

---

## Checklist Completamento PID

- [x] Product Vision compilato
- [x] Scope in/out definito
- [x] Feature priorizzate P0/P1/P2
- [x] Decisioni già prese elencate
- [x] Top 5 edge case documentati
- [x] Architettura rough per Thomas
- [x] Milestone con date
- [x] Decision Maker identificato
- [ ] Upload su GitHub (cartella `docs/`)
- [ ] Link condiviso con team su Discord

---

**Creato il:** 2026-04-16  
**PM:** Elisa  
**Approvato da:** Nico (in attesa)

---
_PID V3 — Quotidiani Geopolitico_