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

### Zwei Modi:

#### Mode 1: Automatische Themen-Entdeckung - STANDARD ⭐

```bash
# Entdeckt automatisch was die Artikel behandeln (DEFAULT!)
python main_with_llm.py --input data/input/meine_artikel.xlsx
```

→ System findet selbst heraus über was Artikel geschrieben wurden
→ Keine vordefinierten Kategorien nötig
→ **EMPFOHLEN** für die meisten Anwendungsfälle

#### Mode 2: Vordefinierte Kategorien

```bash
# Verwendet 10 vordefinierte Content-Themen
python main_with_llm.py --input data/input/meine_artikel.xlsx --use-predefined
```

→ Kategorien: Employee Stories, AI & Innovation, Events & Networking, etc.
→ Gut für konsistente Quartals-Berichte

**Siehe [CATEGORIZATION_MODES.md](CATEGORIZATION_MODES.md) für Details zu beiden Modi!**

### Weitere Optionen:

```bash
# Mehr Themen entdecken (detaillierter)
python main_with_llm.py --input data/input/meine_artikel.xlsx --num-topics 15

# Weniger Themen (grobe Übersicht)
python main_with_llm.py --input data/input/meine_artikel.xlsx --num-topics 5

# Schneller Modus (Lexikon statt LLM - geringere Genauigkeit)
python main_with_llm.py --input data/input/meine_artikel.xlsx --no-llm

# Ohne Web Scraping (nur Kommentar-Analyse)
python main_with_llm.py --input data/input/meine_artikel.xlsx --no-scraping
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

Hier siehst du die Antwort auf deine Frage nach **Content-Themen** (nicht Abteilungen!):

| Content Theme | Avg_Sentiment | Anzahl_Artikel | Positive_Kommentare | Negative_Kommentare |
|---------------|---------------|----------------|---------------------|---------------------|
| Employee Stories | +0.88 | 15 | 142 | 5 |
| Events & Networking | +0.75 | 20 | 158 | 18 |
| Wellness & Benefits | +0.68 | 12 | 95 | 12 |
| Learning & Development | +0.62 | 18 | 120 | 25 |
| AI & Innovation | +0.45 | 25 | 145 | 48 |
| Product News | +0.38 | 22 | 125 | 58 |
| Culture & Values | +0.35 | 10 | 65 | 35 |
| Business & Success | +0.22 | 8 | 45 | 30 |
| Organizational Change | -0.15 | 12 | 35 | 75 |
| CSR & Sustainability | +0.55 | 8 | 52 | 12 |

**Interpretation:**
- ✅ **Employee Stories** funktionieren hervorragend! (+0.88)
- ✅ **Events & Networking** kommen sehr gut an (+0.75)
- ✅ **Wellness & Benefits** werden positiv aufgenommen (+0.68)
- ✅ **Learning & Development** ist beliebt (+0.62)
- ⚠️ **AI & Innovation** ist ok, könnte verständlicher sein (+0.45)
- ⚠️ **Organizational Change** erzeugen negative Reaktionen (-0.15)

### Sheet "Clusters" - Detaillierte Themen-Gruppen

| Cluster | Avg_Sentiment | Anzahl_Artikel |
|---------|---------------|----------------|
| Employee Stories_interview | +0.92 | 8 |
| Events & Networking_hackathon | +0.85 | 12 |
| Wellness & Benefits_sport | +0.72 | 10 |
| AI & Innovation_chatgpt | +0.48 | 15 |
| Organizational Change_restructuring | -0.28 | 5 |

**Interpretation:**
- Employee interviews funktionieren hervorragend
- Hackathon-Ankündigungen kommen sehr gut an
- Sport- & Wellness-Events werden positiv aufgenommen
- ChatGPT/AI-Themen erzeugen gemischte Reaktionen
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

## ⚙️ Eigene Content-Themen hinzufügen

Bearbeite [config/settings.py](config/settings.py):

```python
CATEGORY_KEYWORDS = {
    # Existing content themes (English names, multilingual keywords)
    'AI & Innovation': [
        # English (primary)
        'artificial intelligence', 'ai', 'machine learning', 'chatgpt',
        # German (secondary)
        'künstliche intelligenz', 'ki', 'digitalisierung',
        # French/Italian (tertiary)
        'intelligence artificielle', 'intelligenza artificiale'
    ],

    'Employee Stories': [
        'employee', 'story', 'interview',  # English
        'mitarbeiter', 'kollege', 'geschichte',  # German
        'employé', 'dipendente'  # French, Italian
    ],

    # Add your own content theme:
    'Customer Success': [
        # English (primary)
        'customer', 'client', 'success story', 'case study', 'testimonial',
        # German (secondary)
        'kunde', 'erfolgsgeschichte', 'referenz', 'anwendungsfall',
        # French/Italian (tertiary)
        'client', 'cliente', 'cas d\'usage'
    ],

    'Remote Work': [
        'remote work', 'work from home', 'wfh', 'hybrid',  # English
        'homeoffice', 'remote arbeit', 'hybrid arbeiten',  # German
        'télétravail', 'lavoro remoto'  # French, Italian
    ],
}
```

**Important:**
- Category names in **English** (consistent across all languages)
- Keywords: **English primary**, German secondary, French/Italian tertiary
- Keywords match the **content/topic**, not the department!

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
