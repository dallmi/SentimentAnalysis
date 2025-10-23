"""
Report Generator Modul
Erstellt Excel-Reports und Visualisierungen
"""

import pandas as pd
from datetime import datetime
from pathlib import Path
import logging
from typing import Dict, List
import sys
sys.path.append('..')
from config.settings import OUTPUT_DIR, GENERATE_VISUALIZATIONS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generiert Reports aus Analyse-Ergebnissen"""
    
    def __init__(self, output_dir: str = OUTPUT_DIR):
        """
        Initialisiert den Report Generator
        
        Args:
            output_dir: Ausgabe-Verzeichnis
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def create_detailed_report(
        self, 
        categorized_articles: List[Dict],
        correlation_analysis: Dict,
        insights: List[str]
    ) -> str:
        """
        Erstellt detaillierten Excel-Report
        
        Args:
            categorized_articles: Liste kategorisierter Artikel
            correlation_analysis: Korrelations-Analyse
            insights: Generierte Insights
            
        Returns:
            Pfad zur erstellten Datei
        """
        output_file = self.output_dir / f"detailed_report_{self.timestamp}.xlsx"
        
        logger.info(f"Erstelle detaillierten Report: {output_file}")
        
        # Excel Writer erstellen
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Sheet 1: Artikel-Übersicht
            articles_data = []
            for article in categorized_articles:
                articles_data.append({
                    'URL': article['url'],
                    'Titel': article['title'][:100] if article['title'] else 'N/A',
                    'Kategorie': article['primary_category'],
                    'Keywords': ', '.join(article['keywords'][:5]),
                    'Sentiment-Kategorie': article['sentiment_category'],
                    'Durchschn. Sentiment': article['avg_sentiment_score'],
                    'Anzahl Kommentare': article['total_comments'],
                    'Positive Ratio': article['positive_ratio'],
                    'Negative Ratio': article['negative_ratio'],
                })
            
            df_articles = pd.DataFrame(articles_data)
            df_articles.to_excel(writer, sheet_name='Artikel-Übersicht', index=False)
            
            # Sheet 2: Kategorie-Sentiment-Analyse
            category_stats = correlation_analysis.get('category_sentiment_stats', {})
            category_data = []
            for category, stats in category_stats.items():
                category_data.append({
                    'Kategorie': category,
                    'Durchschn. Sentiment': stats['avg_sentiment'],
                    'Min Sentiment': stats['min_sentiment'],
                    'Max Sentiment': stats['max_sentiment'],
                    'Anzahl Artikel': stats['article_count'],
                    'Positive Artikel': stats['positive_articles'],
                    'Negative Artikel': stats['negative_articles'],
                    'Neutrale Artikel': stats['neutral_articles'],
                })
            
            df_categories = pd.DataFrame(category_data)
            df_categories = df_categories.sort_values('Durchschn. Sentiment', ascending=False)
            df_categories.to_excel(writer, sheet_name='Kategorien-Analyse', index=False)
            
            # Sheet 3: Insights
            insights_data = [{'Insight': insight} for insight in insights]
            df_insights = pd.DataFrame(insights_data)
            df_insights.to_excel(writer, sheet_name='Insights', index=False)
            
            # Sheet 4: Sentiment-Verteilung pro Artikel
            sentiment_dist_data = []
            for article in categorized_articles:
                dist = article.get('sentiment_distribution', {})
                sentiment_dist_data.append({
                    'URL': article['url'][:50],
                    'Titel': article['title'][:50] if article['title'] else 'N/A',
                    'Very Positive': dist.get('very_positive', 0),
                    'Positive': dist.get('positive', 0),
                    'Neutral': dist.get('neutral', 0),
                    'Negative': dist.get('negative', 0),
                    'Very Negative': dist.get('very_negative', 0),
                })
            
            df_sentiment_dist = pd.DataFrame(sentiment_dist_data)
            df_sentiment_dist.to_excel(writer, sheet_name='Sentiment-Verteilung', index=False)
        
        logger.info(f"Detaillierter Report erstellt: {output_file}")
        return str(output_file)
    
    def create_summary_report(
        self, 
        overall_stats: Dict,
        correlation_analysis: Dict
    ) -> str:
        """
        Erstellt Zusammenfassungs-Report
        
        Args:
            overall_stats: Gesamt-Statistiken
            correlation_analysis: Korrelations-Analyse
            
        Returns:
            Pfad zur erstellten Datei
        """
        output_file = self.output_dir / f"summary_report_{self.timestamp}.xlsx"
        
        logger.info(f"Erstelle Zusammenfassungs-Report: {output_file}")
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Gesamt-Statistiken
            stats_data = {
                'Metrik': [
                    'Gesamt Artikel',
                    'Gesamt Kommentare',
                    'Durchschn. Kommentare pro Artikel',
                    'Durchschn. Sentiment-Score',
                ],
                'Wert': [
                    overall_stats.get('total_articles', 0),
                    overall_stats.get('total_comments', 0),
                    overall_stats.get('avg_comments_per_article', 0),
                    overall_stats.get('overall_avg_sentiment', 0),
                ]
            }
            
            df_stats = pd.DataFrame(stats_data)
            df_stats.to_excel(writer, sheet_name='Gesamt-Statistik', index=False)
            
            # Top/Bottom Artikel
            top_positive = overall_stats.get('top_5_positive_articles', [])
            top_negative = overall_stats.get('top_5_negative_articles', [])
            
            top_data = []
            for i, (url, score) in enumerate(top_positive[:5], 1):
                top_data.append({
                    'Rang': i,
                    'Typ': 'Positiv',
                    'URL': url[:80],
                    'Sentiment-Score': score
                })
            
            for i, (url, score) in enumerate(reversed(top_negative[-5:]), 1):
                top_data.append({
                    'Rang': i,
                    'Typ': 'Negativ',
                    'URL': url[:80],
                    'Sentiment-Score': score
                })
            
            df_top = pd.DataFrame(top_data)
            df_top.to_excel(writer, sheet_name='Top-Bottom Artikel', index=False)
            
            # Kategorien-Übersicht
            articles_by_category = overall_stats.get('articles_by_category', {})
            cat_overview_data = []
            for category, count in articles_by_category.items():
                cat_overview_data.append({
                    'Sentiment-Kategorie': category,
                    'Anzahl Artikel': count
                })
            
            df_cat_overview = pd.DataFrame(cat_overview_data)
            df_cat_overview.to_excel(writer, sheet_name='Sentiment-Kategorien', index=False)
        
        logger.info(f"Zusammenfassungs-Report erstellt: {output_file}")
        return str(output_file)
    
    def create_visualization_report(
        self,
        categorized_articles: List[Dict],
        correlation_analysis: Dict
    ) -> str:
        """
        Erstellt HTML-Report mit Visualisierungen
        
        Args:
            categorized_articles: Kategorisierte Artikel
            correlation_analysis: Korrelations-Analyse
            
        Returns:
            Pfad zur HTML-Datei
        """
        if not GENERATE_VISUALIZATIONS:
            logger.info("Visualisierungen deaktiviert")
            return ""
        
        output_file = self.output_dir / f"visualization_report_{self.timestamp}.html"
        
        try:
            import matplotlib
            matplotlib.use('Agg')  # Non-interactive backend
            import matplotlib.pyplot as plt
            
            # HTML-Template
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Sentiment Analysis Report</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    h1 {{ color: #333; }}
                    h2 {{ color: #666; }}
                    .chart {{ margin: 20px 0; }}
                    table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #4CAF50; color: white; }}
                    .insight {{ background-color: #f0f0f0; padding: 10px; margin: 10px 0; border-left: 4px solid #4CAF50; }}
                </style>
            </head>
            <body>
                <h1>Sentiment Analysis Report</h1>
                <p>Generiert am: {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}</p>
                
                <h2>Übersicht</h2>
                <p>Gesamtanzahl Artikel: {len(categorized_articles)}</p>
                
                <h2>Kategorien-Performance</h2>
                <div class="chart">
                    <img src="category_sentiment.png" alt="Kategorien Sentiment" width="800">
                </div>
                
                <h2>Details</h2>
                <p>Detaillierte Berichte siehe Excel-Dateien im Output-Ordner.</p>
            </body>
            </html>
            """
            
            # Schreibe HTML
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Erstelle Visualisierung (optional, wenn matplotlib verfügbar)
            try:
                self._create_category_chart(correlation_analysis)
            except Exception as e:
                logger.warning(f"Visualisierung konnte nicht erstellt werden: {e}")
            
            logger.info(f"Visualisierungs-Report erstellt: {output_file}")
            return str(output_file)
            
        except ImportError:
            logger.warning("Matplotlib nicht verfügbar, überspringe Visualisierungen")
            return ""
    
    def _create_category_chart(self, correlation_analysis: Dict):
        """Erstellt Balkendiagramm für Kategorien"""
        try:
            import matplotlib.pyplot as plt
            
            stats = correlation_analysis.get('category_sentiment_stats', {})
            if not stats:
                return
            
            categories = list(stats.keys())
            sentiments = [data['avg_sentiment'] for data in stats.values()]
            
            plt.figure(figsize=(12, 6))
            colors = ['green' if s > 0 else 'red' for s in sentiments]
            plt.barh(categories, sentiments, color=colors, alpha=0.7)
            plt.xlabel('Durchschnittlicher Sentiment-Score')
            plt.title('Sentiment-Score nach Kategorie')
            plt.axvline(x=0, color='black', linestyle='--', linewidth=0.5)
            plt.tight_layout()
            
            chart_file = self.output_dir / f"category_sentiment_{self.timestamp}.png"
            plt.savefig(chart_file, dpi=150, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Visualisierung erstellt: {chart_file}")
            
        except Exception as e:
            logger.warning(f"Chart konnte nicht erstellt werden: {e}")
    
    def save_raw_data(self, data: Dict, filename: str):
        """
        Speichert Rohdaten als JSON
        
        Args:
            data: Zu speichernde Daten
            filename: Dateiname
        """
        import json
        
        output_file = self.output_dir / f"{filename}_{self.timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Rohdaten gespeichert: {output_file}")


if __name__ == "__main__":
    # Test
    generator = ReportGenerator()
    print("ReportGenerator Modul bereit")
