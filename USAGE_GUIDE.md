# Verwendungs-Anleitung - Artikel-Analyse mit LLM

## 🎯 Dein Use Case

Du möchtest:
1. ✅ URLs von News & Events Artikeln analysieren
2. ✅ Artikel-Inhalte verstehen und kategorisieren
3. ✅ Kommentare analysieren (Sentiment)
4. ✅ Korrelation finden: Welche Artikel-Typen → positives/negatives Feedback
5. ✅ Artikel clustern (ähnliche Artikel gruppieren)

## 📊 Input-Format

### Excel-Datei vorbereiten:

```
Spalte A (URL)                              | Spalte B (Kommentar)
-------------------------------------------|---------------------------
https://intranet.firma.de/artikel/123      | Great article, very helpful!
https://intranet.firma.de/artikel/123      | Thanks for sharing
https://intranet.firma.de/artikel/456      | Not clear, confusing
https://intranet.firma.de/artikel/456      | Could be better explained
https://intranet.firma.de/artikel/789      | Excellent overview!
```

**Wichtig:**
- Mehrere Zeilen pro Artikel möglich (für mehrere Kommentare)
- URLs werden automatisch gruppiert
- Kommentare werden pro Artikel aggregiert

### Speicherort:

```
data/input/deine_artikel.xlsx
```

---

## 🚀 Verwendung

### Option 1: Standard (Auto-Optimiert) - ⭐ EMPFOHLEN

```bash
python main.py --input data/input/deine_artikel.xlsx
```

**Was passiert:**
1. Lädt Excel-Datei
2. Scrapt Artikel-Inhalte von URLs
3. Analysiert Kommentare mit **BERT-Model** (hohe Genauigkeit, mehrsprachig)
4. **Auto-Clustering**: Findet automatisch optimale Anzahl Topics mit Silhouette Score (k=2-10)
5. Erstellt detaillierten Excel-Report

**Dauer:** ~3-5 Minuten für 50 Artikel (Model-Loading + Auto-Optimierung + Analyse)

### Option 2: Manuelle Anzahl Topics

Falls du eine bestimmte Anzahl Topics möchtest:

```bash
python main.py --input data/input/deine_artikel.xlsx --manual-topics --num-topics 7
```

**Verwendet:**
- ✅ Exakt 7 Topics (ohne Auto-Optimierung)
- ⚠️ Kann zu Over-/Under-Clustering führen

### Option 3: Vordefinierte Content-Kategorien

Falls du die 10 vordefinierten Content-Themen verwenden möchtest:

```bash
python main.py --input data/input/deine_artikel.xlsx --use-predefined
```

**Verwendet:**
- ✅ 10 Content-Themes (AI & Innovation, Employee Stories, Culture & Values, etc.)
- ⚠️ Keine neuen Topics - nur vordefinierte Kategorien

### Option 4: Ohne Web Scraping

Falls URLs nicht erreichbar oder nur Kommentare wichtig:

```bash
python main.py --input data/input/deine_artikel.xlsx --no-scraping
```

### Option 5: Schneller (ohne LLM)

```bash
python main.py --input data/input/deine_artikel.xlsx --no-llm
```

**Verwendet Lexikon-Modus:**
- ✅ ~10x schneller
- ⚠️ Etwas geringere Genauigkeit

---

## 📈 Output

### Generierte Datei:

```
data/output/llm_analysis_20251022_143022.xlsx
```

### Sheets:

#### 1. **Artikel** - Übersicht aller Artikel
| URL | Titel | Content Theme | Cluster | Avg_Sentiment | Total_Comments | Positive | Negative | Neutral |
|-----|-------|---------------|---------|---------------|----------------|----------|----------|---------|
| ... | ...   | Employee Stories | Employee Stories_interview | +0.85 | 12 | 10 | 1 | 1 |

#### 2. **Kategorien** - Sentiment pro Content-Thema ⭐ **WICHTIGSTE ANSICHT**
| Content Theme | Avg_Sentiment | Anzahl_Artikel | Positive_Kommentare | Negative_Kommentare |
|---------------|---------------|----------------|---------------------|---------------------|
| Employee Stories | +0.88 | 15 | 142 | 5 |
| Events & Networking | +0.75 | 20 | 158 | 18 |
| Wellness & Benefits | +0.68 | 12 | 95 | 12 |
| AI & Innovation | +0.45 | 25 | 145 | 48 |
| Organizational Change | -0.15 | 12 | 35 | 75 |

