"""
Agendador para execução automática da coleta de notícias
Executa em intervalos configurados e gera relatórios diários
"""

import schedule
import time
import threading
from datetime import datetime, timedelta
import logging
import os
from typing import Optional

from config import COLLECTION_CONFIG, OUTPUT_CONFIG, LOG_CONFIG
from news_collector import NewsCollectionManager
from data_processor import DataProcessor

logger = logging.getLogger(__name__)


class NewsScheduler:
    """Agendador para execução automática da coleta de notícias"""
    
    def __init__(self):
        self.collection_manager = NewsCollectionManager()
        self.data_processor = DataProcessor()
        self.is_running = False
        self.last_collection = None
        self.collection_count = 0
        
        # Configurações
        self.collection_interval = COLLECTION_CONFIG['collection_interval_hours']
        self.daily_summary_time = COLLECTION_CONFIG['daily_summary_time']
        
        logger.info("Agendador de notícias inicializado")
    
    def start_scheduler(self):
        """Inicia o agendador"""
        if self.is_running:
            logger.warning("Agendador já está em execução")
            return
        
        self.is_running = True
        logger.info("Iniciando agendador de notícias")
        
        # Agenda coleta periódica
        schedule.every(self.collection_interval).hours.do(self.run_collection)
        
        # Agenda resumo diário
        schedule.every().day.at(self.daily_summary_time).do(self.run_daily_summary)
        
        # Executa coleta inicial
        self.run_collection()
        
        # Loop principal do agendador
        try:
            while self.is_running:
                schedule.run_pending()
                time.sleep(60)  # Verifica a cada minuto
        except KeyboardInterrupt:
            logger.info("Agendador interrompido pelo usuário")
            self.stop_scheduler()
        except Exception as e:
            logger.error(f"Erro no agendador: {e}")
            self.stop_scheduler()
    
    def stop_scheduler(self):
        """Para o agendador"""
        self.is_running = False
        logger.info("Agendador parado")
    
    def run_collection(self):
        """Executa uma coleta de notícias"""
        try:
            logger.info("Iniciando coleta agendada de notícias")
            start_time = datetime.now()
            
            # Coleta notícias
            articles = self.collection_manager.collect_all_news()
            
            if not articles:
                logger.warning("Nenhuma notícia foi coletada")
                return
            
            # Processa e salva dados
            self._save_collection_results(articles)
            
            # Atualiza estatísticas
            self.last_collection = start_time
            self.collection_count += 1
            
            end_time = datetime.now()
            duration = end_time - start_time
            
            logger.info(f"Coleta concluída em {duration.total_seconds():.2f} segundos")
            logger.info(f"Total de notícias coletadas: {len(articles)}")
            
        except Exception as e:
            logger.error(f"Erro durante a coleta: {e}")
    
    def run_daily_summary(self):
        """Executa resumo diário"""
        try:
            logger.info("Gerando resumo diário")
            
            # Busca arquivo mais recente de coleta
            latest_file = self._find_latest_collection_file()
            
            if not latest_file:
                logger.warning("Nenhum arquivo de coleta encontrado para resumo diário")
                return
            
            # Carrega dados existentes
            existing_data = self.data_processor.load_existing_data(latest_file)
            
            if not existing_data:
                logger.warning("Dados existentes não puderam ser carregados")
                return
            
            # Converte para objetos NewsArticle
            articles = []
            for data in existing_data:
                try:
                    from news_collector import NewsArticle
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
                    articles.append(article)
                except Exception as e:
                    logger.warning(f"Erro ao converter artigo: {e}")
                    continue
            
            # Gera resumo diário
            summary = self.data_processor.generate_daily_summary(articles)
            
            # Salva resumo
            summary_file = self.data_processor.save_daily_summary(summary)
            
            # Gera relatório HTML
            html_file = self.data_processor.save_to_html(articles)
            
            logger.info(f"Resumo diário gerado: {summary_file}")
            logger.info(f"Relatório HTML gerado: {html_file}")
            
        except Exception as e:
            logger.error(f"Erro ao gerar resumo diário: {e}")
    
    def _save_collection_results(self, articles):
        """Salva resultados da coleta"""
        try:
            # Salva em múltiplos formatos
            csv_file = self.data_processor.save_to_csv(articles)
            json_file = self.data_processor.save_to_json(articles)
            html_file = self.data_processor.save_to_html(articles)
            
            logger.info(f"Resultados salvos em:")
            logger.info(f"  CSV: {csv_file}")
            logger.info(f"  JSON: {json_file}")
            logger.info(f"  HTML: {html_file}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar resultados: {e}")
    
    def _find_latest_collection_file(self) -> Optional[str]:
        """Encontra o arquivo de coleta mais recente"""
        try:
            output_dir = OUTPUT_CONFIG['output_directory']
            if not os.path.exists(output_dir):
                return None
            
            # Lista arquivos de coleta
            collection_files = []
            for filename in os.listdir(output_dir):
                if filename.startswith('noticias_tecnologia_') and filename.endswith('.csv'):
                    filepath = os.path.join(output_dir, filename)
                    collection_files.append((filepath, os.path.getmtime(filepath)))
            
            if not collection_files:
                return None
            
            # Retorna o mais recente
            latest_file = max(collection_files, key=lambda x: x[1])[0]
            return latest_file
            
        except Exception as e:
            logger.error(f"Erro ao buscar arquivo mais recente: {e}")
            return None
    
    def get_status(self) -> dict:
        """Retorna status atual do agendador"""
        return {
            'is_running': self.is_running,
            'last_collection': self.last_collection.isoformat() if self.last_collection else None,
            'collection_count': self.collection_count,
            'next_collection': schedule.next_run(),
            'next_daily_summary': schedule.next_run('daily_summary')
        }


