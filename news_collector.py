"""
Sistema Automatizado de Coleta de Notícias de Tecnologia
Coleta notícias de múltiplas fontes, remove duplicatas e gera relatórios
"""

import requests
import time
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
from urllib.parse import urljoin, urlparse
import re

from bs4 import BeautifulSoup
from config import NEWS_SOURCES, COLLECTION_CONFIG, LOG_CONFIG

# Configurar logging
logging.basicConfig(
    level=getattr(logging, LOG_CONFIG['log_level']),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_CONFIG['log_file']),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class NewsArticle:
    """Classe para representar uma notícia"""
    
    def __init__(self, title: str, url: str, source: str, published_date: str = None, 
                 summary: str = None, content: str = None):
        self.title = title.strip()
        self.url = url
        self.source = source
        self.published_date = published_date
        self.summary = summary
        self.content = content
        self.collected_at = datetime.now()
        self.hash_id = self._generate_hash()
    
    def _generate_hash(self) -> str:
        """Gera um hash único baseado no título e URL"""
        content = f"{self.title}{self.url}{self.source}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            'title': self.title,
            'url': self.url,
            'source': self.source,
            'published_date': self.published_date,
            'summary': self.summary,
            'content': self.content,
            'collected_at': self.collected_at.isoformat(),
            'hash_id': self.hash_id
        }
    
    def __str__(self):
        return f"{self.title} - {self.source}"


