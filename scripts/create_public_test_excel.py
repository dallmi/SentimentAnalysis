"""
Creates a test Excel file with public URLs for testing web scraping functionality.
Uses real, public news sites that are accessible without authentication.
"""

import pandas as pd
from pathlib import Path


def create_public_test_excel():
    """Create test Excel file with public URLs for scraping."""

    # Sample data: Public URLs and test comments
    data = {
        'URL': [
            # BBC News articles (publicly accessible)
            'https://www.bbc.com/news',
            'https://www.bbc.com/news',
            'https://www.bbc.com/news',

            # Wikipedia articles (publicly accessible)
            'https://en.wikipedia.org/wiki/Artificial_intelligence',
            'https://en.wikipedia.org/wiki/Artificial_intelligence',
            'https://en.wikipedia.org/wiki/Artificial_intelligence',

            # Simple example.com
            'http://example.com',
            'http://example.com',
        ],
        'Comment': [
            # BBC comments
            'Great news coverage, very informative.',
            'Excellent journalism!',
            'Not very detailed, could be better.',

            # Wikipedia comments
            'Very comprehensive article about AI.',
            'Excellent overview of the topic!',
            'Great resource for learning.',

            # Example.com comments
            'Interesting site.',
            'Simple but clear.',
        ]
    }

    # Create DataFrame
    df = pd.DataFrame(data)

    # Save to Excel
    output_dir = Path(__file__).parent / 'data' / 'input'
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / 'public_test_articles.xlsx'
    df.to_excel(output_file, index=False, sheet_name='Articles')

    print(f"✅ Public test Excel file created: {output_file}")
    print(f"\nFile contains:")
    print(f"  - {len(df)} rows (comments)")
    print(f"  - {df['URL'].nunique()} unique URLs")
    print(f"\nPublic URLs for testing web scraping:")
    for i, url in enumerate(df['URL'].unique(), 1):
        article_comments = df[df['URL'] == url]
        print(f"  {i}. {url}: {len(article_comments)} comments")

    print(f"\n⚠️  NOTE: These are PUBLIC websites for testing only!")
    print(f"     For real analysis, replace with your corporate intranet URLs.")

    print(f"\nUsage (WITH web scraping):")
    print(f"  python main.py --input {output_file}")
    print(f"\nThis will:")
    print(f"  1. Scrape content from each URL")
    print(f"  2. Analyze comment sentiments")
    print(f"  3. Categorize articles based on scraped content")
    print(f"  4. Cluster similar articles")

    print(f"\n⚠️  WARNING: Web scraping may fail if:")
    print(f"  - Sites block automated requests")
    print(f"  - Corporate proxy blocks external sites")
    print(f"  - Network issues occur")
    print(f"\n  If scraping fails, you'll see error messages but analysis continues.")

    return output_file


if __name__ == "__main__":
    create_public_test_excel()
