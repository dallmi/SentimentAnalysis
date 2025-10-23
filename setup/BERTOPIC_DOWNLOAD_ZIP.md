# BERTopic Offline Packages - ZIP Download Guide

**Für Corporate Environments ohne `git clone` Zugriff**

## Problem
In vielen Corporate Environments ist `git clone` blockiert. Normales "Download ZIP" von GitHub funktioniert nicht mit Git LFS Dateien (du bekommst nur kleine Pointer-Dateien statt der echten Modelle).

## Lösung: ZIP mit echten Dateien herunterladen

### Option 1: Direkter ZIP Download von GitHub (Empfohlen)

**Lade die richtige Version für dein Betriebssystem:**

#### Für Windows (Python 3.9+):
1. **Lade herunter:** `bertopic-offline-packages-WINDOWS.zip` (900 MB)
2. **Entpacke auf Windows PC**
3. **Installiere:**
   ```cmd
   cd offline_packages\bertopic_windows
   pip install --no-index --find-links . bertopic sentence-transformers umap-learn hdbscan
   ```

   **Oder doppelklicke:** `install_bertopic_offline_windows.bat`

#### Für macOS / Linux (Python 3.9+):
1. **Lade herunter:** `bertopic-offline-packages.zip` (783 MB)
2. **Entpacke auf deinem Mac/Linux PC:**
   ```bash
   unzip bertopic-offline-packages.zip
   ```
3. **Installiere:**
   ```bash
   cd offline_packages/bertopic
   pip install --no-index --find-links . bertopic sentence-transformers umap-learn hdbscan
   ```

### Option 2: Gesamtes Repository als ZIP (Fallback)

Falls Releases nicht zugänglich sind:

1. **Lade das komplette Repo inkl. ZIP:**
   - Klicke auf GitHub: "Code" → "Download ZIP"
   - Entpacken
   - In `SentimentAnalysis/` findest du `bertopic-offline-packages.zip`
   - Entpacke auch diese Datei

2. **Installiere wie oben beschrieben**

## Was ist enthalten?

**55 Python Packages (Wheels):**
- bertopic 0.17.3
- sentence-transformers 5.1.2
- umap-learn 0.5.9
- hdbscan 0.8.40
- torch 2.2.2
- transformers 4.57.1
- numpy, scipy, scikit-learn, pandas
- und alle weiteren Dependencies

**2 Pre-trained Models (multilingual):**
- `all-MiniLM-L6-v2` - Schnelles Englisch-Modell (90 MB)
- `paraphrase-multilingual-MiniLM-L12-v2` - Multilingual (50+ Sprachen inkl. Deutsch) (420 MB)

**Gesamtgröße:** 783 MB (komprimiert) → 857 MB (entpackt)

## Nutzung mit BERTopic

```python
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

# Lade multilinguales Modell (offline)
embedding_model = SentenceTransformer('offline_packages/models/paraphrase-multilingual-MiniLM-L12-v2')

# Erstelle BERTopic
topic_model = BERTopic(embedding_model=embedding_model, language='multilingual')

# Analysiere deutsche Texte
docs = ["KI-Tools verbessern Produktivität", "Neue Software kommt gut an"]
topics, probs = topic_model.fit_transform(docs)
```

## Unterstützte Sprachen

Das multilingual Modell unterstützt 50+ Sprachen:
- 🇩🇪 Deutsch
- 🇬🇧 Englisch
- 🇫🇷 Französisch
- 🇪🇸 Spanisch
- 🇮🇹 Italienisch
- 🇵🇱 Polnisch
- 🇷🇺 Russisch
- 🇨🇳 Chinesisch
- 🇯🇵 Japanisch
- und 40+ weitere

## Troubleshooting

**ZIP kann nicht heruntergeladen werden (zu groß):**
- Verwende einen Download Manager (z.B. Free Download Manager)
- Oder kontaktiere deinen IT-Admin für alternative Übertragungswege (File Share, USB)

**Installation schlägt fehl:**
- Stelle sicher, dass du Python 3.9+ hast
- Prüfe, ob alle Wheels für deine Plattform passen (aktuell: macOS x86_64)
- Für Windows/Linux: Lade die Packages neu mit `setup_bertopic_offline.py` auf dem Ziel-OS

**Modelle werden nicht gefunden:**
- Stelle sicher, dass du den vollständigen Pfad zum Modell angibst
- Beispiel: `SentenceTransformer('/full/path/to/offline_packages/models/paraphrase-multilingual-MiniLM-L12-v2')`

## Support

Bei Fragen siehe auch:
- [BERTOPIC_OFFLINE_INSTALL.md](BERTOPIC_OFFLINE_INSTALL.md) - Komplette Installation
- [BERTOPIC_QUICK_START.md](BERTOPIC_QUICK_START.md) - Schnellstart Guide
