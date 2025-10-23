# Complete Browser-Based Extraction Guide

This guide shows you how to extract **both article content AND comments** directly from your browser, bypassing all authentication and scraping issues.

## 🎯 Overview

**Problem**: Your SharePoint/Intranet articles require authentication and can't be scraped automatically.

**Solution**: Extract everything manually from your browser using JavaScript, then convert to Excel for analysis.

## 📋 Two Workflows

### Workflow 1: Comments Already in Excel (Simple)

Use this if you already have comments exported from your system.

1. **Extract article content only** → Use [extract_article_content.js](extract_article_content.js)
2. **Convert to JSON** → Use [convert_articles_json.py](convert_articles_json.py)
3. **Run analysis** → `python main.py --input comments.xlsx --articles-json articles.json`

### Workflow 2: Extract Everything from Browser (Complete)

Use this if you need to extract both articles AND comments from the page.

## 🚀 Workflow 2: Complete Extraction (Step-by-Step)

### Step 1: Extract Articles with Comments

For **each article page**:

1. **Open the article** in your browser (logged in to intranet)
2. **Press F12** → Go to **Console** tab
3. **Copy and paste** [extract_article_with_comments.js](extract_article_with_comments.js)
4. **Press Enter**
5. The script will:
   - Extract article URL, title, and content
   - Find and extract all comments (text, author, date)
   - Show you a preview
   - Copy JSON to clipboard

**Output Example**:
```json
{
  "url": "https://intranet.com/article.aspx",
  "title": "New AI Tools Announcement",
  "content": "We are excited to announce...",
  "comments": [
    {
      "text": "Great initiative! Looking forward to trying these tools.",
      "author": "John Doe",
      "date": "2024-01-15"
    },
    {
      "text": "Will there be training sessions?",
      "author": "Jane Smith",
      "date": "2024-01-16"
    }
  ]
}
```

### Step 2: Save Extracted Data

Create a file `extracted_articles.json` with all your articles:

```json
[
  {
    "url": "https://intranet.com/article1.aspx",
    "title": "Article 1",
    "content": "...",
    "comments": [...]
  },
  {
    "url": "https://intranet.com/article2.aspx",
    "title": "Article 2",
    "content": "...",
    "comments": [...]
  }
]
```

**Tip**: Paste each article's JSON separated by commas, wrapped in `[ ]`.

### Step 3: Convert Comments to Excel

```bash
python convert_extracted_comments_to_excel.py extracted_articles.json comments.xlsx
```

This creates an Excel file:

| URL | Comment | Author | Date |
|-----|---------|--------|------|
| https://intranet.com/article1.aspx | Great initiative! | John Doe | 2024-01-15 |
| https://intranet.com/article1.aspx | Will there be training? | Jane Smith | 2024-01-16 |
| https://intranet.com/article2.aspx | Very helpful article | Bob Johnson | 2024-01-17 |

### Step 4: Convert Articles to JSON

```bash
python convert_articles_json.py extracted_articles.json
```

This creates `articles.json`:

```json
{
  "https://intranet.com/article1.aspx": {
    "title": "Article 1",
    "content": "Full article text..."
  },
  "https://intranet.com/article2.aspx": {
    "title": "Article 2",
    "content": "Full article text..."
  }
}
```

### Step 5: Run Complete Analysis

```bash
python main.py --input comments.xlsx --articles-json articles.json
```

## 🎯 What if Comments Section Isn't Found?

The script tries many common selectors, but if it doesn't find comments:

### Option A: Inspect the Page

1. **Open DevTools** (F12)
2. **Click the inspector** (top-left icon in DevTools)
3. **Click on a comment** in the page
4. Look at the highlighted element in DevTools
5. Note the class name (e.g., `class="ms-feedbackItem"`)

### Option B: Manual Selector

Modify the script to add your specific selector:

```javascript
// At line ~70, add your selector:
const commentSectionCandidates = [
    '.your-specific-comment-class',  // ← Add this
    '.comments',
    // ... rest of selectors
];
```

### Option C: Extract Comments Manually

If the script can't find comments automatically:

1. **Copy all comment text** from the page
2. **Paste into Excel** with the URL
3. One row per comment

## 📊 Comparison of Methods

| Method | Article Content | Comments | Complexity | Authentication |
|--------|----------------|----------|------------|----------------|
| **Automatic Scraping** | ✅ | ❌ | Medium | ❌ Fails |
| **Manual Excel Only** | ❌ | ✅ | Low | ✅ No issue |
| **Browser Extraction** | ✅ | ✅ | Medium | ✅ No issue |
| **Hybrid (Recommended)** | ✅ Browser | ✅ CMS Export | Low | ✅ No issue |

## 🔍 Troubleshooting

### Q: Script says "No comment section found"

**A**: The page structure is different. Try:

1. Run this in console to see all elements:
```javascript
document.querySelectorAll('[class*="comment"]')
```

2. Look for elements with "comment", "feedback", or "discussion" in class names

3. Manually modify the script to use the correct selector

### Q: Comments are extracted but text is wrong

**A**: The script might be picking up metadata. Try:

1. Inspect a comment element
2. Find the exact element that contains just the comment text
3. Modify the script's `textCandidates` array with your specific selector

### Q: Can I extract just one article to test?

**A**: Yes! Extract one article, save as:

```json
{
  "url": "...",
  "title": "...",
  "content": "...",
  "comments": [...]
}
```

Then run:
```bash
python convert_extracted_comments_to_excel.py single_article.json test.xlsx
python convert_articles_json.py single_article.json
python main.py --input test.xlsx --articles-json articles.json
```

## 💡 Pro Tips

### Tip 1: Use Browser Tabs
- Open all 5 articles in separate tabs
- Run the extraction script in each tab sequentially
- Press `↑` in console to recall the script

### Tip 2: Save Intermediate Files
- Save `extracted_articles.json` for future use
- If extraction fails, you don't lose your work

### Tip 3: Batch Processing
Extract in stages:
1. Day 1: Extract all articles (15 minutes for 5 articles)
2. Day 2: Convert and run analysis (5 minutes)

### Tip 4: Validate JSON
Before running conversion, validate your JSON at https://jsonlint.com/

## 🎉 Complete Example

```bash
# Step 1: Extract articles in browser → save as extracted_articles.json

# Step 2: Convert comments to Excel
python convert_extracted_comments_to_excel.py extracted_articles.json comments.xlsx

# Step 3: Convert articles to JSON
python convert_articles_json.py extracted_articles.json

# Step 4: Run analysis
python main.py --input comments.xlsx --articles-json articles.json

# Output: data/output/sentiment_analysis_YYYY-MM-DD_HH-MM-SS.xlsx
```

## 📚 Related Documentation

- [extract_article_with_comments.js](extract_article_with_comments.js) - Main extraction script
- [convert_extracted_comments_to_excel.py](convert_extracted_comments_to_excel.py) - Comments to Excel converter
- [convert_articles_json.py](convert_articles_json.py) - Articles to JSON converter
- [MANUAL_CONTENT_EXTRACTION.md](MANUAL_CONTENT_EXTRACTION.md) - Article-only extraction
- [SCRAPING_TROUBLESHOOTING.md](SCRAPING_TROUBLESHOOTING.md) - Web scraping alternatives
