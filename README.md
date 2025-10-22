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

## Quick Start

### 1. Installation

#### Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
```

#### Install dependencies
```bash
pip install -r requirements.txt
```

#### Set up offline models (one-time)
```bash
python setup_offline_model.py
```
This downloads the BERT model (~600MB) and saves it locally in `models/`.

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
