# PERFORMANCE TRACKING HINZUGEFÜGT

## Zusammenfassung der Änderungen:

Ich habe **detaillierte Performance-Messung** zu allen kritischen Schritten hinzugefügt, um genau zu verstehen, wo die Zeit verloren geht.

---

## 🎯 Was du jetzt sehen wirst:

### 1. **Article Summaries - Progress Tracking**

Alle 5 Artikel siehst du:
```
Progress: 5/15 Artikel | Avg: 3.2s/Artikel | ETA: 6.4 Min
Progress: 10/15 Artikel | Avg: 3.1s/Artikel | ETA: 2.6 Min
```

**Was du daraus ablesen kannst:**
- Wie lange dauert EIN Artikel im Durchschnitt?
- Wie lange dauert es noch insgesamt? (ETA)
- Falls ein Artikel plötzlich 30s dauert statt 3s → **PROBLEM gefunden!**

---

### 2. **Topic Labels - Einzelne Zeitmessung**

Für jeden Topic siehst du:
```
🔍 Calling mBART for topic 0...
   Keywords: [('kudos', 0.123), ('technology', 0.098), ...]
   Docs: 3
   Generated label: 'Kudos & It & Ubs' (took 2.34s)
```

**Was du daraus ablesen kannst:**
- Wie lange dauert mBART für EIN Topic-Label?
- Falls es 60s dauert statt 2-3s → **PROBLEM bei mBART!**
- Falls Fallback ausgelöst wird → mBART generiert schlechte Outputs

---

### 3. **Comment Sentiment - Progress Tracking**

Alle 50 Kommentare siehst du:
```
Progress: 50/200 Kommentare | Avg: 45.3ms/Kommentar | ETA: 6.8s
Progress: 100/200 Kommentare | Avg: 44.1ms/Kommentar | ETA: 4.4s
```

**Was du daraus ablesen kannst:**
- Wie lange dauert EIN Kommentar im Durchschnitt? (sollte <100ms sein)
- Wie lange dauern 200 Kommentare insgesamt?
- Falls plötzlich 500ms/Kommentar → **PROBLEM beim BERT Model!**

---

### 4. **FINALE PERFORMANCE-ZUSAMMENFASSUNG**

Am Ende siehst du:
```
⏱️  PERFORMANCE BREAKDOWN:
   Gesamtzeit: 12.3 Minuten (738.5s)
   └─ Article Summaries: 450.2s (3.0s/Artikel, 15 Artikel)
   └─ Topic Labels: 23.4s (5.9s/Topic, 4 Topics)
   └─ Comment Sentiment: 8.8s (44ms/Kommentar, 200 Kommentare)
```

**Was du daraus ablesen kannst:**
- **WO geht die meiste Zeit verloren?**
  - Artikel Summaries? → mBART ist langsam oder Artikel sind sehr lang
  - Topic Labels? → mBART-Generierung dauert zu lange
  - Comment Sentiment? → BERT Model ist langsam oder zu viele Kommentare
  - **FEHLT ZEIT?** → BERTopic Clustering oder andere Steps nicht gemessen

---

## 📊 Beispiel-Analyse bei 1 Stunde für 15 Artikel:

Wenn die Analyse 60 Minuten dauert, siehst du z.B.:

```
⏱️  PERFORMANCE BREAKDOWN:
   Gesamtzeit: 60.0 Minuten (3600s)
   └─ Article Summaries: 2400s (160s/Artikel, 15 Artikel)  ← 40 Minuten!!! ❌
   └─ Topic Labels: 120s (30s/Topic, 4 Topics)              ← 2 Minuten
   └─ Comment Sentiment: 180s (900ms/Kommentar, 200 Kommentare)  ← 3 Minuten
```

**Analyse:**
- **Article Summaries nehmen 40 Minuten** → Das ist das Problem!
  - Normalerweise: 3-5s/Artikel = 45-75s für 15 Artikel
  - Hier: 160s/Artikel = **53x langsamer als erwartet!**
  - **Mögliche Ursachen:**
    - mBART läuft auf CPU statt GPU
    - Artikel sind extrem lang (>5000 Wörter)
    - max_length=350 ist zu hoch
    - mBART Model ist beschädigt

---

## 🔍 Was du JETZT tun musst:

### SCHRITT 1: Führe die Analysis erneut aus
```cmd
cd "P:\IMPORTANT\Projects\SentimentAnalysis"
python main_bertopic.py --input "artikel_ueberarbeitet\articles_with_comments.json" --output "data\output\sentiment_analysis.xlsx" --abstractive
```

### SCHRITT 2: Achte auf die Progress-Meldungen

**Während der Ausführung:**
- Bei Artikel 5: Schau dir die "Avg: X.Xs/Artikel" an
  - **Normal:** 2-5s/Artikel
  - **Langsam:** 10-30s/Artikel → CPU-bound, kein GPU
  - **SEHR LANGSAM:** >60s/Artikel → **PROBLEM!**

- Bei Topic Labels: Schau dir "took X.XXs" an
  - **Normal:** 2-5s/Topic
  - **Langsam:** 10-20s/Topic
  - **SEHR LANGSAM:** >30s/Topic → **PROBLEM!**

- Bei Kommentaren: Schau dir "Avg: Xms/Kommentar" an
  - **Normal:** 30-100ms/Kommentar
  - **Langsam:** 200-500ms/Kommentar
  - **SEHR LANGSAM:** >1000ms/Kommentar → **PROBLEM!**

### SCHRITT 3: Kopiere die FINALE PERFORMANCE-ZUSAMMENFASSUNG

Am Ende der Ausführung siehst du:
```
⏱️  PERFORMANCE BREAKDOWN:
   Gesamtzeit: ...
   └─ Article Summaries: ...
   └─ Topic Labels: ...
   └─ Comment Sentiment: ...
```

**Schicke mir diese Ausgabe!**

---

## 💡 Erwartete Performance (für Vergleich):

### **MIT mBART (--abstractive):**
- Artikel Summaries: **3-5s pro Artikel** (CPU), 0.5-1s (GPU)
- Topic Labels: **2-5s pro Topic** (CPU), 0.5-1s (GPU)
- Comment Sentiment: **50-100ms pro Kommentar**

**15 Artikel, 4 Topics, 200 Kommentare:**
- Summaries: 45-75s
- Labels: 8-20s
- Comments: 10-20s
- **GESAMT: ~2-3 Minuten** (plus BERTopic Clustering ~10-30s)

### **OHNE mBART (extractive):**
- Artikel Summaries: **0.1-0.3s pro Artikel**
- Topic Labels: **instant** (nur Top 3 Keywords)
- Comment Sentiment: **50-100ms pro Kommentar**

**15 Artikel, 4 Topics, 200 Kommentare:**
- Summaries: 1.5-4.5s
- Labels: <1s
- Comments: 10-20s
- **GESAMT: ~30-60 Sekunden**

---

## 🚨 Wenn 1 Stunde für 15 Artikel:

Das bedeutet **50-100x langsamer als erwartet**!

Mögliche Ursachen:
1. **mBART läuft auf CPU** (sollte auf GPU laufen für 10x Speedup)
2. **Artikel sind EXTREM lang** (>10.000 Wörter pro Artikel)
3. **max_length=350 ist zu hoch** (versuche 100-150)
4. **mBART Model ist beschädigt** (re-download erforderlich)
5. **System ist extrem langsam** (CPU-Auslastung prüfen)

**Mit der neuen Performance-Messung sehen wir GENAU was das Problem ist!** 🎯
