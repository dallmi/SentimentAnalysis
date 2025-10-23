# Abstractive Summarization mit mBART-large-50

**Generiere neue, zusammengefasste Texte statt nur Sätze zu extrahieren**

---

## Überblick

**Extractive Summarization** (Standard):
- Kopiert die 3 wichtigsten Sätze aus dem Original
- Schnell und ressourcenschonend
- Verwendet keine zusätzlichen Modelle

**Abstractive Summarization** (Option 3):
- **Generiert neue Texte** die den Inhalt zusammenfassen
- Wie ein Mensch, der einen Text in eigenen Worten zusammenfasst
- Benötigt mBART-large-50 Modell (~2.4 GB)
- Unterstützt 50+ Sprachen inkl. Deutsch

---

## Installation

### Schritt 1: mBART Model herunterladen

**Option A: Mit Internet (empfohlen)**

```bash
cd setup
python download_mbart_model.py
```

Das Modell wird hier gespeichert:
```
LLM Solution/models/mbart-large-50/
```

**Option B: Offline Installation**

1. **Mit Internet:** Download von GitHub Release
   ```bash
   # Download mbart-large-50-model.zip from:
   # https://github.com/dallmi/SentimentAnalysis/releases/tag/v1.0-abstractive
   ```

2. **Transfer zur Corporate Workstation** (USB/Email/FileShare)

3. **Auf Corporate Laptop:**
   ```bash
   unzip mbart-large-50-model.zip
   mv mbart-large-50 "LLM Solution/models/"
   ```

4. **Verify Installation:**
   ```bash
   ls "LLM Solution/models/mbart-large-50"
   # Should show: config.json, pytorch_model.bin, etc.
   ```

---

## Verwendung

### Extractive Summarization (Standard)

```bash
python main_bertopic.py --input data/input/article_content.json
```

**Output:**
- Extrahiert 3 Originalsätze aus jedem Artikel
- Schnell (~1 Sekunde pro Artikel)

**Beispiel:**
```
Original: [10 Sätze über neue Homeoffice-Policy]

Summary: "Die Geschäftsführung hat eine neue Richtlinie für flexibles
Arbeiten verabschiedet. Ab dem 1. Januar 2025 können alle Mitarbeiter
bis zu drei Tage pro Woche von zu Hause arbeiten. Die IT-Abteilung
stellt die notwendige Hardware und Software zur Verfügung."
```

---

### Abstractive Summarization (mBART)

```bash
python main_bertopic.py --input data/input/article_content.json --abstractive
```

**Output:**
- Generiert **neue Texte** die den Inhalt zusammenfassen
- Langsamer (~5-10 Sekunden pro Artikel)
- Höhere Qualität und Lesbarkeit

**Beispiel:**
```
Original: [10 Sätze über neue Homeoffice-Policy]

Summary: "Das Unternehmen führt eine flexible Homeoffice-Regelung ein,
die Mitarbeitern erlaubt, bis zu drei Tage wöchentlich von zu Hause
zu arbeiten. Die IT unterstützt mit der nötigen Ausstattung."
```

---

## Vergleich

| Feature | Extractive | Abstractive |
|---------|------------|-------------|
| **Methode** | Sätze kopieren | Neuer Text generieren |
| **Geschwindigkeit** | ⚡ Schnell | 🐢 Langsamer |
| **Modell** | Keins nötig | mBART (~2.4 GB) |
| **Qualität** | ✓ Gut | ✓✓ Sehr gut |
| **Lesbarkeit** | ✓ OK | ✓✓ Besser |
| **Disk Space** | 0 MB | 2.4 GB |
| **Sprachen** | Alle | 50+ (DE, EN, FR, IT, ES) |

---

## Technische Details

### mBART-large-50

**Model:** facebook/mbart-large-50-many-to-many-mmt
**Type:** Sequence-to-sequence transformer
**Training:** Multilingual BART trained on 50 languages

**Supported Languages:**
- 🇩🇪 German (de_DE)
- 🇬🇧 English (en_XX)
- 🇫🇷 French (fr_XX)
- 🇮🇹 Italian (it_IT)
- 🇪🇸 Spanish (es_XX)
- ... und 45 weitere

**Parameters:**
- Model size: ~611M parameters
- Disk space: ~2.4 GB
- RAM requirement: ~4 GB during inference
- GPU: Optional (10x faster with GPU)

### Implementierung

Die abstractive Zusammenfassung verwendet:

```python
from abstractive_summarizer import AbstractiveSummarizer

summarizer = AbstractiveSummarizer()
summary = summarizer.summarize(
    text="Langer Artikel Text...",
    source_lang="de_DE",     # Deutsch
    max_length=100,          # Max 100 tokens
    min_length=30            # Min 30 tokens
)
```

