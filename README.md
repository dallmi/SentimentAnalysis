# Sentiment Analysis System für Corporate Intranet Artikel

## Übersicht
Vollautomatisches LLM-basiertes Sentiment Analysis System für Corporate Intranet Artikel. Das System analysiert Artikel-Inhalte, kategorisiert sie nach Content-Themen, führt unsupervised Topic Discovery durch und bewertet Kommentar-Sentiments mit mehrsprachigen BERT-Modellen.

## Key Features
- **LLM-Powered Analysis**: BERT-basierte mehrsprachige Sentiment-Analyse (EN/DE/FR/IT)
- **Auto-Clustering**: Automatische Topic Discovery mit Silhouette Score Optimierung (k=2-10)
- **Offline-Deployment**: Vollständig offline lauffähig - keine HuggingFace API benötigt
- **Content-Theme Kategorisierung**: 10 vordefinierte Content-Kategorien (AI, HR, Culture, etc.)
- **Drei Analyse-Modi**: Auto-optimiert, Manuell, Vordefiniert
- **Corporate Proxy Support**: Funktioniert in geschützten Netzwerk-Umgebungen
- **Excel I/O**: Einfacher Import/Export für Business-User

## Quick Start

### 1. Installation

#### Virtuelle Umgebung erstellen
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
```

#### Dependencies installieren
```bash
pip install -r requirements.txt
```

#### Offline-Modelle einrichten (einmalig)
```bash
python setup_offline_model.py
```
Dies lädt das BERT-Modell (~600MB) herunter und speichert es lokal in `models/`.

### 2. Verwendung

#### Standard: Auto-Optimierte Topic Discovery (empfohlen)
```bash
python main.py --input data/input/meine_artikel.xlsx
```
→ Testet automatisch k=2 bis k=10 Cluster und wählt optimales k mit Silhouette Score

#### Manuelle Anzahl Topics
```bash
python main.py --input data/input/meine_artikel.xlsx --manual-topics --num-topics 7
```

#### Vordefinierte Content-Kategorien
```bash
python main.py --input data/input/meine_artikel.xlsx --use-predefined
```

### 3. Input-Format

Excel-Datei mit folgenden Spalten:
- **Spalte A**: Artikel-URLs
- **Spalte B**: Kommentare
- Mehrere Kommentare pro Artikel möglich (mehrere Zeilen)

### 4. Output

Generierte Dateien in `data/output/`:
- `results_TIMESTAMP.xlsx` - Detaillierte Analyse mit Sentiments
- `summary_TIMESTAMP.xlsx` - Aggregierte Topic-Statistiken
- `report_TIMESTAMP.html` - Interaktiver HTML-Report

## Dokumentation

Ausführliche Dokumentation verfügbar:
- **[QUICKSTART.md](QUICKSTART.md)** - Schnellstart-Guide mit allen Modi
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Detaillierte Verwendung
- **[CLUSTER_OPTIMIZATION.md](CLUSTER_OPTIMIZATION.md)** - Silhouette Score Deep-Dive
- **[CATEGORIZATION_MODES.md](CATEGORIZATION_MODES.md)** - Supervised vs Unsupervised
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Fehlerbehandlung

## Architektur

### Projektstruktur
```
SentimentAnalysis/
├── main.py                          # Hauptprogramm (LLM-Version)
├── setup_offline_model.py           # Offline-Modell Setup
├── config/
│   └── settings.py                  # Konfiguration (Content-Themes, Proxy)
├── src/
│   ├── data_loader.py               # Excel-Import
│   ├── web_scraper.py               # Artikel-Scraping
│   ├── article_categorizer.py       # Content-Theme Kategorisierung
│   └── report_generator.py          # Report-Erstellung
├── LLM Solution/
│   ├── llm_sentiment_analyzer.py    # BERT Sentiment-Analyse
│   ├── topic_discovery.py           # Unsupervised Topic Discovery
│   └── offline_sentiment_analyzer.py # Offline BERT-Wrapper
├── models/
│   └── bert-base-multilingual-uncased-sentiment/  # Lokales BERT-Modell (~600MB)
├── data/
│   ├── input/                       # Input Excel-Dateien
│   └── output/                      # Generierte Reports
└── archive/
    ├── main_lightweight.py          # Alte lightweight Version
    ├── QUICKSTART.md                # Alte Dokumentation
    └── PROJECT_SUMMARY.md           # Alte Projekt-Übersicht
