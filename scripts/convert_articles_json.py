#!/usr/bin/env python3
"""
Convert flat articles JSON to URL-keyed format for main.py

Usage:
    python convert_articles_json.py data/input/article_content.json

This will create data/input/articles.json in the correct format.
"""

import json
import sys
import os

def convert_flat_to_keyed(input_file, output_file=None):
    """
    Convert flat array structure to URL-keyed dictionary structure.

    From:
    [
        {"url": "...", "title": "...", "content": "..."},
        {"url": "...", "title": "...", "content": "..."}
    ]

    To:
    {
        "url1": {"title": "...", "content": "..."},
        "url2": {"title": "...", "content": "..."}
    }
    """

    # Read input file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            articles_array = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File not found: {input_file}")
        print(f"\nPlease make sure your article_content.json file exists.")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {input_file}")
        print(f"   {e}")
        return False

    # Validate structure
    if not isinstance(articles_array, list):
        print(f"❌ Error: Expected a JSON array, got {type(articles_array).__name__}")
        return False

    if len(articles_array) == 0:
        print(f"⚠️  Warning: No articles found in {input_file}")
        return False

    print(f"✓ Loaded {len(articles_array)} articles from {input_file}")

    # Convert to URL-keyed dictionary
    articles_dict = {}
    for idx, article in enumerate(articles_array):
        if not isinstance(article, dict):
            print(f"⚠️  Skipping item {idx}: Not a dictionary")
            continue

        url = article.get('url')
        if not url:
            print(f"⚠️  Skipping item {idx}: No URL found")
            continue

        # Extract title and content
        articles_dict[url] = {
            'title': article.get('title', ''),
            'content': article.get('content', '')
        }

    print(f"✓ Converted {len(articles_dict)} articles to URL-keyed format")

    # Determine output file
    if output_file is None:
        output_file = os.path.join(os.path.dirname(input_file), 'articles.json')

    # Save output
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(articles_dict, f, indent=2, ensure_ascii=False)

    print(f"✓ Saved to {output_file}")

    # Show summary
    print(f"\n{'='*60}")
    print(f"CONVERSION COMPLETE")
    print(f"{'='*60}")
    print(f"Input:  {input_file}")
    print(f"Output: {output_file}")
    print(f"Articles: {len(articles_dict)}")
    print(f"\nURLs:")
    for url in list(articles_dict.keys())[:5]:
        print(f"  - {url}")
    if len(articles_dict) > 5:
        print(f"  ... and {len(articles_dict) - 5} more")

    print(f"\n{'='*60}")
    print(f"NEXT STEPS")
    print(f"{'='*60}")
    print(f"1. Make sure you have your comments Excel file ready")
    print(f"2. Run the analysis:")
    print(f"   python main.py --input YOUR_COMMENTS.xlsx --articles-json {output_file}")

    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python convert_articles_json.py <input_json_file>")
        print("\nExample:")
        print("  python convert_articles_json.py data/input/article_content.json")
        print("\nThis will create data/input/articles.json in the correct format.")
        sys.exit(1)

    input_file = sys.argv[1]
    success = convert_flat_to_keyed(input_file)

    sys.exit(0 if success else 1)
