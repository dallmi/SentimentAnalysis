# Sentiment Analysis with BERTopic for Corporate Intranet

**Automated sentiment analysis and topic discovery for corporate intranet articles with multilingual BERT embeddings.**

---

## Features

- **Automatic Topic Discovery**: BERTopic automatically finds content themes in your articles
- **Multilingual Support**: Analyzes German, English, and 50+ other languages
- **Comment Sentiment Analysis**: BERT-based sentiment analysis for all comments
- **Extractive Summarization**: Auto-generates 3-sentence summaries for each article
- **Emoji Ratings**: Stakeholder-friendly ratings (⭐⭐⭐⭐⭐ to ❌)
- **Offline Capable**: Works completely offline in corporate environments
- **Excel Output**: Easy-to-use Excel reports with multiple sheets

---

## Quick Start

### 1. Install BERTopic (Offline)

**Windows (Python 3.12):**
```cmd
# Download from GitHub Releases:
# https://github.com/dallmi/SentimentAnalysis/releases/tag/v1.0-bertopic-offline

# Extract and install
unzip bertopic-offline-packages-WINDOWS-PY312.zip
cd offline_packages\bertopic_windows_py312
pip install --no-index --find-links . bertopic sentence-transformers umap-learn hdbscan
```

**macOS/Linux:**
```bash
# Download from GitHub Releases
unzip bertopic-offline-packages.zip
cd offline_packages/bertopic
pip install --no-index --find-links . bertopic sentence-transformers umap-learn hdbscan
```

See [setup/BERTOPIC_OFFLINE_INSTALL.md](setup/BERTOPIC_OFFLINE_INSTALL.md) for detailed instructions.

---

### 2. Download BERT Models

Place your BERT models in the following location:
```
LLM Solution/models/
└── paraphrase-multilingual-MiniLM-L12-v2/
    ├── config.json
    ├── pytorch_model.bin
    ├── tokenizer_config.json
    └── vocab.txt
```

**Download from HuggingFace:**
- [paraphrase-multilingual-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)

Or use the download script:
```bash
cd "LLM Solution"
python download_model.py
```

---

### 3. Prepare Input Data

Create a JSON file with your articles:

**Format**: `data/input/article_content.json`

```json
[
  {
    "url": "https://intranet.company.com/article/123",
    "title": "New Home Office Policy 2025",
    "content": "The management has approved a new flexible work policy. Starting January 1st, 2025, all employees can work from home up to 3 days per week. The IT department will provide necessary equipment...",
    "comments": [
      {
        "text": "Great news! This will help with work-life balance.",
        "author": "John Doe",
        "date": "2024-12-15"
      },
      {
        "text": "I'm concerned about team collaboration.",
        "author": "Jane Smith",
        "date": "2024-12-16"
      }
    ]
  }
]
```

---

### 4. Run Analysis

```bash
python main_bertopic.py --input data/input/article_content.json
```

**Output**: Excel file with 3 sheets:
1. **Articles** - Article overview with topics, sentiment, ratings, and summaries
2. **Comments_Detail** - Individual comment sentiments
3. **Topic_Statistics** - Sentiment aggregated by topic

---

## Project Structure

```
SentimentAnalysis/
├── main_bertopic.py              # Main analysis script (NEW)
├── test_summarization.py         # Test extractive summarization
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── TROUBLESHOOTING.md            # Common issues
│
├── setup/                        # BERTopic installation guides
│   ├── BERTOPIC_OFFLINE_INSTALL.md
│   ├── BERTOPIC_QUICK_START.md
│   ├── setup_bertopic_offline.py
│   └── setup_bertopic_offline_windows.py
│
├── tools/                        # Data extraction tools
│   ├── extract_article_with_comments.js
│   ├── extract_clean_content.js
│   ├── EXTRACT_EVERYTHING_FROM_BROWSER.md
│   └── SIMPLE_WORKFLOW.md
│
├── scripts/                      # Utility scripts
│   ├── convert_articles_json.py
│   └── create_test_excel.py
│
├── LLM Solution/                 # Core analysis modules
│   ├── offline_sentiment_analyzer.py
│   ├── llm_sentiment_analyzer.py
│   └── models/                   # BERT models go here
│
├── data/
│   ├── input/                    # Your article_content.json files
│   └── output/                   # Generated Excel reports
│
└── old_version/                  # Archived old version
    ├── main.py                   # Old manual categorization version
    └── src/                      # Old architecture
```

---

## Excel Output

### Sheet 1: Articles
| URL | Title | Summary | Topic | Topic_ID | Avg_Sentiment | Rating | Total_Comments | Positive_Count | Negative_Count | Neutral_Count |
|-----|-------|---------|-------|----------|---------------|--------|----------------|----------------|----------------|---------------|
| ... | New Policy | The management has... | Work Policy | 2 | 0.654 | ⭐⭐⭐⭐⭐ Excellent | 45 | 32 | 8 | 5 |

