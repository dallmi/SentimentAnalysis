#!/usr/bin/env python3
"""
Process extracted article data (content + comments) from browser extraction.

This script takes a single JSON file with articles and their comments,
and creates both:
1. articles.json (for article content)
2. comments.xlsx (for sentiment analysis)

Input JSON format:
[
  {
    "url": "https://...",
    "title": "...",
    "content": "...",
    "comments": [
      {"text": "...", "author": "...", "date": "..."},
      {"text": "...", "author": "...", "date": "..."}
    ]
  },
  ...
]

Usage:
    python process_extracted_data.py extracted_data.json

This will create:
    - data/input/articles.json (article content, URL-keyed)
    - data/input/comments.xlsx (comments in Excel format)

Then run analysis:
    python main.py --input data/input/comments.xlsx --articles-json data/input/articles.json
"""

import json
import sys
import os
import pandas as pd
from pathlib import Path

def process_extracted_data(input_file, articles_output=None, comments_output=None):
    """
    Process extracted data and create both articles.json and comments.xlsx.

    Args:
        input_file: Path to JSON file with extracted articles and comments
        articles_output: Path for articles.json (default: data/input/articles.json)
        comments_output: Path for comments.xlsx (default: data/input/comments.xlsx)
    """

    # Default output paths
    if articles_output is None:
        articles_output = 'data/input/articles.json'
    if comments_output is None:
        comments_output = 'data/input/comments.xlsx'

    # Ensure output directories exist
    Path(articles_output).parent.mkdir(parents=True, exist_ok=True)
    Path(comments_output).parent.mkdir(parents=True, exist_ok=True)

    # Load input data
    print(f"Loading data from {input_file}...")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File not found: {input_file}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {input_file}")
        print(f"   {e}")
        return False

    # Normalize to array
    if isinstance(data, dict):
        data = [data]

    if not isinstance(data, list):
        print(f"❌ Error: Expected JSON array or object, got {type(data).__name__}")
        return False

    print(f"✓ Loaded {len(data)} articles")

    # ========================================
    # 1. CREATE ARTICLES.JSON
    # ========================================

    print(f"\n[1/2] Creating articles.json...")
    articles_dict = {}

    for article in data:
        url = article.get('url')
        if not url:
            print(f"⚠️  Skipping article without URL")
            continue

        articles_dict[url] = {
            'title': article.get('title', ''),
            'content': article.get('content', '')
        }

    # Save articles.json
    with open(articles_output, 'w', encoding='utf-8') as f:
        json.dump(articles_dict, f, indent=2, ensure_ascii=False)

    print(f"✓ Created {articles_output}")
    print(f"  {len(articles_dict)} articles")

    # ========================================
    # 2. CREATE COMMENTS.XLSX
    # ========================================

    print(f"\n[2/2] Creating comments.xlsx...")
    comment_rows = []

    total_comments = 0
    for article in data:
        url = article.get('url', '')
        comments = article.get('comments', [])

        if not comments:
            print(f"⚠️  No comments found for {url}")
            continue

        for comment in comments:
            comment_text = comment.get('text', '')
            author = comment.get('author', '')
            date = comment.get('date', '')

            if comment_text:  # Only add if there's actual comment text
                comment_rows.append({
                    'URL': url,
                    'Comment': comment_text,
                    'Author': author,
                    'Date': date
                })
                total_comments += 1

    if not comment_rows:
        print(f"⚠️  Warning: No comments found in any article!")
        print(f"   Articles may not have comments, or extraction failed.")
        return False

    # Create DataFrame
    df = pd.DataFrame(comment_rows)

    # Save to Excel
    df.to_excel(comments_output, index=False, sheet_name='Sheet1')

    print(f"✓ Created {comments_output}")
    print(f"  {total_comments} comments from {len(data)} articles")

    # ========================================
    # SUMMARY
    # ========================================

    print(f"\n{'='*70}")
    print(f"PROCESSING COMPLETE")
    print(f"{'='*70}")
    print(f"Input:  {input_file}")
    print(f"Output: {articles_output}")
    print(f"        {comments_output}")
    print(f"\nStatistics:")
    print(f"  Articles: {len(articles_dict)}")
    print(f"  Comments: {total_comments}")

    # Show breakdown per article
    print(f"\nBreakdown by Article:")
    for article in data:
        url = article.get('url', 'Unknown URL')
        title = article.get('title', 'No title')
        num_comments = len(article.get('comments', []))

        # Truncate URL if too long
        display_url = url if len(url) < 60 else url[:57] + '...'
        print(f"  • {title}")
        print(f"    {display_url}")
        print(f"    {num_comments} comments")

    print(f"\n{'='*70}")
    print(f"NEXT STEP")
    print(f"{'='*70}")
    print(f"Run sentiment analysis with:")
    print(f"  python main.py --input {comments_output} --articles-json {articles_output}")
    print(f"\nOr if you want to skip article content analysis:")
    print(f"  python main.py --input {comments_output} --no-scraping")

    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python process_extracted_data.py <input_json_file>")
        print("\nExample:")
        print("  python process_extracted_data.py extracted_articles.json")
        print("\nThe input JSON should contain articles with comments from browser extraction.")
        print("\nOutput:")
        print("  - data/input/articles.json (article content)")
        print("  - data/input/comments.xlsx (comments for analysis)")
        sys.exit(1)

    input_file = sys.argv[1]
    success = process_extracted_data(input_file)

    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
