# Windows Dependency Wheels

## 📦 Was ist hier?

24 Windows-kompatible `.whl` Dateien (633 MB) für **offline Installation** von:
- `transformers` 4.57.1
- `torch` 2.8.0 (CPU-Version)
- Alle Dependencies

## ✅ Installation (Windows Corporate)

```cmd
cd "P:\IMPORTANT\Projects\SentimentAnalysis\LLM Solution"

# Installiere von diesen Wheels (kein Internet nötig!)
python -m pip install --no-index --find-links=wheels transformers torch
```

## 📋 Enthaltene Pakete:

- torch-2.8.0+cpu-cp39-cp39-win_amd64.whl (619 MB)
- transformers-4.57.1-py3-none-any.whl
- tokenizers-0.22.1-cp39-abi3-win_amd64.whl
- numpy-2.0.2-cp39-cp39-win_amd64.whl
- safetensors-0.6.2-cp38-abi3-win_amd64.whl
- + 19 weitere Dependencies

**Total: 633 MB**

## ⚠️ Wichtig:

Diese Wheels wurden für:
- **Windows 64-bit** (win_amd64)
- **Python 3.9** (cp39)
- **CPU-only** (kein GPU-Support)

Falls andere Python-Version, neu erstellen:
```bash
pip download transformers torch --platform win_amd64 --python-version 310 -d wheels/
```

## 🔄 Update Wheels:

```bash
# In privater Umgebung mit Internet
cd "LLM Solution"
rm -rf wheels/*.whl

# Neu downloaden
pip download transformers torch \
  --platform win_amd64 \
  --python-version 39 \
  --only-binary=:all: \
  --index-url https://download.pytorch.org/whl/cpu \
  -d wheels/
```

## 🚫 Nicht in Git committen

Diese Wheels sind zu groß für Git (633 MB).

**Alternativen:**
1. Auf USB-Stick kopieren
2. Via SharePoint/OneDrive teilen
3. Auf Corporate File-Server legen
4. Direkt in Corporate neu erstellen (siehe WINDOWS_SETUP.md)
