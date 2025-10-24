#!/usr/bin/env python3
"""
End-to-End Test for BERTopic Sentiment Analysis
- Test with realistic 15-article dataset
- Verify topic clustering quality (should find 3 topics: AI, Sustainability, Remote Work)
- Compare mBART topic labels vs BERTopic keywords
- Measure performance
"""

import subprocess
import time
import json
import sys
from pathlib import Path
import pandas as pd

def run_test():
    """Run end-to-end test"""

    print("=" * 80)
    print("END-TO-END TEST: BERTopic Sentiment Analysis")
    print("=" * 80)
    print()

    # Step 1: Verify test data exists
    test_file = "test_realistic_articles.json"
    if not Path(test_file).exists():
        print(f"❌ Test file not found: {test_file}")
        print("   Creating test dataset first...")
        subprocess.run(["python3", "create_test_dataset.py"], check=True)
        print()

    with open(test_file, 'r') as f:
        articles = json.load(f)

    print(f"✓ Test dataset loaded: {len(articles)} articles")
    print(f"  - Expected topics: AI/Technology (4), Sustainability (4), Remote Work/HR (7)")
    print(f"  - Total comments: {sum(len(a['comments']) for a in articles)}")
    print()

    # Step 2: Run WITHOUT --abstractive (BERTopic keywords only)
    print("=" * 80)
    print("TEST 1: WITHOUT --abstractive (BERTopic keywords)")
    print("=" * 80)
    print()

    output_file_keywords = "data/output/test_bertopic_keywords.xlsx"

    start_time = time.time()
    try:
        result = subprocess.run([
            "python3", "main_bertopic.py",
            "--input", test_file,
            "--output", output_file_keywords
        ], capture_output=True, text=True, timeout=300)

        elapsed_keywords = time.time() - start_time

        print("STDOUT:")
        print(result.stdout)
        print()

        if result.returncode != 0:
            print("STDERR:")
            print(result.stderr)
            print(f"\n❌ Test 1 FAILED with return code {result.returncode}")
            return False
        else:
            print(f"✓ Test 1 PASSED in {elapsed_keywords:.1f}s")
            print()
    except subprocess.TimeoutExpired:
        print("❌ Test 1 TIMEOUT (>5 minutes)")
        return False
    except Exception as e:
        print(f"❌ Test 1 ERROR: {e}")
        return False

    # Step 3: Run WITH --abstractive (mBART topic labels)
    print("=" * 80)
    print("TEST 2: WITH --abstractive (mBART topic labels)")
    print("=" * 80)
    print()

    output_file_mbart = "data/output/test_mbart_labels.xlsx"

    start_time = time.time()
    try:
        result = subprocess.run([
            "python3", "main_bertopic.py",
            "--input", test_file,
            "--output", output_file_mbart,
            "--abstractive"
        ], capture_output=True, text=True, timeout=600)

        elapsed_mbart = time.time() - start_time

        print("STDOUT:")
        print(result.stdout)
        print()

        if result.returncode != 0:
            print("STDERR:")
            print(result.stderr)
            print(f"\n❌ Test 2 FAILED with return code {result.returncode}")
            return False
        else:
            print(f"✓ Test 2 PASSED in {elapsed_mbart:.1f}s")
            print()
    except subprocess.TimeoutExpired:
        print("❌ Test 2 TIMEOUT (>10 minutes)")
        return False
    except Exception as e:
        print(f"❌ Test 2 ERROR: {e}")
        return False

    # Step 4: Compare results
    print("=" * 80)
    print("RESULTS COMPARISON")
    print("=" * 80)
    print()

    try:
        # Load both Excel files
        df_keywords = pd.read_excel(output_file_keywords, sheet_name='Articles')
        df_mbart = pd.read_excel(output_file_mbart, sheet_name='Articles')

        print(f"📊 BERTopic Keywords (Test 1):")
        print(f"   Time: {elapsed_keywords:.1f}s")
        print(f"   Topics found: {df_keywords['Topic_ID'].nunique()}")
        print()

        topic_counts_keywords = df_keywords.groupby(['Topic', 'Topic_ID']).size().reset_index(name='Count')
        for _, row in topic_counts_keywords.iterrows():
            print(f"   Topic {row['Topic_ID']}: {row['Count']} articles - '{row['Topic']}'")
        print()

        print(f"📊 mBART Topic Labels (Test 2):")
        print(f"   Time: {elapsed_mbart:.1f}s")
        print(f"   Topics found: {df_mbart['Topic_ID'].nunique()}")
        print()

        topic_counts_mbart = df_mbart.groupby(['Topic', 'Topic_ID']).size().reset_index(name='Count')
        for _, row in topic_counts_mbart.iterrows():
            print(f"   Topic {row['Topic_ID']}: {row['Count']} articles - '{row['Topic']}'")
        print()

        # Performance comparison
        print(f"⏱️  PERFORMANCE:")
        print(f"   WITHOUT --abstractive: {elapsed_keywords:.1f}s ({elapsed_keywords/len(articles):.2f}s per article)")
        print(f"   WITH --abstractive:    {elapsed_mbart:.1f}s ({elapsed_mbart/len(articles):.2f}s per article)")
        print(f"   Difference: {elapsed_mbart - elapsed_keywords:.1f}s ({(elapsed_mbart/elapsed_keywords - 1)*100:.0f}% slower)")
        print()

        # Clustering quality check
        print(f"✅ CLUSTERING QUALITY:")
        num_topics = df_keywords['Topic_ID'].nunique()
        if num_topics == 3:
            print(f"   ✓ Found exactly 3 topics (expected: AI, Sustainability, Remote Work)")
        elif num_topics < 3:
            print(f"   ⚠️  Found only {num_topics} topics (expected 3) - topics may be merged")
        else:
            print(f"   ⚠️  Found {num_topics} topics (expected 3) - some topics may be split")
        print()

        # Label quality comparison
        print(f"📝 LABEL QUALITY COMPARISON:")
        print()
        print("BERTopic Keywords (Test 1):")
        for _, row in topic_counts_keywords.iterrows():
            print(f"  Topic {row['Topic_ID']}: '{row['Topic']}'")
        print()
        print("mBART Labels (Test 2):")
        for _, row in topic_counts_mbart.iterrows():
            print(f"  Topic {row['Topic_ID']}: '{row['Topic']}'")
        print()

        # Check sentiment analysis
        if 'Avg_Sentiment' in df_keywords.columns:
            avg_sentiment = df_keywords['Avg_Sentiment'].mean()
            print(f"💭 SENTIMENT ANALYSIS:")
            print(f"   Average sentiment: {avg_sentiment:.3f}")
            print(f"   Comments analyzed: {df_keywords['Total_Comments'].sum():.0f}")
            print(f"   Positive: {df_keywords['Positive_Count'].sum():.0f}")
            print(f"   Negative: {df_keywords['Negative_Count'].sum():.0f}")
            print(f"   Neutral: {df_keywords['Neutral_Count'].sum():.0f}")
        print()

    except Exception as e:
        print(f"❌ Error comparing results: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("=" * 80)
    print("✅ END-TO-END TEST COMPLETED SUCCESSFULLY")
    print("=" * 80)
    print()
    print(f"Output files:")
    print(f"  - BERTopic Keywords: {output_file_keywords}")
    print(f"  - mBART Labels:      {output_file_mbart}")
    print()

    return True

if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
