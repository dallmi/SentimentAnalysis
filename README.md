# Sentiment Analysis für Corporate Intranet Artikel

## Übersicht
Dieses Tool analysiert Intranet-Artikel und deren Kommentare, um zu verstehen, welche Artikeltypen positive oder negative Sentiments in den Kommentaren erzeugen.

## Features
- Excel-Import von Artikel-URLs und Kommentaren
- Web Scraping von Artikel-Inhalten (Corporate Proxy-Support)
- Sentiment-Analyse der Kommentare
- Artikel-Kategorisierung basierend auf Kommentar-Sentiments
- Excel-Report-Generierung mit Visualisierungen

## Installation

### Virtuelle Umgebung erstellen
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
```

### Dependencies installieren
```bash
pip install -r requirements.txt
```

### NLTK Daten herunterladen (einmalig)
```bash
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt'); nltk.download('stopwords')"
```

## Verwendung

### 1. Input-Datei vorbereiten
Legen Sie Ihre Excel-Datei in `data/input/` ab mit:
- **Spalte A**: URLs der Artikel
- **Spalte B**: Kommentare zu den Artikeln
- Mehrere Zeilen pro Artikel möglich

### 2. Konfiguration anpassen
Bearbeiten Sie `config/settings.py` für:
- Proxy-Einstellungen
- Sentiment-Schwellenwerte
- Timeout-Werte

### 3. Programm ausführen
```bash
python main.py --input data/input/ihre_datei.xlsx
```

### 4. Ergebnisse prüfen
Die Ergebnisse finden Sie in `data/output/`:
- `results_TIMESTAMP.xlsx` - Detaillierte Analyse
- `summary_TIMESTAMP.xlsx` - Zusammenfassung
- `report_TIMESTAMP.html` - Visueller Report

## Projektstruktur
```
SentimentAnalysis/
├── src/
│   ├── data_loader.py          # Excel-Import
│   ├── web_scraper.py          # Artikel-Scraping
│   ├── sentiment_analyzer.py   # Sentiment-Analyse
│   ├── article_categorizer.py  # Kategorisierung
│   └── report_generator.py     # Report-Erstellung
├── models/
│   └── sentiment_model.py      # Lightweight Sentiment Model
├── config/
│   └── settings.py             # Konfiguration
├── data/
│   ├── input/                  # Input Excel-Dateien
│   └── output/                 # Generierte Reports
└── main.py                     # Hauptprogramm
```

## Corporate Network
Das Tool unterstützt Corporate Proxies. Konfigurieren Sie in `config/settings.py`:
```python
PROXY_CONFIG = {
    'http': 'http://your-proxy:8080',
    'https': 'http://your-proxy:8080'
}
```

## Lizenz
Interner Gebrauch
