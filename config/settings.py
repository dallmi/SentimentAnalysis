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

# Kategorisierung nach INHALTS-THEMEN (nicht Abteilungen!)
MIN_COMMENTS_FOR_ANALYSIS = 1  # Mindestanzahl Kommentare pro Artikel

# Content-Theme Kategorien: Was ist das THEMA des Artikels?
CATEGORY_KEYWORDS = {
    # Technologie & Innovation
    'KI & Innovation': [
        'künstliche intelligenz', 'ki', 'ai', 'machine learning', 'chatgpt',
        'automation', 'innovation', 'digital transformation', 'digitalisierung',
        'startup', 'technologie', 'zukunft', 'forschung'
    ],

    # Persönliche Geschichten & Erfolge
    'Mitarbeiter-Stories': [
        'mitarbeiter', 'kollege', 'team', 'geschichte', 'erfahrung', 'interview',
        'porträt', 'karriere', 'erfolg', 'persönlich', 'story', 'profil',
        'erlebnis', 'werdegang', 'mein weg'
    ],

    # Unternehmenskultur & Werte
    'Unternehmenskultur': [
        'kultur', 'werte', 'vision', 'mission', 'diversität', 'inklusion',
        'diversity', 'zusammenarbeit', 'teamwork', 'gemeinschaft', 'values',
        'purpose', 'nachhaltigkeit', 'verantwortung', 'ethik'
    ],

    # Lernen & Entwicklung
    'Weiterbildung & Training': [
        'training', 'schulung', 'workshop', 'seminar', 'weiterbildung',
        'lernen', 'entwicklung', 'kurs', 'coaching', 'mentoring',
        'upskilling', 'fortbildung', 'akademie', 'programm'
    ],

    # Veranstaltungen & Events
    'Events & Networking': [
        'event', 'veranstaltung', 'konferenz', 'meetup', 'networking',
        'feier', 'jubiläum', 'fest', 'party', 'treffen', 'community',
        'hackathon', 'summit', 'conference'
    ],

    # Produkte & Projekte
    'Produkt-News': [
        'produkt', 'launch', 'release', 'feature', 'projekt', 'entwicklung',
        'beta', 'update', 'version', 'lösung', 'service', 'plattform',
        'tool', 'application', 'software'
    ],

    # Unternehmenserfolge & Zahlen
    'Business & Erfolge': [
        'quartal', 'umsatz', 'wachstum', 'erfolg', 'award', 'auszeichnung',
        'partner', 'kunde', 'vertrag', 'deal', 'expansion', 'markt',
        'geschäftsjahr', 'finanzen', 'gewinn'
    ],

    # Wellness & Work-Life
    'Wellness & Benefits': [
        'gesundheit', 'wellness', 'sport', 'fitness', 'work-life-balance',
        'flexible', 'homeoffice', 'remote', 'benefits', 'gesundheitstag',
        'yoga', 'meditation', 'wohlbefinden', 'mental health'
    ],

    # Change & Transformation
    'Organisatorische Änderungen': [
        'change', 'transformation', 'reorganisation', 'umstrukturierung',
        'strategie', 'führung', 'management', 'neue struktur', 'änderung',
        'prozess', 'optimierung', 'effizienz', 'umstellung'
    ],

    # Soziale Verantwortung
    'CSR & Nachhaltigkeit': [
        'nachhaltigkeit', 'csr', 'umwelt', 'klimaschutz', 'sozial',
        'spende', 'charity', 'volunteering', 'engagement', 'green',
        'ökologisch', 'recycling', 'co2', 'klimaneutral'
    ],
}

# Output Einstellungen
OUTPUT_DIR = 'data/output'
INPUT_DIR = 'data/input'
GENERATE_VISUALIZATIONS = True
INCLUDE_STATISTICS = True

# Sprache
LANGUAGE = 'de'  # Deutsch