**→ Interpretation:** Employee Stories bekommen bestes Feedback! 🎯

#### 3. **Clusters** - Thematische Gruppen innerhalb der Content-Themen
| Cluster | Avg_Sentiment | Anzahl_Artikel |
|---------|---------------|----------------|
| HR_recruiting | +0.88 | 8 |
| IT_software_update | +0.35 | 12 |
| Management_restructuring | -0.22 | 5 |

**→ Interpretation:** Recruiting-Artikel sehr positiv, Restructuring negativ

#### 4. **Insights** - Top & Worst Artikel
- Top 5 Artikel mit bestem Feedback
- Worst 5 Artikel mit schlechtestem Feedback

---

## 🔍 Wie funktioniert die Kategorisierung?

Das System verwendet **Keyword-Matching**:

```python
CATEGORY_KEYWORDS = {
    'HR': ['mitarbeiter', 'personal', 'recruiting', 'bewerbung', 'employee', 'hiring'],
    'IT': ['software', 'hardware', 'system', 'update', 'server', 'application'],
    'Management': ['strategie', 'führung', 'management', 'leadership', 'restructuring'],
    'Training': ['schulung', 'training', 'workshop', 'seminar', 'course'],
    'Benefits': ['benefits', 'urlaub', 'gehalt', 'salary', 'bonus', 'pension'],
    # ... weitere Kategorien
}
```

**Du kannst eigene Kategorien hinzufügen** in `config/settings.py`!

---

## 🎨 Clustering-Logik

Artikel werden geclustert basierend auf:
1. **Hauptkategorie** (HR, IT, etc.)
2. **Dominantes Keyword** (das häufigste Keyword)

**Beispiel:**
- Artikel über "Recruiting" → Cluster: `HR_recruiting`
- Artikel über "Benefits" → Cluster: `HR_benefits`
- Artikel über "Software-Update" → Cluster: `IT_software`

→ So siehst du **welche Themen innerhalb einer Kategorie** gut/schlecht ankommen!

---

## 💡 Erweiterte Verwendung

### Custom Spalten

```bash
python main.py \
  --input data/input/datei.xlsx \
  --url-column C \
  --comment-column D
```

### Alle Optionen

```bash
python main.py --help
```

Zeigt:
```
--input PATH          Input Excel-Datei
--url-column COL      Spalte mit URLs (Standard: A)
--comment-column COL  Spalte mit Kommentaren (Standard: B)
--use-predefined      Verwende vordefinierte Kategorien statt Auto-Clustering
--manual-topics       Verwende fixe Anzahl Topics (benötigt --num-topics)
--num-topics N        Fixe Anzahl Topics (nur mit --manual-topics)
--no-llm              Verwende Lexikon statt LLM
--no-scraping         Überspringe Web Scraping
--no-clustering       Überspringe Clustering komplett
```

---

## 📊 Beispiel-Workflow

### Schritt 1: Daten vorbereiten

```bash
# Lege Excel-Datei ab
cp meine_artikel.xlsx data/input/
```

### Schritt 2: Analyse ausführen

```bash
# In Corporate-Umgebung (Windows)
cd P:\IMPORTANT\Projects\SentimentAnalysis
python main.py --input data/input/meine_artikel.xlsx
```

