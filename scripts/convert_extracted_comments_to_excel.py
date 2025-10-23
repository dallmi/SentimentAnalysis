#!/usr/bin/env python3
"""
Convert extracted comments from browser to Excel format

This script takes the JSON output from extract_article_with_comments.js
and converts it to the Excel format needed for sentiment analysis.

Usage:
1. Extract articles with comments using extract_article_with_comments.js
2. Save the JSON outputs to a file (one article per line, or as an array)
3. Run: python convert_extracted_comments_to_excel.py input.json output.xlsx
"""

import json
import sys
import pandas as pd
from pathlib import Path

def load_extracted_data(input_file):
    """
    Load extracted article data from JSON file.

    Supports two formats:
    1. Array of articles: [{"url": ..., "comments": [...]}, ...]
    2. Single article: {"url": ..., "comments": [...]}
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Normalize to array
    if isinstance(data, dict):
        data = [data]

    return data

def convert_to_excel(articles, output_file):
    """
    Convert extracted articles with comments to Excel format.

    Excel format:
    | URL | Comment |
    """
    rows = []

    for article in articles:
        url = article.get('url', '')
        comments = article.get('comments', [])

        if not comments:
            print(f"⚠️  No comments found for {url}")
            continue

        for comment in comments:
            comment_text = comment.get('text', '')
            author = comment.get('author', '')
            date = comment.get('date', '')

            # Create row
            row = {
                'URL': url,
                'Comment': comment_text,
                'Author': author,
                'Date': date
            }
            rows.append(row)

    # Create DataFrame
    df = pd.DataFrame(rows)

    # Save to Excel
    df.to_excel(output_file, index=False, sheet_name='Sheet1')

    print(f"✓ Created {output_file}")
    print(f"  {len(df)} comments from {len(articles)} articles")
    print(f"\nBreakdown:")
    for article in articles:
        url = article.get('url', '')
        num_comments = len(article.get('comments', []))
        print(f"  {url}: {num_comments} comments")

    return df

def main():
    if len(sys.argv) < 2:
        print("Usage: python convert_extracted_comments_to_excel.py <input_json> [output_xlsx]")
        print("\nExample:")
        print("  python convert_extracted_comments_to_excel.py extracted_data.json comments.xlsx")
        print("\nThe input JSON should contain the output from extract_article_with_comments.js")
        print("It can be either a single article or an array of articles.")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'data/input/comments_extracted.xlsx'

    # Ensure output directory exists
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    # Load data
    print(f"Loading data from {input_file}...")
    try:
        articles = load_extracted_data(input_file)
        print(f"✓ Loaded {len(articles)} articles")
    except FileNotFoundError:
        print(f"❌ File not found: {input_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        sys.exit(1)

    # Convert to Excel
    print(f"\nConverting to Excel format...")
    df = convert_to_excel(articles, output_file)

    print(f"\n{'='*60}")
    print(f"CONVERSION COMPLETE")
    print(f"{'='*60}")
    print(f"You can now run sentiment analysis with:")
    print(f"  python main.py --input {output_file}")
    print(f"\nOr if you also have article content JSON:")
    print(f"  python main.py --input {output_file} --articles-json data/input/articles.json")

if __name__ == '__main__':
    main()
