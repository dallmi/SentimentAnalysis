# Troubleshooting Guide

## Häufige Probleme und Lösungen

### 1. Import-Fehler: Modul nicht gefunden

**Problem**: `ModuleNotFoundError: No module named 'pandas'`

**Lösung**:
```bash
# Virtuelle Umgebung aktivieren
source venv/bin/activate

# Dependencies installieren
pip install -r requirements.txt
```

### 2. Excel-Datei kann nicht gelesen werden

**Problem**: `Error loading Excel file`

**Lösungen**:
- Prüfe ob Datei existiert und Berechtigungen korrekt sind
- Stelle sicher, dass es eine .xlsx oder .xls Datei ist
- Prüfe ob Spalten A und B existieren
- Verwende `--url-column` und `--comment-column` Parameter falls andere Spalten

### 3. Corporate Proxy Probleme

**Problem**: `Connection Error` beim Web Scraping

**Lösungen**:
1. Konfiguriere Proxy in `config/settings.py`:
```python
PROXY_CONFIG = {
    'http': 'http://proxy.firma.de:8080',
    'https': 'http://proxy.firma.de:8080'
}
```

2. Oder setze Umgebungsvariablen:
```bash
export http_proxy="http://proxy.firma.de:8080"
export https_proxy="http://proxy.firma.de:8080"
```

3. Überspringe Web Scraping:
```bash
python main.py --input data/input/datei.xlsx --no-scraping
```

### 4. NLTK VADER nicht verfügbar

**Problem**: `VADER not available`

**Lösungen**:
- Ist kein kritischer Fehler, System nutzt automatisch Lightweight Model
- Falls VADER gewünscht:
```bash
pip install nltk
python -c "import nltk; nltk.download('vader_lexicon')"
```

### 5. SSL Zertifikat Fehler

**Problem**: `SSL: CERTIFICATE_VERIFY_FAILED`

**Lösung**: In `src/web_scraper.py` Zeile ~55, ändere:
```python
response = self.session.get(url, timeout=REQUEST_TIMEOUT, verify=False)
```

**WARNUNG**: Nur in sicheren Intranet-Umgebungen verwenden!

### 6. Keine Output-Dateien generiert

**Problem**: Programm läuft durch, aber keine Excel-Dateien

**Lösungen**:
- Prüfe Schreibrechte im `data/output/` Verzeichnis
- Prüfe Logs in `sentiment_analysis.log`
- Stelle sicher dass pandas und openpyxl installiert sind

### 7. Speicherprobleme bei vielen URLs

**Problem**: `MemoryError` oder sehr langsam

**Lösungen**:
- Teile Input-Datei in kleinere Chunks auf
- Erhöhe `DELAY_BETWEEN_REQUESTS` in `config/settings.py`
- Reduziere gleichzeitige Verarbeitung

### 8. Nexus Repository / Corporate Packages

**Problem**: Packages können nicht aus PyPI installiert werden

**Lösungen**:
1. Nutze Corporate Nexus:
```bash
pip install --index-url https://nexus.firma.de/repository/pypi-all/simple -r requirements.txt
```

2. Falls gar keine externen Packages erlaubt:
- Nutze nur Python Standard Library Version
- Siehe `docs/minimal_dependencies.md` (erstelle ich gleich)

### 9. Encoding-Probleme

**Problem**: `UnicodeDecodeError` beim Lesen von Dateien

**Lösung**: Excel sollte UTF-8 oder Latin-1 encoded sein

### 10. Tests schlagen fehl

**Problem**: `test_modules.py` gibt Fehler

**Lösung**:
```bash
# Stelle sicher, dass du im richtigen Verzeichnis bist
cd /Users/micha/Documents/Arbeit/SentimentAnalysis

# Aktiviere venv
source venv/bin/activate

# Führe Tests aus
python test_modules.py
```

## Support

Bei weiteren Problemen:
1. Prüfe `sentiment_analysis.log` für detaillierte Fehler
2. Aktiviere Debug-Logging in der jeweiligen Modul-Datei
3. Teste mit `--no-scraping` Option für schnellere Fehlersuche
