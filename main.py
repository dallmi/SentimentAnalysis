"""
Hauptprogramm für Sentiment-Analyse von Intranet-Artikeln

Verwendung:
    python main.py --input data/input/ihre_datei.xlsx [--use-vader] [--no-scraping]
"""

import argparse
import logging
import sys
from pathlib import Path

# Importiere Module
from src.data_loader import DataLoader
from src.web_scraper import WebScraper
from src.sentiment_analyzer import SentimentAnalyzer
from src.article_categorizer import ArticleCategorizer
from src.report_generator import ReportGenerator
from config.settings import INPUT_DIR, OUTPUT_DIR

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sentiment_analysis.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse Kommandozeilen-Argumente"""
    parser = argparse.ArgumentParser(
        description='Sentiment-Analyse für Intranet-Artikel und Kommentare'
    )
    
    parser.add_argument(
        '--input',
        type=str,
        help='Pfad zur Input Excel-Datei',
        default=None
    )
    
    parser.add_argument(
        '--url-column',
        type=str,
        default='A',
        help='Spalte mit URLs (Standard: A)'
    )
    
    parser.add_argument(
        '--comment-column',
        type=str,
        default='B',
        help='Spalte mit Kommentaren (Standard: B)'
    )
    
    parser.add_argument(
        '--use-vader',
        action='store_true',
        help='Verwende VADER Sentiment Analyzer (benötigt NLTK)'
    )
    
    parser.add_argument(
        '--no-scraping',
        action='store_true',
        help='Überspringe Web Scraping (nur Sentiment-Analyse der Kommentare)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default=OUTPUT_DIR,
        help=f'Ausgabe-Verzeichnis (Standard: {OUTPUT_DIR})'
    )
    
    return parser.parse_args()


def find_input_file():
    """Sucht nach Input-Datei im Input-Verzeichnis"""
    input_path = Path(INPUT_DIR)
    
    if not input_path.exists():
        return None
    
    # Suche nach Excel-Dateien
    excel_files = list(input_path.glob('*.xlsx')) + list(input_path.glob('*.xls'))
    
    if not excel_files:
        return None
    
    # Nimm die neueste Datei
    newest_file = max(excel_files, key=lambda p: p.stat().st_mtime)
    return str(newest_file)


def main():
    """Hauptfunktion"""
    logger.info("=" * 80)
    logger.info("Sentiment Analysis für Corporate Intranet - START")
    logger.info("=" * 80)
    
    # Parse Argumente
    args = parse_arguments()
    
    # 1. INPUT LADEN
    logger.info("\n--- SCHRITT 1: Input-Daten laden ---")
    
    input_file = args.input
    if not input_file:
        input_file = find_input_file()
        if not input_file:
            logger.error(f"Keine Excel-Datei in {INPUT_DIR} gefunden!")
            logger.info(f"Bitte legen Sie eine Excel-Datei in {INPUT_DIR} ab oder verwenden Sie --input")
            sys.exit(1)
    
    logger.info(f"Verwende Input-Datei: {input_file}")
    
    try:
        data_loader = DataLoader(input_file)
        df = data_loader.load_excel(
            url_column=args.url_column,
            comment_column=args.comment_column
        )
        
        # Validiere Daten
        is_valid, errors = data_loader.validate_data()
        if not is_valid:
            logger.error(f"Daten-Validierung fehlgeschlagen: {errors}")
            sys.exit(1)
        
        # Gruppiere nach URL
        grouped_data = data_loader.group_by_url()
        
        # Statistiken
        stats = data_loader.get_statistics()
        logger.info(f"Statistiken: {stats}")
        
    except Exception as e:
        logger.error(f"Fehler beim Laden der Daten: {e}")
        sys.exit(1)
    
    # 2. WEB SCRAPING (optional)
    logger.info("\n--- SCHRITT 2: Artikel-Inhalte laden ---")
    
    scraped_data = {}
    if not args.no_scraping:
        try:
            scraper = WebScraper()
            urls = list(grouped_data.keys())
            logger.info(f"Scrape {len(urls)} URLs...")
            scraped_data = scraper.scrape_multiple_urls(urls)
        except Exception as e:
            logger.error(f"Fehler beim Scraping: {e}")
            logger.warning("Fahre ohne Scraping-Daten fort...")
    else:
        logger.info("Web Scraping übersprungen (--no-scraping)")
    
    # 3. SENTIMENT-ANALYSE
    logger.info("\n--- SCHRITT 3: Sentiment-Analyse ---")
    
    try:
        sentiment_analyzer = SentimentAnalyzer(use_vader=args.use_vader)
        
        sentiment_results = {}
        for url, comments in grouped_data.items():
            logger.info(f"Analysiere Kommentare für: {url[:60]}...")
            sentiment_results[url] = sentiment_analyzer.analyze_comments_for_article(comments)
        
        # Gesamt-Zusammenfassung
        overall_stats = sentiment_analyzer.get_sentiment_summary(sentiment_results)
        logger.info(f"Gesamt-Sentiment-Statistik: {overall_stats}")
        
    except Exception as e:
        logger.error(f"Fehler bei Sentiment-Analyse: {e}")
        sys.exit(1)
    
    # 4. KATEGORISIERUNG
    logger.info("\n--- SCHRITT 4: Artikel-Kategorisierung ---")
    
    try:
        categorizer = ArticleCategorizer()
        
        categorized_articles = []
        for url, sentiment_data in sentiment_results.items():
            # Hole Scraping-Daten falls verfügbar
            article_data = scraped_data.get(url, {})
            title = article_data.get('title', 'N/A')
            content = article_data.get('content', '')
            
            categorization = categorizer.categorize_article(
                url=url,
                title=title,
                content=content,
                sentiment_data=sentiment_data
            )
            categorized_articles.append(categorization)
        
        # Korrelations-Analyse
        correlation_analysis = categorizer.analyze_category_sentiment_correlation(
            categorized_articles
        )
        
        # Generiere Insights
        insights = categorizer.generate_insights(
            categorized_articles,
            correlation_analysis
        )
        
        logger.info(f"\n--- INSIGHTS ---")
        for insight in insights:
            logger.info(f"  • {insight}")
        
    except Exception as e:
        logger.error(f"Fehler bei Kategorisierung: {e}")
        sys.exit(1)
    
    # 5. REPORT-GENERIERUNG
    logger.info("\n--- SCHRITT 5: Report-Generierung ---")
    
    try:
        report_generator = ReportGenerator(output_dir=args.output_dir)
        
        # Detaillierter Report
        detailed_report = report_generator.create_detailed_report(
            categorized_articles=categorized_articles,
            correlation_analysis=correlation_analysis,
            insights=insights
        )
        logger.info(f"Detaillierter Report: {detailed_report}")
        
        # Zusammenfassungs-Report
        summary_report = report_generator.create_summary_report(
            overall_stats=overall_stats,
            correlation_analysis=correlation_analysis
        )
        logger.info(f"Zusammenfassungs-Report: {summary_report}")
        
        # Visualisierungs-Report
        viz_report = report_generator.create_visualization_report(
            categorized_articles=categorized_articles,
            correlation_analysis=correlation_analysis
        )
        if viz_report:
            logger.info(f"Visualisierungs-Report: {viz_report}")
        
        # Speichere Rohdaten
        report_generator.save_raw_data(
            {
                'categorized_articles': categorized_articles,
                'correlation_analysis': correlation_analysis,
                'overall_stats': overall_stats,
                'insights': insights
            },
            'raw_analysis_data'
        )
        
    except Exception as e:
        logger.error(f"Fehler bei Report-Generierung: {e}")
        sys.exit(1)
    
    logger.info("\n" + "=" * 80)
    logger.info("Sentiment Analysis ERFOLGREICH ABGESCHLOSSEN")
    logger.info(f"Reports gespeichert in: {args.output_dir}")
    logger.info("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\nProgramm abgebrochen durch Benutzer")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unerwarteter Fehler: {e}", exc_info=True)
        sys.exit(1)
