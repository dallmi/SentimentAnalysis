"""
BERT-based Content Analyzer
Uses BERT embeddings to understand article content and cluster similar topics
"""

import numpy as np
from typing import List, Dict, Optional
import logging
from pathlib import Path
import sys

# Add LLM Solution to path
sys.path.insert(0, str(Path(__file__).parent.parent / "LLM Solution"))

try:
    from transformers import AutoTokenizer, AutoModel
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BERTContentAnalyzer:
    """
    Analyzes article content using BERT embeddings for semantic understanding.

    This allows us to:
    - Understand article topics semantically (not just keywords)
    - Cluster similar articles together
    - Identify which content themes resonate with employees
    """

    def __init__(self, model_dir: Optional[str] = None):
        """
        Initialize BERT content analyzer.

        Args:
            model_dir: Path to locally saved BERT model (for offline mode)
        """
        self.model = None
        self.tokenizer = None
        self.embeddings_cache = {}

        if not TRANSFORMERS_AVAILABLE:
            logger.warning("⚠️  Transformers not available. BERT content analysis disabled.")
            logger.warning("   Install with: pip install transformers torch")
            return

        # Try to load model
        if model_dir is None:
            model_dir = Path(__file__).parent.parent / "LLM Solution" / "models" / "sentiment-multilingual"

        try:
            if Path(model_dir).exists():
                logger.info(f"Loading BERT model from {model_dir}...")
                self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
                self.model = AutoModel.from_pretrained(model_dir)
                logger.info("✓ BERT model loaded for content analysis")
            else:
                logger.info("Downloading BERT model (first time only)...")
                model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModel.from_pretrained(model_name)
                logger.info("✓ BERT model downloaded and loaded")

            # Set to evaluation mode
            self.model.eval()

        except Exception as e:
            logger.error(f"❌ Could not load BERT model: {e}")
            logger.warning("   Content analysis will use fallback method")

    def get_embedding(self, text: str, max_length: int = 512) -> np.ndarray:
        """
        Get BERT embedding for text.

        Args:
            text: Input text
            max_length: Maximum token length (512 for BERT)

        Returns:
            768-dimensional embedding vector
        """
        if self.model is None or self.tokenizer is None:
            # Fallback: return random embedding (for testing without BERT)
            return np.random.randn(768)

        # Check cache
        cache_key = text[:100]  # Use first 100 chars as cache key
        if cache_key in self.embeddings_cache:
            return self.embeddings_cache[cache_key]

        try:
            # Tokenize
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=max_length,
                padding=True
            )

            # Get embeddings (no gradient needed)
            with torch.no_grad():
                outputs = self.model(**inputs)

            # Use [CLS] token embedding as document embedding
            embedding = outputs.last_hidden_state[:, 0, :].numpy()[0]

            # Cache it
            self.embeddings_cache[cache_key] = embedding

            return embedding

        except Exception as e:
            logger.warning(f"Error getting embedding: {e}")
            return np.random.randn(768)

    def get_embeddings_batch(self, texts: List[str], max_length: int = 512) -> np.ndarray:
        """
        Get BERT embeddings for multiple texts (more efficient).

        Args:
            texts: List of input texts
            max_length: Maximum token length

        Returns:
            Array of shape (len(texts), 768)
        """
        if self.model is None or self.tokenizer is None:
            return np.random.randn(len(texts), 768)

        embeddings = []
        batch_size = 8  # Process 8 at a time to avoid memory issues

        logger.info(f"Creating BERT embeddings for {len(texts)} articles...")

        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]

            try:
                # Tokenize batch
                inputs = self.tokenizer(
                    batch_texts,
                    return_tensors="pt",
                    truncation=True,
                    max_length=max_length,
                    padding=True
                )

                # Get embeddings
                with torch.no_grad():
                    outputs = self.model(**inputs)

                # Use [CLS] token embeddings
                batch_embeddings = outputs.last_hidden_state[:, 0, :].numpy()
                embeddings.append(batch_embeddings)

            except Exception as e:
                logger.warning(f"Error in batch {i//batch_size}: {e}")
                # Fallback for this batch
                embeddings.append(np.random.randn(len(batch_texts), 768))

            # Progress
            if (i // batch_size) % 5 == 0:
                logger.info(f"  Processed {min(i + batch_size, len(texts))}/{len(texts)} articles")

        result = np.vstack(embeddings)
        logger.info(f"✓ Created embeddings with shape {result.shape}")
        return result

    def cluster_by_content(
        self,
        texts: List[str],
        n_clusters: Optional[int] = None,
        min_clusters: int = 2,
        max_clusters: int = 10
    ) -> Dict:
        """
        Cluster articles by content using BERT embeddings.

        Args:
            texts: Article texts (title + content)
            n_clusters: Fixed number of clusters (None = auto-optimize)
            min_clusters: Minimum clusters to try
            max_clusters: Maximum clusters to try

        Returns:
            Dictionary with clustering results
        """
        # Get embeddings
        embeddings = self.get_embeddings_batch(texts)

        if n_clusters is None:
            # Auto-optimize number of clusters
            logger.info(f"Auto-optimizing clusters ({min_clusters}-{max_clusters})...")
            best_k = self._find_optimal_clusters(
                embeddings,
                min_k=min_clusters,
                max_k=min(max_clusters, len(texts) - 1)
            )
            n_clusters = best_k
            logger.info(f"✓ Optimal number of clusters: {n_clusters}")

        # Perform clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(embeddings)

        # Calculate silhouette score
        if len(set(cluster_labels)) > 1:
            silhouette = silhouette_score(embeddings, cluster_labels)
        else:
            silhouette = 0.0

        # Get cluster centers
        cluster_centers = kmeans.cluster_centers_

        return {
            'cluster_labels': cluster_labels,
            'n_clusters': n_clusters,
            'silhouette_score': silhouette,
            'cluster_centers': cluster_centers,
            'embeddings': embeddings
        }

    def _find_optimal_clusters(
        self,
        embeddings: np.ndarray,
        min_k: int = 2,
        max_k: int = 10
    ) -> int:
        """
        Find optimal number of clusters using silhouette score.

        Args:
            embeddings: Article embeddings
            min_k: Minimum clusters
            max_k: Maximum clusters

        Returns:
            Optimal k
        """
        silhouette_scores = {}

        for k in range(min_k, max_k + 1):
            try:
                kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                labels = kmeans.fit_predict(embeddings)

                if len(set(labels)) > 1:
                    score = silhouette_score(embeddings, labels)
                    silhouette_scores[k] = score
                else:
                    silhouette_scores[k] = -1.0

            except Exception as e:
                logger.warning(f"Error with k={k}: {e}")
                silhouette_scores[k] = -1.0

        # Return k with best silhouette score
        best_k = max(silhouette_scores.items(), key=lambda x: x[1])[0]
        return best_k

    def get_cluster_theme(
        self,
        cluster_texts: List[str],
        max_keywords: int = 5
    ) -> str:
        """
        Extract theme/topic from cluster of articles.

        Args:
            cluster_texts: Texts in this cluster
            max_keywords: Maximum keywords to extract

        Returns:
            Theme string (e.g., "AI Tools and Innovation")
        """
        # Simple keyword extraction from cluster
        # Combine all texts
        combined_text = " ".join(cluster_texts).lower()

        # Count word frequency
        words = combined_text.split()
        word_freq = {}

        # Common stop words to ignore
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these',
            'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which',
            'who', 'when', 'where', 'why', 'how', 'der', 'die', 'das', 'und',
            'oder', 'aber', 'für', 'mit', 'von', 'zu', 'im', 'am'
        }

        for word in words:
            word = word.strip('.,;:!?()"\'')
            if len(word) > 3 and word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1

        # Get top keywords
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        keywords = [word for word, freq in top_words[:max_keywords]]

        # Create theme name
        if len(keywords) >= 2:
            theme = f"{keywords[0].capitalize()} & {keywords[1].capitalize()}"
        elif len(keywords) == 1:
            theme = keywords[0].capitalize()
        else:
            theme = "Mixed Topics"

        return theme


if __name__ == "__main__":
    # Test
    analyzer = BERTContentAnalyzer()

    test_texts = [
        "New AI tools for employees to improve productivity",
        "Employee benefits update for 2024",
        "Machine learning workshop announcement"
    ]

    # Test embeddings
    embeddings = analyzer.get_embeddings_batch(test_texts)
    print(f"Created embeddings with shape: {embeddings.shape}")

    # Test clustering
    results = analyzer.cluster_by_content(test_texts, n_clusters=2)
    print(f"Cluster labels: {results['cluster_labels']}")
    print(f"Silhouette score: {results['silhouette_score']:.3f}")
