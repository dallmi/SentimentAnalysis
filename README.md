# Sentiment Analysis System for Corporate Intranet Articles

## Overview
Fully automated LLM-based sentiment analysis system for corporate intranet articles. The system analyzes article content, categorizes by content themes, performs unsupervised topic discovery, and evaluates comment sentiments using multilingual BERT models.

## Key Features
- **LLM-Powered Analysis**: BERT-based multilingual sentiment analysis (EN/DE/FR/IT)
- **Auto-Clustering**: Automatic topic discovery with Silhouette Score optimization (k=2-10)
- **Offline Deployment**: Fully offline capable - no HuggingFace API required
- **Content-Theme Categorization**: 10 predefined content categories (AI, HR, Culture, etc.)
- **Three Analysis Modes**: Auto-optimized, Manual, Predefined
- **Corporate Proxy Support**: Works in protected network environments
- **Excel I/O**: Simple import/export for business users

## Setup for Corporate Environment

### Step 1: Get the Repository into Your Corporate Network

#### Option A: Clone from GitHub (if allowed)

```bash
# If your corporate network allows GitHub access:
git clone https://github.com/dallmi/SentimentAnalysis.git
cd SentimentAnalysis
```

**If you have a corporate proxy:**
```bash
# Configure git to use proxy
git config --global http.proxy http://proxy.company.com:8080
git config --global https.proxy http://proxy.company.com:8080

# Then clone
git clone https://github.com/dallmi/SentimentAnalysis.git
```

#### Option B: Download as ZIP (if GitHub is blocked)

1. **On your personal computer:**
   - Go to https://github.com/dallmi/SentimentAnalysis
   - Click "Code" → "Download ZIP"
   - Extract the ZIP file

2. **Transfer to corporate environment:**
   - **Via USB stick**: Copy folder to USB, plug into corporate laptop
   - **Via email**: Zip and email to yourself (if allowed)
   - **Via file share**: Upload to corporate file server (e.g., SharePoint, network drive)
   - **Via cloud**: OneDrive/Dropbox if allowed in your organization

3. **On your corporate laptop:**
   ```bash
   # Navigate to where you transferred the files
   cd /path/to/SentimentAnalysis
   ```

#### Option C: Use Corporate Git Server (if available)

```bash
# If your company has internal GitLab/Bitbucket:
# 1. Fork/import the repo to your corporate git server
# 2. Clone from internal server
git clone https://git.company.com/your-username/SentimentAnalysis.git
```

---

### Step 2: Set Up Python Environment

#### Check Python version
```bash
python --version  # Should be 3.8 or higher
# Or try:
python3 --version
```

#### Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

---

### Step 3: Install Dependencies

#### Option A: Direct installation (if PyPI is allowed)

```bash
pip install -r requirements.txt
```

#### Option B: With corporate proxy

```bash
# Configure pip to use proxy
pip install --proxy http://proxy.company.com:8080 -r requirements.txt

# Or set environment variables (Windows)
set HTTP_PROXY=http://proxy.company.com:8080
set HTTPS_PROXY=http://proxy.company.com:8080
pip install -r requirements.txt

# Or set environment variables (macOS/Linux)
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
pip install -r requirements.txt
```

#### Option C: Use corporate Nexus/Artifactory

```bash
# If your company has an internal PyPI mirror:
pip install --index-url https://nexus.company.com/repository/pypi-all/simple -r requirements.txt
```

#### Option D: Offline installation (if no internet at all)

**On a machine WITH internet:**
```bash
# Download all packages
pip download -r requirements.txt -d packages/
```

**Transfer `packages/` folder to corporate laptop, then:**
```bash
# Install from local packages
pip install --no-index --find-links=packages/ -r requirements.txt
```

---

### Step 4: Download the BERT Model (~600MB)

#### Option A: Direct download (if HuggingFace is accessible)

```bash
python setup_offline_model.py
```

This downloads the BERT model and saves it locally in `models/`.

#### Option B: With corporate proxy

Edit `setup_offline_model.py` and add proxy configuration at the top:
```python
import os
os.environ['HTTP_PROXY'] = 'http://proxy.company.com:8080'
os.environ['HTTPS_PROXY'] = 'http://proxy.company.com:8080'
```

Then run:
```bash
python setup_offline_model.py
```

#### Option C: Manual download (if HuggingFace is blocked)

**On a machine WITH internet:**

1. Download the model manually:
   ```bash
   # Option 1: Using git-lfs
   git lfs install
   git clone https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment
   ```

   **Or download via browser:**
   - Go to: https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment/tree/main
   - Download all files (config.json, pytorch_model.bin, tokenizer_config.json, vocab.txt, etc.)

2. **Transfer to corporate laptop:**
   - Copy the entire `bert-base-multilingual-uncased-sentiment/` folder
   - Place it in `SentimentAnalysis/models/` directory

**On corporate laptop:**
```bash
# Verify model is in correct location
ls models/bert-base-multilingual-uncased-sentiment/
# Should show: config.json, pytorch_model.bin, vocab.txt, etc.
```

---

### Step 5: Configure for Corporate Network

#### Edit `config/settings.py`:

```python
# Proxy configuration (if needed for web scraping)
PROXY_CONFIG = {
    'http': 'http://proxy.company.com:8080',
    'https': 'http://proxy.company.com:8080'
}

# SSL Certificate verification
# Set to False for self-signed certificates (internal intranets only!)
VERIFY_SSL = False
```

---

### Step 6: Test Installation

