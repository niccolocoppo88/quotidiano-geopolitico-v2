"""
lib/news_fetcher.py — Fetch notizie da RSS + NewsAPI
"""
import feedparser
import requests
import random
from datetime import datetime
from config import RSS_FEEDS, NEWS_API_KEY, NEWS_API_URL

class Article:
    def __init__(self, title, summary, source, category, url="", published=None):
        self.title = title
        self.summary = summary
        self.source = source
        self.category = category
        self.url = url
        self.published = published or datetime.now().isoformat()

    def __repr__(self):
        return f"<Article({self.category}): {self.title[:50]}>"


def fetch_rss(feed_url: str) -> list[Article]:
    """Fetch singolo feed RSS."""
    try:
        feed = feedparser.parse(feed_url)
        articles = []
        for entry in feed.entries[:8]:
            title = getattr(entry, "title", "").strip()
            summary = getattr(entry, "summary", "").strip()
            # Strip HTML tags from summary
            import re
            summary = re.sub(r"<[^>]+>", "", summary)
            source = getattr(feed.feed, "title", feed_url)
            published = getattr(entry, "published", "")
            articles.append(Article(title, summary[:300], source, "", "", published))
        return articles
    except Exception as e:
        print(f"[news_fetcher] Errore RSS {feed_url}: {e}")
        return []


def fetch_all() -> dict[str, list[Article]]:
    """Fetch tutti i feed RSS e organizza per categoria."""
    all_articles = {"geopolitica": [], "economia": [], "tech": []}

    for category, feeds in RSS_FEEDS.items():
        for feed_url in feeds:
            articles = fetch_rss(feed_url)
            for a in articles:
                a.category = category
            all_articles[category].extend(articles)

    # Deduplica per titolo
    seen = set()
    for cat in all_articles:
        unique = []
        for a in all_articles[cat]:
            key = a.title[:80].lower()
            if key not in seen:
                seen.add(key)
                unique.append(a)
        all_articles[cat] = unique[:6]  # max 6 per categoria

    print(f"[news_fetcher] Totale articoli: {sum(len(v) for v in all_articles.values())}")
    return all_articles


def fetch_newsapi(category: str = "general", country: str = "us") -> list[Article]:
    """Fetch da NewsAPI (se chiave disponibile)."""
    if not NEWS_API_KEY:
        return []

    try:
        params = {
            "apikey": NEWS_API_KEY,
            "category": category,
            "country": country,
            "pageSize": 10,
        }
        resp = requests.get(f"{NEWS_API_URL}", params=params, timeout=10)
        data = resp.json()
        articles = []
        for item in data.get("articles", []):
            articles.append(Article(
                title=item.get("title", ""),
                summary=item.get("description", "")[:300],
                source=item.get("source", {}).get("name", ""),
                category=category,
                url=item.get("url", ""),
            ))
        return articles
    except Exception as e:
        print(f"[news_fetcher] Errore NewsAPI: {e}")
        return []


# Mock per test locale senza RSS
MOCK_ARTICLES = {
    "geopolitica": [
        Article(
            "NATO: più truppe al confine russo. Vertice a Bruxelles per la nuova strategia",
            "I leader dell'Alleanza Atlantica si riuniscono per discutere il rafforzamento delle forze nell'Europa orientale. Tensioni ai massimi dall'inizio della crisi.",
            "Reuters", "geopolitica"
        ),
        Article(
            "Iran: negoziati nucleare ripresi a Vienna",
            "Le potenze mondiali e l'Iran tornano al tavolo per tentare di rilanciare l'accordo sul programma nucleare.",
            "ANSA", "geopolitica"
        ),
        Article(
            "Cina blocca i dazi Usa con contromisure su tech",
            "Pechino risponde alle nuove tariffe americane con restrizioni sulle esportazioni di terre rare.",
            "BBC World", "geopolitica"
        ),
    ],
    "economia": [
        Article(
            "Borsa Milano: +1.2% dopo manovra economica",
            "Piazza Affari registra il miglior rialzo settimanale dell'anno trainata dal settore bancario.",
            "Reuters Business", "economia"
        ),
        Article(
            "Petrolio: +3% dopo taglio OPEC+",
            "Il barile supera i 90 dollari dopo l'annuncio di un nuovo taglio alla produzione da parte dell'alleanza.",
            "FT", "economia"
        ),
        Article(
            "Inflazione Eurozona: +2.1%, BCE pronta a tagliare",
            "Il dato inflattivo torna vicino all'obiettivo della Banca Centrale Europea.",
            "Reuters Business", "economia"
        ),
    ],
    "tech": [
        Article(
            "OpenAI lancia GPT-5 con capacità multimodali avanzate",
            "Il nuovo modello segna un passo avanti significativo nell'intelligenza artificiale generativa.",
            "TechCrunch", "tech"
        ),
        Article(
            "Apple: evento speciale il 23 per nuovi prodotti",
            "Attesi aggiornamenti per MacBook Pro e visori Vision Pro di nuova generazione.",
            "BBC Tech", "tech"
        ),
        Article(
            "Meta: tagli in Europa, 5.000 posti a rischio",
            "Il gigante social annuncia una ristrutturazione significativa delle operazioni europee.",
            "Ars Technica", "tech"
        ),
    ],
}

def fetch_with_fallback() -> dict[str, list[Article]]:
    """Prova RSS veri, altrimenti mock."""
    all_articles = fetch_all()
    total = sum(len(v) for v in all_articles.values())
    if total < 3:
        print("[news_fetcher] RSS non disponibili, uso mock data")
        return MOCK_ARTICLES
    return all_articles
