"""
Erweiterte Hauptprogramm mit LLM Sentiment-Analyse und Clustering

Verwendet das bessere BERT-Model aus LLM Solution für höhere Genauigkeit.
Fügt Artikel-Clustering hinzu um ähnliche Artikel zu gruppieren.

Verwendung:
    python main_with_llm.py --input data/input/ihre_datei.xlsx
"""

import argparse
import logging
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

# Füge LLM Solution zum Path hinzu
sys.path.insert(0, str(Path(__file__).parent / "LLM Solution"))

# Importiere Standard-Module
from src.data_loader import DataLoader
from src.web_scraper import WebScraper
from src.article_categorizer import ArticleCategorizer
from src.report_generator import ReportGenerator
from config.settings import INPUT_DIR, OUTPUT_DIR

# Importiere LLM Analyzer
try:
    from offline_sentiment_analyzer import OfflineSentimentAnalyzer
    LLM_AVAILABLE = True
except ImportError:
    print("⚠️  LLM Solution nicht verfügbar, verwende Standard-Analyzer")
    from models.sentiment_model import LightweightSentimentAnalyzer
    LLM_AVAILABLE = False

# Importiere Topic Discovery
try:
    from topic_discovery import TopicDiscovery
    TOPIC_DISCOVERY_AVAILABLE = True
except ImportError:
    print("⚠️  Topic Discovery nicht verfügbar")
    TOPIC_DISCOVERY_AVAILABLE = False

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sentiment_analysis_llm.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class EnhancedSentimentAnalyzer:
    """
    Erweiterte Sentiment-Analyse mit LLM-Model
    """

    def __init__(self, use_llm: bool = True):
        """
        Initialisiert den Analyzer

        Args:
            use_llm: Verwende LLM-Model wenn verfügbar
        """
        logger.info("Initialisiere Enhanced Sentiment Analyzer...")

        if use_llm and LLM_AVAILABLE:
            logger.info("Lade LLM Model (kann ~60s dauern)...")
            self.analyzer = OfflineSentimentAnalyzer()
            self.mode = self.analyzer.mode
            logger.info(f"✓ LLM Model geladen (Mode: {self.mode})")
        else:
            logger.info("Verwende Standard Lightweight Analyzer")
            self.analyzer = LightweightSentimentAnalyzer()
            self.mode = 'lightweight'

    def analyze_comments(self, comments: list) -> list:
        """
        Analysiert Liste von Kommentaren

        Args:
            comments: Liste von Kommentar-Texten

        Returns:
            Liste von Sentiment-Ergebnissen
        """
        if not comments:
            return []

        logger.info(f"Analysiere {len(comments)} Kommentare mit {self.mode} Model...")

        # Batch-Analyse für bessere Performance
        if hasattr(self.analyzer, 'analyze_batch'):
            results = self.analyzer.analyze_batch(comments)
        else:
            # Fallback auf einzelne Analysen
            results = [self.analyzer.analyze(comment) for comment in comments]

        logger.info(f"✓ {len(results)} Kommentare analysiert")
        return results


class ArticleClusterer:
    """
    Clustert Artikel basierend auf Inhalt und Keywords
    """

    def __init__(self):
        """Initialisiert den Clusterer"""
        logger.info("Initialisiere Article Clusterer...")

    def cluster_articles(self, articles_df: pd.DataFrame) -> pd.DataFrame:
        """
        Clustert Artikel in thematische Gruppen

        Args:
            articles_df: DataFrame mit Artikeln (muss 'content', 'keywords' haben)

        Returns:
            DataFrame mit zusätzlicher 'cluster' Spalte
        """
        if articles_df.empty:
            return articles_df

        logger.info(f"Clustere {len(articles_df)} Artikel...")

        # Einfaches Keyword-basiertes Clustering
        # (In Produktion: Verwende TF-IDF + K-Means oder DBSCAN)

        clusters = []
        for idx, row in articles_df.iterrows():
            keywords_str = row.get('keywords', '')
            category = row.get('category', 'Unknown')

            # Cluster-ID basierend auf Hauptkategorie + dominantes Keyword
            # keywords is now a comma-separated string, so split it
            if keywords_str:
                keywords_list = [k.strip() for k in keywords_str.split(',')]
                cluster_id = f"{category}_{keywords_list[0]}"
            else:
                cluster_id = f"{category}_general"

            clusters.append(cluster_id)

        articles_df['cluster'] = clusters

        # Zähle Artikel pro Cluster
        cluster_counts = articles_df['cluster'].value_counts()
        logger.info(f"✓ {len(cluster_counts)} Cluster gefunden")

        for cluster, count in cluster_counts.head(5).items():
            logger.info(f"  - {cluster}: {count} Artikel")

        return articles_df

    def get_cluster_insights(self, articles_df: pd.DataFrame) -> dict:
        """
        Analysiert Cluster und gibt Insights zurück

        Args:
            articles_df: DataFrame mit Artikeln und 'cluster', 'avg_sentiment'

        Returns:
            Dictionary mit Cluster-Insights
        """
        if 'cluster' not in articles_df.columns:
            return {}

        insights = {}

        for cluster in articles_df['cluster'].unique():
            cluster_articles = articles_df[articles_df['cluster'] == cluster]

            avg_sentiment = cluster_articles['avg_sentiment'].mean() if 'avg_sentiment' in cluster_articles else 0
            article_count = len(cluster_articles)

            insights[cluster] = {
                'count': article_count,
                'avg_sentiment': round(avg_sentiment, 3),
                'category': cluster_articles['category'].mode()[0] if 'category' in cluster_articles else 'Unknown'
            }

        # Sortiere nach Sentiment
        insights = dict(sorted(
            insights.items(),
            key=lambda x: x[1]['avg_sentiment'],
            reverse=True
        ))

        return insights


