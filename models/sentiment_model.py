"""
Lightweight Sentiment Model
Sentiment-Analyse ohne externe LLM-Dependencies
"""

import re
from typing import Dict, List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LightweightSentimentAnalyzer:
    """
    Minimales Sentiment-Analyse-Modell ohne externe Dependencies
    Nutzt Sentiment-Wörterbücher für deutsche Sprache
    """
    
    def __init__(self):
        """Initialisiert das Sentiment Model"""
        self.positive_words = set()
        self.negative_words = set()
        self.intensifiers = set()
        self.negations = set()
        self.load_lexicons()
    
    def load_lexicons(self):
        """Lädt Sentiment-Wörterbücher"""
        
        # Positive Wörter (Deutsch)
        self.positive_words = {
            # Allgemein positiv
            'gut', 'super', 'toll', 'exzellent', 'hervorragend', 'ausgezeichnet',
            'fantastisch', 'großartig', 'wunderbar', 'prima', 'perfekt',
            'spitze', 'klasse', 'genial', 'brillant', 'ideal',
            
            # Zustimmung
            'richtig', 'korrekt', 'passend', 'angemessen', 'treffend',
            'zustimmen', 'einverstanden', 'genau', 'absolut',
            
            # Qualität
            'hilfreich', 'nützlich', 'wertvoll', 'wichtig', 'interessant',
            'informativ', 'aufschlussreich', 'lehrreich', 'konstruktiv',
            'produktiv', 'effektiv', 'effizient', 'erfolgreich',
            
            # Klarheit
            'klar', 'verständlich', 'deutlich', 'transparent', 'eindeutig',
            'übersichtlich', 'strukturiert', 'nachvollziehbar',
            
            # Emotion positiv
            'freuen', 'freude', 'gefallen', 'mögen', 'lieben', 'begeistert',
            'erfreut', 'glücklich', 'zufrieden', 'dankbar', 'angenehm',
            'positiv', 'optimistisch', 'hoffnungsvoll',
            
            # Lob
            'loben', 'anerkennen', 'würdigen', 'schätzen', 'respektieren',
            'empfehlen', 'unterstützen', 'befürworten',
            
            # Verbesserung
            'verbessern', 'besser', 'fortschritt', 'entwicklung', 'innovation',
            'modern', 'aktuell', 'zeitgemäß', 'zukunftsorientiert',
        }
        
        # Negative Wörter (Deutsch)
        self.negative_words = {
            # Allgemein negativ
            'schlecht', 'schrecklich', 'furchtbar', 'katastrophal', 'miserabel',
            'entsetzlich', 'grauenhaft', 'verheerend', 'desaströs',
            
            # Ablehnung
            'falsch', 'inkorrekt', 'unpassend', 'unangemessen', 'ablehnen',
            'widersprechen', 'dagegen', 'kontra',
            
            # Qualität negativ
            'unnütz', 'nutzlos', 'wertlos', 'unwichtig', 'langweilig',
            'uninteressant', 'überflüssig', 'sinnlos', 'destruktiv',
            'ineffektiv', 'ineffizient', 'erfolglos', 'gescheitert',
            
            # Unklarheit
            'unklar', 'unverständlich', 'undeutlich', 'intransparent',
            'verwirrend', 'chaotisch', 'unübersichtlich', 'kompliziert',
            
            # Emotion negativ
            'ärger', 'wut', 'enttäuscht', 'enttäuschung', 'frustration',
            'frustriert', 'verärgert', 'unzufrieden', 'unglücklich',
            'traurig', 'negativ', 'pessimistisch', 'hoffnungslos',
            
            # Kritik
            'kritisieren', 'bemängeln', 'beanstanden', 'monieren',
            'tadeln', 'missbilligen', 'ablehnen',
            
            # Probleme
            'problem', 'fehler', 'mangel', 'schwäche', 'defizit',
            'versagen', 'scheitern', 'schwierig', 'schwierigkeit',
            'hindernis', 'barriere', 'risiko', 'gefahr',
            
            # Verschlechterung
            'verschlechtern', 'schlechter', 'rückschritt', 'veraltet',
            'überholt', 'antiquiert', 'rückständig',
        }
        
        # Verstärker
        self.intensifiers = {
            'sehr', 'extrem', 'besonders', 'außerordentlich', 'äußerst',
            'höchst', 'überaus', 'total', 'absolut', 'völlig', 'komplett',
            'wirklich', 'echt', 'richtig', 'ziemlich', 'erheblich',
        }
        
        # Negationen
        self.negations = {
            'nicht', 'kein', 'keine', 'keinen', 'niemals', 'nie',
            'nichts', 'niemand', 'nirgends', 'weder', 'ohne',
        }
        
        logger.info(f"Lexikon geladen: {len(self.positive_words)} positive, "
                   f"{len(self.negative_words)} negative Wörter")
    
    def preprocess_text(self, text: str) -> List[str]:
        """
        Bereitet Text für Analyse vor
        
        Args:
            text: Input-Text
            
        Returns:
            Liste von Tokens
        """
        if not text or not isinstance(text, str):
            return []
        
        # Kleinbuchstaben
        text = text.lower()
        
        # Entferne URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Entferne Sonderzeichen, behalte aber Satzzeichen für Kontext
        text = re.sub(r'[^\w\s.,!?]', ' ', text)
        
        # Tokenisierung
        tokens = text.split()
        
        return tokens
    
    def analyze(self, text: str) -> Dict[str, float]:
        """
        Führt Sentiment-Analyse durch
        
        Args:
            text: Zu analysierender Text
            
        Returns:
            Dictionary mit Sentiment-Scores und Kategorien
        """
        tokens = self.preprocess_text(text)
        
        if not tokens:
            return {
                'score': 0.0,
                'category': 'neutral',
                'positive_count': 0,
                'negative_count': 0,
                'confidence': 0.0
            }
        
        positive_count = 0
        negative_count = 0
        intensity_multiplier = 1.0
        negation_active = False
        
        for i, token in enumerate(tokens):
            # Prüfe auf Negation
            if token in self.negations:
                negation_active = True
                continue
            
            # Prüfe auf Verstärker
            if token in self.intensifiers:
                intensity_multiplier = 1.5
                continue
            
            # Prüfe auf Sentiment-Wörter
            if token in self.positive_words:
                score = intensity_multiplier
                if negation_active:
                    score = -score
                    negative_count += abs(score)
                else:
                    positive_count += score
                    
            elif token in self.negative_words:
                score = intensity_multiplier
                if negation_active:
                    score = -score
                    positive_count += abs(score)
                else:
                    negative_count += score
            
            # Reset nach jedem Sentiment-Wort
            intensity_multiplier = 1.0
            negation_active = False
        
        # Berechne Gesamt-Score
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            score = 0.0
            confidence = 0.0
        else:
            score = (positive_count - negative_count) / total_sentiment_words
            # Confidence basierend auf Anzahl Sentiment-Wörter
            confidence = min(total_sentiment_words / len(tokens), 1.0)
        
        # Kategorisiere
        if score > 0.5:
            category = 'very_positive'
        elif score > 0.1:
            category = 'positive'
        elif score < -0.5:
            category = 'very_negative'
        elif score < -0.1:
            category = 'negative'
        else:
            category = 'neutral'
        
        return {
            'score': round(score, 3),
            'category': category,
            'positive_count': round(positive_count, 2),
            'negative_count': round(negative_count, 2),
            'confidence': round(confidence, 3),
            'total_tokens': len(tokens)
        }
    
    def analyze_batch(self, texts: List[str]) -> List[Dict]:
        """
        Analysiert mehrere Texte
        
        Args:
            texts: Liste von Texten
            
        Returns:
            Liste von Sentiment-Ergebnissen
        """
        return [self.analyze(text) for text in texts]
    
    def get_aggregate_sentiment(self, texts: List[str]) -> Dict[str, float]:
        """
        Berechnet aggregiertes Sentiment über mehrere Texte
        
        Args:
            texts: Liste von Texten
            
        Returns:
            Aggregiertes Sentiment
        """
        if not texts:
            return {
                'avg_score': 0.0,
                'median_score': 0.0,
                'total_texts': 0,
                'positive_ratio': 0.0,
                'negative_ratio': 0.0,
                'neutral_ratio': 0.0
            }
        
        results = self.analyze_batch(texts)
        scores = [r['score'] for r in results]
        categories = [r['category'] for r in results]
        
        return {
            'avg_score': round(sum(scores) / len(scores), 3),
            'median_score': round(sorted(scores)[len(scores) // 2], 3),
            'total_texts': len(texts),
            'positive_ratio': round(sum(1 for c in categories if 'positive' in c) / len(categories), 3),
            'negative_ratio': round(sum(1 for c in categories if 'negative' in c) / len(categories), 3),
            'neutral_ratio': round(sum(1 for c in categories if c == 'neutral') / len(categories), 3),
        }


if __name__ == "__main__":
    # Test
    analyzer = LightweightSentimentAnalyzer()
    
    test_texts = [
        "Das ist ein sehr guter Artikel! Super hilfreich und informativ.",
        "Leider sehr schlecht erklärt und unverständlich.",
        "Ganz okay, nichts Besonderes.",
    ]
    
    for text in test_texts:
        result = analyzer.analyze(text)
        print(f"\nText: {text}")
        print(f"Score: {result['score']}, Kategorie: {result['category']}")
