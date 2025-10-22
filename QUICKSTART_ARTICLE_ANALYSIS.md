# Quickstart: Artikel-Analyse mit LLM

## 🎯 Dein Ziel

URLs von News & Events Artikeln analysieren und verstehen:
- **Welche Artikel-Typen bekommen positives Feedback?**
- **Welche Artikel-Typen bekommen negatives Feedback?**

## 📊 1. Excel-Datei vorbereiten

Erstelle eine Excel-Datei mit 2 Spalten:

```
Spalte A (URL)                              | Spalte B (Kommentar)
-------------------------------------------|---------------------------
https://intranet.firma.de/artikel/123      | Great article!
https://intranet.firma.de/artikel/123      | Very helpful
https://intranet.firma.de/artikel/456      | Not clear
https://intranet.firma.de/artikel/789      | Excellent!
```

**Speichere die Datei in:**
```
data/input/meine_artikel.xlsx
```

## 🚀 2. Analyse starten

### In Corporate-Umgebung (Windows):

```cmd
cd P:\IMPORTANT\Projects\SentimentAnalysis
python main_with_llm.py --input data/input/meine_artikel.xlsx
```

### Optionen:

```bash
# Standard (mit LLM Model - hohe Genauigkeit)
python main_with_llm.py --input data/input/meine_artikel.xlsx

# Schneller Modus (Lexikon statt LLM - geringere Genauigkeit)
python main_with_llm.py --input data/input/meine_artikel.xlsx --no-llm

# Ohne Web Scraping (nur Kommentar-Analyse)
python main_with_llm.py --input data/input/meine_artikel.xlsx --no-scraping

# Ohne Clustering
python main_with_llm.py --input data/input/meine_artikel.xlsx --no-clustering
```

## 📈 3. Ergebnis öffnen

Die Analyse erstellt eine Excel-Datei:
```
data/output/llm_analysis_20251022_143022.xlsx
```

**Diese Datei öffnen:**
```cmd
start data\output\llm_analysis_20251022_143022.xlsx
```

## 📊 4. Ergebnisse interpretieren

### Sheet "Kategorien" - **Wichtigste Ansicht!**

Hier siehst du die Antwort auf deine Frage:

| Kategorie | Avg_Sentiment | Anzahl_Artikel | Positive_Kommentare | Negative_Kommentare |
|-----------|---------------|----------------|---------------------|---------------------|
| Training  | +0.82         | 15             | 120                 | 8                   |
| HR        | +0.65         | 25             | 180                 | 45                  |
| IT        | +0.42         | 30             | 145                 | 78                  |
| Management| +0.15         | 10             | 65                  | 52                  |

**Interpretation:**
- ✅ **Training-Artikel** bekommen bestes Feedback (+0.82)
- ✅ **HR-Artikel** kommen gut an (+0.65)
- ⚠️ **IT-Artikel** sind ok (+0.42)
- ⚠️ **Management-Artikel** brauchen Verbesserung (+0.15)

### Sheet "Clusters" - Detaillierte Themen-Gruppen

| Cluster | Avg_Sentiment | Anzahl_Artikel |
|---------|---------------|----------------|
| Training_workshop | +0.88 | 8 |
| HR_recruiting | +0.75 | 12 |
| IT_software | +0.35 | 15 |
| Management_restructuring | -0.22 | 5 |

**Interpretation:**
- Workshop-Ankündigungen funktionieren hervorragend
- Recruiting-News kommen gut an
- Software-Updates könnten verständlicher sein
- Restructuring-News erzeugen negative Reaktionen

### Sheet "Artikel" - Alle Artikel im Detail

Vollständige Liste mit:
- URL
- Titel
- Kategorie
- Cluster
- Durchschnittliches Sentiment
- Anzahl Kommentare (positiv/negativ/neutral)

### Sheet "Insights" - Top & Worst Artikel

- **Top 5 Artikel** mit bestem Feedback
- **Worst 5 Artikel** mit schlechtestem Feedback

## 🎯 Actionable Insights

Basierend auf den Ergebnissen kannst du:

1. **Mehr von gut funktionierenden Artikel-Typen** veröffentlichen
2. **Schlecht bewertete Artikel-Typen** verbessern oder vermeiden
3. **Spezifische Themen identifizieren** die gut/schlecht ankommen
4. **Content-Strategie anpassen**

## ⚙️ Eigene Kategorien hinzufügen

Bearbeite `config/settings.py`:

```python
CATEGORY_KEYWORDS = {
    'HR': ['mitarbeiter', 'personal', 'recruiting', ...],
    'IT': ['software', 'hardware', 'system', ...],

    # Füge eigene Kategorie hinzu:
    'Sustainability': ['nachhaltigkeit', 'umwelt', 'green', 'co2'],
    'Innovation': ['innovation', 'digital', 'transformation', 'ai'],
}
```

## 🔧 Performance-Tipps

### Erste Verwendung (~60s Model Loading):
```
[3/6] Sentiment-Analyse der Kommentare...
Lade LLM Model (kann ~60s dauern)...
✓ LLM Model geladen (Mode: bert)
```
→ **Normal!** Das Model wird nur einmal geladen.

### Viele Artikel (>100):
```bash
# Verwende Lexikon-Modus (10x schneller)
python main_with_llm.py --input datei.xlsx --no-llm
```

### URLs nicht erreichbar:
```bash
# Überspringe Web Scraping (nur Kommentar-Analyse)
python main_with_llm.py --input datei.xlsx --no-scraping
```

## 📝 Vollständige Dokumentation

- **USAGE_GUIDE.md** - Ausführliche Anleitung mit allen Optionen
- **LLM Solution/CORPORATE_DEPLOYMENT.md** - Setup-Guide für Corporate-Umgebung
- **LLM Solution/README.md** - Technische Details zum LLM Model

## 🆘 Troubleshooting

### "Keine Input-Datei gefunden"
→ Lege Excel-Datei in `data/input/` ab

### "LLM Solution nicht verfügbar"
→ Stelle sicher dass `LLM Solution/` Ordner existiert und Dependencies installiert sind

### "transformers nicht verfügbar"
→ Installiere Dependencies:
```cmd
cd "P:\IMPORTANT\Projects\SentimentAnalysis\LLM Solution"
python -m pip install --no-index --find-links=wheels transformers torch
```

### "Scraping schlägt fehl"
→ Verwende `--no-scraping` falls URLs nicht erreichbar sind

## ✅ Zusammenfassung

**Input:**
```
Excel mit URLs + Kommentaren
```

**Befehl:**
```bash
python main_with_llm.py --input data/input/meine_artikel.xlsx
```

**Output:**
```
Excel Report mit Antwort auf:
"Welche Artikel-Typen haben positives/negatives Feedback?"
```

**Ergebnis:**
```
Sheet "Kategorien" → Sortiert nach Avg_Sentiment
→ Top-Kategorien = Beste Artikel-Typen!
```

---

**Los geht's! 🚀**

Lege deine Excel-Datei in `data/input/` und starte die Analyse!