def parse_arguments():
    """Parse Kommandozeilen-Argumente"""
    parser = argparse.ArgumentParser(
        description='Erweiterte Sentiment-Analyse mit LLM und Clustering'
    )

    parser.add_argument(
        '--input',
        type=str,
        help='Pfad zur Input Excel-Datei',
        default=None
    )

    parser.add_argument(
        '--url-column',
        type=str,
        default='A',
        help='Spalte mit URLs (Standard: A)'
    )

    parser.add_argument(
        '--comment-column',
        type=str,
        default='B',
        help='Spalte mit Kommentaren (Standard: B)'
    )

    parser.add_argument(
        '--no-llm',
        action='store_true',
        help='Verwende Standard-Analyzer statt LLM'
    )

    parser.add_argument(
        '--no-scraping',
        action='store_true',
        help='Überspringe Web Scraping'
    )

    parser.add_argument(
        '--no-clustering',
        action='store_true',
        help='Überspringe Artikel-Clustering'
    )

    parser.add_argument(
        '--use-predefined',
        action='store_true',
        help='Verwende vordefinierte Kategorien statt automatische Themen-Entdeckung'
    )

    parser.add_argument(
        '--num-topics',
        type=int,
        default=None,
        help='Fixe Anzahl Themen (überschreibt Auto-Optimierung, nur mit --manual-topics)'
    )

    parser.add_argument(
        '--manual-topics',
        action='store_true',
        help='Verwende fixe Anzahl Themen statt Auto-Optimierung (benötigt --num-topics)'
    )

    return parser.parse_args()


def get_sentiment_rating(score: float) -> str:
    """
    Convert sentiment score to human-readable rating for stakeholders.

    Args:
        score: Sentiment score from -1.0 to +1.0

    Returns:
        Rating string (Excellent, Very Good, Good, Fair, Poor, Very Poor)
    """
    if score >= 0.6:
        return "⭐⭐⭐⭐⭐ Excellent"
    elif score >= 0.4:
        return "⭐⭐⭐⭐ Very Good"
    elif score >= 0.2:
        return "⭐⭐⭐ Good"
    elif score >= 0.0:
        return "⭐⭐ Fair"
    elif score >= -0.2:
        return "⭐ Poor"
    else:
        return "❌ Very Poor"


def find_input_file():
    """Sucht nach Input-Datei im Input-Verzeichnis"""
    input_path = Path(INPUT_DIR)

    if not input_path.exists():
        return None

    excel_files = list(input_path.glob('*.xlsx')) + list(input_path.glob('*.xls'))

    if not excel_files:
        return None

    newest_file = max(excel_files, key=lambda p: p.stat().st_mtime)
    return str(newest_file)


