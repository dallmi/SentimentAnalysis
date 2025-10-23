"""
Test script for extractive summarization function
"""

import sys
from pathlib import Path

# Add LLM Solution to path
sys.path.insert(0, str(Path(__file__).parent / "LLM Solution"))

from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import re


def extractive_summarize(text: str, embedding_model, num_sentences: int = 3) -> str:
    """
    Create extractive summary by selecting most representative sentences using BERT embeddings.
    """
    if not text or not text.strip():
        return ""

    # Split text into sentences
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


# Test with a sample German article
if __name__ == "__main__":
    print("Loading model...")
    model_path = "P:/IMPORTANT/Projects/SentimentAnalysis/LLM Solution/models/paraphrase-multilingual-MiniLM-L12-v2"
    model = SentenceTransformer(model_path)
    print("Model loaded!\n")

    # Sample German text (corporate intranet article style)
    test_article = """
    Neue Homeoffice-Regelung ab 2025.
    Die Geschäftsführung hat eine neue Richtlinie für flexibles Arbeiten verabschiedet.
    Ab dem 1. Januar 2025 können alle Mitarbeiter bis zu drei Tage pro Woche von zu Hause arbeiten.
    Diese Entscheidung wurde nach umfangreichen Mitarbeiterbefragungen getroffen.
    Die IT-Abteilung stellt die notwendige Hardware und Software zur Verfügung.
    Für die Nutzung ist ein Antrag über das HR-Portal erforderlich.
    Führungskräfte müssen die Anträge innerhalb von fünf Arbeitstagen prüfen.
    Die neue Regelung gilt für alle Abteilungen außer dem Kundenservice.
    Mitarbeiter im Kundenservice haben spezielle Schichtpläne und sind davon ausgenommen.
    Weitere Details finden Sie im Mitarbeiterhandbuch oder können bei HR erfragt werden.
    """

    print("Original text:")
    print(test_article.strip())
    print("\n" + "="*70 + "\n")

    print("Summary (3 sentences):")
    summary = extractive_summarize(test_article, model, num_sentences=3)
    print(summary)
    print("\n" + "="*70 + "\n")

    # Test with shorter text
    short_text = "Neue Homeoffice-Regelung ab 2025. Die Geschäftsführung hat flexibles Arbeiten genehmigt."
    print("Short text (2 sentences):")
    print(short_text)
    print("\nSummary (should return all):")
    summary_short = extractive_summarize(short_text, model, num_sentences=3)
    print(summary_short)