### Sheet 2: Comments_Detail
| URL | Title | Topic | Comment | Comment_Sentiment | Sentiment_Score | Positive | Neutral | Negative | Author | Date |
|-----|-------|-------|---------|-------------------|-----------------|----------|---------|----------|--------|------|
| ... | ... | ... | Great news! | Positive | 0.889 | 1 | 0 | 0 | John | ... |

### Sheet 3: Topic_Statistics
| Topic | Total_Comments | Sentiment_Distribution | Avg_Sentiment_Score |
|-------|----------------|------------------------|---------------------|
| Work Policy | 127 | {Positive: 89, Neutral: 25, Negative: 13} | 0.432 |

---

## Features Explained

### 1. Automatic Topic Discovery (BERTopic)
BERTopic automatically discovers themes in your articles using:
- **BERT embeddings**: Semantic understanding of content
- **UMAP**: Dimensionality reduction
- **HDBSCAN**: Density-based clustering
- **c-TF-IDF**: Topic label generation

**Example Topics Found:**
- "home office policy remote work"
- "employee training development skills"
- "company culture values diversity"

### 2. Multilingual Sentiment Analysis
Uses `paraphrase-multilingual-MiniLM-L12-v2` for 50+ languages:
- German (DE)
- English (EN)
- French (FR)
- Italian (IT)
- Spanish (ES)
- And more...

### 3. Extractive Summarization
Selects the 3 most representative sentences from each article:
- Uses BERT embeddings for semantic similarity
- Finds sentences closest to document centroid
- Preserves original wording (no text generation)

### 4. Emoji Rating System
Converts sentiment scores to stakeholder-friendly ratings:
- ⭐⭐⭐⭐⭐ Excellent (≥0.6)
- ⭐⭐⭐⭐ Very Good (≥0.4)
- ⭐⭐⭐ Good (≥0.2)
- ⭐⭐ Fair (≥0.0)
- ⭐ Poor (≥-0.2)
- ❌ Very Poor (<-0.2)

---

## Data Extraction

### Option 1: Browser Console (Recommended)
Use our JavaScript extraction tools to get article data directly from your intranet:

```javascript
// In browser console on article page
// Copy from: tools/extract_article_with_comments.js
```

See [tools/EXTRACT_EVERYTHING_FROM_BROWSER.md](tools/EXTRACT_EVERYTHING_FROM_BROWSER.md) for full guide.

### Option 2: Manual JSON Creation
Create `article_content.json` manually with the format shown above.

---

## System Requirements

- **Python**: 3.9 or higher (3.12 recommended)
- **RAM**: 8GB minimum (16GB recommended)
- **Disk**: 2GB free space
- **OS**: Windows, macOS, or Linux

---

## Troubleshooting

### "Could not find a version that satisfies the requirement bertopic"
**Solution**: Make sure you're in the correct directory when installing:
```cmd
cd offline_packages\bertopic_windows_py312
pip install --no-index --find-links . bertopic
```

### "Model not found"
**Solution**: Check model path:
```bash
ls "LLM Solution/models/paraphrase-multilingual-MiniLM-L12-v2"
```

### "Out of memory"
**Solution**: Process fewer articles at a time or increase system RAM.

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more issues.

---

## Documentation

- **[setup/BERTOPIC_OFFLINE_INSTALL.md](setup/BERTOPIC_OFFLINE_INSTALL.md)** - Detailed BERTopic installation
- **[setup/BERTOPIC_QUICK_START.md](setup/BERTOPIC_QUICK_START.md)** - Quick setup guide
- **[tools/EXTRACT_EVERYTHING_FROM_BROWSER.md](tools/EXTRACT_EVERYTHING_FROM_BROWSER.md)** - Data extraction guide
- **[tools/SIMPLE_WORKFLOW.md](tools/SIMPLE_WORKFLOW.md)** - End-to-end workflow
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions

---

## Version History

### Version 3.0 (Current - BERTopic)
- ✅ Automatic topic discovery with BERTopic
- ✅ Extractive summarization with BERT embeddings
- ✅ Multilingual support (50+ languages)
- ✅ Emoji rating system
- ✅ Offline installation packages
- ✅ Sentiment aggregation per article

### Version 2.0 (Archived - in old_version/)
- Manual categories with BERT embeddings
- KMeans clustering
- Silhouette Score optimization

---

## License

Internal use - Corporate Intranet Analysis

---

## Support

For issues or questions:
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review documentation in `setup/` and `tools/` folders
3. Check old version in `old_version/` for reference

---

**Last Updated**: 2025-10-23
**Current Version**: 3.0 (BERTopic with Extractive Summarization)
