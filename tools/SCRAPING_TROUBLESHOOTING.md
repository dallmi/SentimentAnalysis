# Web Scraping Troubleshooting Guide

This guide helps resolve common issues when scraping corporate intranet articles.

## Common Errors

### 403 Forbidden Error

**Error Message**: `WARNING:src.web_scraper: HTTP Error scraping https://... 403 Client Error: Forbidden`

**Causes**:
1. **Authentication Required** - Intranet pages often require Windows/NTLM authentication
2. **Access Permissions** - Your account may not have permission to access the article
3. **Bot Detection** - Server may block automated requests

**Solutions**:

#### Solution 1: Use --no-scraping Flag (Recommended for Testing)

If you only have comments and URLs in your Excel file, use the `--no-scraping` flag:

```bash
python main.py --input data/input/your_file.xlsx --no-scraping
```

This will:
- Analyze sentiment from the comments only
- Skip web scraping entirely
- Still provide full analysis (sentiment, categories, clusters)

#### Solution 2: Add Windows Authentication (For Intranet Scraping)

For SharePoint and other Windows-authenticated intranet sites:

1. Install the `requests-ntlm` package:
```bash
pip install requests-ntlm
```

2. Update `src/web_scraper.py` to use NTLM authentication:
```python
from requests_ntlm import HttpNtlmAuth

# In WebScraper.__init__():
self.session.auth = HttpNtlmAuth('DOMAIN\\username', 'password')
```

3. Or use your current Windows session credentials:
```python
import win32com.client
# Uses current user's Windows credentials automatically
```

#### Solution 3: Manual Content Entry

If authentication is too complex:

1. Open each article URL in your browser (where you're already authenticated)
2. Copy the article content
3. Add a `content` column to your Excel file
4. Paste the content for each article
5. Modify the code to use the content column instead of scraping

#### Solution 4: Export from Source System

Many corporate content management systems (SharePoint, Confluence, etc.) allow bulk export:

- **SharePoint**: Use PowerShell or Power Automate to export article content
- **Confluence**: Use REST API to fetch page content
- **Other CMS**: Check for export/API functionality

### SSL Certificate Errors

**Error Message**: `SSL: CERTIFICATE_VERIFY_FAILED`

**Solution**: SSL verification is now disabled by default for corporate environments.

If you still encounter SSL errors, check:
- Corporate proxy settings in `config/settings.py`
- Firewall/antivirus software blocking Python requests

### Connection Timeout

**Error Message**: `Timeout bei [URL]`

**Causes**:
- Slow network connection
- Large article pages
- Server overload

**Solutions**:
- Increase timeout in `config/settings.py`: `REQUEST_TIMEOUT = 30`
- Add delays between requests: `DELAY_BETWEEN_REQUESTS = 2.0`
- Use `--no-scraping` if content is not needed

## Testing Scraping

### Test with Public URLs

Before testing with corporate intranet, verify scraping works with public URLs:

```bash
# Create test file with public URLs
python create_public_test_excel.py

# Test scraping
python main.py --input data/input/public_test_articles.xlsx
```

If public URLs work but intranet URLs don't, it's an authentication issue.

### Test Accessibility

Check if you can access the URL in your browser:

1. Copy the URL from error message
2. Open in your browser
3. Check if:
   - You're prompted to log in → Authentication needed
   - You see "Access Denied" → Permission issue
   - Page loads normally → May be User-Agent/headers issue

## Recommendations

### For Corporate Intranet Analysis

**Best Practice**: Use `--no-scraping` mode

Why?
- Comments already contain sentiment data (what users think)
- Article content categorization can be done manually or via CMS metadata
- Avoids authentication and permission complexities
- Faster processing
- No legal/compliance concerns about automated access

### Workflow Without Scraping

1. Export data from your CMS:
   - Article URL
   - User comments
   - (Optional) Article category/tags from CMS

2. Create Excel file with columns:
   ```
   URL | Comment | Category (optional)
   ```

3. Run analysis:
   ```bash
   python main.py --input your_file.xlsx --no-scraping
   ```

4. The system will:
   - Analyze comment sentiment (positive/negative/neutral)
   - Group comments by article
   - If categories provided, aggregate by category
   - If not, cluster articles by comment patterns

## Still Having Issues?

1. Check `logs/` directory for detailed error messages
2. Verify your Excel file format matches requirements
3. Test with the provided `test_articles.xlsx` to rule out code issues
4. Contact your IT department about:
   - Proxy settings for Python applications
   - SSL certificate requirements
   - API access to your content management system
