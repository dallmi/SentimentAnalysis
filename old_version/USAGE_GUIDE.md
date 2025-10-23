# Usage Guide - Article Analysis with LLM

## 🎯 Your Use Case

You want to:
1. ✅ Analyze URLs from News & Events articles
2. ✅ Understand and categorize article content
3. ✅ Analyze comments (Sentiment)
4. ✅ Find correlation: Which article types → positive/negative feedback
5. ✅ Cluster articles (group similar articles)

## 📊 Input Format

### Prepare Excel file:

```
Column A (URL)                             | Column B (Comment)
-------------------------------------------|---------------------------
https://intranet.firma.de/artikel/123      | Great article, very helpful!
https://intranet.firma.de/artikel/123      | Thanks for sharing
https://intranet.firma.de/artikel/456      | Not clear, confusing
https://intranet.firma.de/artikel/456      | Could be better explained
https://intranet.firma.de/artikel/789      | Excellent overview!
```

**Important:**
- Multiple rows per article possible (for multiple comments)
- URLs are automatically grouped
- Comments are aggregated per article

### Storage location:

```
data/input/your_articles.xlsx
```

---

## 🚀 Usage

### Option 1: Standard (Auto-Optimized) - ⭐ RECOMMENDED

```bash
python main.py --input data/input/your_articles.xlsx
```

**What happens:**
1. Loads Excel file
2. Scrapes article content from URLs
3. Analyzes comments with **BERT model** (high accuracy, multilingual)
4. **Auto-Clustering**: Automatically finds optimal number of topics with Silhouette Score (k=2-10)
5. Creates detailed Excel report

**Duration:** ~3-5 minutes for 50 articles (model loading + auto-optimization + analysis)

### Option 2: Manual Number of Topics

If you want a specific number of topics:

```bash
python main.py --input data/input/your_articles.xlsx --manual-topics --num-topics 7
```

**Uses:**
- ✅ Exactly 7 topics (without auto-optimization)
- ⚠️ May lead to over-/under-clustering

### Option 3: Predefined Content Categories

If you want to use the 10 predefined content themes:

```bash
python main.py --input data/input/your_articles.xlsx --use-predefined
```

**Uses:**
- ✅ 10 Content-Themes (AI & Innovation, Employee Stories, Culture & Values, etc.)
- ⚠️ No new topics - only predefined categories

### Option 4: Without Web Scraping

If URLs are not accessible or only comments are important:

```bash
python main.py --input data/input/your_articles.xlsx --no-scraping
```

### Option 5: Faster (without LLM)

```bash
python main.py --input data/input/your_articles.xlsx --no-llm
```

**Uses Lexicon Mode:**
- ✅ ~10x faster
- ⚠️ Slightly lower accuracy

---

## 📈 Output

### Generated file:

```
data/output/llm_analysis_20251022_143022.xlsx
```

### Sheets:

#### 1. **Articles** - Overview of all articles
| URL | Title | Content Theme | Cluster | Avg_Sentiment | Total_Comments | Positive | Negative | Neutral |
|-----|-------|---------------|---------|---------------|----------------|----------|----------|---------|
| ... | ...   | Employee Stories | Employee Stories_interview | +0.85 | 12 | 10 | 1 | 1 |

#### 2. **Categories** - Sentiment per content theme ⭐ **MOST IMPORTANT VIEW**
| Content Theme | Avg_Sentiment | Number_Articles | Positive_Comments | Negative_Comments |
|---------------|---------------|-----------------|-------------------|-------------------|
| Employee Stories | +0.88 | 15 | 142 | 5 |
| Events & Networking | +0.75 | 20 | 158 | 18 |
| Wellness & Benefits | +0.68 | 12 | 95 | 12 |
| AI & Innovation | +0.45 | 25 | 145 | 48 |
| Organizational Change | -0.15 | 12 | 35 | 75 |

**→ Interpretation:** Employee Stories receive the best feedback! 🎯

#### 3. **Clusters** - Thematic groups within content themes
| Cluster | Avg_Sentiment | Number_Articles |
|---------|---------------|-----------------|
| HR_recruiting | +0.88 | 8 |
| IT_software_update | +0.35 | 12 |
| Management_restructuring | -0.22 | 5 |

**→ Interpretation:** Recruiting articles very positive, restructuring negative

#### 4. **Insights** - Top & Worst Articles
- Top 5 articles with best feedback
- Worst 5 articles with worst feedback

---

## 🔍 How does categorization work?

The system uses **keyword matching**:

```python
CATEGORY_KEYWORDS = {
    'HR': ['mitarbeiter', 'personal', 'recruiting', 'bewerbung', 'employee', 'hiring'],
    'IT': ['software', 'hardware', 'system', 'update', 'server', 'application'],
    'Management': ['strategie', 'führung', 'management', 'leadership', 'restructuring'],
    'Training': ['schulung', 'training', 'workshop', 'seminar', 'course'],
    'Benefits': ['benefits', 'urlaub', 'gehalt', 'salary', 'bonus', 'pension'],
    # ... more categories
}
```

**You can add your own categories** in `config/settings.py`!

---

## 🎨 Clustering Logic

Articles are clustered based on:
1. **Main category** (HR, IT, etc.)
2. **Dominant keyword** (the most frequent keyword)

**Example:**
- Article about "Recruiting" → Cluster: `HR_recruiting`
- Article about "Benefits" → Cluster: `HR_benefits`
- Article about "Software Update" → Cluster: `IT_software`

→ This way you can see **which topics within a category** are well/poorly received!

---

## 💡 Advanced Usage