**Output:**
```
==============================================================================
  ERWEITERTE SENTIMENT-ANALYSE mit LLM & CLUSTERING
==============================================================================
Input-Datei: data/input/meine_artikel.xlsx

[1/6] Lade Daten aus Excel...
✓ 150 Zeilen geladen
✓ 50 unique Artikel gefunden

[2/6] Scrape Artikel-Inhalte...
  Scraping 1/50: https://intranet.firma.de/artikel/123
  ...
✓ 50 Artikel gescraped

[3/6] Sentiment-Analyse der Kommentare...
Lade LLM Model (kann ~60s dauern)...
✓ LLM Model geladen (Mode: bert)
Analysiere 150 Kommentare mit bert Model...
✓ 150 Kommentare analysiert
  Durchschnittliches Sentiment: +0.456

[4/6] Entdecke optimale Anzahl Themen automatisch (AUTO-OPTIMIERT - DEFAULT)...
      (Verwendet Silhouette Score - testet k=2 bis k=10)
Teste k=2: Silhouette score = 0.234
Teste k=3: Silhouette score = 0.312
Teste k=4: Silhouette score = 0.445
Teste k=5: Silhouette score = 0.498  ← OPTIMAL
Teste k=6: Silhouette score = 0.456
...
✓ Optimale Anzahl Themen: 5 (Silhouette Score: 0.498)

[5/6] Clustere Artikel in 5 Topics...
✓ 5 Topics gefunden:
  - Topic_0 (HR & Recruiting): 15 Artikel
  - Topic_1 (AI & Innovation): 20 Artikel
  - Topic_2 (Employee Benefits): 10 Artikel
  - Topic_3 (Training & Development): 8 Artikel
  - Topic_4 (Organizational Change): 7 Artikel

Top Topics nach Sentiment:
  Topic_3 (Training & Development): 8 Artikel, Sentiment: +0.88
  Topic_0 (HR & Recruiting): 15 Artikel, Sentiment: +0.76
  Topic_1 (AI & Innovation): 20 Artikel, Sentiment: +0.42
  ...

[6/6] Erstelle Reports...
✓ Report gespeichert: data/output/llm_analysis_20251022_143022.xlsx

==============================================================================
  ZUSAMMENFASSUNG
==============================================================================
Analysierte Artikel: 50
Total Kommentare: 150
Durchschn. Sentiment: +0.456
LLM Model: bert

✅ Analyse abgeschlossen! Report: data/output/llm_analysis_20251022_143022.xlsx
```

### Schritt 3: Report öffnen

```bash
# Windows
start data\output\llm_analysis_20251022_143022.xlsx

# macOS
open data/output/llm_analysis_20251022_143022.xlsx
```

### Schritt 4: Insights interpretieren

**Frage:** Welche Artikel-Typen bekommen positives Feedback?

**Antwort aus Report:**
1. Öffne Sheet "Kategorien"
2. Sortiere nach "Avg_Sentiment" (absteigend)
3. → Top-Kategorien sehen!

**Beispiel-Ergebnis:**
```
1. Training: +0.82 → Mitarbeiter lieben Trainings-Ankündigungen!
2. HR: +0.65      → HR-News kommen gut an
3. IT: +0.42      → IT-Updates ok
4. Management: +0.15 → Management-News weniger beliebt
```

**Actionable Insights:**
- ✅ Mehr Training-Artikel veröffentlichen
- ✅ HR-Content funktioniert gut
- ⚠️ IT-Updates verständlicher schreiben
- ⚠️ Management-Kommunikation verbessern

---

## 🔧 Performance-Tipps

### Für viele Artikel (>100):

```bash
# Verwende Lexikon-Modus (schneller)
python main.py --input datei.xlsx --no-llm

# Oder: Erst ohne Scraping testen
python main.py --input datei.xlsx --no-scraping

# Oder: Verwende manuelle Topic-Anzahl (schneller als Auto-Optimierung)
python main.py --input datei.xlsx --manual-topics --num-topics 5
```

### Für wenige Artikel (<50):

```bash
# Verwende LLM + Auto-Clustering für beste Genauigkeit
python main.py --input datei.xlsx
```

---

## 📝 Eigene Kategorien hinzufügen

Bearbeite `config/settings.py`:

```python
CATEGORY_KEYWORDS = {
    'HR': ['mitarbeiter', 'personal', ...],
    'IT': ['software', 'hardware', ...],

    # Füge eigene Kategorie hinzu:
    'Sustainability': ['nachhaltigkeit', 'umwelt', 'green', 'co2', 'klimaschutz'],
    'Innovation': ['innovation', 'digital', 'transformation', 'ai', 'ki'],
}
```

Dann funktioniert die Kategorisierung automatisch mit deinen neuen Kategorien!

---

## 🆘 Troubleshooting

### "LLM Solution nicht verfügbar"
→ Stelle sicher, dass `LLM Solution/` Ordner existiert und `transformers` installiert ist

### "Keine Input-Datei gefunden"
→ Lege Excel-Datei in `data/input/` ab oder verwende `--input pfad`

### "Model Loading dauert zu lange"
→ Verwende `--no-llm` für Lexikon-Modus (schneller)

### "Scraping schlägt fehl"
→ Verwende `--no-scraping` falls URLs nicht erreichbar

---

## 🎯 Nächste Schritte

1. **Teste mit kleinem Datensatz** (10-20 Artikel)
2. **Prüfe Kategorisierung** - passe Keywords an wenn nötig
3. **Interpretiere Cluster** - welche Themen funktionieren?
4. **Skaliere** auf vollständigen Datensatz

**Viel Erfolg!** 🚀
