# Quotidiano Geopolitico v2

Generatore giornaliero di un quotidiano geopolitico in stile italiano classico.

## Stack
- **ReportLab** + **Pillow** per rendering PDF/PNG
- **Google Fonts** bundled (Playfair Display, EB Garamond, Courier Prime)

## Setup

```bash
# Installa dipendenze
pip install -r requirements.txt

# Scarica font da Google Fonts
./scripts/download_fonts.sh

# Esegui manualmente
python main.py
```

## Architettura
Vedi `ARCHITECTURE_LOCK.md` per i dettagli completi.

## Cron
Esegui ogni giorno alle 07:30 (Europe/Rome):
```bash
./scripts/setup_cron.sh
```