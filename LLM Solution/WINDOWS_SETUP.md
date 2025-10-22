# Windows Setup Guide - Sentiment Analyzer

## 🪟 Spezielle Anleitung für Windows Corporate-Umgebung

### Problem: "Transformers nicht verfügbar"

Das bedeutet, die `transformers` Library ist nicht installiert.

---

## ✅ Schritt-für-Schritt Installation (Windows)

### 1. Prüfe Python Installation

```cmd
python --version
```

Sollte zeigen: `Python 3.8` oder höher

Falls nicht installiert:
- Download: https://www.python.org/downloads/
- Oder via Corporate Software Center

### 2. Prüfe pip

```cmd
python -m pip --version
```

### 3. Installiere Dependencies

#### Option A: Standard Installation (wenn Internet verfügbar)

```cmd
python -m pip install transformers torch
```

#### Option B: Corporate Proxy

```cmd
# Mit Proxy
python -m pip install --proxy http://proxy.firma.de:8080 transformers torch

# Oder mit Nexus
python -m pip install --index-url https://nexus.firma.de/repository/pypi-all/simple transformers torch
```

#### Option C: Ohne Internet (Offline Wheels)

Falls kein Internet/Nexus:

1. **In privater Umgebung** (mit Internet):
```bash
# Download alle Dependencies als Wheels
pip download transformers torch -d wheels/
```

2. **Kopiere `wheels/` Ordner** auf USB-Stick oder via Email

3. **In Corporate-Umgebung**:
```cmd
cd P:\path\to\wheels
python -m pip install --no-index --find-links=. transformers torch
```

---

## 🧪 Test nach Installation

```cmd
# Test ob transformers installiert ist
python -c "import transformers; print('✓ transformers verfügbar')"

# Test ob torch installiert ist
python -c "import torch; print('✓ torch verfügbar')"
```

Beide sollten erfolgreich sein!

---

## 🎯 Vollständiger Test

```cmd
cd "P:\IMPORTANT\Projects\SentimentAnalysis\LLM Solution"

# Vollständiger Test
python test_offline_model.py
```

### Erwartetes Ergebnis:

```
======================================================================
  TEST 1: Model Availability
======================================================================
✓ Model gefunden: sentiment-multilingual
  - Größe: 641.7 MB
  - Sprachen: en, de, fr, it, es

✓ 1 Model(s) verfügbar

======================================================================
  TEST 2: Offline Mode
======================================================================
✓ Analyzer initialisiert
  Modus: bert

✓ BERT Model erfolgreich geladen (offline)
```

---

## 🔧 Troubleshooting

### Problem 1: "pip nicht gefunden"

```cmd
# Installiere pip
python -m ensurepip --upgrade

# Oder verwende python -m pip statt pip
python -m pip install transformers torch
```

### Problem 2: SSL/Zertifikat-Fehler

```cmd
# Temporär SSL-Verifizierung deaktivieren
python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org transformers torch
```

### Problem 3: "Permission Denied"

```cmd
# Installiere nur für aktuellen User
python -m pip install --user transformers torch
```

### Problem 4: Alte pip-Version

```cmd
# Upgrade pip
python -m pip install --upgrade pip
```

### Problem 5: "HeaderTooLarge" beim Model laden

Das bedeutet die `.safetensors` Datei ist korrupt oder unvollständig.

**Lösung:**
```cmd
cd "P:\IMPORTANT\Projects\SentimentAnalysis"

# Lösche models/ Ordner
rmdir /s /q "LLM Solution\models"

# Git LFS prüfen und nochmal pullen
git lfs install
git lfs pull

# Oder: Model-Datei manuell neu laden
cd "LLM Solution\models\sentiment-multilingual"
del model.safetensors

# Neu von GitHub laden
git lfs pull
```

---

## 📦 Minimale Requirements

**Was wird benötigt:**

1. **Python 3.8+** (~50 MB)
2. **transformers** (~4 MB)
3. **torch** (~100-200 MB, CPU-Version)
4. **Model-Dateien** (~642 MB, bereits im Git)

**Gesamt: ~800 MB**

---

## 💡 Schnelltest (ohne volle Test-Suite)

```cmd
cd "P:\IMPORTANT\Projects\SentimentAnalysis\LLM Solution"

# Direkter Analyzer-Test
python -c "from offline_sentiment_analyzer import OfflineSentimentAnalyzer; a = OfflineSentimentAnalyzer(); result = a.analyze('This is excellent!'); print(f'Score: {result[\"score\"]}, Category: {result[\"category\"]}, Mode: {result[\"mode\"]}')"
```

**Erwartete Ausgabe:**
```
Score: 0.8, Category: positive, Mode: bert
```

Falls Mode: `lexicon` statt `bert` → transformers nicht richtig installiert oder Model nicht gefunden

---

## 🆘 Falls gar nichts funktioniert

### Fallback: Lexikon-Modus (ohne transformers)

Der Analyzer funktioniert auch ohne `transformers`, dann mit Lexikon-basierter Analyse:

```cmd
python -c "from llm_sentiment_analyzer import LLMSentimentAnalyzer; a = LLMSentimentAnalyzer(use_bert=False); print(a.analyze('Excellent article!'))"
```

**Vorteile Lexikon-Modus:**
- ✅ Keine transformers nötig
- ✅ Sehr schnell
- ✅ Keine großen Downloads
- ⚠️ Etwas geringere Genauigkeit (~75-85% statt ~90%)

---

## 📞 Hilfe anfordern

Bei Problemen, sende diese Info an Support:

```cmd
# System-Info sammeln
python --version > system_info.txt
python -m pip list >> system_info.txt
python -c "import sys; print(f'Python Path: {sys.executable}')" >> system_info.txt
python -c "import os; print(f'CWD: {os.getcwd()}')" >> system_info.txt

# Zeige Datei
type system_info.txt
```

---

## ✅ Erfolgreiche Installation checken

Nach Installation sollte das funktionieren:

```cmd
python -c "from offline_sentiment_analyzer import OfflineSentimentAnalyzer; a = OfflineSentimentAnalyzer(); print('✓ Setup erfolgreich!' if a.mode == 'bert' else '⚠ Fallback auf Lexikon-Modus')"
```

---

## 🎯 Nächste Schritte nach erfolgreicher Installation

Siehe: [CORPORATE_DEPLOYMENT.md](CORPORATE_DEPLOYMENT.md) für Integration in dein Projekt.

**Viel Erfolg!** 🚀
