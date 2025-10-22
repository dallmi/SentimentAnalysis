"""
Unsupervised Topic Discovery Module

Automatically discovers what articles are about WITHOUT predefined categories.
Uses TF-IDF + clustering algorithms to find natural topic groupings.

Two modes:
1. Supervised: Use predefined categories (AI & Innovation, Employee Stories, etc.)
2. Unsupervised: Automatically discover topics from the data

Unsupervised is useful when:
- You don't know what topics to expect
- You want to discover emerging themes
- Your content is diverse and unpredictable
- You want data-driven insights rather than assumptions
"""

import logging
from typing import Dict, List, Tuple
import re
from collections import Counter
import math

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TopicDiscovery:
    """
    Discovers topics automatically from article text using TF-IDF and clustering
    """

    def __init__(self, num_topics: int = 10, min_articles_per_topic: int = 2, auto_optimize: bool = False):
        """
        Initialize topic discovery

        Args:
            num_topics: Target number of topics to discover (ignored if auto_optimize=True)
            min_articles_per_topic: Minimum articles needed to form a topic
            auto_optimize: Automatically determine optimal number of clusters using Silhouette score
        """
        self.num_topics = num_topics
        self.min_articles_per_topic = min_articles_per_topic
        self.auto_optimize = auto_optimize
        self.stopwords = self._load_stopwords()

    def _load_stopwords(self) -> set:
        """Load multilingual stopwords"""
        # English stopwords
        english = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'should', 'could', 'can', 'may', 'might', 'must', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'what', 'which', 'who', 'when', 'where', 'why', 'how', 'all', 'each',
            'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such',
            'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
            'very', 'just', 'about', 'after', 'before', 'into', 'through',
            'during', 'above', 'below', 'between', 'under', 'over', 'again',
        }

        # German stopwords
        german = {
            'der', 'die', 'das', 'und', 'ist', 'in', 'zu', 'den', 'von',
            'mit', 'auf', 'für', 'eine', 'ein', 'als', 'sich', 'nicht',
            'im', 'werden', 'an', 'oder', 'auch', 'dem', 'des', 'bei',
            'um', 'zum', 'zur', 'durch', 'aus', 'sind', 'am', 'kann',
            'wird', 'hat', 'haben', 'wurde', 'sein', 'alle', 'dieser',
            'diese', 'dieses', 'wenn', 'dann', 'aber', 'über', 'nach',
            'vor', 'mehr', 'noch', 'nur', 'hier', 'dort', 'wie', 'was',
            'wer', 'wo', 'wann', 'warum', 'welche', 'welcher', 'sehr',
        }

        # French stopwords
        french = {
            'le', 'la', 'les', 'de', 'un', 'une', 'et', 'est', 'dans',
            'pour', 'que', 'qui', 'avec', 'sur', 'par', 'pas', 'plus',
            'ce', 'sont', 'aussi', 'mais', 'comme', 'tout', 'cette',
            'nous', 'vous', 'ils', 'elle', 'ont', 'été', 'fait', 'faire',
        }

        # Italian stopwords
        italian = {
            'il', 'la', 'di', 'e', 'un', 'una', 'in', 'per', 'che',
            'con', 'su', 'da', 'sono', 'come', 'anche', 'ma', 'tutto',
            'questa', 'questo', 'noi', 'voi', 'loro', 'hanno', 'stato',
        }

        return english | german | french | italian

    def _preprocess_text(self, text: str) -> List[str]:
        """
        Preprocess text: lowercase, remove punctuation, filter stopwords

        Args:
            text: Raw text

        Returns:
            List of cleaned tokens
        """
        if not text:
            return []

        # Lowercase and remove special characters
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)

        # Tokenize
        tokens = text.split()

        # Filter: length > 3, not stopword, not number
        tokens = [
            t for t in tokens
            if len(t) > 3 and t not in self.stopwords and not t.isdigit()
        ]

        return tokens

    def _compute_tfidf(self, documents: List[List[str]]) -> Tuple[List[Dict[str, float]], List[str]]:
        """
        Compute TF-IDF scores for documents

        Args:
            documents: List of tokenized documents

        Returns:
            Tuple of (TF-IDF vectors, vocabulary)
        """
        # Build vocabulary
        vocab = set()
        for doc in documents:
            vocab.update(doc)
        vocab = sorted(list(vocab))

        # Compute document frequency
        df = {}
        num_docs = len(documents)

        for word in vocab:
            df[word] = sum(1 for doc in documents if word in doc)

        # Compute TF-IDF for each document
        tfidf_vectors = []

        for doc in documents:
            # Term frequency
            tf = Counter(doc)
            total_terms = len(doc)

            # TF-IDF vector
            vector = {}
            for word in vocab:
                if word in tf:
                    # TF: frequency / total terms
                    tf_score = tf[word] / total_terms if total_terms > 0 else 0

                    # IDF: log(N / df)
                    idf_score = math.log(num_docs / df[word]) if df[word] > 0 else 0

                    # TF-IDF
                    vector[word] = tf_score * idf_score
                else:
                    vector[word] = 0.0

            tfidf_vectors.append(vector)

        return tfidf_vectors, vocab

    def _cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """
        Compute cosine similarity between two TF-IDF vectors

        Args:
            vec1: First vector
            vec2: Second vector

        Returns:
            Cosine similarity score (0-1)
        """
        # Dot product
        dot_product = sum(vec1.get(k, 0) * vec2.get(k, 0) for k in set(vec1.keys()) | set(vec2.keys()))

        # Magnitudes
        mag1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
        mag2 = math.sqrt(sum(v ** 2 for v in vec2.values()))

        if mag1 == 0 or mag2 == 0:
            return 0.0

        return dot_product / (mag1 * mag2)

    def _simple_kmeans(
        self,
        vectors: List[Dict[str, float]],
        k: int,
        max_iterations: int = 50
    ) -> List[int]:
        """
        Simple K-Means clustering implementation

        Args:
            vectors: TF-IDF vectors
            k: Number of clusters
            max_iterations: Maximum iterations

        Returns:
            List of cluster assignments
        """
        import random

        if len(vectors) < k:
            # Not enough documents for k clusters
            return list(range(len(vectors)))

        # Initialize centroids randomly
        centroids = random.sample(vectors, k)
        assignments = [0] * len(vectors)

        for iteration in range(max_iterations):
            # Assign each vector to nearest centroid
            new_assignments = []
            for vec in vectors:
                similarities = [self._cosine_similarity(vec, centroid) for centroid in centroids]
                cluster = similarities.index(max(similarities))
                new_assignments.append(cluster)

            # Check convergence
            if new_assignments == assignments:
                break

            assignments = new_assignments

            # Update centroids (mean of assigned vectors)
            new_centroids = []
            for cluster_id in range(k):
                cluster_vecs = [vectors[i] for i, c in enumerate(assignments) if c == cluster_id]

                if not cluster_vecs:
                    # Empty cluster, keep old centroid
                    new_centroids.append(centroids[cluster_id])
                    continue

                # Average all vectors in cluster
                avg_vector = {}
                vocab = set()
                for vec in cluster_vecs:
                    vocab.update(vec.keys())

                for word in vocab:
                    avg_vector[word] = sum(vec.get(word, 0) for vec in cluster_vecs) / len(cluster_vecs)

                new_centroids.append(avg_vector)

            centroids = new_centroids

        return assignments

    def _calculate_silhouette_score(
        self,
        vectors: List[Dict[str, float]],
        assignments: List[int]
    ) -> float:
        """
        Calculate Silhouette score for clustering quality

        Silhouette score ranges from -1 to 1:
        - 1: Perfect clustering (samples far from other clusters)
        - 0: Overlapping clusters
        - -1: Wrong clustering (samples closer to other clusters)

        Args:
            vectors: TF-IDF vectors
            assignments: Cluster assignments

        Returns:
            Average Silhouette score
        """
        n = len(vectors)
        if n == 0:
            return 0.0

        silhouette_scores = []

        for i in range(n):
            # Current cluster
            cluster_i = assignments[i]

            # a(i): Average distance to points in same cluster
            same_cluster_indices = [j for j in range(n) if assignments[j] == cluster_i and j != i]

            if not same_cluster_indices:
                # Only point in cluster
                silhouette_scores.append(0.0)
                continue

            a_i = sum(
                1 - self._cosine_similarity(vectors[i], vectors[j])  # Distance = 1 - similarity
                for j in same_cluster_indices
            ) / len(same_cluster_indices)

            # b(i): Minimum average distance to points in other clusters
            other_clusters = set(assignments) - {cluster_i}

            if not other_clusters:
                # Only one cluster
                silhouette_scores.append(0.0)
                continue

            b_i = float('inf')
            for other_cluster in other_clusters:
                other_cluster_indices = [j for j in range(n) if assignments[j] == other_cluster]

                if other_cluster_indices:
                    avg_dist = sum(
                        1 - self._cosine_similarity(vectors[i], vectors[j])
                        for j in other_cluster_indices
                    ) / len(other_cluster_indices)

                    b_i = min(b_i, avg_dist)

            # Silhouette score for point i
            s_i = (b_i - a_i) / max(a_i, b_i) if max(a_i, b_i) > 0 else 0
            silhouette_scores.append(s_i)

        return sum(silhouette_scores) / len(silhouette_scores) if silhouette_scores else 0.0

    def _find_optimal_clusters(
        self,
        vectors: List[Dict[str, float]],
        min_k: int = 2,
        max_k: int = 20
    ) -> Tuple[int, Dict[int, float]]:
        """
        Find optimal number of clusters using Silhouette score

        Args:
            vectors: TF-IDF vectors
            min_k: Minimum number of clusters to try
            max_k: Maximum number of clusters to try

        Returns:
            Tuple of (optimal_k, silhouette_scores_dict)
        """
        n = len(vectors)

        # Adjust max_k based on number of documents
        max_k = min(max_k, n // 3)  # At least 3 docs per cluster on average
        max_k = max(max_k, min_k)  # Ensure max_k >= min_k

        logger.info(f"Finding optimal cluster count (testing k={min_k} to k={max_k})...")

        silhouette_scores = {}

        for k in range(min_k, max_k + 1):
            # Cluster with k clusters
            assignments = self._simple_kmeans(vectors, k)

            # Calculate Silhouette score
            score = self._calculate_silhouette_score(vectors, assignments)
            silhouette_scores[k] = score

            logger.info(f"  k={k}: Silhouette score = {score:.3f}")

        # Find k with highest Silhouette score
        optimal_k = max(silhouette_scores.items(), key=lambda x: x[1])[0]
        best_score = silhouette_scores[optimal_k]

        logger.info(f"✓ Optimal cluster count: k={optimal_k} (Silhouette score: {best_score:.3f})")

        return optimal_k, silhouette_scores

    def discover_topics(
        self,
        articles: List[Dict],
        text_field: str = 'content'
    ) -> Dict:
        """
        Automatically discover topics from articles

        Args:
            articles: List of article dicts (must have text_field)
            text_field: Field containing article text

        Returns:
            Dictionary with discovered topics and assignments
        """
        logger.info(f"Discovering topics from {len(articles)} articles...")

        # Preprocess all documents
        documents = []
        for article in articles:
            text = article.get(text_field, '') + ' ' + article.get('title', '')
            tokens = self._preprocess_text(text)
            documents.append(tokens)

        # Compute TF-IDF
        logger.info("Computing TF-IDF vectors...")
        tfidf_vectors, vocab = self._compute_tfidf(documents)

        # Determine optimal number of clusters if auto_optimize enabled
        if self.auto_optimize:
            optimal_k, silhouette_scores = self._find_optimal_clusters(
                tfidf_vectors,
                min_k=max(2, self.min_articles_per_topic),
                max_k=min(20, len(articles) // 3)
            )
            num_topics = optimal_k
        else:
            num_topics = self.num_topics
            silhouette_scores = {}

        # Cluster with K-Means
        logger.info(f"Clustering into {num_topics} topics...")
        cluster_assignments = self._simple_kmeans(tfidf_vectors, num_topics)

        # Calculate final Silhouette score
        final_silhouette = self._calculate_silhouette_score(tfidf_vectors, cluster_assignments)
        logger.info(f"Final Silhouette score: {final_silhouette:.3f}")

        # Extract topic keywords (top TF-IDF terms per cluster)
        topic_keywords = {}
        topic_sizes = Counter(cluster_assignments)

        for topic_id in range(num_topics):
            # Get all vectors in this cluster
            cluster_indices = [i for i, c in enumerate(cluster_assignments) if c == topic_id]

            if not cluster_indices:
                topic_keywords[topic_id] = []
                continue

            # Average TF-IDF scores across cluster
            avg_tfidf = {}
            for word in vocab:
                avg_tfidf[word] = sum(
                    tfidf_vectors[i][word] for i in cluster_indices
                ) / len(cluster_indices)

            # Top 5 keywords for this topic
            top_words = sorted(avg_tfidf.items(), key=lambda x: x[1], reverse=True)[:5]
            topic_keywords[topic_id] = [word for word, score in top_words]

        # Generate topic names from keywords
        topic_names = {}
        for topic_id, keywords in topic_keywords.items():
            if keywords:
                # Use top 2-3 keywords as topic name
                topic_names[topic_id] = ' & '.join(keywords[:2]).title()
            else:
                topic_names[topic_id] = f"Topic {topic_id + 1}"

        # Filter out small topics
        valid_topics = {
            tid: name for tid, name in topic_names.items()
            if topic_sizes[tid] >= self.min_articles_per_topic
        }

        logger.info(f"✓ Discovered {len(valid_topics)} topics:")
        for topic_id, name in valid_topics.items():
            size = topic_sizes[topic_id]
            keywords = ', '.join(topic_keywords[topic_id][:3])
            logger.info(f"  - {name}: {size} articles ({keywords})")

        return {
            'topic_assignments': cluster_assignments,
            'topic_names': topic_names,
            'topic_keywords': topic_keywords,
            'topic_sizes': dict(topic_sizes),
            'valid_topics': valid_topics,
            'num_topics': num_topics,
            'silhouette_score': final_silhouette,
            'silhouette_scores_by_k': silhouette_scores if self.auto_optimize else {},
        }

    def get_topic_sentiment_analysis(
        self,
        articles: List[Dict],
        topic_assignments: List[int],
        topic_names: Dict[int, str]
    ) -> Dict:
        """
        Analyze sentiment per discovered topic

        Args:
            articles: List of article dicts with sentiment data
            topic_assignments: Cluster assignment for each article
            topic_names: Name for each topic

        Returns:
            Sentiment statistics per topic
        """
        topic_stats = {}

        for topic_id, topic_name in topic_names.items():
            # Get articles in this topic
            topic_articles = [
                articles[i] for i, tid in enumerate(topic_assignments)
                if tid == topic_id
            ]

            if not topic_articles:
                continue

            # Compute sentiment stats
            sentiments = [a.get('avg_sentiment', 0) for a in topic_articles]
            avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0

            topic_stats[topic_name] = {
                'article_count': len(topic_articles),
                'avg_sentiment': round(avg_sentiment, 3),
                'min_sentiment': round(min(sentiments), 3) if sentiments else 0,
                'max_sentiment': round(max(sentiments), 3) if sentiments else 0,
                'positive_articles': sum(1 for s in sentiments if s > 0.05),
                'negative_articles': sum(1 for s in sentiments if s < -0.05),
            }

        # Sort by sentiment
        topic_stats = dict(sorted(
            topic_stats.items(),
            key=lambda x: x[1]['avg_sentiment'],
            reverse=True
        ))

        return topic_stats


if __name__ == "__main__":
    # Test
    discoverer = TopicDiscovery(num_topics=5)
    print("Topic Discovery Module ready")
