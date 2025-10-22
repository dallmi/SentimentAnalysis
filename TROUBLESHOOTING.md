# Troubleshooting Guide

## Common Problems and Solutions

### 1. Import Error: Module Not Found

**Problem**: `ModuleNotFoundError: No module named 'pandas'`

**Solution**:
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Excel File Cannot Be Read

**Problem**: `Error loading Excel file`

**Solutions**:
- Check if file exists and permissions are correct
- Ensure it is a .xlsx or .xls file
- Check if columns A and B exist
- Use `--url-column` and `--comment-column` parameters if using other columns

### 3. Corporate Proxy Problems

**Problem**: `Connection Error` during web scraping

**Solutions**:
1. Configure proxy in `config/settings.py`:
```python
PROXY_CONFIG = {
    'http': 'http://proxy.firma.de:8080',
    'https': 'http://proxy.firma.de:8080'
}
```

2. Or set environment variables:
```bash
export http_proxy="http://proxy.firma.de:8080"
export https_proxy="http://proxy.firma.de:8080"
```

3. Skip web scraping:
```bash
python main.py --input data/input/datei.xlsx --no-scraping
```

### 4. NLTK VADER Not Available

**Problem**: `VADER not available`

**Solutions**:
- Not a critical error, system automatically uses Lightweight Model
- If VADER is desired:
```bash
pip install nltk
python -c "import nltk; nltk.download('vader_lexicon')"
```

### 5. SSL Certificate Error

**Problem**: `SSL: CERTIFICATE_VERIFY_FAILED`

**Solution**: In `src/web_scraper.py` line ~55, change:
```python
response = self.session.get(url, timeout=REQUEST_TIMEOUT, verify=False)
```

**WARNING**: Only use in secure intranet environments!

### 6. No Output Files Generated

**Problem**: Program runs through, but no Excel files

**Solutions**:
- Check write permissions in `data/output/` directory
- Check logs in `sentiment_analysis.log`
- Ensure pandas and openpyxl are installed

### 7. Memory Problems with Many URLs

**Problem**: `MemoryError` or very slow

**Solutions**:
- Split input file into smaller chunks
- Increase `DELAY_BETWEEN_REQUESTS` in `config/settings.py`
- Reduce concurrent processing

### 8. Nexus Repository / Corporate Packages

**Problem**: Packages cannot be installed from PyPI

**Solutions**:
1. Use Corporate Nexus:
```bash
pip install --index-url https://nexus.firma.de/repository/pypi-all/simple -r requirements.txt
```

2. If no external packages are allowed:
- Use Python Standard Library version only
- See `docs/minimal_dependencies.md` (will create shortly)

### 9. Encoding Problems

**Problem**: `UnicodeDecodeError` when reading files

**Solution**: Excel should be UTF-8 or Latin-1 encoded

### 10. Tests Fail

**Problem**: `test_modules.py` gives errors

**Solution**:
```bash
# Make sure you're in the right directory
cd /Users/micha/Documents/Arbeit/SentimentAnalysis

# Activate venv
source venv/bin/activate

# Run tests
python test_modules.py
```

## Support

For further problems:
1. Check `sentiment_analysis.log` for detailed errors
2. Enable debug logging in the respective module file
3. Test with `--no-scraping` option for faster troubleshooting
