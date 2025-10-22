# Quickstart: Article Analysis with LLM

## 🎯 Your Goal

Analyze and understand URLs from News & Events articles:
- **Which article types receive positive feedback?**
- **Which article types receive negative feedback?**

## 📊 1. Prepare Excel File

Create an Excel file with 2 columns:

```
Column A (URL)                             | Column B (Comment)
-------------------------------------------|---------------------------
https://intranet.firma.de/artikel/123      | Great article!
https://intranet.firma.de/artikel/123      | Very helpful
https://intranet.firma.de/artikel/456      | Not clear
https://intranet.firma.de/artikel/789      | Excellent!
```

**Save the file in:**
```
data/input/meine_artikel.xlsx
```

## 🚀 2. Start Analysis

### In Corporate Environment (Windows):

```cmd
cd P:\IMPORTANT\Projects\SentimentAnalysis
python main.py --input data/input/meine_artikel.xlsx
```

### Two Modes:

#### Mode 1: Auto-Optimized (Silhouette Score) - DEFAULT ⭐⭐⭐

```bash
# Automatically finds optimal number of topics (DEFAULT!)
python main.py --input data/input/meine_artikel.xlsx
```

→ Tests k=2 to k=10 clusters
→ Selects optimal k with Silhouette Score
→ **BEST QUALITY** - recommended for most use cases
→ Duration: ~1-2 minutes for 100 articles

#### Mode 2: Manual Number of Topics

```bash
# Uses fixed number of topics (faster)
python main.py --input data/input/meine_artikel.xlsx --manual-topics --num-topics 7
```

→ Faster (~30 seconds)
→ Good if you already know the optimal k

#### Mode 3: Predefined Categories

```bash
# Uses 10 predefined content topics
python main.py --input data/input/meine_artikel.xlsx --use-predefined
```

→ Categories: Employee Stories, AI & Innovation, Events & Networking, etc.
→ Good for consistent quarterly reports

**See [CATEGORIZATION_MODES.md](CATEGORIZATION_MODES.md) for details on both modes!**

### Additional Options:

```bash
# Use fixed number of topics (7) - faster
python main.py --input data/input/meine_artikel.xlsx --manual-topics --num-topics 7

# Fast mode (Lexicon instead of LLM - lower accuracy)
python main.py --input data/input/meine_artikel.xlsx --no-llm

# Without web scraping (comment analysis only)
python main.py --input data/input/meine_artikel.xlsx --no-scraping
```

**💡 New Defaults:**
- **Auto-optimization is now default!** Automatically finds optimal number of topics (k=2 to k=10)
- Uses Silhouette Score for best clustering quality
→ See [CLUSTER_OPTIMIZATION.md](CLUSTER_OPTIMIZATION.md) for details

## 📈 3. Open Results

The analysis creates an Excel file:
```
data/output/llm_analysis_20251022_143022.xlsx
```

**Open this file:**
```cmd
start data\output\llm_analysis_20251022_143022.xlsx
```

## 📊 4. Interpret Results

### Sheet "Kategorien" - **Most Important View!**

Here you see the answer to your question about **content topics** (not departments!):

| Content Theme | Avg_Sentiment | Anzahl_Artikel | Positive_Kommentare | Negative_Kommentare |
|---------------|---------------|----------------|---------------------|---------------------|
| Employee Stories | +0.88 | 15 | 142 | 5 |
| Events & Networking | +0.75 | 20 | 158 | 18 |
| Wellness & Benefits | +0.68 | 12 | 95 | 12 |
| Learning & Development | +0.62 | 18 | 120 | 25 |
| AI & Innovation | +0.45 | 25 | 145 | 48 |
| Product News | +0.38 | 22 | 125 | 58 |
| Culture & Values | +0.35 | 10 | 65 | 35 |
| Business & Success | +0.22 | 8 | 45 | 30 |
| Organizational Change | -0.15 | 12 | 35 | 75 |
| CSR & Sustainability | +0.55 | 8 | 52 | 12 |

**Interpretation:**
- ✅ **Employee Stories** work excellently! (+0.88)
- ✅ **Events & Networking** are very well received (+0.75)
- ✅ **Wellness & Benefits** are received positively (+0.68)
- ✅ **Learning & Development** is popular (+0.62)
- ⚠️ **AI & Innovation** is okay, could be more understandable (+0.45)
- ⚠️ **Organizational Change** generates negative reactions (-0.15)

### Sheet "Clusters" - Detailed Topic Groups

