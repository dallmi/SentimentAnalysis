# Simple Workflow: Browser Extraction to Analysis

This is the **simplest workflow** for extracting and analyzing corporate intranet articles with comments.

## 🎯 Overview

**One JSON file** → **One Python script** → **Ready for analysis**

No need to manually create separate files for articles and comments!

## 📋 Complete Workflow (3 Steps)

### Step 1: Extract Articles with Comments (Browser)

For each article:

1. Open article in browser (logged in to your intranet)
2. Press **F12** → **Console** tab
3. Copy and paste **[extract_article_with_comments_custom.js](extract_article_with_comments_custom.js)**
4. Press **Enter**
5. JSON is copied to clipboard automatically

### Step 2: Save All Extracted Data

Create a file `extracted_articles.json` with all your articles:

```json
[
  {
    "url": "https://intranet.com/article1.aspx",
    "title": "Article Title 1",
    "content": "Full article content here...",
    "comments": [
      {
        "text": "Great article!",
        "author": "John Doe",
        "date": "2024-01-15"
      },
      {
        "text": "Very helpful, thanks!",
        "author": "Jane Smith",
        "date": "2024-01-16"
      }
    ]
  },
  {
    "url": "https://intranet.com/article2.aspx",
    "title": "Article Title 2",
    "content": "Another article content...",
    "comments": [
      {
        "text": "Interesting perspective",
        "author": "Bob Johnson",
        "date": "2024-01-17"
      }
    ]
  }
]
```

**Tip**: Just paste each article's JSON output, separated by commas, wrapped in `[ ]`.

### Step 3: Process and Analyze

```bash
# Process the extracted data (creates articles.json + comments.xlsx)
python process_extracted_data.py extracted_articles.json

# Run sentiment analysis
python main.py --input data/input/comments.xlsx --articles-json data/input/articles.json
```

**That's it!** ✅

## 📊 What Gets Created

`process_extracted_data.py` creates **two files** automatically:

### 1. `data/input/articles.json`
Article content in URL-keyed format:
```json
{
  "https://intranet.com/article1.aspx": {
    "title": "Article Title 1",
    "content": "Full article content..."
  },
  "https://intranet.com/article2.aspx": {
    "title": "Article Title 2",
    "content": "Another article content..."
  }
}
```

### 2. `data/input/comments.xlsx`
Comments in Excel format:

| URL | Comment | Author | Date |
|-----|---------|--------|------|
| https://intranet.com/article1.aspx | Great article! | John Doe | 2024-01-15 |
| https://intranet.com/article1.aspx | Very helpful... | Jane Smith | 2024-01-16 |
| https://intranet.com/article2.aspx | Interesting... | Bob Johnson | 2024-01-17 |

## 🚀 Full Example

```bash
# Step 1: Extract articles in browser → save as extracted_articles.json

# Step 2: Process the data
python process_extracted_data.py extracted_articles.json
# Output:
# ✓ Created data/input/articles.json (5 articles)
# ✓ Created data/input/comments.xlsx (23 comments)

# Step 3: Run analysis
python main.py --input data/input/comments.xlsx --articles-json data/input/articles.json
# Output:
# ✓ Sentiment analysis complete
# ✓ Report: data/output/sentiment_analysis_2024-01-20_14-30-00.xlsx
```

## 📈 Analysis Output

The final Excel report contains:

- **Articles Sheet**: All articles with sentiment scores and ratings
- **Categories Sheet**: Articles grouped by category (HR, IT, Company News, etc.)
- **Clusters Sheet**: Similar articles grouped together
- **Insights Sheet**: Summary and recommendations

## 💡 Pro Tips

### Tip 1: Extract in Batches
- Day 1: Extract articles 1-5 in browser
- Save as `extracted_batch1.json`
- Day 2: Extract articles 6-10
- Combine the batches into one file

### Tip 2: Test with One Article First
Extract one article, process it, and run analysis to verify everything works:

```bash
# Single article test
python process_extracted_data.py test_single_article.json
python main.py --input data/input/comments.xlsx --articles-json data/input/articles.json
```

### Tip 3: Check Your JSON
Before processing, validate your JSON at https://jsonlint.com/

Common mistakes:
- ❌ Missing comma between articles
- ❌ Not wrapping articles in `[ ]`
- ❌ Quotes not properly escaped in text

### Tip 4: Use Browser Tabs
- Open all articles in separate tabs
- Extract from each tab sequentially
- Press `↑` in console to recall the extraction script
- Much faster than navigating back and forth!

## 🔍 Troubleshooting

### Q: Script says "No comments found in any article"

**A**: Check your `extracted_articles.json`:
- Does each article have a `"comments"` array?
- Are the comments non-empty?
- Did the browser extraction script work?

### Q: Some articles have no comments

**A**: That's OK! The script will:
- Still process articles with content
- Show warning for articles without comments
- Include them in analysis (just no comment sentiment)

### Q: Can I add more articles later?

**A**: Yes! Just:
1. Extract new articles
2. Add them to your JSON file
3. Re-run `process_extracted_data.py`
4. Re-run analysis

## 📚 Related Files

- **[extract_article_with_comments_custom.js](extract_article_with_comments_custom.js)** - Browser extraction script
- **[process_extracted_data.py](process_extracted_data.py)** - Data processing script
- **[main.py](main.py)** - Main analysis script

## 🆚 Comparison with Other Methods

| Method | Files Needed | Steps | Complexity |
|--------|-------------|-------|------------|
| **This Simple Workflow** | 1 JSON | 3 steps | ⭐ Easy |
| Manual Excel + JSON | 2 files | 4 steps | ⭐⭐ Medium |
| Separate converters | 3+ files | 5+ steps | ⭐⭐⭐ Complex |
| Web scraping | 0 files | 1 step | ❌ Doesn't work (auth issues) |

## ✅ Checklist

Before running analysis, make sure:

- [ ] Extracted all articles using browser console script
- [ ] Saved as JSON array in `extracted_articles.json`
- [ ] Validated JSON (https://jsonlint.com)
- [ ] Ran `process_extracted_data.py`
- [ ] Verified `articles.json` and `comments.xlsx` were created
- [ ] Ready to run `main.py`

---

**Need help?** Check:
- [EXTRACT_EVERYTHING_FROM_BROWSER.md](EXTRACT_EVERYTHING_FROM_BROWSER.md) - Detailed extraction guide
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
- [SCRAPING_TROUBLESHOOTING.md](SCRAPING_TROUBLESHOOTING.md) - Alternative methods
