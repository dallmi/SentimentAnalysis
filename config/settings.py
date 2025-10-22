"""
Konfigurationsdatei für Sentiment Analysis
"""

# Corporate Network Einstellungen
PROXY_CONFIG = {
    'http': None,  # Beispiel: 'http://corporate-proxy:8080'
    'https': None,  # Beispiel: 'http://corporate-proxy:8080'
}

# Web Scraping Einstellungen
REQUEST_TIMEOUT = 10  # Sekunden
MAX_RETRIES = 3
USER_AGENT = 'Corporate-SentimentAnalyzer/1.0'
DELAY_BETWEEN_REQUESTS = 0.5  # Sekunden

# Sentiment Analyse Einstellungen
SENTIMENT_THRESHOLDS = {
    'very_positive': 0.5,
    'positive': 0.1,
    'neutral_low': -0.1,
    'neutral_high': 0.1,
    'negative': -0.1,
    'very_negative': -0.5
}

# Kategorisierung
MIN_COMMENTS_FOR_ANALYSIS = 1  # Mindestanzahl Kommentare pro Artikel
CATEGORY_KEYWORDS = {
    'HR': ['mitarbeiter', 'personal', 'team', 'hr', 'recruiting', 'benefits'],
    'IT': ['software', 'hardware', 'system', 'it', 'technologie', 'digital'],
    'Management': ['strategie', 'führung', 'management', 'vision', 'ziele'],
    'Kommunikation': ['kommunikation', 'mitteilung', 'ankündigung', 'news'],
    'Prozesse': ['prozess', 'ablauf', 'workflow', 'optimierung', 'effizienz'],
}

# Output Einstellungen
OUTPUT_DIR = 'data/output'
INPUT_DIR = 'data/input'
GENERATE_VISUALIZATIONS = True
INCLUDE_STATISTICS = True

# Sprache
LANGUAGE = 'de'  # Deutsch