```bash
# Create a test Excel file with 1-2 article URLs
# Save as: data/input/test.xlsx

# Run analysis
python main.py --input data/input/test.xlsx
```

---

## Quick Start (After Setup)

### 1. Installation

✅ **Already completed in Setup section above**

### 2. Usage

#### Standard: Auto-Optimized Topic Discovery (recommended)
```bash
python main.py --input data/input/my_articles.xlsx
```
→ Automatically tests k=2 to k=10 clusters and selects optimal k using Silhouette Score

#### Manual Number of Topics
```bash
python main.py --input data/input/my_articles.xlsx --manual-topics --num-topics 7
```

#### Predefined Content Categories
```bash
python main.py --input data/input/my_articles.xlsx --use-predefined
```

### 3. Input Format

Excel file with the following columns:
- **Column A**: Article URLs
- **Column B**: Comments
- Multiple comments per article possible (multiple rows)

### 4. Output

Generated files in `data/output/`:
- `results_TIMESTAMP.xlsx` - Detailed analysis with sentiments
- `summary_TIMESTAMP.xlsx` - Aggregated topic statistics
- `report_TIMESTAMP.html` - Interactive HTML report

## Documentation

Comprehensive documentation available:
- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide with all modes
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Detailed usage
- **[CLUSTER_OPTIMIZATION.md](CLUSTER_OPTIMIZATION.md)** - Silhouette Score deep-dive
- **[CATEGORIZATION_MODES.md](CATEGORIZATION_MODES.md)** - Supervised vs Unsupervised
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Error handling

## Architecture

### Project Structure
```
SentimentAnalysis/
├── main.py                          # Main program (LLM version)
├── setup_offline_model.py           # Offline model setup
├── config/
│   └── settings.py                  # Configuration (content themes, proxy)
├── src/
│   ├── data_loader.py               # Excel import
│   ├── web_scraper.py               # Article scraping
│   ├── article_categorizer.py       # Content-theme categorization
│   └── report_generator.py          # Report generation
├── LLM Solution/
│   ├── llm_sentiment_analyzer.py    # BERT sentiment analysis
│   ├── topic_discovery.py           # Unsupervised topic discovery
│   └── offline_sentiment_analyzer.py # Offline BERT wrapper
├── models/
│   └── bert-base-multilingual-uncased-sentiment/  # Local BERT model (~600MB)
├── data/
│   ├── input/                       # Input Excel files
│   └── output/                      # Generated reports
└── archive/
    ├── main_lightweight.py          # Old lightweight version
    ├── QUICKSTART.md                # Old documentation
    └── PROJECT_SUMMARY.md           # Old project overview
```

### Technology Stack
- **Sentiment Analysis**: nlptown/bert-base-multilingual-uncased-sentiment
- **Topic Discovery**: TF-IDF + K-Means Clustering + Silhouette Score
- **Languages**: German, English, French, Italian
- **Content-Theme Categories**: 10 predefined themes (AI & Innovation, Employee Stories, Culture & Values, Learning & Development, Events & Networking, Product News, Business & Success, Wellness & Benefits, Organizational Change, CSR & Sustainability)

## Content-Theme Categories

The system uses 10 predefined content themes with multilingual keywords:

1. **AI & Innovation** - AI, Machine Learning, Digitalization
2. **Employee Stories** - Employee portraits, success stories
3. **Culture & Values** - Company culture, values, diversity
4. **Learning & Development** - Training, education, skills
5. **Events & Networking** - Company events, team-building
6. **Product News** - Product launches, updates
7. **Business & Success** - Business results, milestones
8. **Wellness & Benefits** - Work-life balance, benefits
9. **Organizational Change** - Restructuring, new strategies
10. **CSR & Sustainability** - Sustainability, social responsibility

See details in [config/settings.py:36-164](config/settings.py#L36-L164)

## Cluster Optimization

The system uses Silhouette Score to automatically determine the optimal number of clusters:

- **Range**: k=2 to k=10
- **Metric**: Silhouette Score (-1 to +1)
- **Selection**: Highest score wins
- **Fallback**: Default k=5 if no clear optimization possible

More details in [CLUSTER_OPTIMIZATION.md](CLUSTER_OPTIMIZATION.md)

## Corporate Network Setup

### Proxy Configuration
In `config/settings.py`:
```python
PROXY_CONFIG = {
    'http': 'http://your-proxy:8080',
    'https': 'http://your-proxy:8080'
}
```

### Offline Operation
The system requires **no** internet connection after setup:
1. Models are downloaded once using `setup_offline_model.py`
2. All models are stored locally in `models/` (~600MB)
3. No HuggingFace API calls at runtime

## System Requirements

- **Python**: 3.8+
- **RAM**: At least 4GB (BERT model)
- **Disk**: ~1GB (models + dependencies)
- **Network**: Only for initial setup (then offline)

## Troubleshooting

### Common Issues

**"Model not found"**
```bash
python setup_offline_model.py  # Re-download model
```

**"Out of memory"**
→ Split large batches into smaller parts or allocate more RAM

**Proxy errors**
→ Configure proxy in `config/settings.py`

Complete troubleshooting: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## Performance

- **Sentiment Analysis**: ~10-20 articles/minute (depending on hardware)
- **Topic Discovery**: ~5-10 seconds for auto-optimization (k=2-10)
- **Total Runtime**: ~5-15 minutes for 100 articles with 500 comments

## License

Internal use - Corporate Intranet Analysis

---

**Version**: 2.0 (LLM-based with Auto-Clustering)
**Last Updated**: 2025-10-22
**Archived Version**: Lightweight version in `/archive/main_lightweight.py`
