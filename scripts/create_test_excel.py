"""
Creates a test Excel file with sample article URLs and comments
for testing the sentiment analysis system.
"""

import pandas as pd
from pathlib import Path


def create_test_excel():
    """Create test Excel file with sample data."""

    # Sample data: Article URLs and Comments
    data = {
        'URL': [
            'https://example.com/article/ai-innovation',
            'https://example.com/article/ai-innovation',
            'https://example.com/article/ai-innovation',
            'https://example.com/article/employee-spotlight',
            'https://example.com/article/employee-spotlight',
            'https://example.com/article/employee-spotlight',
            'https://example.com/article/office-redesign',
            'https://example.com/article/office-redesign',
            'https://example.com/article/new-training-program',
            'https://example.com/article/new-training-program',
            'https://example.com/article/new-training-program',
            'https://example.com/article/company-results',
            'https://example.com/article/company-results',
            'https://example.com/article/sustainability-initiative',
            'https://example.com/article/sustainability-initiative',
        ],
        'Comment': [
            # AI Article - Mixed sentiment
            'Great article! Very informative about the new AI tools.',
            'Excellent explanation of how AI will help our work.',
            'Not sure I understand all the technical details.',

            # Employee Spotlight - Very positive
            'Love these employee stories! Very inspiring.',
            'Great to see recognition of our colleagues.',
            'Fantastic profile, well written!',

            # Office Redesign - Negative
            'Not happy about the open office concept.',
            'I preferred the old layout, this is too loud.',

            # Training Program - Positive
            'Excited about this new training opportunity!',
            'Perfect timing, I needed to learn these skills.',
            'Great initiative by HR!',

            # Company Results - Neutral/Mixed
            'Interesting results for Q3.',
            'Good to see growth but margins could be better.',

            # Sustainability - Positive
            'Love the focus on sustainability!',
            'Great to see the company taking climate action seriously.',
        ]
    }

    # Create DataFrame
    df = pd.DataFrame(data)

    # Save to Excel
    output_dir = Path(__file__).parent / 'data' / 'input'
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / 'test_articles.xlsx'
    df.to_excel(output_file, index=False, sheet_name='Articles')

    print(f"✅ Test Excel file created: {output_file}")
    print(f"\nFile contains:")
    print(f"  - {len(df)} rows (comments)")
    print(f"  - {df['URL'].nunique()} unique articles")
    print(f"\nArticles:")
    for i, url in enumerate(df['URL'].unique(), 1):
        article_comments = df[df['URL'] == url]
        print(f"  {i}. {url.split('/')[-1]}: {len(article_comments)} comments")

    print(f"\nUsage:")
    print(f"  python main.py --input {output_file}")
    print(f"\nNote: These are example URLs. For real testing:")
    print(f"  1. Replace URLs with your actual intranet article URLs")
    print(f"  2. Replace comments with real comments from your intranet")
    print(f"  3. Or use --no-scraping flag to test with example URLs")

    return output_file


if __name__ == "__main__":
    create_test_excel()
