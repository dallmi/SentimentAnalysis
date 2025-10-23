"""
Sentiment Analysis mit BERTopic für Content Clustering
Automatische Kategorisierung und Clustering von Intranet-Artikeln basierend auf Inhalt

Verwendung:
    python main_bertopic.py --input data/input/article_content.json
"""

import argparse
import logging
import sys
import json
from pathlib import Path
import pandas as pd
from datetime import datetime
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import re

# Add LLM Solution to path
sys.path.insert(0, str(Path(__file__).parent / "LLM Solution"))

# Try to import BERTopic
try:
    from bertopic import BERTopic
    from sentence_transformers import SentenceTransformer
    BERTOPIC_AVAILABLE = True
except ImportError:
    print("❌ BERTopic nicht installiert!")
    print("   Installiere mit: pip install bertopic sentence-transformers")
    BERTOPIC_AVAILABLE = False

# Try to import sentiment analyzer
try:
    from offline_sentiment_analyzer import OfflineSentimentAnalyzer
    SENTIMENT_AVAILABLE = True
except ImportError:
    print("⚠️  Sentiment Analyzer nicht verfügbar")
    SENTIMENT_AVAILABLE = False

# Try to import abstractive summarizer
try:
    from abstractive_summarizer import AbstractiveSummarizer
    ABSTRACTIVE_AVAILABLE = True