**Beam Search Parameters:**
- `num_beams=4`: Mehr Beams = bessere Qualität
- `length_penalty=2.0`: >1.0 bevorzugt längere Summaries
- `early_stopping=True`: Stop when beams are done

---

## Offline Distribution Setup

### Für GitHub Release Maintainer

**1. Download Model:**
```bash
python setup/download_mbart_model.py
```

**2. Package for Distribution:**
```bash
python setup/package_mbart_model.py
```

**3. Create GitHub Release:**
```bash
gh release create v1.0-abstractive \
  --title "Abstractive Summarization (mBART-large-50)" \
  --notes "mBART-large-50 model for abstractive summarization" \
  offline_packages/mbart-large-50-model.zip
```

**4. Upload to Release:**
```bash
gh release upload v1.0-abstractive \
  offline_packages/mbart-large-50-model.zip
```

---

## Troubleshooting

### "Model not found"

**Problem:**
```
FileNotFoundError: Model not found at LLM Solution/models/mbart-large-50
```

**Solution:**
```bash
# Download model
python setup/download_mbart_model.py

# Or install from ZIP
unzip mbart-large-50-model.zip
mv mbart-large-50 "LLM Solution/models/"
```

---

### "Out of memory"

**Problem:**
```
RuntimeError: CUDA out of memory
```

**Solutions:**
1. **Reduce batch size** - Process fewer articles at once
2. **Use CPU instead of GPU**:
   ```python
   # In abstractive_summarizer.py, force CPU:
   self.device = "cpu"
   ```
3. **Close other applications** to free RAM
4. **Allocate more RAM** to your system/VM

---

### "Summarization is slow"

**Problem:** Abstractive summarization takes 10+ seconds per article

**Solutions:**
1. **Use GPU** if available (10x faster)
   - Requires: CUDA-enabled GPU + PyTorch with CUDA
2. **Use Extractive mode** instead:
   ```bash
   python main_bertopic.py --input data.json  # No --abstractive flag
   ```
3. **Reduce max_length**:
   ```python
   # In main_bertopic.py, reduce from 100 to 50 tokens
   summary = self.abstractive_summarizer.summarize(
       text, max_length=50  # Faster
   )
   ```

---

### "Wrong language in summary"

**Problem:** Summary is in English but article is German

**Solution:** Set correct source language:

```python
# In main_bertopic.py, line ~249
summary = self.abstractive_summarizer.summarize(
    combined_text,
    source_lang="de_DE",  # ← Ensure this is set correctly
    max_length=100,
    min_length=30
)
```

**Language Codes:**
- German: `de_DE`
- English: `en_XX`
- French: `fr_XX`
- Italian: `it_IT`
- Spanish: `es_XX`

---

## Performance

### Speed Comparison

**Extractive (BERT):**
- ~1 second per article
- 100 articles: ~2 minutes

**Abstractive (mBART):**
- ~5-10 seconds per article (CPU)
- ~0.5-1 second per article (GPU)
- 100 articles: ~10-15 minutes (CPU) / ~2-3 minutes (GPU)

### Quality Comparison

**Extractive:**
- ✓ Preserves original wording
- ✓ Factually accurate (just copies)
- ✗ Can be choppy/disconnected
- ✗ May miss context

**Abstractive:**
- ✓ Fluent, natural language
- ✓ Better context integration
- ✓ More concise
- ✗ Small risk of hallucination
- ✗ Requires more compute

---

## Empfehlung

**Verwende Extractive (Standard) wenn:**
- ✓ Geschwindigkeit wichtiger als Qualität
- ✓ Keine GPU verfügbar
- ✓ Wenig Disk Space (~2.4 GB gespart)
- ✓ Originalformulierungen wichtig

**Verwende Abstractive (--abstractive) wenn:**
- ✓ Beste Qualität gewünscht
- ✓ GPU verfügbar
- ✓ Genug Disk Space (2.4 GB)
- ✓ Natürliche Sprache wichtiger als Originaltreue

---

## System Requirements

**Minimum:**
- Python 3.9+
- 8 GB RAM
- 3 GB Disk Space
- CPU: Any modern processor

**Empfohlen:**
- Python 3.12
- 16 GB RAM
- 5 GB Disk Space
- GPU: NVIDIA with CUDA support (optional, but 10x faster)

---

## Weitere Ressourcen

- **mBART Paper:** [mBART: Denoising Sequence-to-Sequence Pre-training](https://arxiv.org/abs/2001.08210)
- **HuggingFace Model:** [facebook/mbart-large-50-many-to-many-mmt](https://huggingface.co/facebook/mbart-large-50-many-to-many-mmt)
- **GitHub Release:** [v1.0-abstractive](https://github.com/dallmi/SentimentAnalysis/releases/tag/v1.0-abstractive)

---

**Version:** 3.1 (Abstractive Summarization)
**Last Updated:** 2025-10-23