```

### Technologie-Stack
- **Sentiment Analysis**: nlptown/bert-base-multilingual-uncased-sentiment
- **Topic Discovery**: TF-IDF + K-Means Clustering + Silhouette Score
- **Sprachen**: Deutsch, Englisch, Französisch, Italienisch
- **Content-Theme Kategorien**: 10 vordefinierte Themen (AI & Innovation, Employee Stories, Culture & Values, Learning & Development, Events & Networking, Product News, Business & Success, Wellness & Benefits, Organizational Change, CSR & Sustainability)

## Content-Theme Kategorien

Das System verwendet 10 vordefinierte Content-Themes mit mehrsprachigen Keywords:

1. **AI & Innovation** - KI, Machine Learning, Digitalisierung
2. **Employee Stories** - Mitarbeiter-Portraits, Erfolgsgeschichten
3. **Culture & Values** - Unternehmenskultur, Werte, Diversity
4. **Learning & Development** - Training, Weiterbildung, Skills
5. **Events & Networking** - Firmen-Events, Team-Building
6. **Product News** - Produkt-Launches, Updates
7. **Business & Success** - Geschäftsergebnisse, Meilensteine
8. **Wellness & Benefits** - Work-Life Balance, Benefits
9. **Organizational Change** - Restrukturierung, neue Strategien
10. **CSR & Sustainability** - Nachhaltigkeit, soziale Verantwortung

Details siehe [config/settings.py:36-164](config/settings.py#L36-L164)

## Cluster-Optimierung

Das System verwendet Silhouette Score zur automatischen Bestimmung der optimalen Cluster-Anzahl:

- **Range**: k=2 bis k=10
- **Metrik**: Silhouette Score (-1 bis +1)
- **Auswahl**: Höchster Score gewinnt
- **Fallback**: Standardmäßig k=5 wenn keine klare Optimierung möglich

Mehr Details in [CLUSTER_OPTIMIZATION.md](CLUSTER_OPTIMIZATION.md)

## Corporate Network Setup

### Proxy-Konfiguration
In `config/settings.py`:
```python
PROXY_CONFIG = {
    'http': 'http://your-proxy:8080',
    'https': 'http://your-proxy:8080'
}
```

### Offline-Betrieb
Das System benötigt **keine** Internet-Verbindung nach dem Setup:
1. Modelle werden einmalig mit `setup_offline_model.py` heruntergeladen
2. Alle Modelle liegen lokal in `models/` (~600MB)
3. Keine HuggingFace API-Calls zur Laufzeit

## Systemanforderungen

- **Python**: 3.8+
- **RAM**: Mindestens 4GB (BERT-Modell)
- **Disk**: ~1GB (Modelle + Dependencies)
- **Netzwerk**: Nur für initiales Setup (dann offline)

## Troubleshooting

### Häufige Probleme

**"Model not found"**
```bash
python setup_offline_model.py  # Modell neu herunterladen
```

**"Out of memory"**
→ Großen Batch in kleinere Teile aufteilen oder mehr RAM zuweisen

**Proxy-Fehler**
→ Proxy in `config/settings.py` konfigurieren

Vollständige Fehlerbehebung: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## Performance

- **Sentiment-Analyse**: ~10-20 Artikel/Minute (abhängig von Hardware)
- **Topic Discovery**: ~5-10 Sekunden für Auto-Optimierung (k=2-10)
- **Total Runtime**: ~5-15 Minuten für 100 Artikel mit 500 Kommentaren

## Lizenz

Interner Gebrauch - Corporate Intranet Analyse

---

**Version**: 2.0 (LLM-basiert mit Auto-Clustering)
**Letzte Aktualisierung**: 2025-10-22
**Archivierte Version**: Lightweight Version in `/archive/main_lightweight.py`
