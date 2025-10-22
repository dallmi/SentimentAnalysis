"""
Data Loader Modul
Lädt Excel-Dateien mit URLs und Kommentaren
"""

import pandas as pd
from typing import Dict, List, Tuple
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """Lädt und validiert Input-Daten aus Excel"""
    
    def __init__(self, file_path: str):
        """
        Initialisiert den DataLoader
        
        Args:
            file_path: Pfad zur Excel-Datei
        """
        self.file_path = Path(file_path)
        self.df = None
        self.grouped_data = {}
        
    def load_excel(self, url_column: str = 'A', comment_column: str = 'B') -> pd.DataFrame:
        """
        Lädt Excel-Datei
        
        Args:
            url_column: Name oder Index der URL-Spalte
            comment_column: Name oder Index der Kommentar-Spalte
            
        Returns:
            DataFrame mit geladenen Daten
        """
        logger.info(f"Lade Excel-Datei: {self.file_path}")
        
        try:
            # Versuche mit verschiedenen Engines
            try:
                self.df = pd.read_excel(self.file_path, engine='openpyxl')
            except:
                self.df = pd.read_excel(self.file_path)
            
            logger.info(f"Erfolgreich geladen: {len(self.df)} Zeilen")
            
            # Wenn Spalten als Buchstaben angegeben (A, B), konvertiere zu Index
            if url_column == 'A':
                url_col_idx = 0
            else:
                url_col_idx = url_column
                
            if comment_column == 'B':
                comment_col_idx = 1
            else:
                comment_col_idx = comment_column
            
            # Verwende Index-basierte Auswahl
            if isinstance(url_col_idx, int) and isinstance(comment_col_idx, int):
                columns = self.df.columns.tolist()
                url_col_name = columns[url_col_idx]
                comment_col_name = columns[comment_col_idx]
            else:
                url_col_name = url_col_idx
                comment_col_name = comment_col_idx
            
            # Erstelle standardisierte Spalten
            self.df['url'] = self.df[url_col_name]
            self.df['comment'] = self.df[comment_col_name]
            
            return self.df
            
        except Exception as e:
            logger.error(f"Fehler beim Laden der Excel-Datei: {e}")
            raise
    
    def validate_data(self) -> Tuple[bool, List[str]]:
        """
        Validiert die geladenen Daten
        
        Returns:
            Tuple (is_valid, error_messages)
        """
        errors = []
        
        if self.df is None:
            errors.append("Keine Daten geladen")
            return False, errors
        
        # Prüfe auf leere URLs
        null_urls = self.df['url'].isnull().sum()
        if null_urls > 0:
            errors.append(f"{null_urls} Zeilen mit fehlenden URLs")
        
        # Prüfe auf leere Kommentare
        null_comments = self.df['comment'].isnull().sum()
        if null_comments > 0:
            logger.warning(f"{null_comments} Zeilen mit fehlenden Kommentaren")
        
        # Prüfe auf duplizierte Zeilen
        duplicates = self.df.duplicated().sum()
        if duplicates > 0:
            logger.warning(f"{duplicates} duplizierte Zeilen gefunden")
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def group_by_url(self) -> Dict[str, List[str]]:
        """
        Gruppiert Kommentare nach URL
        
        Returns:
            Dictionary mit URL als Key und Liste von Kommentaren als Value
        """
        logger.info("Gruppiere Kommentare nach URL...")
        
        # Entferne Zeilen mit null URLs
        df_clean = self.df[self.df['url'].notna()].copy()
        
        # Gruppiere nach URL
        grouped = df_clean.groupby('url')['comment'].apply(list).to_dict()
        
        # Entferne null/NaN Kommentare
        for url, comments in grouped.items():
            grouped[url] = [c for c in comments if pd.notna(c)]
        
        self.grouped_data = grouped
        logger.info(f"{len(grouped)} eindeutige URLs gefunden")
        
        return grouped
    
    def get_statistics(self) -> Dict:
        """
        Gibt Statistiken über die Daten zurück
        
        Returns:
            Dictionary mit Statistiken
        """
        if self.df is None:
            return {}
        
        stats = {
            'total_rows': len(self.df),
            'unique_urls': self.df['url'].nunique(),
            'total_comments': self.df['comment'].notna().sum(),
            'avg_comments_per_url': 0,
            'urls_without_comments': 0
        }
        
        if self.grouped_data:
            comment_counts = [len(comments) for comments in self.grouped_data.values()]
            stats['avg_comments_per_url'] = sum(comment_counts) / len(comment_counts) if comment_counts else 0
            stats['urls_without_comments'] = sum(1 for c in comment_counts if c == 0)
            stats['min_comments_per_url'] = min(comment_counts) if comment_counts else 0
            stats['max_comments_per_url'] = max(comment_counts) if comment_counts else 0
        
        return stats
    
    def export_cleaned_data(self, output_path: str):
        """
        Exportiert bereinigte Daten
        
        Args:
            output_path: Pfad für Export-Datei
        """
        if self.df is not None:
            self.df[['url', 'comment']].to_excel(output_path, index=False)
            logger.info(f"Bereinigte Daten exportiert nach: {output_path}")


if __name__ == "__main__":
    # Test
    print("DataLoader Modul bereit")
