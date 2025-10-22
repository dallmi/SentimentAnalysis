# Schnellstart-Anleitung

## 🚀 Quick Start in 3 Schritten

### 1. Installation
```bash
# Installation ausführen
./install.sh
```

Das Skript:
- Erstellt eine virtuelle Python-Umgebung
- Installiert alle benötigten Packages
- Lädt NLTK-Daten (optional für VADER)

### 2. Excel-Datei vorbereiten

Lege deine Excel-Datei in `data/input/` ab mit:
- **Spalte A**: URLs der Artikel
- **Spalte B**: Kommentare

Beispiel:
```
A: https://intranet.firma.de/artikel1
B: Super Artikel, sehr hilfreich!

A: https://intranet.firma.de/artikel1  
B: Gut erklärt!

A: https://intranet.firma.de/artikel2
B: Leider unklar
```

### 3. Programm ausführen

**Option A - Automatisch** (empfohlen für den Start):
```bash
./run.sh
```

**Option B - Manuell**:
```bash
# Aktiviere virtuelle Umgebung
source venv/bin/activate

# Führe Analyse aus
python main.py --input data/input/ihre_datei.xlsx
```

## 📊 Erweiterte Optionen

### Mit VADER Sentiment Analyzer (bessere Genauigkeit)
```bash
python main.py --input data/input/datei.xlsx --use-vader
```

### Ohne Web Scraping (nur Kommentar-Analyse)
```bash
python main.py --input data/input/datei.xlsx --no-scraping
```

### Custom Spalten angeben
```bash
python main.py --input data/input/datei.xlsx --url-column C --comment-column D
```

### Alle Optionen anzeigen
```bash
python main.py --help
```

## 📁 Output

Nach der Ausführung findest du in `data/output/`:

1. **detailed_report_TIMESTAMP.xlsx**
   - Artikel-Übersicht mit Kategorien und Sentiment
   - Kategorie-Sentiment-Analyse
   - Insights und Empfehlungen
   - Sentiment-Verteilung pro Artikel

2. **summary_report_TIMESTAMP.xlsx**
   - Gesamt-Statistiken
   - Top/Bottom Artikel
   - Sentiment-Kategorien-Übersicht

3. **visualization_report_TIMESTAMP.html** (optional)
   - HTML-Report mit Visualisierungen
   
4. **raw_analysis_data_TIMESTAMP.json**
   - Rohdaten für weitere Analysen

## 🔧 Konfiguration

Bearbeite `config/settings.py` für:

### Corporate Proxy
```python
PROXY_CONFIG = {
    'http': 'http://proxy.firma.de:8080',
    'https': 'http://proxy.firma.de:8080'
}
```

### Sentiment-Schwellenwerte
```python
SENTIMENT_THRESHOLDS = {
    'very_positive': 0.5,
    'positive': 0.1,
    'negative': -0.1,
    'very_negative': -0.5
}
```

### Kategorien anpassen
```python
CATEGORY_KEYWORDS = {
    'HR': ['mitarbeiter', 'personal', ...],
    'IT': ['software', 'hardware', ...],
    # Füge eigene Kategorien hinzu
}
```

## 🧪 System testen

```bash
# Test-Script ausführen
python test_modules.py
```

Testet:
- ✓ Sentiment Model
- ✓ Article Categorizer  
- ✓ Integration

## ❓ Probleme?

Siehe **TROUBLESHOOTING.md** für häufige Probleme und Lösungen.

## 📚 Beispiel-Workflow

```bash
# 1. Installation (einmalig)
./install.sh

# 2. Excel-Datei vorbereiten und ablegen
cp meine_artikel_kommentare.xlsx data/input/

# 3. Analyse ausführen
source venv/bin/activate
python main.py --input data/input/meine_artikel_kommentare.xlsx

# 4. Ergebnisse prüfen
open data/output/detailed_report_*.xlsx
```

## 🎯 Was macht das System?

1. **Lädt Excel-Daten**: URLs und Kommentare
2. **Scrapt Artikel**: Lädt Artikel-Inhalte von den URLs
3. **Analysiert Sentiment**: Bewertet jeden Kommentar (-1 bis +1)
4. **Kategorisiert Artikel**: Nach Thema (HR, IT, etc.)
5. **Korreliert**: Findet welche Kategorien positives/negatives Feedback erhalten
6. **Generiert Reports**: Excel + Visualisierungen

## 💡 Tipps

- Starte mit `--no-scraping` für schnelle Tests
- Nutze kleine Datenmengen zum Testen
- Prüfe `sentiment_analysis.log` bei Problemen
- Passe Kategorien in `config/settings.py` an deine Firma an

## 🔐 Corporate Environment

Das System ist für Corporate Netzwerke optimiert:
- ✓ Proxy-Support
- ✓ Nexus Repository kompatibel
- ✓ Keine Cloud-LLMs erforderlich
- ✓ Alles läuft lokal
- ✓ Kein Internet für Sentiment-Analyse nötig (nur für Scraping)

Bei Problemen mit Nexus:
```bash
pip install --index-url https://nexus.firma.de/repository/pypi-all/simple -r requirements.txt
```
