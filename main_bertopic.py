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
import time
from typing import Dict, Any

# Try to import tqdm for progress bars
try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
    # Fallback: simple counter
    def tqdm(iterable, desc=None, **kwargs):
        return iterable

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

        logger.info(f"\n[1/4] Lade Embedding Model für Article Clustering...")
        logger.info(f"   📦 Model: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        logger.info(f"   🎯 Verwendung: Semantische Embeddings für BERTopic Clustering")
        logger.info(f"   🌍 Sprachen: 50+ (multilingual)")
        logger.info(f"   📍 Path: {model_path}")
        start_time = time.time()
        self.embedding_model = SentenceTransformer(str(model_path))
        load_time = time.time() - start_time
        logger.info(f"   ✓ Geladen in {load_time:.2f}s")

        # Initialize BERTopic
        logger.info(f"\n[2/4] Initialisiere BERTopic Clustering Pipeline...")
        logger.info(f"   📦 Framework: BERTopic (HDBSCAN + UMAP)")
        logger.info(f"   🎯 Verwendung: Gruppiert Artikel in thematische Cluster")
        logger.info(f"   ⚙️  Config: min_cluster_size=2, n_neighbors=3, n_components=5")

        # Import HDBSCAN for custom parameters
        from hdbscan import HDBSCAN
        from umap import UMAP

        start_time = time.time()

        # Custom HDBSCAN for small datasets (< 50 documents)
        hdbscan_model = HDBSCAN(
            min_cluster_size=2,      # Minimum 2 documents per cluster (default: 10)
            min_samples=1,            # Minimum samples in neighborhood (default: 5)
            metric='euclidean',
            cluster_selection_method='eom',
            prediction_data=True
        )

        # Custom UMAP for small datasets
        umap_model = UMAP(
            n_neighbors=3,            # Reduced from default 15 for small datasets
            n_components=5,           # Dimensionality
            min_dist=0.0,
            metric='cosine'
        )

        self.topic_model = BERTopic(
            embedding_model=self.embedding_model,
            hdbscan_model=hdbscan_model,
            umap_model=umap_model,
            language='multilingual',
            calculate_probabilities=True,
            verbose=True,
            min_topic_size=2          # Minimum documents per topic (default: 10)
        )

        load_time = time.time() - start_time
        logger.info(f"   ✓ Initialisiert in {load_time:.2f}s")

        # Load sentiment analyzer for comments
        logger.info(f"\n[3/4] Lade Sentiment Analyzer für Kommentare...")
        if SENTIMENT_AVAILABLE:
            start_time = time.time()
            self.sentiment_analyzer = OfflineSentimentAnalyzer()
            load_time = time.time() - start_time

            # Get detailed model info
            if hasattr(self.sentiment_analyzer, 'model') and self.sentiment_analyzer.model:
                model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
                logger.info(f"   📦 Model: {model_name}")
                logger.info(f"   🎯 Verwendung: Sentiment-Analyse von Kommentaren (Positiv/Neutral/Negativ)")
                logger.info(f"   🌍 Sprachen: en, de, fr, it, es, nl")
                logger.info(f"   ⚙️  Output: 5-star rating → 3 Kategorien")
            else:
                logger.info(f"   📦 Mode: Lexikon-basiert (Fallback)")

            logger.info(f"   ✓ Geladen in {load_time:.2f}s")
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
                    start_time = time.time()
                    self.abstractive_summarizer = AbstractiveSummarizer()
                    load_time = time.time() - start_time
                    logger.info(f"   📦 Model: facebook/mBART-large-50-many-to-many-mmt")
                    logger.info(f"   🎯 Verwendung: Generiert Article Summaries + Topic Labels")
                    logger.info(f"   🌍 Sprachen: 50+ (inkl. de_DE, en_XX)")
                    logger.info(f"   ⚙️  Params: ~611M, Beam Search (num_beams=4)")
                    logger.info(f"   ✓ Geladen in {load_time:.2f}s")
                except Exception as e:
                    logger.warning(f"   ⚠️  Konnte nicht geladen werden: {e}")
                    logger.info("   → Verwende stattdessen Extractive Summarization")
                    self.use_abstractive = False
            else:
                logger.warning("   ⚠️  Abstractive Summarizer nicht verfügbar")
                logger.info("   → Download mit: python setup/download_mbart_model.py")
                logger.info("   → Verwende stattdessen Extractive Summarization")
                self.use_abstractive = False
        else:
            logger.info("   📦 Mode: Extractive (Standard)")
            logger.info("   🎯 Verwendung: Extrahiert 3 beste Sätze aus Artikeln")
            logger.info("   ⚙️  Methode: Cosine Similarity mit Sentence Embeddings")

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

        # Track overall time
        analysis_start_time = time.time()

        # Step 1: Load data
        logger.info(f"\n[STEP 1/5] Lade Daten aus {json_file}...")
        step_start = time.time()
        with open(json_file, 'r', encoding='utf-8') as f:
            articles_data = json.load(f)
        step_time = time.time() - step_start
        logger.info(f"   ✓ {len(articles_data)} Artikel geladen in {step_time:.2f}s")

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
        logger.info(f"   📝 Generiere Artikel-Zusammenfassungen...")
        step_start = time.time()
        article_summaries = []

        if self.use_abstractive and self.abstractive_summarizer:
            logger.info(f"   🤖 Mode: ABSTRACTIVE (mBART) - ~2-5s pro Artikel")
            for combined_text in tqdm(article_texts, desc="      Summaries", disable=not TQDM_AVAILABLE):
                summary = self.abstractive_summarizer.summarize(
                    combined_text,
                    source_lang="de_DE",
                    max_length=350,  # 350 tokens ≈ 250 Wörter ≈ 1800-2200 Zeichen
                    min_length=80    # Mindestens 80 tokens für aussagekräftige Summaries
                )
                article_summaries.append(summary)
        else:
            logger.info(f"   ⚡ Mode: EXTRACTIVE (3 beste Sätze) - ~0.1s pro Artikel")
            for combined_text in tqdm(article_texts, desc="      Summaries", disable=not TQDM_AVAILABLE):
                summary = extractive_summarize(combined_text, self.embedding_model, num_sentences=3)
                article_summaries.append(summary)

        articles_df['summary'] = article_summaries
        step_time = time.time() - step_start
        logger.info(f"   ✓ {len(article_summaries)} Zusammenfassungen erstellt in {step_time:.2f}s ({step_time/len(article_summaries):.2f}s pro Artikel)")

        # Step 3: Cluster articles with BERTopic
        logger.info(f"\n[STEP 3/5] Clustere Artikel mit BERTopic...")
        logger.info(f"   🔄 Embedding → UMAP → HDBSCAN Clustering...")
        step_start = time.time()

        topics, probabilities = self.topic_model.fit_transform(article_texts)

        step_time = time.time() - step_start
        # Get topic info
        topic_info = self.topic_model.get_topic_info()
        n_topics = len(topic_info) - 1  # Exclude outlier topic (-1)

        logger.info(f"   ✓ {n_topics} Topics gefunden in {step_time:.2f}s")
        logger.info(f"\nTopic Overview:")
        for idx, row in topic_info.iterrows():
            if row['Topic'] != -1:  # Skip outlier topic
                logger.info(f"   Topic {row['Topic']}: {row['Count']} Artikel - {row['Name']}")

        # Add topics to dataframe
        articles_df['topic'] = topics
        articles_df['topic_probability'] = probabilities.max(axis=1) if len(probabilities.shape) > 1 else probabilities

        # Get topic labels
        topic_labels = {}

        # Use mBART for better topic labels if available
        if self.use_abstractive and self.abstractive_summarizer:
            logger.info(f"   🤖 Generiere prägnante Topic-Labels mit mBART (1-3 Schlagwörter)...")
            step_start = time.time()
            topic_ids = [tid for tid in set(topics) if tid != -1]

            for topic_id in tqdm(topic_ids, desc="      Topic Labels", disable=not TQDM_AVAILABLE):
                # Get topic keywords and representative documents
                topic_words = self.topic_model.get_topic(topic_id)
                representative_docs = [article_texts[i] for i, t in enumerate(topics) if t == topic_id][:3]

                if topic_words:
                    # Generate concise label with mBART
                    label = self.abstractive_summarizer.generate_topic_label(
                        keywords=topic_words,
                        representative_docs=representative_docs,
                        source_lang="de_DE",
                        max_keywords=3
                    )
                    topic_labels[topic_id] = label
                else:
                    topic_labels[topic_id] = f"Topic {topic_id}"

            topic_labels[-1] = "Uncategorized"  # Handle outliers
            step_time = time.time() - step_start
            logger.info(f"   ✓ {len(topic_ids)} Topic-Labels generiert in {step_time:.2f}s ({step_time/len(topic_ids):.2f}s pro Topic)")
        else:
            # Fallback: Use top 3 keywords
            logger.info(f"   Generiere Topic-Labels aus Keywords (Standard)...")
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
        logger.info(f"   💭 {total_comments} Kommentare mit BERT Multilingual Model...")
        step_start = time.time()

        if self.sentiment_analyzer:
            for idx, article in tqdm(enumerate(articles_data), total=len(articles_data), desc="      Comments", disable=not TQDM_AVAILABLE):
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
                        sentiment_result = self.sentiment_analyzer.analyze(comment_text)
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

            step_time = time.time() - step_start
            logger.info(f"   ✓ Sentiment-Analyse abgeschlossen in {step_time:.2f}s ({step_time/total_comments:.3f}s pro Kommentar)")
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