class BackgroundScheduler(threading.Thread):
    """Agendador em thread separada para execução em background"""
    
    def __init__(self):
        super().__init__()
        self.scheduler = NewsScheduler()
        self.daemon = True  # Thread será encerrada quando o programa principal terminar
    
    def run(self):
        """Executa o agendador em background"""
        self.scheduler.start_scheduler()
    
    def stop(self):
        """Para o agendador"""
        self.scheduler.stop_scheduler()


def run_single_collection():
    """Executa uma única coleta (útil para testes)"""
    try:
        logger.info("Executando coleta única")
        
        collection_manager = NewsCollectionManager()
        data_processor = DataProcessor()
        
        # Coleta notícias
        articles = collection_manager.collect_all_news()
        
        if not articles:
            logger.warning("Nenhuma notícia foi coletada")
            return
        
        # Salva resultados
        csv_file = data_processor.save_to_csv(articles)
        json_file = data_processor.save_to_json(articles)
        html_file = data_processor.save_to_html(articles)
        
        # Gera resumo
        summary = data_processor.generate_daily_summary(articles)
        summary_file = data_processor.save_daily_summary(summary)
        
        logger.info(f"Coleta única concluída:")
        logger.info(f"  Total de notícias: {len(articles)}")
        logger.info(f"  Arquivos gerados:")
        logger.info(f"    CSV: {csv_file}")
        logger.info(f"    JSON: {json_file}")
        logger.info(f"    HTML: {html_file}")
        logger.info(f"    Resumo: {summary_file}")
        
    except Exception as e:
        logger.error(f"Erro na coleta única: {e}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Sistema de Coleta Automatizada de Notícias')
    parser.add_argument('--mode', choices=['scheduler', 'single'], default='single',
                       help='Modo de execução: scheduler (contínuo) ou single (único)')
    parser.add_argument('--daemon', action='store_true',
                       help='Executa em background como daemon')
    
    args = parser.parse_args()
    
    if args.mode == 'scheduler':
        if args.daemon:
            # Executa em background
            bg_scheduler = BackgroundScheduler()
            bg_scheduler.start()
            
            try:
                # Mantém o programa principal rodando
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Encerrando programa...")
                bg_scheduler.stop()
        else:
            # Executa no foreground
            scheduler = NewsScheduler()
            scheduler.start_scheduler()
    else:
        # Executa coleta única
        run_single_collection()