class BaseNewsCollector:
    """Classe base para coletores de notícias"""
    
    def __init__(self, source_config: Dict):
        self.source_config = source_config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def collect_news(self) -> List[NewsArticle]:
        """Método base para coleta de notícias"""
        raise NotImplementedError("Subclasses devem implementar este método")
    
    def _make_request(self, url: str) -> Optional[requests.Response]:
        """Faz requisição HTTP com tratamento de erro"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error(f"Erro ao acessar {url}: {e}")
            return None
    
    def _clean_text(self, text: str) -> str:
        """Limpa texto removendo caracteres especiais e espaços extras"""
        if not text:
            return ""
        # Remove caracteres especiais e normaliza espaços
        text = re.sub(r'\s+', ' ', text.strip())
        text = re.sub(r'[^\w\s\-.,!?]', '', text)
        return text


class G1TecnologiaCollector(BaseNewsCollector):
    """Coletor específico para G1 Tecnologia"""
    
    def collect_news(self) -> List[NewsArticle]:
        """Coleta notícias do G1 Tecnologia"""
        articles = []
        response = self._make_request(self.source_config['url'])
        
        if not response:
            return articles
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Busca por links de notícias
        news_links = soup.find_all('a', href=True)
        
        for link in news_links:
            try:
                href = link.get('href')
                if not href or href.startswith('#'):
                    continue
                
                # Filtra apenas links de notícias
                if self._is_news_link(href):
                    title = link.get_text(strip=True)
                    if len(title) < COLLECTION_CONFIG['min_title_length']:
                        continue
                    
                    # Constrói URL completa
                    full_url = urljoin(self.source_config['url'], href)
                    
                    # Busca por data de publicação
                    published_date = self._extract_published_date(link)
                    
                    # Busca por resumo
                    summary = self._extract_summary(link)
                    
                    article = NewsArticle(
                        title=title,
                        url=full_url,
                        source=self.source_config['name'],
                        published_date=published_date,
                        summary=summary
                    )
                    
                    articles.append(article)
                    
                    if len(articles) >= COLLECTION_CONFIG['max_articles_per_source']:
                        break
                        
            except Exception as e:
                logger.error(f"Erro ao processar link do G1: {e}")
                continue
        
        logger.info(f"Coletadas {len(articles)} notícias do G1 Tecnologia")
        return articles
    
    def _is_news_link(self, href: str) -> bool:
        """Verifica se o link é de uma notícia"""
        # Padrões típicos de URLs de notícias do G1
        patterns = [
            r'/tecnologia/noticia/',
            r'/tecnologia/',
            r'/noticia/'
        ]
        return any(re.search(pattern, href) for pattern in patterns)
    
    def _extract_published_date(self, link_element) -> Optional[str]:
        """Extrai data de publicação do elemento"""
        try:
            # Busca por elementos de data próximos
            parent = link_element.parent
            if parent:
                time_element = parent.find('time')
                if time_element:
                    return time_element.get('datetime') or time_element.get_text(strip=True)
        except:
            pass
        return None
    
    def _extract_summary(self, link_element) -> Optional[str]:
        """Extrai resumo da notícia"""
        try:
            # Busca por resumo próximo ao link
            parent = link_element.parent
            if parent:
                summary_element = parent.find(['p', 'div'], class_=re.compile(r'summary|resumo|desc'))
                if summary_element:
                    return self._clean_text(summary_element.get_text())
        except:
            pass
        return None


class FolhaTecCollector(BaseNewsCollector):
    """Coletor específico para Folha de S.Paulo - Tec"""
    
    def collect_news(self) -> List[NewsArticle]:
        """Coleta notícias da Folha Tec"""
        articles = []
        response = self._make_request(self.source_config['url'])
        
        if not response:
            return articles
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Busca por links de notícias
        news_links = soup.find_all('a', href=True)
        
        for link in news_links:
            try:
                href = link.get('href')
                if not href or href.startswith('#'):
                    continue
                
                # Filtra apenas links de notícias
                if self._is_news_link(href):
                    title = link.get_text(strip=True)
                    if len(title) < COLLECTION_CONFIG['min_title_length']:
                        continue
                    
                    # Constrói URL completa
                    full_url = urljoin(self.source_config['url'], href)
                    
                    # Busca por data de publicação
                    published_date = self._extract_published_date(link)
                    
                    # Busca por resumo
                    summary = self._extract_summary(link)
                    
                    article = NewsArticle(
                        title=title,
                        url=full_url,
                        source=self.source_config['name'],
                        published_date=published_date,
                        summary=summary
                    )
                    
                    articles.append(article)
                    
                    if len(articles) >= COLLECTION_CONFIG['max_articles_per_source']:
                        break
                        
            except Exception as e:
                logger.error(f"Erro ao processar link da Folha: {e}")
                continue
        
        logger.info(f"Coletadas {len(articles)} notícias da Folha Tec")
        return articles
    
    def _is_news_link(self, href: str) -> bool:
        """Verifica se o link é de uma notícia"""
        # Padrões típicos de URLs de notícias da Folha
        patterns = [
            r'/tec/',
            r'/noticias/',
            r'/colunas/'
        ]
        return any(re.search(pattern, href) for pattern in patterns)
    
    def _extract_published_date(self, link_element) -> Optional[str]:
        """Extrai data de publicação do elemento"""
        try:
            # Busca por elementos de data próximos
            parent = link_element.parent
            if parent:
                time_element = parent.find('time')
                if time_element:
                    return time_element.get('datetime') or time_element.get_text(strip=True)
        except:
            pass
        return None
    
    def _extract_summary(self, link_element) -> Optional[str]:
        """Extrai resumo da notícia"""
        try:
            # Busca por resumo próximo ao link
            parent = link_element.parent
            if parent:
                summary_element = parent.find(['p', 'div'], class_=re.compile(r'summary|resumo|desc'))
                if summary_element:
                    return self._clean_text(summary_element.get_text())
        except:
            pass
        return None


class UOLTiltCollector(BaseNewsCollector):
    """Coletor específico para UOL Tilt"""
    
    def collect_news(self) -> List[NewsArticle]:
        """Coleta notícias do UOL Tilt"""
        articles = []
        response = self._make_request(self.source_config['url'])
        
        if not response:
            return articles
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Busca por links de notícias
        news_links = soup.find_all('a', href=True)
        
        for link in news_links:
            try:
                href = link.get('href')
                if not href or href.startswith('#'):
                    continue
                
                # Filtra apenas links de notícias
                if self._is_news_link(href):
                    title = link.get_text(strip=True)
                    if len(title) < COLLECTION_CONFIG['min_title_length']:
                        continue
                    
                    # Constrói URL completa
                    full_url = urljoin(self.source_config['url'], href)
                    
                    # Busca por data de publicação
                    published_date = self._extract_published_date(link)
                    
                    # Busca por resumo
                    summary = self._extract_summary(link)
                    
                    article = NewsArticle(
                        title=title,
                        url=full_url,
                        source=self.source_config['name'],
                        published_date=published_date,
                        summary=summary
                    )
                    
                    articles.append(article)
                    
                    if len(articles) >= COLLECTION_CONFIG['max_articles_per_source']:
                        break
                        
            except Exception as e:
                logger.error(f"Erro ao processar link do UOL Tilt: {e}")
                continue
        
        logger.info(f"Coletadas {len(articles)} notícias do UOL Tilt")
        return articles
    
    def _is_news_link(self, href: str) -> bool:
        """Verifica se o link é de uma notícia"""
        # Padrões típicos de URLs de notícias do UOL Tilt
        patterns = [
            r'/tilt/',
            r'/noticias/',
            r'/colunas/'
        ]
        return any(re.search(pattern, href) for pattern in patterns)
    
    def _extract_published_date(self, link_element) -> Optional[str]:
        """Extrai data de publicação do elemento"""
        try:
            # Busca por elementos de data próximos
            parent = link_element.parent
            if parent:
                time_element = parent.find('time')
                if time_element:
                    return time_element.get('datetime') or time_element.get_text(strip=True)
        except:
            pass
        return None
    
    def _extract_summary(self, link_element) -> Optional[str]:
        """Extrai resumo da notícia"""
        try:
            # Busca por resumo próximo ao link
            parent = link_element.parent
            if parent:
                summary_element = parent.find(['p', 'div'], class_=re.compile(r'summary|resumo|desc'))
                if summary_element:
                    return self._clean_text(summary_element.get_text())
        except:
            pass
        return None


class NewsCollectionManager:
    """Gerenciador principal da coleta de notícias"""
    
    def __init__(self):
        self.collectors = {
            'g1_tecnologia': G1TecnologiaCollector(NEWS_SOURCES['g1_tecnologia']),
            'folha_tec': FolhaTecCollector(NEWS_SOURCES['folha_tec']),
            'uol_tilt': UOLTiltCollector(NEWS_SOURCES['uol_tilt'])
        }
        self.collected_articles = []
    
    def collect_all_news(self) -> List[NewsArticle]:
        """Coleta notícias de todas as fontes"""
        all_articles = []
        
        for source_name, collector in self.collectors.items():
            try:
                logger.info(f"Iniciando coleta de {source_name}")
                articles = collector.collect_news()
                all_articles.extend(articles)
                
                # Pausa entre coletas para não sobrecarregar os servidores
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Erro na coleta de {source_name}: {e}")
                continue
        
        # Remove duplicatas se configurado
        if COLLECTION_CONFIG['remove_duplicates']:
            all_articles = self._remove_duplicates(all_articles)
        
        # Filtra por palavras-chave
        all_articles = self._filter_by_keywords(all_articles)
        
        self.collected_articles = all_articles
        logger.info(f"Coleta concluída. Total de {len(all_articles)} notícias únicas")
        
        return all_articles
    
    def _remove_duplicates(self, articles: List[NewsArticle]) -> List[NewsArticle]:
        """Remove notícias duplicadas baseado no hash"""
        seen_hashes = set()
        unique_articles = []
        
        for article in articles:
            if article.hash_id not in seen_hashes:
                seen_hashes.add(article.hash_id)
                unique_articles.append(article)
        
        logger.info(f"Removidas {len(articles) - len(unique_articles)} duplicatas")
        return unique_articles
    
    def _filter_by_keywords(self, articles: List[NewsArticle]) -> List[NewsArticle]:
        """Filtra notícias por palavras-chave relevantes"""
        keywords = COLLECTION_CONFIG['keywords_filter']
        filtered_articles = []
        
        for article in articles:
            title_lower = article.title.lower()
            summary_lower = (article.summary or "").lower()
            
            # Verifica se alguma palavra-chave está presente
            if any(keyword.lower() in title_lower or keyword.lower() in summary_lower 
                   for keyword in keywords):
                filtered_articles.append(article)
        
        logger.info(f"Filtradas {len(articles) - len(filtered_articles)} notícias por palavras-chave")
        return filtered_articles


if __name__ == "__main__":
    # Teste da coleta
    manager = NewsCollectionManager()
    articles = manager.collect_all_news()
    
    print(f"\nColetadas {len(articles)} notícias:")
    for article in articles[:5]:  # Mostra apenas as primeiras 5
        print(f"- {article}")
