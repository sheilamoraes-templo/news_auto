#!/usr/bin/env python3
"""
Script para execução agendada do sistema de coleta de notícias
Este script é executado pelo Windows Task Scheduler diariamente às 12:00
"""

import sys
import os
import logging
from datetime import datetime

# Adiciona o diretório atual ao path para importações
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import LOG_CONFIG, OUTPUT_CONFIG
from news_collector import NewsCollectionManager
from data_processor import DataProcessor


def setup_logging():
    """Configura o sistema de logging"""
    # Cria diretório de logs se não existir
    log_dir = os.path.dirname(LOG_CONFIG['log_file'])
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configura logging
    logging.basicConfig(
        level=getattr(logging, LOG_CONFIG['log_level']),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_CONFIG['log_file'], encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def executar_coleta_agendada():
    """Executa uma coleta agendada e envia email"""
    print(f"\n{'='*60}")
    print("🚀 COLETA AGENDADA AUTOMÁTICA DE NOTÍCIAS")
    print(f"📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"{'='*60}")
    
    try:
        # Inicializa componentes
        collection_manager = NewsCollectionManager()
        data_processor = DataProcessor()
        
        # Coleta notícias
        print("📡 Coletando notícias das fontes...")
        articles = collection_manager.collect_all_news()
        
        if not articles:
            print("❌ Nenhuma notícia foi coletada")
            return False
        
        print(f"✅ Coletadas {len(articles)} notícias")
        
        # Salva resultados (opcional - para backup)
        if OUTPUT_CONFIG.get('save_to_file', False):
            print("💾 Salvando resultados...")
            csv_file = data_processor.save_to_csv(articles)
            json_file = data_processor.save_to_json(articles)
            html_file = data_processor.save_to_html(articles)
            
            print(f"✅ Resultados salvos:")
            print(f"   CSV: {os.path.basename(csv_file)}")
            print(f"   JSON: {os.path.basename(json_file)}")
            print(f"   HTML: {os.path.basename(html_file)}")
        
        # Gera resumo
        summary = data_processor.generate_daily_summary(articles)
        if summary:
            summary_file = data_processor.save_daily_summary(summary)
            print(f"   Resumo: {os.path.basename(summary_file)}")
        
        # Envia email
        if OUTPUT_CONFIG.get('save_to_email', False):
            print("\n📧 Enviando email...")
            if data_processor.send_email_report(articles):
                print("✅ Email enviado com sucesso!")
                return True
            else:
                print("❌ Erro ao enviar email")
                return False
        else:
            print("\n📧 Email não configurado para envio automático")
            return False
        
    except Exception as e:
        print(f"❌ Erro durante a coleta agendada: {e}")
        logging.error(f"Erro na coleta agendada: {e}")
        return False


if __name__ == "__main__":
    # Configura logging
    setup_logging()
    
    # Executa coleta
    sucesso = executar_coleta_agendada()
    
    if sucesso:
        print("\n🎉 Coleta agendada concluída com sucesso!")
        sys.exit(0)
    else:
        print("\n❌ Coleta agendada falhou!")
        sys.exit(1)
