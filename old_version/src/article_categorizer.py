"""
Article Categorizer Modul
Kategorisiert Artikel basierend auf Inhalt und Sentiment
"""

import logging
from typing import Dict, List, Set
import re
import sys
sys.path.append('..')
from config.settings import CATEGORY_KEYWORDS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ArticleCategorizer:
    """Kategorisiert Artikel nach Thema und Sentiment"""
    
    def __init__(self, custom_keywords: Dict[str, List[str]] = None):
        """
        Initialisiert den Categorizer
        
        Args:
            custom_keywords: Optionale benutzerdefinierte Kategorie-Keywords
        """
        self.category_keywords = custom_keywords or CATEGORY_KEYWORDS
        logger.info(f"Categorizer initialisiert mit {len(self.category_keywords)} Kategorien")
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """
        Extrahiert Keywords aus Text
        
        Args:
            text: Input-Text
            top_n: Anzahl Top-Keywords
            
        Returns:
            Liste von Keywords
        """
        if not text:
            return []
        
        # Stopwords (erweiterte deutsche Liste)
        stopwords = {
            'der', 'die', 'das', 'und', 'ist', 'in', 'zu', 'den', 'von',
            'mit', 'auf', 'für', 'eine', 'ein', 'als', 'sich', 'nicht',
            'im', 'werden', 'an', 'oder', 'auch', 'dem', 'des', 'bei',
            'um', 'zum', 'zur', 'durch', 'aus', 'sind', 'am', 'kann',
            'wird', 'hat', 'haben', 'wurde', 'wird', 'sein', 'alle',
            'dieser', 'diese', 'dieses', 'wenn', 'dann', 'aber', 'über',
            'nach', 'vor', 'mehr', 'noch', 'nur', 'hier', 'dort', 'wie',
            'was', 'wer', 'wo', 'wann', 'warum', 'welche', 'welcher',
        }
        
        # Text preprocessen
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        
        words = text.split()
        words = [w for w in words if len(w) > 3 and w not in stopwords]
        
        # Häufigkeit zählen
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Nach Häufigkeit sortieren
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        return [word for word, freq in sorted_words[:top_n]]
    
    def categorize_by_content(self, title: str, content: str) -> Dict[str, float]:
        """
        Kategorisiert Artikel basierend auf Inhalt
        
        Args:
            title: Artikel-Titel
            content: Artikel-Inhalt
            
        Returns:
            Dictionary mit Kategorien und Confidence-Scores
        """
        # Kombiniere Titel (gewichtet) und Content
        full_text = (title + ' ' + title + ' ' + content).lower()
        
        category_scores = {}
        
        for category, keywords in self.category_keywords.items():
            score = 0
            for keyword in keywords:
                # Zähle Vorkommen des Keywords
                count = len(re.findall(r'\b' + keyword + r'\b', full_text))
                score += count
            
            # Normalisiere Score
            if score > 0:
                category_scores[category] = score
        
        # Normalisiere auf 0-1 Skala
        total_score = sum(category_scores.values())
        if total_score > 0:
            category_scores = {
                cat: round(score / total_score, 3) 
                for cat, score in category_scores.items()
            }
        
        return category_scores
    
    def get_primary_category(self, category_scores: Dict[str, float]) -> str:
        """
        Ermittelt Hauptkategorie
        
        Args:
            category_scores: Dictionary mit Kategorie-Scores
            
        Returns:
            Primäre Kategorie
        """
        if not category_scores:
            return 'Sonstiges'
        
        return max(category_scores.items(), key=lambda x: x[1])[0]
    
    def categorize_article(
        self, 
        url: str,
        title: str, 
        content: str,
        sentiment_data: Dict
    ) -> Dict:
        """
        Vollständige Kategorisierung eines Artikels
        
        Args:
            url: Artikel-URL
            title: Artikel-Titel
            content: Artikel-Inhalt
            sentiment_data: Sentiment-Analyse-Daten
            
        Returns:
            Vollständige Kategorisierung
        """
        # Inhaltliche Kategorisierung
        category_scores = self.categorize_by_content(title, content)
        primary_category = self.get_primary_category(category_scores)
        
        # Extrahiere Keywords
        keywords = self.extract_keywords(title + ' ' + content, top_n=5)
        
        # Sentiment-Kategorie
        sentiment_category = sentiment_data.get('overall_category', 'neutral')
        avg_sentiment = sentiment_data.get('avg_score', 0.0)
        
        return {
            'url': url,
            'title': title,
            'primary_category': primary_category,
            'category_scores': category_scores,
            'keywords': keywords,
            'sentiment_category': sentiment_category,
            'avg_sentiment_score': avg_sentiment,
            'total_comments': sentiment_data.get('total_comments', 0),
            'positive_ratio': sentiment_data.get('positive_ratio', 0),
            'negative_ratio': sentiment_data.get('negative_ratio', 0),
            'sentiment_distribution': sentiment_data.get('sentiment_distribution', {}),
        }
    
    def analyze_category_sentiment_correlation(
        self, 
        categorized_articles: List[Dict]
    ) -> Dict:
        """
        Analysiert Korrelation zwischen Artikel-Kategorie und Sentiment
        
        Args:
            categorized_articles: Liste von kategorisierten Artikeln
            
        Returns:
            Korrelations-Analyse
        """
        category_sentiments = {}
        
        for article in categorized_articles:
            category = article['primary_category']
            sentiment = article['avg_sentiment_score']
            
            if category not in category_sentiments:
                category_sentiments[category] = []
            
            category_sentiments[category].append(sentiment)
        
        # Berechne Durchschnitte
        category_avg_sentiments = {}
        for category, sentiments in category_sentiments.items():
            if sentiments:
                category_avg_sentiments[category] = {
                    'avg_sentiment': round(sum(sentiments) / len(sentiments), 3),
                    'min_sentiment': round(min(sentiments), 3),
                    'max_sentiment': round(max(sentiments), 3),
                    'article_count': len(sentiments),
                    'positive_articles': sum(1 for s in sentiments if s > 0.05),
                    'negative_articles': sum(1 for s in sentiments if s < -0.05),
                    'neutral_articles': sum(1 for s in sentiments if -0.05 <= s <= 0.05),
                }
        
        # Sortiere nach durchschnittlichem Sentiment
        sorted_categories = sorted(
            category_avg_sentiments.items(),
            key=lambda x: x[1]['avg_sentiment'],
            reverse=True
        )
        
        return {
            'category_sentiment_stats': category_avg_sentiments,
            'best_performing_categories': [cat for cat, _ in sorted_categories[:3]],
            'worst_performing_categories': [cat for cat, _ in sorted_categories[-3:]],
            'total_categories': len(category_avg_sentiments),
        }
    
    def generate_insights(
        self, 
        categorized_articles: List[Dict],
        correlation_analysis: Dict
    ) -> List[str]:
        """
        Generiert Insights aus der Analyse
        
        Args:
            categorized_articles: Liste von kategorisierten Artikeln
            correlation_analysis: Korrelations-Analyse
            
        Returns:
            Liste von Insight-Strings
        """
        insights = []
        
        # Best/Worst Categories
        best_cats = correlation_analysis.get('best_performing_categories', [])
        worst_cats = correlation_analysis.get('worst_performing_categories', [])
        
        if best_cats:
            insights.append(
                f"Kategorien mit positivstem Feedback: {', '.join(best_cats)}"
            )
        
        if worst_cats:
            insights.append(
                f"Kategorien mit negativstem Feedback: {', '.join(worst_cats)}"
            )
        
        # Sentiment-Verteilung
        stats = correlation_analysis.get('category_sentiment_stats', {})
        for category, data in stats.items():
            if data['article_count'] >= 3:  # Nur bei genug Artikeln
                ratio = data['positive_articles'] / data['article_count']
                if ratio > 0.7:
                    insights.append(
                        f"Kategorie '{category}': Überwiegend positives Feedback "
                        f"({data['positive_articles']}/{data['article_count']} Artikel)"
                    )
                elif ratio < 0.3:
                    insights.append(
                        f"Kategorie '{category}': Überwiegend negatives Feedback "
                        f"({data['negative_articles']}/{data['article_count']} Artikel)"
                    )
        
        return insights


if __name__ == "__main__":
    # Test
    categorizer = ArticleCategorizer()
    print("ArticleCategorizer Modul bereit")