### Custom Columns

```bash
python main.py \
  --input data/input/file.xlsx \
  --url-column C \
  --comment-column D
```

### All Options

```bash
python main.py --help
```

Shows:
```
--input PATH          Input Excel file
--url-column COL      Column with URLs (default: A)
--comment-column COL  Column with comments (default: B)
--use-predefined      Use predefined categories instead of auto-clustering
--manual-topics       Use fixed number of topics (requires --num-topics)
--num-topics N        Fixed number of topics (only with --manual-topics)
--no-llm              Use lexicon instead of LLM
--no-scraping         Skip web scraping
--no-clustering       Skip clustering completely
```

---

## 📊 Example Workflow

### Step 1: Prepare data

```bash
# Place Excel file
cp my_articles.xlsx data/input/
```

### Step 2: Run analysis

```bash
# In corporate environment (Windows)
cd P:\IMPORTANT\Projects\SentimentAnalysis
python main.py --input data/input/my_articles.xlsx
```

**Output:**
```
==============================================================================
  EXTENDED SENTIMENT ANALYSIS with LLM & CLUSTERING
==============================================================================
Input file: data/input/my_articles.xlsx

[1/6] Load data from Excel...
✓ 150 rows loaded
✓ 50 unique articles found

[2/6] Scrape article content...
  Scraping 1/50: https://intranet.firma.de/artikel/123
  ...
✓ 50 articles scraped

[3/6] Sentiment analysis of comments...
Loading LLM model (may take ~60s)...
✓ LLM model loaded (Mode: bert)
Analyzing 150 comments with bert model...
✓ 150 comments analyzed
  Average sentiment: +0.456

[4/6] Discover optimal number of topics automatically (AUTO-OPTIMIZED - DEFAULT)...
      (Uses Silhouette Score - tests k=2 to k=10)
Testing k=2: Silhouette score = 0.234
Testing k=3: Silhouette score = 0.312
Testing k=4: Silhouette score = 0.445
Testing k=5: Silhouette score = 0.498  ← OPTIMAL
Testing k=6: Silhouette score = 0.456
...
✓ Optimal number of topics: 5 (Silhouette Score: 0.498)

[5/6] Cluster articles into 5 topics...
✓ 5 topics found:
  - Topic_0 (HR & Recruiting): 15 articles
  - Topic_1 (AI & Innovation): 20 articles
  - Topic_2 (Employee Benefits): 10 articles
  - Topic_3 (Training & Development): 8 articles
  - Topic_4 (Organizational Change): 7 articles

Top topics by sentiment:
  Topic_3 (Training & Development): 8 articles, Sentiment: +0.88
  Topic_0 (HR & Recruiting): 15 articles, Sentiment: +0.76
  Topic_1 (AI & Innovation): 20 articles, Sentiment: +0.42
  ...

[6/6] Create reports...
✓ Report saved: data/output/llm_analysis_20251022_143022.xlsx

==============================================================================
  SUMMARY
==============================================================================
Analyzed articles: 50
Total comments: 150
Avg. sentiment: +0.456
LLM model: bert

✅ Analysis completed! Report: data/output/llm_analysis_20251022_143022.xlsx
```

### Step 3: Open report

```bash
# Windows
start data\output\llm_analysis_20251022_143022.xlsx

# macOS
open data/output/llm_analysis_20251022_143022.xlsx
```

### Step 4: Interpret insights

**Question:** Which article types receive positive feedback?

**Answer from report:**
1. Open sheet "Categories"
2. Sort by "Avg_Sentiment" (descending)
3. → See top categories!

**Example result:**
```
1. Training: +0.82 → Employees love training announcements!
2. HR: +0.65      → HR news are well received
3. IT: +0.42      → IT updates ok
4. Management: +0.15 → Management news less popular
```

**Actionable insights:**
- ✅ Publish more training articles
- ✅ HR content works well
- ⚠️ Make IT updates more understandable
- ⚠️ Improve management communication

---

## 🔧 Performance Tips

### For many articles (>100):

```bash
# Use lexicon mode (faster)
python main.py --input file.xlsx --no-llm

# Or: Test without scraping first
python main.py --input file.xlsx --no-scraping

# Or: Use manual topic number (faster than auto-optimization)
python main.py --input file.xlsx --manual-topics --num-topics 5
```

### For few articles (<50):

```bash
# Use LLM + auto-clustering for best accuracy
python main.py --input file.xlsx
```

---

## 📝 Add Custom Categories

Edit `config/settings.py`:

```python
CATEGORY_KEYWORDS = {
    'HR': ['mitarbeiter', 'personal', ...],
    'IT': ['software', 'hardware', ...],

    # Add your own category:
    'Sustainability': ['nachhaltigkeit', 'umwelt', 'green', 'co2', 'klimaschutz'],
    'Innovation': ['innovation', 'digital', 'transformation', 'ai', 'ki'],
}
```

Then categorization automatically works with your new categories!

---

## 🆘 Troubleshooting

### "LLM Solution not available"
→ Make sure the `LLM Solution/` folder exists and `transformers` is installed

### "No input file found"
→ Place Excel file in `data/input/` or use `--input path`

### "Model loading takes too long"
→ Use `--no-llm` for lexicon mode (faster)

### "Scraping fails"
→ Use `--no-scraping` if URLs are not accessible

---

## 🎯 Next Steps

1. **Test with small dataset** (10-20 articles)
2. **Check categorization** - adjust keywords if needed
3. **Interpret clusters** - which topics work?
4. **Scale** to full dataset

**Good luck!** 🚀
