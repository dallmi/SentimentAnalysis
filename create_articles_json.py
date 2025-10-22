#!/usr/bin/env python3
"""
Create articles.json file from manually extracted article content.

This script helps you create a JSON file with article content that was
manually extracted using the browser DevTools console script.

Usage:
1. Use extract_article_content.js in browser to extract each article
2. Paste each JSON object into this script
3. Run this script to create articles.json
"""

import json
import os

def create_articles_json():
    """
    Create articles.json from manually extracted content.

    Edit the 'articles' list below to add your extracted articles.
    """

    # Add your extracted articles here
    # Copy the JSON output from the browser console for each article
    articles = [
        # Example format:
        # {
        #     "url": "https://your-intranet.com/article1.aspx",
        #     "title": "Article Title",
        #     "content": "Full article text content..."
        # },
        # {
        #     "url": "https://your-intranet.com/article2.aspx",
        #     "title": "Another Article",
        #     "content": "More article content..."
        # }
    ]

    # Convert to dictionary with URL as key
    articles_dict = {article['url']: article for article in articles}

    # Save to JSON file
    output_dir = 'data/input'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'articles.json')

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(articles_dict, f, indent=2, ensure_ascii=False)

    print(f"✓ Created {output_file}")
    print(f"  {len(articles)} articles saved")
    print(f"\nStructure:")
    print(f"  {{")
    print(f"    \"url1\": {{\"title\": \"...\", \"content\": \"...\"}},")
    print(f"    \"url2\": {{\"title\": \"...\", \"content\": \"...\"}}")
    print(f"  }}")
    print(f"\nNext steps:")
    print(f"  1. Edit this file and paste your extracted articles into the 'articles' list")
    print(f"  2. Run: python create_articles_json.py")
    print(f"  3. Use the JSON file with: python main.py --input your_excel.xlsx --articles-json data/input/articles.json")

    return articles_dict

if __name__ == '__main__':
    articles_dict = create_articles_json()

    if not articles_dict:
        print("\n⚠️  No articles found!")
        print("Please edit this file and add your extracted articles to the 'articles' list.")
        print("\nExample:")
        print("""
articles = [
    {
        "url": "https://your-intranet.com/article.aspx",
        "title": "Sample Article",
        "content": "This is the article content extracted from the browser..."
    }
]
""")
