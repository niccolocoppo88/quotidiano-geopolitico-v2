"""
lib/content_generator.py — Generazione contenuti con MiniMax AI
"""
import os
import requests
import json
from datetime import datetime
from config import MINIMAX_API_KEY, MINIMAX_BASE_URL
from lib.news_fetcher import Article

class ContentGenerator:
    def __init__(self):
        self.api_key = MINIMAX_API_KEY or os.getenv("MINIMAX_API_KEY", "")
        self.base_url = MINIMAX_BASE_URL
        self.model = "MiniMax-Text-01"

    def _call(self, messages: list[dict]) -> str:
        """Chiama l'API MiniMax per generazione testo."""
        if not self.api_key:
            print("[content_generator] AVVISO: MINIMAX_API_KEY non impostata, uso fallback locale")
            return None

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 600,
        }
        try:
            resp = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"]
            else:
                print(f"[content_generator] Errore API: {resp.status_code} {resp.text[:200]}")
                return None
        except Exception as e:
            print(f"[content_generator] Errore chiamata API: {e}")
            return None

    def _system_prompt(self) -> str:
        return (
            "Sei un giornalista esperto de Il Quotidiano Geopolitico, ispirato al Corriere della Sera degli anni '70. "
            "Scrivi titoli solenni e autorevoli, sommari incisivi, articoli strutturati. "
            "Usa un italiano colto e formale. Non essere mai banale."
        )

    def generate_titolo(self, article: Article) -> str:
        """Genera un titolo da articolo grezzo."""
        prompt = (
            f"{self._system_prompt()}\n\n"
            f"Notizia: {article.title}\n"
            f"Riassunto: {article.summary}\n\n"
            f"Genera un titolo da prima pagina (massimo 12 parole):"
        )
        result = self._call([
            {"role": "system", "content": prompt},
            {"role": "user", "content": f" Scrivi il titolo per questa notizia: {article.title}"}
        ])
        return result or article.title

    def generate_sommario(self, article: Article) -> str:
        """Genera un sommario da articolo."""
        result = self._call([
            {"role": "system", "content": self._system_prompt()},
            {"role": "user", "content": f" Scrivi un sommario di 2-3 righe per: {article.title}\n\nContenuto: {article.summary[:400]}"}
        ])
        return result or article.summary[:200]

    def generate_articolo(self, article: Article) -> str:
        """Genera un articolo completo."""
        result = self._call([
            {"role": "system", "content": self._system_prompt()},
            {"role": "user", "content": (
                f"Scrivi un articolo completo (300 parole) per il Quotidiano Geopolitico.\n"
                f"Titolo: {article.title}\n"
                f"Contesto: {article.summary}\n\n"
                f"Usa il tono del Corriere della Sera: autorevole, colto, informato. "
                f"Struttura: occhiello, titolo, lead, corpo.\n"
                f"Usacapolettera per il primo paragrafo."
            )}
        ])
        return result or f"{article.title}\n\n{article.summary}"

    def generate_flash_news(self, articles: list[Article]) -> list[str]:
        """Genera 2 flash news brevi da una lista di articoli."""
        if not articles:
            return ["Nessuna notizia disponibile"]
        titles = " | ".join([a.title for a in articles[:4]])
        result = self._call([
            {"role": "system", "content": self._system_prompt()},
            {"role": "user", "content": f"Da queste notizie: {titles}\n\nScrivi 2 flash brevissimi (max 20 parole l'uno), no titoli, solo la notizia. Formato: una notizia per riga."}
        ])
        if result:
            lines = [l.strip() for l in result.split("\n") if l.strip()]
            return lines[:2]
        return [a.title[:60] for a in articles[:2]]

    def generate_editoriale(self, articles: list[Article]) -> str:
        """Genera un editoriale breve."""
        if not articles:
            return "La geopolitica di oggi richiede lucidità e longatità. L'Europa deve trovare la sua voce."
        context = " | ".join([f"{a.category.upper()}: {a.title}" for a in articles[:4]])
        result = self._call([
            {"role": "system", "content": self._system_prompt()},
            {"role": "user", "content": f"Contesto notizie di oggi: {context}\n\nScrivi un editoriale breve (150 parole) in stile Quotidiano Geopolitico, tono colto e riflessivo. Chiudi con una frase memorabile."}
        ])
        return result or "L'ordine mondiale sta cambiando. L'Europa deve saper leggere i segni del tempo."

    def enrich_articles(self, articles: dict[str, list[Article]]) -> dict:
        """Arricchisce tutti gli articoli con contenuti generati."""
        enriched = {}
        for category, arts in articles.items():
            enriched[category] = []
            for art in arts[:4]:
                enriched[category].append({
                    "original": art,
                    "titolo": self.generate_titolo(art),
                    "sommario": self.generate_sommario(art),
                    "articolo": self.generate_articolo(art),
                })
        return enriched


