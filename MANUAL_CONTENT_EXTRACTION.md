# Manual Article Content Extraction Guide

This guide shows you how to manually extract article content from your corporate intranet when automatic web scraping fails due to authentication issues.

## Why Manual Extraction?

Corporate intranet sites (especially SharePoint) often require Windows/NTLM authentication that's difficult to automate. Manual extraction is:

- ✅ **Faster** than setting up authentication
- ✅ **More reliable** than dealing with SSL/proxy issues
- ✅ **Secure** - you use your existing browser session
- ✅ **Simple** - no coding required

## Method 1: Browser Console (Recommended)

### Step-by-Step Process

1. **Open your first article in the browser**
   - Navigate to the intranet article URL
   - Make sure the page is fully loaded

2. **Open Browser DevTools**
   - Press `F12` (or `Ctrl+Shift+I` on Windows, `Cmd+Option+I` on Mac)
   - Click on the **Console** tab

3. **Run the extraction script**
   - Open [extract_article_content.js](extract_article_content.js)
   - Copy the entire script
   - Paste into the Console
   - Press `Enter`

4. **Copy the extracted JSON**
   - The script will display the extracted article as JSON
   - It will also try to copy it to your clipboard automatically
   - If auto-copy doesn't work, manually select and copy the JSON from the console

5. **Repeat for each article**
   - Open the next article URL
   - Run the script again (you can press `↑` in console to recall previous command)
   - Copy the JSON

### Example Output

```json
{
  "url": "https://your-intranet.com/article.aspx",
  "title": "New AI Tools for Employees",
  "content": "Our company is introducing new AI tools to help employees work more efficiently..."
}
```

## Method 2: Bulk Extraction with Python

### Step 1: Extract All Articles

For each article, run the browser console script and save the JSON output.

### Step 2: Create articles.json

1. Open `create_articles_json.py`
2. Paste your extracted articles into the `articles` list:

```python
articles = [
    {
        "url": "https://intranet.com/article1.aspx",
        "title": "New AI Tools",
        "content": "Full article text here..."
    },
    {
        "url": "https://intranet.com/article2.aspx",
        "title": "Employee Benefits Update",
        "content": "More article content here..."
    }
]
```

3. Run the script:
```bash
python create_articles_json.py
```

This creates `data/input/articles.json` with all your articles.

### Step 3: Run Analysis with Pre-Extracted Content

```bash
python main.py --input your_comments.xlsx --articles-json data/input/articles.json
```

This will:
- ✅ Load comments from your Excel file
- ✅ Load article content from the JSON file (no scraping!)
- ✅ Perform full sentiment analysis
- ✅ Categorize articles based on their content
- ✅ Cluster similar articles
- ✅ Generate comprehensive Excel report

## Alternative: Simple Copy-Paste

If the JavaScript method doesn't work on your corporate browser:

### Manual Copy-Paste Method

1. **Create a simple text file for each article**
   - Open the article in browser
   - Select all content (`Ctrl+A` or `Cmd+A`)
   - Copy (`Ctrl+C` or `Cmd+C`)
   - Paste into a text file

2. **Create JSON manually**

Create `data/input/articles.json`:

```json
{
  "https://intranet.com/article1.aspx": {
    "title": "Article Title 1",
    "content": "Paste full article text here..."
  },
  "https://intranet.com/article2.aspx": {
    "title": "Article Title 2",
    "content": "Paste full article text here..."
  }
}
```

3. **Run analysis**
```bash
python main.py --input your_comments.xlsx --articles-json data/input/articles.json
```

## Tips for Efficient Extraction

### 1. Use Browser Tabs
- Open all article URLs in separate tabs
- Extract from each tab sequentially
- This is faster than navigating back and forth

### 2. Keyboard Shortcuts
- `F12` - Open DevTools
- `Ctrl+L` or `Cmd+L` - Focus URL bar (to copy URL)
- `↑` in Console - Recall previous command
- `Ctrl+A` then `Ctrl+C` - Select all and copy from console

### 3. Template for Quick Editing

Keep this template in a text editor:

```json
{
  "url": "PASTE_URL_HERE",
  "title": "PASTE_TITLE_HERE",
  "content": "PASTE_CONTENT_HERE"
}
```

Then just fill in the blanks for each article.

### 4. Batch Processing

If you have many articles:
1. Extract all to separate text files first
2. Format as JSON in one session
3. This separates the browsing task from the formatting task

## Workflow Comparison

### Without Articles Content (--no-scraping)
```bash
python main.py --input comments.xlsx --no-scraping
```
- ✅ Analyzes comment sentiment
- ✅ Groups by article URL
- ❌ No article categorization (needs content)
- ❌ No content-based insights

### With Manual Articles Content
```bash
python main.py --input comments.xlsx --articles-json articles.json
```
- ✅ Analyzes comment sentiment
- ✅ Groups by article URL
- ✅ Categorizes articles by content (HR, IT, Company News, etc.)
- ✅ Identifies article keywords
- ✅ Clusters similar articles
- ✅ Content-based insights

## Troubleshooting

### Q: The JavaScript script doesn't find any content

**A:** Try these selectors manually in the console:

```javascript
// Find the main content container
document.querySelector('article')
document.querySelector('main')
document.querySelector('.content')
document.querySelector('#content')

// Look at the page structure
document.body.innerHTML
```

Find the element that contains the article text, then modify the script to target that specific selector.

### Q: Can I extract just titles and skip content?

**A:** Yes! Titles are often enough for basic categorization:

```json
{
  "url": "https://intranet.com/article.aspx",
  "title": "New AI Tools for Employees",
  "content": ""
}
```

The system will use titles for categorization if content is empty.

### Q: Some articles have dynamic content that loads after page load

**A:** Wait a few seconds after the page loads, then run the extraction script. Or scroll down to trigger lazy-loading, then extract.

## Next Steps

After extracting articles:

1. **Review the JSON file** - Make sure all URLs and content look correct
2. **Test with one article first** - Create a small JSON with one article to test
3. **Run full analysis** - Process all articles once you confirm it works
4. **Check output** - Review the Excel report for categorization accuracy

## Need Help?

- Check [SCRAPING_TROUBLESHOOTING.md](SCRAPING_TROUBLESHOOTING.md) for web scraping alternatives
- Review [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for general issues
- Validate your JSON at https://jsonlint.com/
