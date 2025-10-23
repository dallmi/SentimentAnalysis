# Clean Content Extraction Guide

This guide helps you extract **clean article content** without page structure noise (navigation, footer, comments, etc.).

## 🎯 Problem

When extracting articles, you might get unwanted content like:
- Navigation menus
- Footer text
- Comment sections
- Sidebars
- "Share this article" buttons
- Related posts

This pollutes your content analysis and BERT clustering.

## ✅ Solution: Two-Step Process

### Step 1: Inspect Page Structure

Run this **once per website** to understand the page structure:

```javascript
// In browser console (F12 → Console):
// Copy and paste: inspect_page_structure.js
```

**Output:**
```
RECOMMENDATION:
Best container: article
Clean text length: 1847 chars

Use this selector in your extraction script:
const mainContent = document.querySelector('article');
```

### Step 2: Extract Clean Content

1. **Open** [extract_clean_content.js](extract_clean_content.js)

2. **Update line 15** with your content selector:
   ```javascript
   const CONTENT_SELECTOR = 'article';  // ← Update this!
   ```

3. **Optional**: Add more elements to remove (lines 18-39):
   ```javascript
   const ELEMENTS_TO_REMOVE = [
       'script',
       'nav',
       '.your-specific-class',  // ← Add custom selectors
       // ...
   ];
   ```

4. **Run in browser console** for each article

5. **JSON is auto-copied** to clipboard!

## 🔍 Troubleshooting

### Issue: Still getting unwanted content

**Solution**: Add more selectors to `ELEMENTS_TO_REMOVE`

Example - removing social share buttons:
```javascript
const ELEMENTS_TO_REMOVE = [
    // ... existing selectors ...
    '.social-share',
    '.share-buttons',
    '[class*="share"]',
    '.addthis',
    '.sharethis'
];
```

### Issue: Content is too short or missing

**Problem**: Wrong content selector

**Solution**:
1. Right-click on article text → Inspect
2. Look for the parent container
3. Note its class or ID
4. Update `CONTENT_SELECTOR`

Example:
```javascript
// If your article is in <div class="post-content">
const CONTENT_SELECTOR = '.post-content';

// If your article is in <div id="main-article">
const CONTENT_SELECTOR = '#main-article';
```

### Issue: Comments are missing

**Problem**: Comment selector is wrong

**Solution**:
In [extract_clean_content.js](extract_clean_content.js), update line 87:
```javascript
// Current (for your site):
const commentList = document.querySelector('#comment-list.main');

// If your comments are elsewhere:
const commentList = document.querySelector('.comments-section');
```

## 📋 Common Page Structures

### SharePoint (.aspx pages)
```javascript
const CONTENT_SELECTOR = '[class*="PublishingPageContent"]';
// or
const CONTENT_SELECTOR = '.ms-rtestate-field';
```

### WordPress
```javascript
const CONTENT_SELECTOR = '.entry-content';
// or
const CONTENT_SELECTOR = 'article .post-content';
```

### Confluence
```javascript
const CONTENT_SELECTOR = '#main-content';
// or
const CONTENT_SELECTOR = '.wiki-content';
```

### Custom CMS
Use `inspect_page_structure.js` to find the correct selector!

## 🎨 Visual Inspection Method

If scripts don't work:

1. **Open DevTools** (F12)
2. **Click inspector** (top-left icon)
3. **Hover over article text** on the page
4. DevTools highlights the element
5. **Look at the HTML** - note the class/id
6. **Use that selector**

Example:
```html
<div class="article-body">  ← This is your selector!
    <h1>Article Title</h1>
    <p>Article content...</p>
</div>
```

→ `CONTENT_SELECTOR = '.article-body'`

## ⚙️ Advanced: Site-Specific Script

For complex sites, create a custom extraction script:

```javascript
// custom_extractor.js
(function extractMyCompanySite() {
    // Your company's specific structure
    const contentElement = document.querySelector('.company-specific-content');
    const commentsElement = document.querySelector('.company-comments');

    // Remove company-specific noise
    contentElement.querySelectorAll('.company-ad, .company-promo').forEach(el => el.remove());

    // Extract...
})();
```

## 🧪 Testing

Before extracting all articles:

1. **Test on one article**
2. **Check the content preview** in console
3. **Verify it's clean** (no nav/footer text)
4. **If clean → extract all articles**
5. **If not → adjust selectors and retry**

## 💡 Pro Tips

### Tip 1: Use Browser Tabs
- Open all articles in tabs
- Run extraction script in each tab
- Press `↑` in console to recall script
- Very fast!

### Tip 2: Content Preview
The script shows a 500-char preview. Check if it looks clean:

✅ **Good preview:**
```
"Our company is introducing new AI tools to help employees work more
efficiently. These tools include automated document processing, smart
email categorization, and intelligent meeting schedulers..."
```

❌ **Bad preview (has noise):**
```
"Home About Contact Login Menu Search Our company is introducing new
AI tools Footer Copyright 2024 Privacy Policy Terms of Service..."
```

### Tip 3: Regex Cleanup (Advanced)

If you still have small artifacts, add cleanup in Python:

```python
# In your article_content.json, you can manually clean:
import re
content = re.sub(r'Home|About|Contact|Login|Menu', '', content)
content = re.sub(r'Copyright \d{4}', '', content)
```

## 📊 Expected Results

**Before cleanup:**
- Content: "Home Menu About Contact Login New AI Tools for Employees We are excited... Footer Copyright 2024 Share on Facebook Twitter"
- Length: 2500 chars (with noise)
- BERT clustering: All articles → "Menu & Contact" cluster ❌

**After cleanup:**
- Content: "New AI Tools for Employees We are excited to announce our new AI-powered tools..."
- Length: 1800 chars (clean)
- BERT clustering: "AI & Tools" cluster ✅

## 🆘 Still Having Issues?

1. **Share your page structure** - Run `inspect_page_structure.js` and share output
2. **Check browser console for errors**
3. **Try the visual inspection method**
4. **Worst case**: Manually copy-paste article text into JSON

Remember: Clean content = Better BERT clustering = Better insights! 🎯
