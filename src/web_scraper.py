"""
Web Scraper Modul
Lädt Artikel-Inhalte von URLs
"""

import requests
from bs4 import BeautifulSoup
import time
import logging
from typing import Dict, Optional, List
from urllib.parse import urlparse
import sys
sys.path.append('..')
from config.settings import (
    PROXY_CONFIG, REQUEST_TIMEOUT, MAX_RETRIES, 
    USER_AGENT, DELAY_BETWEEN_REQUESTS
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebScraper:
    """Scrapt Artikel-Inhalte von Intranet-URLs"""
    
    def __init__(self, proxy_config: Optional[Dict] = None):
        """
        Initialisiert den WebScraper
        
        Args:
            proxy_config: Dictionary mit Proxy-Konfiguration
        """
        self.proxy_config = proxy_config or PROXY_CONFIG
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
        
        if self.proxy_config and any(self.proxy_config.values()):
            self.session.proxies.update(self.proxy_config)
            logger.info("Proxy konfiguriert")
    
    def scrape_url(self, url: str) -> Dict[str, str]:
        """
        Scrapt eine einzelne URL
        
        Args:
            url: URL des Artikels
            
        Returns:
            Dictionary mit 'title', 'content', 'url', 'success'
        """
        result = {
            'url': url,
            'title': '',
            'content': '',
            'meta_description': '',
            'success': False,
            'error': None
        }
        
        for attempt in range(MAX_RETRIES):
            try:
                logger.info(f"Scraping {url} (Versuch {attempt + 1}/{MAX_RETRIES})")
                
                response = self.session.get(
                    url, 
                    timeout=REQUEST_TIMEOUT,
                    verify=True  # SSL-Verifizierung, kann bei Bedarf deaktiviert werden
                )
                response.raise_for_status()
                
                # Parse HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extrahiere Titel
                title_tag = soup.find('title')
                if title_tag:
                    result['title'] = title_tag.get_text().strip()
                
                # Alternative: h1 als Titel
                if not result['title']:
                    h1_tag = soup.find('h1')
                    if h1_tag:
                        result['title'] = h1_tag.get_text().strip()
                
                # Extrahiere Meta-Description
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                if meta_desc and meta_desc.get('content'):
                    result['meta_description'] = meta_desc.get('content').strip()
                
                # Extrahiere Hauptinhalt
                # Versuche verschiedene gängige Content-Container
                content_candidates = [
                    soup.find('article'),
                    soup.find('main'),
                    soup.find('div', class_='content'),
                    soup.find('div', class_='article-content'),
                    soup.find('div', id='content'),
                    soup.find('div', class_='post-content'),
                ]
                
                content_element = None
                for candidate in content_candidates:
                    if candidate:
                        content_element = candidate
                        break
                
                if content_element:
                    # Entferne Scripts und Styles
                    for script in content_element(['script', 'style']):
                        script.decompose()
                    
                    # Extrahiere Text
                    result['content'] = content_element.get_text(separator=' ', strip=True)
                else:
                    # Fallback: gesamter body Text
                    body = soup.find('body')
                    if body:
                        for script in body(['script', 'style', 'nav', 'footer', 'header']):
                            script.decompose()
                        result['content'] = body.get_text(separator=' ', strip=True)
                
                result['success'] = True
                logger.info(f"Erfolgreich gescrapt: {url}")
                break
                
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout bei {url}")
                result['error'] = "Timeout"
                
            except requests.exceptions.ConnectionError:
                logger.warning(f"Verbindungsfehler bei {url}")
                result['error'] = "Connection Error"
                
            except requests.exceptions.HTTPError as e:
                logger.warning(f"HTTP Fehler bei {url}: {e}")
                result['error'] = f"HTTP {e.response.status_code}"
                
            except Exception as e:
                logger.error(f"Unerwarteter Fehler bei {url}: {e}")
                result['error'] = str(e)
            
            # Warte vor erneutem Versuch
            if attempt < MAX_RETRIES - 1:
                time.sleep(DELAY_BETWEEN_REQUESTS * (attempt + 1))
        
        return result
    
    def scrape_multiple_urls(self, urls: List[str]) -> Dict[str, Dict]:
        """
        Scrapt mehrere URLs
        
        Args:
            urls: Liste von URLs
            
        Returns:
            Dictionary mit URL als Key und Scraping-Ergebnis als Value
        """
        results = {}
        total = len(urls)
        
        for idx, url in enumerate(urls, 1):
            logger.info(f"Fortschritt: {idx}/{total}")
            results[url] = self.scrape_url(url)
            
            # Verzögerung zwischen Requests
            if idx < total:
                time.sleep(DELAY_BETWEEN_REQUESTS)
        
        # Statistik
        successful = sum(1 for r in results.values() if r['success'])
        logger.info(f"Scraping abgeschlossen: {successful}/{total} erfolgreich")
        
        return results
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """
        Extrahiert wichtige Keywords aus Text (einfache Implementierung)
        
        Args:
            text: Input-Text
            top_n: Anzahl der Top-Keywords
            
        Returns:
            Liste von Keywords
        """
        # Einfache Keyword-Extraktion basierend auf Worthäufigkeit
        # Entferne Stoppwörter (vereinfachte deutsche Liste)
        stopwords = {
            'der', 'die', 'das', 'und', 'ist', 'in', 'zu', 'den', 'von',
            'mit', 'auf', 'für', 'eine', 'ein', 'als', 'sich', 'nicht',
            'im', 'werden', 'an', 'oder', 'auch', 'werden', 'dem', 'des',
            'bei', 'um', 'zum', 'zur', 'durch', 'aus', 'sind', 'am', 'kann'
        }
        
        words = text.lower().split()
        words = [w.strip('.,;:!?()[]{}') for w in words]
        words = [w for w in words if len(w) > 3 and w not in stopwords]
        
        # Zähle Häufigkeit
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sortiere nach Häufigkeit
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        return [word for word, freq in sorted_words[:top_n]]


if __name__ == "__main__":
    # Test
    scraper = WebScraper()
    print("WebScraper Modul bereit")
