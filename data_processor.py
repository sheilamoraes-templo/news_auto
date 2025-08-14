"""
Processador de dados para o sistema de coleta de notícias
Inclui filtragem, remoção de duplicatas e geração de relatórios
"""

import pandas as pd
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Set
import logging
from collections import defaultdict
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from config import OUTPUT_CONFIG, OUTPUT_DIR, COLLECTION_CONFIG, EMAIL_CONFIG
from news_collector import NewsArticle

logger = logging.getLogger(__name__)


class DataProcessor:
    """Processa e organiza os dados coletados"""
    
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.ensure_output_directory()
    
    def ensure_output_directory(self):
        """Garante que o diretório de saída existe"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def save_to_csv(self, articles: List[NewsArticle], filename: str = None) -> str:
        """Salva notícias em arquivo CSV"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"noticias_tecnologia_{timestamp}.csv"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Converte artigos para lista de dicionários
        articles_data = [article.to_dict() for article in articles]
        
        # Cria DataFrame
        df = pd.DataFrame(articles_data)
        
        # Salva CSV
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        logger.info(f"Notícias salvas em CSV: {filepath}")
        
        return filepath
    
    def save_to_json(self, articles: List[NewsArticle], filename: str = None) -> str:
        """Salva notícias em arquivo JSON"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"noticias_tecnologia_{timestamp}.json"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Converte artigos para lista de dicionários
        articles_data = [article.to_dict() for article in articles]
        
        # Salva JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(articles_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Notícias salvas em JSON: {filepath}")
        return filepath
    
    def save_to_html(self, articles: List[NewsArticle], filename: str = None) -> str:
        """Salva notícias em arquivo HTML formatado"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"noticias_tecnologia_{timestamp}.html"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Gera HTML
        html_content = self._generate_html_report(articles)
        
        # Salva arquivo
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Notícias salvas em HTML: {filepath}")
        return filepath
    
    def send_email_report(self, articles: List[NewsArticle], subject: str = None) -> bool:
        """Envia relatório por email"""
        try:
            if not subject:
                subject = OUTPUT_CONFIG['email_subject_prefix']
            
            # Gera HTML para email
            html_content = self._generate_html_report(articles)
            
            # Configura mensagem
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{EMAIL_CONFIG['from_name']} <{EMAIL_CONFIG['smtp_username']}>"
            msg['To'] = ', '.join(OUTPUT_CONFIG['email_recipients'])
            
            # Adiciona conteúdo HTML
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Conecta ao servidor SMTP
            server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
            server.starttls()
            
            # Faz login
            server.login(EMAIL_CONFIG['smtp_username'], EMAIL_CONFIG['smtp_password'])
            
            # Envia email
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email enviado com sucesso para: {OUTPUT_CONFIG['email_recipients']}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar email: {str(e)}")
            return False
    
    def _generate_html_report(self, articles: List[NewsArticle]) -> str:
        """Gera relatório HTML formatado"""
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        html = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Relatório de Notícias de Tecnologia</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ text-align: center; border-bottom: 3px solid #007bff; padding-bottom: 20px; margin-bottom: 30px; }}
                .header h1 {{ color: #007bff; margin: 0; }}
                .header .timestamp {{ color: #666; font-size: 14px; }}
                .stats {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
                .stats h3 {{ margin-top: 0; color: #495057; }}
                .article {{ border-left: 4px solid #007bff; padding: 15px; margin: 15px 0; background: #f8f9fa; border-radius: 0 5px 5px 0; }}
                .article h3 {{ margin: 0 0 10px 0; color: #212529; }}
                .article .source {{ color: #6c757d; font-size: 12px; margin-bottom: 5px; }}
                .article .url {{ color: #007bff; text-decoration: none; }}
                .article .url:hover {{ text-decoration: underline; }}
                .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #dee2e6; color: #6c757d; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📰 Resumo Diário de Tecnologia</h1>
                    <div class="timestamp">Gerado em: {timestamp}</div>
                </div>
                
                <div class="stats">
                    <h3>📊 Estatísticas da Coleta</h3>
                    <p><strong>Total de notícias:</strong> {len(articles)}</p>
                    <p><strong>Fontes consultadas:</strong> G1, Folha, UOL Tilt</p>
                    <p><strong>Período:</strong> Últimas 24 horas</p>
                </div>
                
                <h2>🔍 Notícias Coletadas</h2>
        """
        
        # Adiciona cada artigo
        for i, article in enumerate(articles, 1):
            summary_text = article.summary[:200] + '...' if article.summary and len(article.summary) > 200 else (article.summary or 'Resumo não disponível')
            html += f"""
                <div class="article">
                    <div class="source">📰 Fonte: {article.source}</div>
                    <h3>{i}. {article.title}</h3>
                    <p>{summary_text}</p>
                    <a href="{article.url}" class="url" target="_blank">🔗 Ler notícia completa</a>
                </div>
            """
        
        html += """
                <div class="footer">
                    <p>📧 Sistema de Coleta Automatizada de Notícias</p>
                    <p>🤖 Coletado automaticamente via Python</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def load_existing_data(self, filepath: str) -> List[Dict]:
        """Carrega dados existentes de um arquivo"""
        try:
            if filepath.endswith('.csv'):
                df = pd.read_csv(filepath, encoding='utf-8-sig')
                return df.to_dict('records')
            elif filepath.endswith('.json'):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                logger.error(f"Formato de arquivo não suportado: {filepath}")
                return []
        except Exception as e:
            logger.error(f"Erro ao carregar arquivo {filepath}: {e}")
            return []
    
    def merge_with_existing(self, new_articles: List[NewsArticle], existing_filepath: str) -> List[NewsArticle]:
        """Combina novas notícias com dados existentes"""
        existing_data = self.load_existing_data(existing_filepath)
        
        if not existing_data:
            return new_articles
        
        # Converte dados existentes para objetos NewsArticle
        existing_articles = []
        for data in existing_data:
            try:
                article = NewsArticle(
                    title=data['title'],
                    url=data['url'],
                    source=data['source'],
                    published_date=data.get('published_date'),
                    summary=data.get('summary'),
                    content=data.get('content')
                )
                article.collected_at = datetime.fromisoformat(data['collected_at'])
                article.hash_id = data['hash_id']
                existing_articles.append(article)
            except Exception as e:
                logger.warning(f"Erro ao converter artigo existente: {e}")
                continue
        
        # Combina listas
        all_articles = existing_articles + new_articles
        
        # Remove duplicatas
        seen_hashes = set()
        unique_articles = []
        
        for article in all_articles:
            if article.hash_id not in seen_hashes:
                seen_hashes.add(article.hash_id)
                unique_articles.append(article)
        
        logger.info(f"Combinadas {len(existing_articles)} notícias existentes com {len(new_articles)} novas")
        logger.info(f"Total após remoção de duplicatas: {len(unique_articles)}")
        
        return unique_articles
    
    def generate_daily_summary(self, articles: List[NewsArticle]) -> Dict:
        """Gera resumo diário das notícias"""
        if not articles:
            return {}
        
        # Estatísticas por fonte
        source_stats = defaultdict(int)
        for article in articles:
            source_stats[article.source] += 1
        
        # Palavras-chave mais frequentes
        keyword_freq = defaultdict(int)
        for article in articles:
            title_words = re.findall(r'\b\w+\b', article.title.lower())
            for word in title_words:
                if len(word) > 3:  # Ignora palavras muito curtas
                    keyword_freq[word] += 1
        
        # Top 10 palavras-chave
        top_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Notícias mais recentes
        recent_articles = sorted(articles, key=lambda x: x.collected_at or datetime.now(), reverse=True)[:5]
        
        summary = {
            'total_articles': len(articles),
            'sources': dict(source_stats),
            'top_keywords': top_keywords,
            'recent_articles': [article.to_dict() for article in recent_articles],
            'generated_at': datetime.now().isoformat(),
            'date': datetime.now().strftime('%d/%m/%Y')
        }
        
        return summary
    
    def save_daily_summary(self, summary: Dict, filename: str = None) -> str:
        """Salva resumo diário em arquivo"""
        if not filename:
            date_str = datetime.now().strftime("%Y%m%d")
            filename = f"resumo_diario_{date_str}.json"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Resumo diário salvo: {filepath}")
        return filepath


if __name__ == "__main__":
    # Teste do processador
    processor = DataProcessor()
    print("Processador de dados inicializado com sucesso!")
    print(f"Diretório de saída: {processor.output_dir}")