# Fallback locale con mock data pre-compilata
def generate_mock_content(articles: dict[str, list[Article]]) -> dict:
    """Contenuti pre-scritti per test locale (nessuna API necessaria)."""
    import random
    all_arts = []
    for cat, arts in articles.items():
        all_arts.extend(arts)

    if not all_arts:
        all_arts = [
            Article("Vertice NATO a Bruxelles sulle nuove strategie", "I leader dell'Alleanza Atlantica discutono il rafforzamento delle forze in Europa orientale.", "Reuters", "geopolitica"),
            Article("Cina risponde ai dazi Usa con contromisure", "Pechino annuncia restrizioni sulle esportazioni di terre rare e tecnologie.", "BBC", "geopolitica"),
        ]

    main = all_arts[0] if all_arts else None
    flashes = [
        "Cina blocca i dazi Usa con contromisure su tecnologie",
        "Petrolio: +3% dopo taglio OPEC+ annunciato",
    ]
    if len(all_arts) > 1:
        flashes[0] = all_arts[1].title[:60]

    rubriche = {
        "mondo": [
            "Iran: nuove trattative nucleari a Vienna",
            "Venezuela: elezioni contestate dall'opposizione",
            "Corea: Kim Jong-un in visita a Pechino",
            "Africa: siccità record nel Corno",
        ],
        "economia": [
            "BCE: tassi invariati, inflazione sotto controllo",
            "Euro in calo sul dollaro dopo dati Usa",
            "Energia: gas naturale a livelli record",
            "Start-up: round da 50M per biotech italiana",
        ],
        "tech": [
            "Apple: Vision Pro 2 atteso per autunno",
            "Google: Gemini Ultra release globale",
            "Cybersecurity: attacco a sistemi istituzionali UE",
            "AI: nuova regolamentazione Ue in arrivo",
        ],
    }

    editoriale = (
        "«La storia non si ripete, ma spesso rima.» Così commentavano gli osservatori stranieri "
        "la situazione geopolitica attuale. L'Europa, che aveva creduto nella fine della storia, "
        "si trova oggi a dover riscrivere il proprio futuro — non come spettatore, ma come protagonista. "
        "Le sfide sono enormi: dalla crisi climatica alla competizione tecnologica, "
        "dalla sicurezza energetica alla tenuta sociale. Ma proprio nelle crisi risiede l'opportunità."
    )

    return {
        "main_article": {
            "original": main,
            "titolo": main.title if main else "NATO: vertice strategico a Bruxelles",
            "occhiello": "geopolitica",
            "sommario": main.summary if main else "I leader dell'Alleanza Atlantica si riuniscono per la nuova strategia.",
            "articolo": (
                "Dopo decenni di disimpegno, l'Europa si trova oggi a dover affrontare una realtà "
                "che aveva creduto di aver superato: la possibilità di un conflitto su larga scala "
                "sul proprio continente. L'invasione dell'Ucraina ha risvegliato antiche paure e, "
                "soprattutto, una nuova consapevolezza strategica.\n\n"
                "«Non possiamo più permetterci di delegare la nostra sicurezza agli altri» ha "
                "dichiarato il Segretario Generale della NATO in un'intervista esclusiva. "
                "«L'Europa deve imparare a camminare con le proprie gambe.»\n\n"
                "I numeri parlano chiaro: la spesa militare europea è cresciuta del 18% nell'ultimo anno, "
                "con la Germania che guida la classifica, seguita da Polonia e Paesi Baltici. "
                "Ma la vera sfida non è solo economica — è culturale e politica."
            ),
        },
        "flash_news": flashes,
        "economia_items": rubriche["economia"],
        "tech_items": rubriche["tech"],
        "mondo_items": rubriche["mondo"],
        "cultura_items": [
            "Biennale di Venezia: padiglione Italiainaugurato",
            "Restauro Colosseo: nuovi ritrovamenti archeologici",
            "Musica: Sanremo 2026, ospite internazionale annunciato",
        ],
        "editoriale": editoriale,
        "all_articles": articles,
    }
