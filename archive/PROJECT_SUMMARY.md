# Sentiment Analysis System - Projekt-Zusammenfassung

## 📋 Projekt-Übersicht

**Zweck**: Analyse von Corporate Intranet-Artikeln und deren Kommentaren zur Identifikation von Sentiment-Patterns und Artikel-Kategorien mit positivem/negativem Feedback.

**Status**: ✅ Vollständig implementiert und einsatzbereit

## �� Hauptfunktionen

### 1. Excel Input-Verarbeitung
- Import von URLs (Spalte A) und Kommentaren (Spalte B)
- Automatische Gruppierung mehrerer Kommentare pro Artikel
- Datenvalidierung und Fehlerbehandlung

### 2. Web Scraping
- Lädt Artikel-Inhalte von Intranet-URLs
- Corporate Proxy-Support
- Robuste Fehlerbehandlung und Retry-Logik
- Extrahiert Titel, Content, Meta-Daten

### 3. Sentiment-Analyse
- **Lightweight Model**: Eigenständiges Sentiment-Wörterbuch (800+ deutsche Wörter)
- **VADER Option**: NLTK VADER als Alternative
- Sentiment-Scores: -1 (sehr negativ) bis +1 (sehr positiv)
- Kategorisierung: very_negative, negative, neutral, positive, very_positive

### 4. Artikel-Kategorisierung
- Thematische Kategorisierung (HR, IT, Management, etc.)
- Keyword-Extraktion
- Korrelations-Analyse: Kategorie ↔ Sentiment

### 5. Report-Generierung
- Detaillierter Excel-Report mit allen Analysen
- Zusammenfassungs-Report mit Statistiken
- Optional: HTML-Report mit Visualisierungen
- JSON-Export der Rohdaten

## 🏗️ Architektur

```
SentimentAnalysis/
├── main.py                    # Hauptprogramm, orchestriert Workflow
├── config/
│   └── settings.py           # Zentrale Konfiguration
├── src/
│   ├── data_loader.py        # Excel-Import und Validierung
│   ├── web_scraper.py        # Artikel-Scraping
│   ├── sentiment_analyzer.py # Sentiment-Analyse Koordinator
│   ├── article_categorizer.py# Thematische Kategorisierung
│   └── report_generator.py   # Report-Erstellung
├── models/
│   └── sentiment_model.py    # Lightweight Sentiment Model
└── data/
    ├── input/                # Excel-Input-Dateien
    └── output/               # Generierte Reports
```

## 🔑 Besondere Features

### Corporate-Network-Ready
- ✅ Proxy-Unterstützung
- ✅ Nexus Repository kompatibel
- ✅ SSL-Zertifikat-Handling
- ✅ Keine Cloud-Services erforderlich

### Lightweight Sentiment Model
- ✅ Keine externe LLM-API nötig
- ✅ 800+ deutsche Sentiment-Wörter
- ✅ Negations-Erkennung
- ✅ Verstärker-Erkennung
- ✅ Kontext-Analyse
- ✅ Funktioniert vollständig offline

### Flexible Konfiguration
- Anpassbare Sentiment-Schwellenwerte
- Eigene Kategorie-Keywords
- Konfigurierbares Web-Scraping
- Multiple Sentiment-Backend-Optionen

## 📊 Output-Beispiele

### Detailed Report (Excel)
1. **Artikel-Übersicht**: URL, Titel, Kategorie, Keywords, Sentiment-Scores
2. **Kategorien-Analyse**: Durchschn. Sentiment pro Kategorie
3. **Insights**: Automatisch generierte Erkenntnisse
4. **Sentiment-Verteilung**: Detaillierte Kommentar-Verteilung

### Summary Report (Excel)
1. **Gesamt-Statistik**: Artikel-Anzahl, Kommentare, Durchschnitte
2. **Top/Bottom Artikel**: Beste und schlechteste nach Sentiment
3. **Sentiment-Kategorien**: Verteilung über alle Artikel

## 🛠️ Technologie-Stack

### Kern-Dependencies
- **pandas** & **openpyxl**: Excel-Verarbeitung
- **requests** & **beautifulsoup4**: Web Scraping
- **nltk** (optional): VADER Sentiment
- **matplotlib** (optional): Visualisierungen

### Python Standard Library
- **re**: Regex für Text-Verarbeitung
- **logging**: Umfassendes Logging
- **pathlib**: Dateisystem-Operationen
- **typing**: Type Hints

## 🚀 Deployment

### Voraussetzungen
- Python 3.8+
- Schreibrechte für data/output/
- (Optional) Nexus Repository Zugang
- (Optional) Corporate Proxy-Konfiguration

### Installation
```bash
./install.sh
```

### Ausführung
```bash
./run.sh
# oder
python main.py --input data/input/ihre_datei.xlsx
```