except ImportError:
    ABSTRACTIVE_AVAILABLE = False

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def get_sentiment_rating(score: float) -> str:
    """
    Convert sentiment score to human-readable rating with emojis for stakeholders.

    Args:
        score: Sentiment score from -1.0 to +1.0

    Returns:
        Rating string with stars/emojis
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


def extractive_summarize(text: str, embedding_model, num_sentences: int = 3) -> str:
    """
    Create extractive summary by selecting most representative sentences using BERT embeddings.

    Uses cosine similarity between sentence embeddings to find sentences most similar
    to the overall document embedding (document centroid).

    Args:
        text: The text to summarize
        embedding_model: SentenceTransformer model for creating embeddings
        num_sentences: Number of sentences to extract (default: 3)

    Returns:
        Summary string with selected sentences
    """
    if not text or not text.strip():
        return ""

    # Split text into sentences
    # Simple sentence splitting on common delimiters
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]

    # If we have fewer sentences than requested, return all
    if len(sentences) <= num_sentences:
        return " ".join(sentences)

    # Create embeddings for all sentences
    sentence_embeddings = embedding_model.encode(sentences)

    # Calculate document centroid (mean of all sentence embeddings)
    doc_embedding = np.mean(sentence_embeddings, axis=0).reshape(1, -1)

    # Calculate similarity of each sentence to the document centroid
    similarities = cosine_similarity(sentence_embeddings, doc_embedding).flatten()

    # Get indices of top N most similar sentences
    top_indices = np.argsort(similarities)[-num_sentences:]

    # Sort indices to maintain original order in text
    top_indices = sorted(top_indices)

    # Extract sentences
    summary_sentences = [sentences[i] for i in top_indices]

    return " ".join(summary_sentences)


class BERTopicSentimentAnalyzer:
    """
    Complete sentiment analysis pipeline with BERTopic for content clustering
    """

    def __init__(self, model_path: str = None, use_abstractive: bool = False):
        """
        Initialize analyzer

        Args:
            model_path: Path to multilingual sentence transformer model
            use_abstractive: Use abstractive summarization (requires mBART model)
        """
        logger.info("\n" + "=" * 70)
        logger.info("BERTopic Sentiment Analyzer - Initialisierung")
        logger.info("=" * 70)

        # Load embedding model for BERTopic
        if model_path is None:
            # Default path
            model_path = Path(__file__).parent / "LLM Solution" / "models" / "paraphrase-multilingual-MiniLM-L12-v2"

        if not Path(model_path).exists():
            logger.warning(f"⚠️  Model nicht gefunden: {model_path}")
            logger.info("   Versuche Online-Download...")
            model_path = "paraphrase-multilingual-MiniLM-L12-v2"

        logger.info(f"\n[1/4] Lade Embedding Model...")
        logger.info(f"   Path: {model_path}")
        self.embedding_model = SentenceTransformer(str(model_path))
        logger.info("   ✓ Embedding Model geladen (50+ Sprachen unterstützt)")

        # Initialize BERTopic
        logger.info(f"\n[2/4] Initialisiere BERTopic...")
        self.topic_model = BERTopic(
            embedding_model=self.embedding_model,
            language='multilingual',
            calculate_probabilities=True,
            verbose=True
        )
        logger.info("   ✓ BERTopic bereit")

        # Load sentiment analyzer for comments
        logger.info(f"\n[3/4] Lade Sentiment Analyzer für Kommentare...")
        if SENTIMENT_AVAILABLE:
            self.sentiment_analyzer = OfflineSentimentAnalyzer()
            logger.info(f"   ✓ Sentiment Analyzer geladen (Mode: {self.sentiment_analyzer.mode})")
        else:
            self.sentiment_analyzer = None
            logger.warning("   ⚠️  Sentiment Analyzer nicht verfügbar")

        # Load abstractive summarizer (optional)
        logger.info(f"\n[4/4] Lade Abstractive Summarizer...")
        self.use_abstractive = use_abstractive
        self.abstractive_summarizer = None

        if use_abstractive:
            if ABSTRACTIVE_AVAILABLE:
                try:
                    self.abstractive_summarizer = AbstractiveSummarizer()
                    logger.info("   ✓ Abstractive Summarizer geladen (mBART-large-50)")
                except Exception as e:
                    logger.warning(f"   ⚠️  Abstractive Summarizer konnte nicht geladen werden: {e}")
                    logger.info("   → Verwende stattdessen Extractive Summarization")
                    self.use_abstractive = False
            else:
                logger.warning("   ⚠️  Abstractive Summarizer nicht verfügbar")
                logger.info("   → Download mit: python setup/download_mbart_model.py")
                logger.info("   → Verwende stattdessen Extractive Summarization")
                self.use_abstractive = False
        else:
            logger.info("   → Verwende Extractive Summarization (Standard)")

        logger.info("\n" + "=" * 70)
        logger.info("Initialisierung abgeschlossen!")
        logger.info("=" * 70 + "\n")

    def analyze(self, json_file: str, output_file: str = None):
        """
        Complete analysis pipeline

        Args:
            json_file: Path to article_content.json
            output_file: Path to output Excel file
        """
        logger.info("\n" + "=" * 70)
        logger.info("START: Sentiment Analysis mit BERTopic")
        logger.info("=" * 70)

        # Step 1: Load data
        logger.info(f"\n[STEP 1/5] Lade Daten aus {json_file}...")
        with open(json_file, 'r', encoding='utf-8') as f:
            articles_data = json.load(f)

        logger.info(f"   ✓ {len(articles_data)} Artikel geladen")

        # Prepare data
        articles_df = pd.DataFrame(articles_data)

        # Extract article texts for clustering
        logger.info(f"\n[STEP 2/5] Bereite Artikel-Texte vor...")
        article_texts = []
        article_ids = []

        for idx, article in enumerate(articles_data):
            title = article.get('title', '')
            content = article.get('content', '')
            combined_text = f"{title}. {content}"
            article_texts.append(combined_text)
            article_ids.append(idx)

        logger.info(f"   ✓ {len(article_texts)} Texte vorbereitet")

        # Generate summaries for each article
        if self.use_abstractive and self.abstractive_summarizer:
            logger.info(f"   Generiere ABSTRACTIVE Zusammenfassungen (mBART)...")
            article_summaries = []
            for combined_text in article_texts:
                summary = self.abstractive_summarizer.summarize(
                    combined_text,
                    source_lang="de_DE",
                    max_length=100,
                    min_length=30
                )
                article_summaries.append(summary)
        else:
            logger.info(f"   Generiere EXTRACTIVE Zusammenfassungen...")
            article_summaries = []
            for combined_text in article_texts:
                summary = extractive_summarize(combined_text, self.embedding_model, num_sentences=3)
                article_summaries.append(summary)

        articles_df['summary'] = article_summaries
        logger.info(f"   ✓ {len(article_summaries)} Zusammenfassungen erstellt")

        # Step 3: Cluster articles with BERTopic
        logger.info(f"\n[STEP 3/5] Clustere Artikel mit BERTopic...")
        logger.info("   (Dies kann einige Minuten dauern...)")

        topics, probabilities = self.topic_model.fit_transform(article_texts)

        # Get topic info
        topic_info = self.topic_model.get_topic_info()
        n_topics = len(topic_info) - 1  # Exclude outlier topic (-1)

        logger.info(f"   ✓ {n_topics} Topics gefunden")
        logger.info(f"\nTopic Overview:")
        for idx, row in topic_info.iterrows():
            if row['Topic'] != -1:  # Skip outlier topic
                logger.info(f"   Topic {row['Topic']}: {row['Count']} Artikel - {row['Name']}")

        # Add topics to dataframe
        articles_df['topic'] = topics
        articles_df['topic_probability'] = probabilities.max(axis=1) if len(probabilities.shape) > 1 else probabilities

        # Get topic labels
        topic_labels = {}
        for topic_id in set(topics):
            if topic_id != -1:
                topic_words = self.topic_model.get_topic(topic_id)
                if topic_words:
                    # Get top 3 words
                    top_words = [word for word, _ in topic_words[:3]]
                    topic_labels[topic_id] = " & ".join(top_words).capitalize()
                else:
                    topic_labels[topic_id] = f"Topic {topic_id}"
            else:
                topic_labels[topic_id] = "Uncategorized"

        articles_df['topic_label'] = articles_df['topic'].map(topic_labels)

        # Step 4: Analyze comment sentiment
        logger.info(f"\n[STEP 4/5] Analysiere Kommentar-Sentiment...")

        comment_details = []
        comment_sentiment_map = {}
        article_sentiments = {}  # Aggregate sentiment per article

        total_comments = sum(len(article.get('comments', [])) for article in articles_data)
        logger.info(f"   Analysiere {total_comments} Kommentare...")

        if self.sentiment_analyzer:
            for idx, article in enumerate(articles_data):
                url = article.get('url', '')
                title = article.get('title', '')
                comments = article.get('comments', [])

                topic = topics[idx]
                topic_label = topic_labels[topic]

                # Initialize sentiment aggregation for this article
                article_sentiments[url] = {
                    'positive_count': 0,
                    'negative_count': 0,
                    'neutral_count': 0,
                    'sentiment_scores': []
                }

                # Analyze sentiment for each comment
                for comment_obj in comments:
                    comment_text = comment_obj.get('text', '')
                    author = comment_obj.get('author', 'Unknown')
                    date = comment_obj.get('date', '')

                    if comment_text:
                        # Analyze sentiment
                        sentiment_result = self.sentiment_analyzer.analyze_text(comment_text)
                        sentiment_category = sentiment_result.get('category', 'unknown')
                        sentiment_score = sentiment_result.get('score', 0.0)

                        # Aggregate sentiment counts per article
                        if sentiment_category == 'positive':
                            article_sentiments[url]['positive_count'] += 1
                        elif sentiment_category == 'negative':
                            article_sentiments[url]['negative_count'] += 1
                        else:
                            article_sentiments[url]['neutral_count'] += 1

                        # Store score for averaging
                        article_sentiments[url]['sentiment_scores'].append(sentiment_score)

                        # Store for detail view
                        comment_sentiment_map[comment_text] = sentiment_result

                        comment_details.append({
                            'URL': url,
                            'Title': title,
                            'Topic': topic_label,
                            'Topic_ID': topic,
                            'Comment': comment_text,
                            'Comment_Sentiment': sentiment_category.capitalize(),
                            'Sentiment_Score': round(sentiment_score, 3),
                            'Positive': 1 if sentiment_category == 'positive' else 0,
                            'Neutral': 1 if sentiment_category == 'neutral' else 0,
                            'Negative': 1 if sentiment_category == 'negative' else 0,
                            'Author': author,
                            'Date': date
                        })

            logger.info(f"   ✓ Sentiment-Analyse abgeschlossen")
        else:
            logger.warning("   ⚠️  Sentiment-Analyse übersprungen (Analyzer nicht verfügbar)")
            # Create details without sentiment
            for idx, article in enumerate(articles_data):
                url = article.get('url', '')
                title = article.get('title', '')
                comments = article.get('comments', [])
                topic = topics[idx]
                topic_label = topic_labels[topic]

                for comment_obj in comments:
                    comment_text = comment_obj.get('text', '')
                    author = comment_obj.get('author', 'Unknown')
                    date = comment_obj.get('date', '')

                    comment_details.append({
                        'URL': url,
                        'Title': title,
                        'Topic': topic_label,
                        'Topic_ID': topic,
                        'Comment': comment_text,
                        'Comment_Sentiment': 'N/A',
                        'Sentiment_Score': 0.0,
                        'Positive': 0,
                        'Neutral': 0,
                        'Negative': 0,
                        'Author': author,
                        'Date': date
                    })

        # Step 5: Generate Excel report
        logger.info(f"\n[STEP 5/5] Erstelle Excel Report...")

        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"sentiment_analysis_bertopic_{timestamp}.xlsx"

        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Sheet 1: Article Overview with Sentiment Aggregation
            overview_df = articles_df[['url', 'title', 'summary', 'topic_label', 'topic']].copy()
            overview_df.columns = ['URL', 'Title', 'Summary', 'Topic', 'Topic_ID']

            # Add sentiment aggregation columns
            if self.sentiment_analyzer and article_sentiments:
                overview_df['Avg_Sentiment'] = overview_df['URL'].apply(
                    lambda url: round(
                        sum(article_sentiments.get(url, {}).get('sentiment_scores', [0.0])) /
                        max(len(article_sentiments.get(url, {}).get('sentiment_scores', [0.0])), 1),
                        3
                    )
                )
                overview_df['Rating'] = overview_df['Avg_Sentiment'].apply(get_sentiment_rating)
                overview_df['Total_Comments'] = overview_df['URL'].apply(
                    lambda url: len(article_sentiments.get(url, {}).get('sentiment_scores', []))
                )
                overview_df['Positive_Count'] = overview_df['URL'].apply(
                    lambda url: article_sentiments.get(url, {}).get('positive_count', 0)
                )
                overview_df['Negative_Count'] = overview_df['URL'].apply(
                    lambda url: article_sentiments.get(url, {}).get('negative_count', 0)
                )
                overview_df['Neutral_Count'] = overview_df['URL'].apply(
                    lambda url: article_sentiments.get(url, {}).get('neutral_count', 0)
                )

                # Reorder columns to match old format (with Summary added)
                overview_df = overview_df[['URL', 'Title', 'Summary', 'Topic', 'Topic_ID', 'Avg_Sentiment', 'Rating',
                                          'Total_Comments', 'Positive_Count', 'Negative_Count', 'Neutral_Count']]

                # Sort by sentiment score (highest first)
                overview_df = overview_df.sort_values('Avg_Sentiment', ascending=False)
            else:
                # No sentiment analysis available
                overview_df['Avg_Sentiment'] = 0.0
                overview_df['Rating'] = 'N/A'
                overview_df['Total_Comments'] = 0

            overview_df.to_excel(writer, sheet_name='Articles', index=False)

            # Sheet 2: Comments Detail
            if comment_details:
                comments_df = pd.DataFrame(comment_details)
                comments_df.to_excel(writer, sheet_name='Comments_Detail', index=False)

            # Sheet 3: Topic Statistics
            if self.sentiment_analyzer:
                # Calculate sentiment per topic
                comments_df = pd.DataFrame(comment_details)
                topic_stats = comments_df.groupby('Topic').agg({
                    'Comment': 'count',
                    'Comment_Sentiment': lambda x: x.value_counts().to_dict(),
                    'Sentiment_Score': 'mean'
                }).reset_index()
                topic_stats.columns = ['Topic', 'Total_Comments', 'Sentiment_Distribution', 'Avg_Sentiment_Score']
                topic_stats['Avg_Sentiment_Score'] = topic_stats['Avg_Sentiment_Score'].round(3)
                topic_stats.to_excel(writer, sheet_name='Topic_Statistics', index=False)

        logger.info(f"   ✓ Excel Report erstellt: {output_file}")

        # Final summary
        logger.info("\n" + "=" * 70)
        logger.info("FERTIG! Zusammenfassung:")
        logger.info("=" * 70)
        logger.info(f"✓ {len(articles_data)} Artikel analysiert")
        logger.info(f"✓ {n_topics} Topics gefunden")
        logger.info(f"✓ {total_comments} Kommentare analysiert")
        logger.info(f"✓ Report gespeichert: {output_file}")
        logger.info("=" * 70 + "\n")

        return output_file


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Sentiment Analysis with BERTopic for Content Clustering'
    )
    parser.add_argument(
        '--input',
        type=str,
        required=True,
        help='Path to article_content.json file'
    )
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Path to output Excel file (optional, auto-generated if not specified)'
    )
    parser.add_argument(
        '--model-path',
        type=str,
        default=None,
        help='Path to multilingual sentence transformer model (optional)'
    )
    parser.add_argument(
        '--abstractive',
        action='store_true',
        help='Use abstractive summarization (requires mBART model)'
    )

    args = parser.parse_args()

    # Check if BERTopic is available
    if not BERTOPIC_AVAILABLE:
        logger.error("❌ BERTopic ist nicht installiert!")
        logger.error("   Bitte installiere mit:")
        logger.error("   pip install bertopic sentence-transformers umap-learn hdbscan")
        sys.exit(1)

    # Check if input file exists
    if not Path(args.input).exists():
        logger.error(f"❌ Input file nicht gefunden: {args.input}")
        sys.exit(1)

    # Run analysis
    analyzer = BERTopicSentimentAnalyzer(
        model_path=args.model_path,
        use_abstractive=args.abstractive
    )
    analyzer.analyze(args.input, args.output)


if __name__ == "__main__":
    main()
