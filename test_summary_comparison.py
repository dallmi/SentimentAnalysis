#!/usr/bin/env python3
"""
Test script to compare EXTRACTIVE vs ABSTRACTIVE summarization
"""

import sys
from pathlib import Path

# Add LLM Solution to path
sys.path.insert(0, str(Path(__file__).parent / "LLM Solution"))

from sentence_transformers import SentenceTransformer
from abstractive_summarizer import AbstractiveSummarizer

def extractive_summarize(text, embedding_model, num_sentences=3):
    """Extract top N sentences based on semantic similarity to full text."""
    if not text or not text.strip():
        return ""

    # Split into sentences
    sentences = [s.strip() for s in text.split('.') if s.strip()]

    if len(sentences) <= num_sentences:
        return text

    # Get embeddings
    sentence_embeddings = embedding_model.encode(sentences)
    full_text_embedding = embedding_model.encode([text])

    # Calculate similarities
    from sklearn.metrics.pairwise import cosine_similarity
    similarities = cosine_similarity(sentence_embeddings, full_text_embedding).flatten()

    # Get top N sentences
    top_indices = similarities.argsort()[-num_sentences:][::-1]
    top_indices = sorted(top_indices)

    summary = '. '.join([sentences[i] for i in top_indices]) + '.'
    return summary


def main():
    print("="*70)
    print("VERGLEICH: EXTRACTIVE vs ABSTRACTIVE SUMMARIZATION")
    print("="*70)

    # Test article (German corporate text)
    test_article = """
    Die Geschäftsführung der Example AG hat am Montag umfassende neue Regelungen
    für Homeoffice und flexible Arbeitszeiten angekündigt. Nach mehrmonatigen
    Verhandlungen mit dem Betriebsrat wurde eine Einigung erzielt, die ab dem
    1. Februar 2025 in Kraft tritt. Mitarbeiter können künftig bis zu drei Tage
    pro Woche von zu Hause arbeiten. Die neue Regelung gilt für alle
    Vollzeitbeschäftigten, die seit mindestens sechs Monaten im Unternehmen tätig sind.
    Teilzeitbeschäftigte erhalten anteilig entsprechende Homeoffice-Tage.
    Der Vorstand betonte, dass diese Maßnahme die Work-Life-Balance der
    Mitarbeiter verbessern und gleichzeitig die Produktivität steigern soll.
    Eine Evaluierung der neuen Regelung ist nach sechs Monaten geplant.
    """

    print("\n📄 ORIGINAL ARTIKEL:")
    print("-" * 70)
    print(test_article.strip())
    print(f"\nLänge: {len(test_article.split())} Wörter")

    # Load models
    print("\n" + "="*70)
    print("Lade Modelle...")
    print("="*70)

    # Extractive (sentence-transformers)
    print("\n[1/2] Lade Embedding Model für Extractive...")
    embedding_model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    print("   ✓ Embedding Model geladen")

    # Abstractive (mBART)
    print("\n[2/2] Lade mBART Model für Abstractive...")
    abstractive_summarizer = AbstractiveSummarizer()
    print("   ✓ mBART Model geladen")

    # Generate summaries
    print("\n" + "="*70)
    print("GENERIERE ZUSAMMENFASSUNGEN...")
    print("="*70)

    # EXTRACTIVE
    print("\n📋 EXTRACTIVE SUMMARY (kopiert Sätze):")
    print("-" * 70)
    extractive_summary = extractive_summarize(test_article, embedding_model, num_sentences=3)
    print(extractive_summary)
    print(f"\nLänge: {len(extractive_summary.split())} Wörter")
    print("⚠️  Beachte: 1:1 kopierte Sätze aus dem Original!")

    # ABSTRACTIVE
    print("\n" + "="*70)
    print("✨ ABSTRACTIVE SUMMARY (mBART generiert neuen Text):")
    print("-" * 70)
    abstractive_summary = abstractive_summarizer.summarize(
        test_article,
        source_lang="de_DE",
        max_length=100,
        min_length=30
    )
    print(abstractive_summary)
    print(f"\nLänge: {len(abstractive_summary.split())} Wörter")
    print("✓ Beachte: Neu formulierter, kompakter Text!")

    # Comparison
    print("\n" + "="*70)
    print("VERGLEICH:")
    print("="*70)
    print(f"Original:     {len(test_article.split())} Wörter")
    print(f"Extractive:   {len(extractive_summary.split())} Wörter (kopiert)")
    print(f"Abstractive:  {len(abstractive_summary.split())} Wörter (generiert)")
    print("\n✓ Abstractive ist kompakter und neu formuliert!")


if __name__ == "__main__":
    main()
