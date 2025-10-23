# Setup & Installation Scripts

This folder contains all setup scripts and installation guides for offline deployment.

---

## Quick Links

### BERTopic Installation
- **[BERTOPIC_OFFLINE_INSTALL.md](BERTOPIC_OFFLINE_INSTALL.md)** - Complete offline installation guide
- **[BERTOPIC_QUICK_START.md](BERTOPIC_QUICK_START.md)** - Quick setup guide
- **[BERTOPIC_DOWNLOAD_ZIP.md](BERTOPIC_DOWNLOAD_ZIP.md)** - How to download packages

### Abstractive Summarization
- **[ABSTRACTIVE_SUMMARIZATION.md](ABSTRACTIVE_SUMMARIZATION.md)** - Complete guide for mBART setup

### Model Downloads
- **[MANUAL_MODEL_DOWNLOAD.md](MANUAL_MODEL_DOWNLOAD.md)** - Manual model installation

---

## Scripts

### BERTopic Setup

**`setup_bertopic_offline.py`**
- Downloads BERTopic packages for macOS/Linux
- Creates offline installation package
- Usage: `python setup_bertopic_offline.py`

**`setup_bertopic_offline_windows.py`**
- Downloads BERTopic packages for Windows
- Creates Python 3.12 compatible package
- Usage: `python setup_bertopic_offline_windows.py`

**`install_bertopic_offline.sh`**
- Shell script for offline BERTopic installation
- Usage: `./install_bertopic_offline.sh`

---

### Abstractive Summarization

**`download_mbart_model.py`**
- Downloads mBART-large-50 model (~2.4 GB)
- For abstractive summarization
- Usage: `python download_mbart_model.py`

**`package_mbart_model.py`**
- Packages mBART model for GitHub Release
- Creates ZIP for offline distribution
- Usage: `python package_mbart_model.py`

---

## Installation Flow

### Standard Setup (Extractive Summarization)

```bash
# 1. Install BERTopic
python setup_bertopic_offline.py  # or setup_bertopic_offline_windows.py

# 2. Install from packages
cd offline_packages/bertopic
pip install --no-index --find-links . bertopic sentence-transformers umap-learn hdbscan

# 3. Done! Use extractive summarization
python main_bertopic.py --input data.json
```

---

### Advanced Setup (Abstractive Summarization)

```bash
# 1. Install BERTopic (same as above)
python setup_bertopic_offline.py

# 2. Download mBART model
python setup/download_mbart_model.py

# 3. Use abstractive summarization
python main_bertopic.py --input data.json --abstractive
```

---

## Offline Distribution

### For Repository Maintainers

**Create BERTopic Offline Packages:**
```bash
# macOS/Linux
python setup_bertopic_offline.py

# Windows
python setup_bertopic_offline_windows.py

# Upload to GitHub Release
gh release upload v1.0-bertopic-offline bertopic-offline-packages*.zip
```

**Create mBART Offline Package:**
```bash
# Download model
python download_mbart_model.py

# Package for distribution
python package_mbart_model.py

# Create release
gh release create v1.0-abstractive \
  --title "Abstractive Summarization (mBART)" \
  offline_packages/mbart-large-50-model.zip
```

---

## GitHub Releases

### Current Releases

**v1.0-bertopic-offline**
- BERTopic packages for Windows/macOS/Linux
- Python 3.9+ and Python 3.12 compatible
- Size: 750 MB - 1.8 GB
- [Download](https://github.com/dallmi/SentimentAnalysis/releases/tag/v1.0-bertopic-offline)

**v1.0-abstractive** (Coming Soon)
- mBART-large-50 model for abstractive summarization
- 50+ languages including German
- Size: ~2.4 GB
- [Download](https://github.com/dallmi/SentimentAnalysis/releases/tag/v1.0-abstractive)

---

## Troubleshooting

See:
- [BERTOPIC_OFFLINE_INSTALL.md](BERTOPIC_OFFLINE_INSTALL.md#troubleshooting)
- [ABSTRACTIVE_SUMMARIZATION.md](ABSTRACTIVE_SUMMARIZATION.md#troubleshooting)
- [../TROUBLESHOOTING.md](../TROUBLESHOOTING.md)

---

## Support

For issues or questions:
1. Check documentation in this folder
2. Review main [README.md](../README.md)
3. Check [TROUBLESHOOTING.md](../TROUBLESHOOTING.md)

---

**Last Updated:** 2025-10-23
