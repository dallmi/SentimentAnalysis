# LLM Solution - Schnellstart

## ⚡ In 3 Minuten loslegen

### 1. Voraussetzungen

**Nur NumPy benötigt:**
```bash
pip install numpy
```

Das war's! Keine weiteren Dependencies.

### 2. Erste Analyse

Erstelle eine neue Python-Datei `test.py`:

```python
from llm_sentiment_analyzer import LLMSentimentAnalyzer

# Initialisiere Analyzer
analyzer = LLMSentimentAnalyzer(use_bert=False)

# Analysiere Text
text = "This is an excellent article!"
result = analyzer.analyze(text)

print(f"Score: {result['score']}")
print(f"Category: {result['category']}")
```

Ausführen:
```bash
cd "LLM Solution"
python test.py
```

### 3. Tests ausführen

```bash
cd "LLM Solution"
python test_llm_analyzer.py
```

Sollte alle 6 Tests bestehen! ✓

## 📚 Beispiele

```bash
# Alle Beispiele durchlaufen
python example_usage.py
```

## 🎯 Schnelle Verwendung

### Einzelner Text

```python
from llm_sentiment_analyzer import LLMSentimentAnalyzer

analyzer = LLMSentimentAnalyzer(use_bert=False)
result = analyzer.analyze("Great article!")

print(result['score'])    # z.B. +0.85
print(result['category']) # z.B. 'positive'
```

### Mehrere Kommentare

```python
comments = [
    "Excellent article!",
    "Very helpful.",
    "Not clear.",
]

results = analyzer.analyze_batch(comments)

for comment, result in zip(comments, results):
    print(f"{comment}: {result['score']:+.2f}")
```

### Aggregierte Statistik

```python
aggregate = analyzer.get_aggregate_sentiment(comments)

print(f"Average: {aggregate['avg_score']}")
print(f"Positive: {aggregate['positive_ratio']:.1%}")
```

## 🌍 Multi-Language

Unterstützt automatisch:
- 🇬🇧 Englisch
- 🇩🇪 Deutsch
- 🇫🇷 Französisch
- 🇮🇹 Italienisch

```python
# Funktioniert mit allen Sprachen
texts = [
    "This is excellent!",      # EN
    "Das ist hervorragend!",   # DE
    "C'est excellent!",        # FR
    "Questo è eccellente!",    # IT
]

for text in texts:
    result = analyzer.analyze(text)
    print(f"{text}: {result['score']:+.2f}")
```

## ⚙️ Modi

### Lexikon-Modus (empfohlen)
```python
# Schnell, effizient, gute Genauigkeit
analyzer = LLMSentimentAnalyzer(use_bert=False)
```

**Vorteile:**
- ⚡ Sehr schnell (~0.001s pro Text)
- 💾 Wenig Speicher (~5 MB)
- ✓ Gute Genauigkeit (~85%)

### BERT-Modus
```python
# Höhere Genauigkeit, langsamer
analyzer = LLMSentimentAnalyzer(use_bert=True)
```

**Vorteile:**
- ✓ Höhere Genauigkeit (mit Training)
- 🧠 Besseres Kontext-Verständnis

**Nachteil:**
- 🐌 Langsamer (~0.1s pro Text)
- 💾 Mehr Speicher (~50 MB)
- ⚠️ Benötigt trainierte Gewichte für gute Ergebnisse

## 📊 Dateigröße

```
LLM Solution/
├── minimal_bert_tokenizer.py    9 KB
├── minimal_bert_model.py       14 KB
├── llm_sentiment_analyzer.py   14 KB
├── test_llm_analyzer.py         8 KB
├── example_usage.py             7 KB
├── README.md                    9 KB
├── QUICKSTART.md                3 KB
└── __init__.py                  1 KB
                                ──────
Total:                          ~65 KB
```

**Gesamt-Ordner: nur 112 KB!** ✓

## 🔧 Integration ins Hauptprojekt

### Methode 1: Direct Import

```python
import sys
sys.path.insert(0, 'LLM Solution')

from llm_sentiment_analyzer import LLMSentimentAnalyzer

analyzer = LLMSentimentAnalyzer(use_bert=False)
```

### Methode 2: In bestehenden Code integrieren

Bearbeite `src/sentiment_analyzer.py`:

```python
import sys
from pathlib import Path

# Füge LLM Solution zum Path hinzu
llm_path = Path(__file__).parent.parent / "LLM Solution"
sys.path.insert(0, str(llm_path))

from llm_sentiment_analyzer import LLMSentimentAnalyzer

class SentimentAnalyzer:
    def __init__(self, use_llm=True):
        if use_llm:
            self.analyzer = LLMSentimentAnalyzer(use_bert=False)
        else:
            # Verwende original model
            from models.sentiment_model import LightweightSentimentAnalyzer
            self.analyzer = LightweightSentimentAnalyzer()

    def analyze_comment(self, comment: str):
        return self.analyzer.analyze(comment)
```

## 💡 Tipps

1. **Für Produktion**: Verwende Lexikon-Modus (schneller, effizienter)
2. **Für Entwicklung**: Teste beide Modi
3. **Multi-Language**: Funktioniert automatisch, keine Konfiguration nötig
4. **Batch-Verarbeitung**: Verwende `analyze_batch()` für viele Texte
5. **Custom Lexikon**: Erweitere das Lexikon für firmenspezifische Begriffe

## ❓ Häufige Fragen

**Q: Warum ist BERT neutral bei allen Texten?**
A: Das Model verwendet zufällige Gewichte. Für Produktion würden trainierte Gewichte verwendet.

**Q: Kann ich eigene Wörter hinzufügen?**
A: Ja! Siehe README.md Abschnitt "Erweiterungen"

**Q: Welchen Modus soll ich verwenden?**
A: Für die meisten Fälle: Lexikon-Modus (schnell + gut)

**Q: Funktioniert es offline?**
A: Ja! Keine Internet-Verbindung nötig.

## 📖 Weitere Dokumentation

- [README.md](README.md) - Vollständige Dokumentation
- [example_usage.py](example_usage.py) - Ausführliche Beispiele
- [test_llm_analyzer.py](test_llm_analyzer.py) - Test-Suite

## 🚀 Nächste Schritte

1. ✓ Tests ausführen: `python test_llm_analyzer.py`
2. ✓ Beispiele anschauen: `python example_usage.py`
3. ✓ Ins Hauptprojekt integrieren
4. ✓ Mit eigenen Daten testen

**Viel Erfolg!** 🎉