def main():
    """Hauptfunktion"""
    logger.info("="*80)
    logger.info("  ERWEITERTE SENTIMENT-ANALYSE mit LLM & CLUSTERING")
    logger.info("="*80)

    # Parse Argumente
    args = parse_arguments()

    # Finde Input-Datei
    input_file = args.input or find_input_file()

    if not input_file:
        logger.error("❌ Keine Input-Datei gefunden!")
        logger.info("Bitte lege eine Excel-Datei in data/input/ ab")
        logger.info("Oder verwende: --input pfad/zur/datei.xlsx")
        return 1

    logger.info(f"Input-Datei: {input_file}")

    # 1. Lade Daten
    logger.info("\n[1/6] Lade Daten aus Excel...")
    data_loader = DataLoader(input_file)
    data = data_loader.load_excel(args.url_column, args.comment_column)

    if data.empty:
        logger.error("❌ Keine Daten geladen!")
        return 1

    logger.info(f"✓ {len(data)} Zeilen geladen")

    # Gruppiere nach URL
    grouped_data = data.groupby('url').agg({
        'comment': list
    }).reset_index()

    logger.info(f"✓ {len(grouped_data)} unique Artikel gefunden")

    # 2. Scrape Artikel-Inhalte
    articles = []
    if not args.no_scraping:
        logger.info("\n[2/6] Scrape Artikel-Inhalte...")
        scraper = WebScraper()

        for idx, row in grouped_data.iterrows():
            url = row['url']
            logger.info(f"  Scraping {idx+1}/{len(grouped_data)}: {url}")

            article_data = scraper.scrape_url(url)
            article_data['url'] = url
            article_data['comments'] = row['comment']
            articles.append(article_data)

        logger.info(f"✓ {len(articles)} Artikel gescraped")
    else:
        logger.info("\n[2/6] Scraping übersprungen")
        for idx, row in grouped_data.iterrows():
            articles.append({
                'url': row['url'],
                'title': 'N/A',
                'content': '',
                'comments': row['comment']
            })

    # Konvertiere zu DataFrame
    articles_df = pd.DataFrame(articles)

    # 3. Sentiment-Analyse der Kommentare
    logger.info("\n[3/6] Sentiment-Analyse der Kommentare...")
    sentiment_analyzer = EnhancedSentimentAnalyzer(use_llm=not args.no_llm)

    all_sentiments = []
    for idx, row in articles_df.iterrows():
        comments = row['comments']

        # Analysiere Kommentare
        sentiments = sentiment_analyzer.analyze_comments(comments)

        # Berechne Durchschnitt
        if sentiments:
            avg_score = sum(s.get('score', 0) for s in sentiments) / len(sentiments)
            sentiment_counts = {
                'positive': sum(1 for s in sentiments if s.get('category') == 'positive'),
                'negative': sum(1 for s in sentiments if s.get('category') == 'negative'),
                'neutral': sum(1 for s in sentiments if s.get('category') == 'neutral')
            }
        else:
            avg_score = 0
            sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}

        articles_df.at[idx, 'avg_sentiment'] = avg_score
        articles_df.at[idx, 'positive_count'] = sentiment_counts['positive']
        articles_df.at[idx, 'negative_count'] = sentiment_counts['negative']
        articles_df.at[idx, 'neutral_count'] = sentiment_counts['neutral']
        articles_df.at[idx, 'total_comments'] = len(comments)

    logger.info(f"✓ Sentiment-Analyse abgeschlossen")
    logger.info(f"  Durchschnittliches Sentiment: {articles_df['avg_sentiment'].mean():.3f}")

    # 4. Kategorisiere Artikel nach INHALTS-THEMEN
    if args.use_predefined:
        # SUPERVISED: Verwende vordefinierte Kategorien
        logger.info("\n[4/6] Kategorisiere Artikel nach Content-Themen (SUPERVISED)...")
        logger.info("      (Verwendet vordefinierte Kategorien: AI & Innovation, Employee Stories, etc.)")
        categorizer = ArticleCategorizer()

        for idx, row in articles_df.iterrows():
            title = row.get('title', '')
            content = row.get('content', '')

            # Kategorisiere nach Inhalt
            category_scores = categorizer.categorize_by_content(title, content)
            primary_category = categorizer.get_primary_category(category_scores)
            keywords = categorizer.extract_keywords(title + ' ' + content, top_n=5)

            articles_df.at[idx, 'category'] = primary_category
            # Store keywords as comma-separated string for pandas compatibility
            articles_df.at[idx, 'keywords'] = ', '.join(keywords) if keywords else ''

        logger.info(f"✓ Kategorisierung abgeschlossen")
        logger.info("\nContent-Themen Verteilung:")
        category_counts = articles_df['category'].value_counts()
        for cat, count in category_counts.head(10).items():
            logger.info(f"  - {cat}: {count} Artikel")

    elif TOPIC_DISCOVERY_AVAILABLE:
        # UNSUPERVISED: Entdecke Themen automatisch (DEFAULT!)

        # Determine if auto-optimization should be used
        if args.manual_topics:
            # Manual mode: user specifies exact number
            num_topics = args.num_topics if args.num_topics else 10
            auto_optimize = False
            logger.info(f"\n[4/6] Entdecke {num_topics} Themen (MANUELL)...")
            logger.info("      (Fixe Anzahl Themen)")
        else:
            # Auto-optimize mode (DEFAULT)
            num_topics = 10  # Fallback, will be ignored
            auto_optimize = True
            logger.info(f"\n[4/6] Entdecke optimale Anzahl Themen automatisch (AUTO-OPTIMIERT - DEFAULT)...")
            logger.info("      (Verwendet Silhouette Score - testet k=2 bis k=10)")

        logger.info("      (Keine vordefinierten Kategorien - entdeckt was Artikel tatsächlich behandeln)")
        logger.info("      (Verwende --use-predefined für vordefinierte Kategorien)")

        discoverer = TopicDiscovery(
            num_topics=num_topics,
            min_articles_per_topic=2,
            auto_optimize=auto_optimize
        )

        # Prepare articles for topic discovery
        articles_list = []
        for idx, row in articles_df.iterrows():
            articles_list.append({
                'title': row.get('title', ''),
                'content': row.get('content', ''),
                'avg_sentiment': row.get('avg_sentiment', 0),
            })

        # Discover topics
        topic_results = discoverer.discover_topics(articles_list, text_field='content')

        # Assign discovered topics to articles
        for idx, topic_id in enumerate(topic_results['topic_assignments']):
            topic_name = topic_results['topic_names'].get(topic_id, f'Topic {topic_id}')
            keywords_list = topic_results['topic_keywords'].get(topic_id, [])

            articles_df.at[idx, 'category'] = topic_name
            # Store keywords as comma-separated string instead of list (pandas compatibility)
            articles_df.at[idx, 'keywords'] = ', '.join(keywords_list) if keywords_list else ''

        logger.info(f"✓ {len(topic_results['valid_topics'])} Themen entdeckt")
        logger.info(f"  Silhouette Score: {topic_results['silhouette_score']:.3f}")

        if auto_optimize and topic_results.get('silhouette_scores_by_k'):
            logger.info("\nSilhouette Scores pro Cluster-Anzahl:")
            for k, score in sorted(topic_results['silhouette_scores_by_k'].items()):
                marker = " ← OPTIMAL" if k == topic_results['num_topics'] else ""
                logger.info(f"  k={k}: {score:.3f}{marker}")

        logger.info("\nEntdeckte Themen:")
        for topic_id, topic_name in topic_results['valid_topics'].items():
            count = topic_results['topic_sizes'][topic_id]
            keywords = ', '.join(topic_results['topic_keywords'][topic_id][:3])
            logger.info(f"  - {topic_name}: {count} Artikel ({keywords})")

    else:
        # Fallback to supervised if topic discovery not available
        logger.warning("⚠️  Topic Discovery nicht verfügbar, verwende vordefinierte Kategorien")
        logger.info("\n[4/6] Kategorisiere Artikel nach Content-Themen (SUPERVISED - FALLBACK)...")
        categorizer = ArticleCategorizer()

        for idx, row in articles_df.iterrows():
            title = row.get('title', '')
            content = row.get('content', '')

            category_scores = categorizer.categorize_by_content(title, content)
            primary_category = categorizer.get_primary_category(category_scores)
            keywords = categorizer.extract_keywords(title + ' ' + content, top_n=5)

            articles_df.at[idx, 'category'] = primary_category
            # Store keywords as comma-separated string for pandas compatibility
            articles_df.at[idx, 'keywords'] = ', '.join(keywords) if keywords else ''

        logger.info(f"✓ Kategorisierung abgeschlossen")
        category_counts = articles_df['category'].value_counts()
        for cat, count in category_counts.head(10).items():
            logger.info(f"  - {cat}: {count} Artikel")

    # 5. Cluster Artikel
    if not args.no_clustering:
        logger.info("\n[5/6] Clustere Artikel...")
        clusterer = ArticleClusterer()
        articles_df = clusterer.cluster_articles(articles_df)

        # Cluster-Insights
        cluster_insights = clusterer.get_cluster_insights(articles_df)

        logger.info("\nTop Cluster nach Sentiment:")
        for cluster, info in list(cluster_insights.items())[:5]:
            logger.info(f"  {cluster}: {info['count']} Artikel, "
                       f"Sentiment: {info['avg_sentiment']:+.3f}")
    else:
        logger.info("\n[5/6] Clustering übersprungen")

    # 6. Erstelle Reports
    logger.info("\n[6/6] Erstelle Reports...")

    # Timestamp für Dateinamen
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Detaillierter Report
    output_file = Path(OUTPUT_DIR) / f"llm_analysis_{timestamp}.xlsx"

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Sheet 1: Articles Overview
        articles_summary = articles_df[[
            'url', 'title', 'category', 'cluster',
            'avg_sentiment', 'total_comments',
            'positive_count', 'negative_count', 'neutral_count'
        ]].copy()

        # Add Rating column for stakeholders
        articles_summary['Rating'] = articles_summary['avg_sentiment'].apply(get_sentiment_rating)

        # Reorder columns to put Rating right after avg_sentiment
        cols = ['url', 'title', 'category', 'cluster', 'avg_sentiment', 'Rating',
                'total_comments', 'positive_count', 'negative_count', 'neutral_count']
        articles_summary = articles_summary[cols]

        articles_summary = articles_summary.sort_values('avg_sentiment', ascending=False)
        articles_summary.to_excel(writer, sheet_name='Articles', index=False)

        # Sheet 2: Category Analysis
        category_analysis = articles_df.groupby('category').agg({
            'avg_sentiment': 'mean',
            'url': 'count',
            'positive_count': 'sum',
            'negative_count': 'sum',
            'neutral_count': 'sum'
        }).reset_index()

        category_analysis.columns = ['Category', 'Avg_Sentiment', 'Article_Count',
                                     'Positive_Comments', 'Negative_Comments', 'Neutral_Comments']

        # Add Rating column for stakeholders
        category_analysis['Rating'] = category_analysis['Avg_Sentiment'].apply(get_sentiment_rating)

        # Reorder columns to put Rating right after Avg_Sentiment
        cols = ['Category', 'Avg_Sentiment', 'Rating', 'Article_Count',
                'Positive_Comments', 'Negative_Comments', 'Neutral_Comments']
        category_analysis = category_analysis[cols]

        category_analysis = category_analysis.sort_values('Avg_Sentiment', ascending=False)
        category_analysis.to_excel(writer, sheet_name='Categories', index=False)

        # Sheet 3: Cluster Analysis (if available)
        if 'cluster' in articles_df.columns:
            cluster_analysis = articles_df.groupby('cluster').agg({
                'avg_sentiment': 'mean',
                'url': 'count'
            }).reset_index()

            cluster_analysis.columns = ['Cluster', 'Avg_Sentiment', 'Article_Count']

            # Add Rating column for stakeholders
            cluster_analysis['Rating'] = cluster_analysis['Avg_Sentiment'].apply(get_sentiment_rating)

            # Reorder columns to put Rating right after Avg_Sentiment
            cols = ['Cluster', 'Avg_Sentiment', 'Rating', 'Article_Count']
            cluster_analysis = cluster_analysis[cols]

            cluster_analysis = cluster_analysis.sort_values('Avg_Sentiment', ascending=False)
            cluster_analysis.to_excel(writer, sheet_name='Clusters', index=False)

        # Sheet 4: Insights
        insights_data = []

        # Top Articles
        top_articles = articles_df.nlargest(5, 'avg_sentiment')
        for _, art in top_articles.iterrows():
            insights_data.append({
                'Type': 'Top Article',
                'Title': art['title'],
                'Category': art['category'],
                'Sentiment': f"{art['avg_sentiment']:+.3f}"
            })

        # Worst Articles
        worst_articles = articles_df.nsmallest(5, 'avg_sentiment')
        for _, art in worst_articles.iterrows():
            insights_data.append({
                'Type': 'Worst Article',
                'Title': art['title'],
                'Category': art['category'],
                'Sentiment': f"{art['avg_sentiment']:+.3f}"
            })

        insights_df = pd.DataFrame(insights_data)
        insights_df.to_excel(writer, sheet_name='Insights', index=False)

    logger.info(f"✓ Report gespeichert: {output_file}")

    # Zusammenfassung
    logger.info("\n" + "="*80)
    logger.info("  ZUSAMMENFASSUNG")
    logger.info("="*80)
    logger.info(f"Analysierte Artikel: {len(articles_df)}")
    logger.info(f"Total Kommentare: {articles_df['total_comments'].sum()}")
    logger.info(f"Durchschn. Sentiment: {articles_df['avg_sentiment'].mean():+.3f}")
    logger.info(f"LLM Model: {sentiment_analyzer.mode}")

    logger.info(f"\n✅ Analyse abgeschlossen! Report: {output_file}")

    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logger.info("\n\n⚠️  Abgebrochen durch Benutzer")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n❌ Fehler: {e}", exc_info=True)
        sys.exit(1)
