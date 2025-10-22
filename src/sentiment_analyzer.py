"""
Sentiment Analyzer Modul
Koordiniert Sentiment-Analyse mit verschiedenen Backends
"""

import logging
from typing import Dict, List, Optional
import sys
sys.path.append('..')
from models.sentiment_model import LightweightSentimentAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """
    Sentiment Analyzer mit Fallback-Optionen
    Nutzt primär lightweight Model, mit Option für NLTK VADER
    """
    
    def __init__(self, use_vader: bool = False):
        """
        Initialisiert Sentiment Analyzer
        
        Args:
            use_vader: Ob VADER (NLTK) verwendet werden soll, falls verfügbar
        """
        self.use_vader = use_vader
        self.vader_analyzer = None
        self.lightweight_analyzer = LightweightSentimentAnalyzer()
        
        if use_vader:
            try:
                from nltk.sentiment.vader import SentimentIntensityAnalyzer
                import nltk
                try:
                    nltk.data.find('sentiment/vader_lexicon.zip')
                except LookupError:
                    logger.info("Lade VADER Lexicon...")
                    nltk.download('vader_lexicon', quiet=True)
                
                self.vader_analyzer = SentimentIntensityAnalyzer()
                logger.info("VADER Sentiment Analyzer aktiviert")
            except Exception as e:
                logger.warning(f"VADER nicht verfügbar: {e}, nutze Lightweight Model")
                self.use_vader = False
    
    def analyze_comment(self, comment: str) -> Dict:
        """
        Analysiert einen einzelnen Kommentar
        
        Args:
            comment: Kommentar-Text
            
        Returns:
            Sentiment-Analyse Ergebnis
        """
        if not comment or not isinstance(comment, str):
            return {
                'score': 0.0,
                'category': 'neutral',
                'method': 'none'
            }
        
        if self.use_vader and self.vader_analyzer:
            return self._analyze_with_vader(comment)
        else:
            result = self.lightweight_analyzer.analyze(comment)
            result['method'] = 'lightweight'
            return result
    
    def _analyze_with_vader(self, text: str) -> Dict:
        """
        Analysiert mit VADER
        
        Args:
            text: Input-Text
            
        Returns:
            Sentiment-Ergebnis
        """
        scores = self.vader_analyzer.polarity_scores(text)
        compound = scores['compound']
        
        # Kategorisiere basierend auf compound score
        if compound >= 0.5:
            category = 'very_positive'
        elif compound >= 0.05:
            category = 'positive'
        elif compound <= -0.5:
            category = 'very_negative'
        elif compound <= -0.05:
            category = 'negative'
        else:
            category = 'neutral'
        
        return {
            'score': round(compound, 3),
            'category': category,
            'positive_count': round(scores['pos'], 3),
            'negative_count': round(scores['neg'], 3),
            'neutral_count': round(scores['neu'], 3),
            'confidence': round(abs(compound), 3),
            'method': 'vader'
        }
    
    def analyze_comments_for_article(self, comments: List[str]) -> Dict:
        """
        Analysiert alle Kommentare für einen Artikel
        
        Args:
            comments: Liste von Kommentaren
            
        Returns:
            Aggregierte Sentiment-Analyse
        """
        if not comments:
            return {
                'total_comments': 0,
                'avg_score': 0.0,
                'sentiment_distribution': {},
                'comments_analysis': []
            }
        
        # Analysiere jeden Kommentar
        comments_results = []
        for comment in comments:
            result = self.analyze_comment(comment)
            result['comment_text'] = comment[:100]  # Nur erste 100 Zeichen speichern
            comments_results.append(result)
        
        # Aggregiere Ergebnisse
        scores = [r['score'] for r in comments_results]
        categories = [r['category'] for r in comments_results]
        
        # Sentiment-Verteilung
        sentiment_dist = {}
        for cat in categories:
            sentiment_dist[cat] = sentiment_dist.get(cat, 0) + 1
        
        # Durchschnitts-Score
        avg_score = sum(scores) / len(scores) if scores else 0
        
        # Gesamt-Kategorisierung
        if avg_score > 0.3:
            overall_category = 'very_positive'
        elif avg_score > 0.05:
            overall_category = 'positive'
        elif avg_score < -0.3:
            overall_category = 'very_negative'
        elif avg_score < -0.05:
            overall_category = 'negative'
        else:
            overall_category = 'neutral'
        
        return {
            'total_comments': len(comments),
            'avg_score': round(avg_score, 3),
            'median_score': round(sorted(scores)[len(scores) // 2], 3) if scores else 0,
            'min_score': round(min(scores), 3) if scores else 0,
            'max_score': round(max(scores), 3) if scores else 0,
            'overall_category': overall_category,
            'sentiment_distribution': sentiment_dist,
            'positive_ratio': round(sum(1 for c in categories if 'positive' in c) / len(categories), 3),
            'negative_ratio': round(sum(1 for c in categories if 'negative' in c) / len(categories), 3),
            'neutral_ratio': round(sum(1 for c in categories if c == 'neutral') / len(categories), 3),
            'comments_analysis': comments_results
        }
    
    def get_sentiment_summary(self, all_results: Dict[str, Dict]) -> Dict:
        """
        Erstellt eine Zusammenfassung über alle Artikel
        
        Args:
            all_results: Dictionary mit URL als Key und Analyse als Value
            
        Returns:
            Gesamt-Zusammenfassung
        """
        if not all_results:
            return {}
        
        total_comments = sum(r['total_comments'] for r in all_results.values())
        avg_scores = [r['avg_score'] for r in all_results.values() if r['total_comments'] > 0]
        
        # Beste und schlechteste Artikel
        sorted_by_sentiment = sorted(
            [(url, r['avg_score']) for url, r in all_results.items() if r['total_comments'] > 0],
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            'total_articles': len(all_results),
            'total_comments': total_comments,
            'avg_comments_per_article': round(total_comments / len(all_results), 2),
            'overall_avg_sentiment': round(sum(avg_scores) / len(avg_scores), 3) if avg_scores else 0,
            'top_5_positive_articles': sorted_by_sentiment[:5],
            'top_5_negative_articles': sorted_by_sentiment[-5:],
            'articles_by_category': self._categorize_articles_by_sentiment(all_results)
        }
    
    def _categorize_articles_by_sentiment(self, all_results: Dict[str, Dict]) -> Dict:
        """Kategorisiert Artikel nach Sentiment"""
        categories = {
            'very_positive': [],
            'positive': [],
            'neutral': [],
            'negative': [],
            'very_negative': []
        }
        
        for url, result in all_results.items():
            if result['total_comments'] > 0:
                category = result['overall_category']
                categories[category].append(url)
        
        return {cat: len(urls) for cat, urls in categories.items()}


if __name__ == "__main__":
    # Test
    analyzer = SentimentAnalyzer()
    test_comments = [
        "Super Artikel, sehr hilfreich!",
        "Leider sehr schlecht geschrieben.",
        "Ganz okay."
    ]
    
    result = analyzer.analyze_comments_for_article(test_comments)
    print(f"Analyse: {result}")