| Cluster | Avg_Sentiment | Anzahl_Artikel |
|---------|---------------|----------------|
| Employee Stories_interview | +0.92 | 8 |
| Events & Networking_hackathon | +0.85 | 12 |
| Wellness & Benefits_sport | +0.72 | 10 |
| AI & Innovation_chatgpt | +0.48 | 15 |
| Organizational Change_restructuring | -0.28 | 5 |

**Interpretation:**
- Employee interviews work excellently
- Hackathon announcements are very well received
- Sport & Wellness events are received positively
- ChatGPT/AI topics generate mixed reactions
- Restructuring news generates negative reactions

### Sheet "Artikel" - All Articles in Detail

Complete list with:
- URL
- Title
- Category
- Cluster
- Average Sentiment
- Number of comments (positive/negative/neutral)

### Sheet "Insights" - Top & Worst Articles

- **Top 5 Articles** with best feedback
- **Worst 5 Articles** with worst feedback

## 🎯 Actionable Insights

Based on the results you can:

1. **Publish more of well-performing article types**
2. **Improve or avoid poorly rated article types**
3. **Identify specific topics** that are well/poorly received
4. **Adjust content strategy**

## ⚙️ Add Your Own Content Topics

Edit [config/settings.py](config/settings.py):

```python
CATEGORY_KEYWORDS = {
    # Existing content themes (English names, multilingual keywords)
    'AI & Innovation': [
        # English (primary)
        'artificial intelligence', 'ai', 'machine learning', 'chatgpt',
        # German (secondary)
        'künstliche intelligenz', 'ki', 'digitalisierung',
        # French/Italian (tertiary)
        'intelligence artificielle', 'intelligenza artificiale'
    ],

    'Employee Stories': [
        'employee', 'story', 'interview',  # English
        'mitarbeiter', 'kollege', 'geschichte',  # German
        'employé', 'dipendente'  # French, Italian
    ],

    # Add your own content theme:
    'Customer Success': [
        # English (primary)
        'customer', 'client', 'success story', 'case study', 'testimonial',
        # German (secondary)
        'kunde', 'erfolgsgeschichte', 'referenz', 'anwendungsfall',
        # French/Italian (tertiary)
        'client', 'cliente', 'cas d\'usage'
    ],

    'Remote Work': [
        'remote work', 'work from home', 'wfh', 'hybrid',  # English
        'homeoffice', 'remote arbeit', 'hybrid arbeiten',  # German
        'télétravail', 'lavoro remoto'  # French, Italian
    ],
}
```

**Important:**
- Category names in **English** (consistent across all languages)
- Keywords: **English primary**, German secondary, French/Italian tertiary
- Keywords match the **content/topic**, not the department!

## 🔧 Performance Tips

### First Use (~60s Model Loading):
```
[3/6] Sentiment-Analyse der Kommentare...
Lade LLM Model (kann ~60s dauern)...
✓ LLM Model geladen (Mode: bert)
```
→ **Normal!** The model is loaded only once.

### Many Articles (>100):
```bash
# Use lexicon mode (10x faster)
python main.py --input datei.xlsx --no-llm
```

### URLs Not Reachable:
```bash
# Skip web scraping (comment analysis only)
python main.py --input datei.xlsx --no-scraping
```

## 📝 Complete Documentation

- **USAGE_GUIDE.md** - Comprehensive guide with all options
- **LLM Solution/CORPORATE_DEPLOYMENT.md** - Setup guide for corporate environment
- **LLM Solution/README.md** - Technical details about the LLM model

## 🆘 Troubleshooting

### "No input file found"
→ Place Excel file in `data/input/`

### "LLM Solution not available"
→ Ensure that `LLM Solution/` folder exists and dependencies are installed

### "transformers not available"
→ Install dependencies:
```cmd
cd "P:\IMPORTANT\Projects\SentimentAnalysis\LLM Solution"
python -m pip install --no-index --find-links=wheels transformers torch
```

### "Scraping fails"
→ Use `--no-scraping` if URLs are not reachable

## ✅ Summary

**Input:**
```
Excel with URLs + Comments
```

**Command:**
```bash
python main.py --input data/input/meine_artikel.xlsx
```

**Output:**
```
Excel Report with answer to:
"Which article types have positive/negative feedback?"
```

**Result:**
```
Sheet "Kategorien" → Sorted by Avg_Sentiment
→ Top categories = Best article types!
```

---

**Let's go! 🚀**

Place your Excel file in `data/input/` and start the analysis!