## 📈 Performance

- **Scraping**: ~1-2 Sekunden pro URL (inkl. Delays)
- **Sentiment-Analyse**: ~0.001 Sekunden pro Kommentar
- **Kategorisierung**: ~0.01 Sekunden pro Artikel
- **Report-Generation**: ~1-2 Sekunden

**Beispiel**: 100 Artikel mit je 10 Kommentaren
- Scraping: ~3 Minuten
- Analyse: ~1 Sekunde
- Total: ~4 Minuten

## 🔒 Sicherheit & Datenschutz

- ✅ Keine Daten verlassen das lokale System
- ✅ Keine Cloud-APIs
- ✅ Alle Berechnungen lokal
- ✅ Logs enthalten keine sensitiven Daten
- ✅ Excel-Dateien bleiben im data/ Ordner

## 🧪 Testing

```bash
python test_modules.py
```

Testet:
- Sentiment Model mit verschiedenen Texten
- Kategorisierung mit Beispiel-Artikeln
- Integration aller Komponenten

## 📚 Dokumentation

- **README.md**: Projekt-Übersicht und Installation
- **QUICKSTART.md**: Schnellstart-Anleitung
- **TROUBLESHOOTING.md**: Problemlösungen
- **PROJECT_SUMMARY.md**: Diese Datei

## 🎓 Verwendete Algorithmen

### Sentiment-Analyse
1. **Tokenisierung**: Text → Wörter
2. **Lexikon-Lookup**: Wörter → Sentiment-Scores
3. **Kontext-Analyse**: Negationen, Verstärker
4. **Aggregation**: Gesamt-Score Berechnung
5. **Kategorisierung**: Score → Kategorie

### Kategorisierung
1. **Keyword-Matching**: Text ↔ Kategorie-Keywords
2. **TF (Term Frequency)**: Worthäufigkeit
3. **Scoring**: Gewichtete Kategorie-Scores
4. **Normalisierung**: Relative Scores

### Korrelations-Analyse
1. **Gruppierung**: Artikel nach Kategorie
2. **Aggregation**: Durchschnittliche Sentiments
3. **Ranking**: Best/Worst Kategorien
4. **Insight-Generation**: Automatische Erkenntnisse

## 🔄 Workflow

```
Excel Input
    ↓
Data Loading & Validation
    ↓
URL Grouping
    ↓
Web Scraping (parallel) ← Proxy
    ↓
Sentiment Analysis
    ↓
Article Categorization
    ↓
Correlation Analysis
    ↓
Report Generation
    ↓
Excel/HTML/JSON Output
```

## 💼 Business Value

### Erkenntnisse
- Welche Artikel-Typen erzeugen positives Feedback?
- Welche Themen sollten anders kommuniziert werden?
- Welche Kategorien haben Optimierungspotential?
- Sentiment-Trends über Zeit (mit mehreren Analysen)

### Anwendungsfälle
- Intranet-Content-Optimierung
- Kommunikations-Strategie
- Mitarbeiter-Feedback-Analyse
- Knowledge-Management
- Change-Management-Support

## 🔮 Erweiterungsmöglichkeiten

### Kurzfristig
- [ ] Zeit-basierte Trend-Analyse
- [ ] Mehr Visualisierungen
- [ ] Export als PDF-Report
- [ ] Email-Benachrichtigungen

### Mittelfristig
- [ ] Web-UI Dashboard
- [ ] Automatisierte Scheduled Runs
- [ ] Erweiterte NLP (Named Entity Recognition)
- [ ] Multi-Language Support

### Langfristig
- [ ] Machine Learning Model Training
- [ ] Topic Modeling (LDA)
- [ ] Sentiment über Zeit Tracking
- [ ] Integration mit anderen Systemen

## 👥 Wartung

### Logging
Alle Logs in: `sentiment_analysis.log`

### Updates
```bash
git pull
pip install --upgrade -r requirements.txt
```

### Backups
- Input-Dateien: Automatisch in `data/input/`
- Output-Dateien: Timestamped in `data/output/`
- Logs: In Root-Verzeichnis

## 📞 Support

Bei Fragen oder Problemen:
1. Prüfe **TROUBLESHOOTING.md**
2. Prüfe **sentiment_analysis.log**
3. Führe **test_modules.py** aus
4. Teste mit **--no-scraping** für schnellere Diagnose

## ✅ Projekt-Status

- [x] Basis-Architektur
- [x] Data Loading
- [x] Web Scraping
- [x] Sentiment-Analyse
- [x] Kategorisierung
- [x] Report-Generierung
- [x] Dokumentation
- [x] Testing
- [x] Installation Scripts
- [x] Git Repository

**Nächster Schritt**: Produktiv-Einsatz mit echten Daten!
