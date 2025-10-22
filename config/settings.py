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

# Content-Theme Categories: What is the article ABOUT?
# Language priority: English (primary), German (secondary), French/Italian (tertiary)
CATEGORY_KEYWORDS = {
    # AI & Technology Innovation
    'AI & Innovation': [
        # English (primary)
        'artificial intelligence', 'ai', 'machine learning', 'ml', 'chatgpt', 'gpt',
        'automation', 'innovation', 'digital transformation', 'technology', 'tech',
        'startup', 'future', 'research', 'data science', 'algorithm', 'deep learning',
        # German (secondary)
        'künstliche intelligenz', 'ki', 'digitalisierung', 'technologie', 'zukunft', 'forschung',
        # French (tertiary)
        'intelligence artificielle', 'ia', 'technologie', 'innovation',
        # Italian (tertiary)
        'intelligenza artificiale', 'tecnologia', 'innovazione'
    ],

    # Employee Stories & Profiles
    'Employee Stories': [
        # English (primary)
        'employee', 'colleague', 'team member', 'story', 'experience', 'interview',
        'profile', 'portrait', 'career', 'journey', 'success', 'personal', 'testimonial',
        'meet the team', 'spotlight', 'feature', 'my path', 'my experience',
        # German (secondary)
        'mitarbeiter', 'kollege', 'geschichte', 'erfahrung', 'porträt', 'karriere',
        'werdegang', 'mein weg', 'persönlich', 'profil', 'erlebnis',
        # French (tertiary)
        'employé', 'collègue', 'histoire', 'expérience', 'carrière', 'parcours',
        # Italian (tertiary)
        'dipendente', 'collega', 'storia', 'esperienza', 'carriera', 'percorso'
    ],

    # Company Culture & Values
    'Culture & Values': [
        # English (primary)
        'culture', 'values', 'vision', 'mission', 'diversity', 'inclusion', 'dei',
        'collaboration', 'teamwork', 'community', 'purpose', 'ethics', 'integrity',
        'belonging', 'equity', 'workplace culture', 'company values',
        # German (secondary)
        'kultur', 'werte', 'diversität', 'inklusion', 'zusammenarbeit', 'gemeinschaft',
        'verantwortung', 'ethik', 'unternehmenskultur',
        # French (tertiary)
        'culture', 'valeurs', 'diversité', 'inclusion', 'collaboration', 'éthique',
        # Italian (tertiary)
        'cultura', 'valori', 'diversità', 'inclusione', 'collaborazione', 'etica'
    ],

    # Learning & Development
    'Learning & Development': [
        # English (primary)
        'training', 'workshop', 'seminar', 'course', 'learning', 'development',
        'coaching', 'mentoring', 'upskilling', 'reskilling', 'education', 'academy',
        'program', 'certification', 'skill building', 'professional development',
        # German (secondary)
        'schulung', 'weiterbildung', 'lernen', 'entwicklung', 'kurs', 'fortbildung',
        'akademie', 'programm', 'ausbildung',
        # French (tertiary)
        'formation', 'atelier', 'apprentissage', 'développement', 'coaching',
        # Italian (tertiary)
        'formazione', 'workshop', 'apprendimento', 'sviluppo', 'corso'
    ],

    # Events & Networking
    'Events & Networking': [
        # English (primary)
        'event', 'conference', 'meetup', 'networking', 'celebration', 'anniversary',
        'party', 'gathering', 'community', 'hackathon', 'summit', 'forum',
        'townhall', 'get-together', 'social event', 'team building',
        # German (secondary)
        'veranstaltung', 'konferenz', 'feier', 'jubiläum', 'fest', 'treffen',
        # French (tertiary)
        'événement', 'conférence', 'rencontre', 'célébration', 'fête', 'réunion',
        # Italian (tertiary)
        'evento', 'conferenza', 'incontro', 'celebrazione', 'festa', 'riunione'
    ],

    # Product & Project News
    'Product News': [
        # English (primary)
        'product', 'launch', 'release', 'feature', 'project', 'development',
        'beta', 'update', 'version', 'solution', 'service', 'platform',
        'tool', 'application', 'software', 'rollout', 'deployment', 'new release',
        # German (secondary)
        'produkt', 'projekt', 'entwicklung', 'lösung', 'anwendung',
        # French (tertiary)
        'produit', 'lancement', 'projet', 'développement', 'solution', 'service',
        # Italian (tertiary)
        'prodotto', 'lancio', 'progetto', 'sviluppo', 'soluzione', 'servizio'
    ],

    # Business Success & Results
    'Business & Success': [
        # English (primary)
        'quarter', 'revenue', 'growth', 'success', 'award', 'achievement',
        'partner', 'customer', 'client', 'contract', 'deal', 'expansion',
        'market', 'fiscal year', 'financial', 'profit', 'milestone', 'win',
        # German (secondary)
        'quartal', 'umsatz', 'wachstum', 'erfolg', 'auszeichnung', 'kunde',
        'vertrag', 'markt', 'geschäftsjahr', 'finanzen', 'gewinn',
        # French (tertiary)
        'trimestre', 'croissance', 'succès', 'récompense', 'client', 'marché',
        # Italian (tertiary)
        'trimestre', 'crescita', 'successo', 'premio', 'cliente', 'mercato'
    ],

    # Wellness & Work-Life Balance
    'Wellness & Benefits': [
        # English (primary)
        'health', 'wellness', 'wellbeing', 'sport', 'fitness', 'work-life balance',
        'flexible', 'remote work', 'home office', 'benefits', 'perks', 'yoga',
        'meditation', 'mental health', 'physical health', 'work from home', 'wfh',
        # German (secondary)
        'gesundheit', 'wohlbefinden', 'homeoffice', 'gesundheitstag',
        # French (tertiary)
        'santé', 'bien-être', 'équilibre', 'télétravail', 'flexibilité',
        # Italian (tertiary)
        'salute', 'benessere', 'equilibrio', 'lavoro remoto', 'flessibilità'
    ],

    # Organizational Change
    'Organizational Change': [
        # English (primary)
        'change', 'transformation', 'reorganization', 'restructuring', 'strategy',
        'leadership', 'management', 'new structure', 'process', 'optimization',
        'efficiency', 'transition', 'shift', 'realignment', 'org change',
        # German (secondary)
        'umstrukturierung', 'strategie', 'führung', 'neue struktur', 'änderung',
        'prozess', 'optimierung', 'effizienz', 'umstellung',
        # French (tertiary)
        'changement', 'restructuration', 'stratégie', 'direction', 'transformation',
        # Italian (tertiary)
        'cambiamento', 'ristrutturazione', 'strategia', 'trasformazione'
    ],

    # CSR & Sustainability
    'CSR & Sustainability': [
        # English (primary)
        'sustainability', 'sustainable', 'csr', 'environment', 'climate', 'green',
        'social responsibility', 'donation', 'charity', 'volunteering', 'volunteer',
        'ecological', 'eco-friendly', 'recycling', 'carbon', 'co2', 'net zero',
        'climate neutral', 'esg', 'impact', 'giving back',
        # German (secondary)
        'nachhaltigkeit', 'umwelt', 'klimaschutz', 'sozial', 'spende',
        'engagement', 'ökologisch', 'klimaneutral',
        # French (tertiary)
        'durabilité', 'environnement', 'climat', 'écologique', 'donation',
        # Italian (tertiary)
        'sostenibilità', 'ambiente', 'clima', 'ecologico', 'donazione'
    ],
}

# Output Einstellungen
OUTPUT_DIR = 'data/output'
INPUT_DIR = 'data/input'
GENERATE_VISUALIZATIONS = True
INCLUDE_STATISTICS = True

# Sprache
LANGUAGE = 'de'  # Deutsch
