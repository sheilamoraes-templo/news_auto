"""
Sistema Principal de Coleta Automatizada de Notícias de Tecnologia
Integra todos os módulos e fornece interface de linha de comando
"""

import sys
import os
import argparse
import logging
from datetime import datetime

# Adiciona o diretório atual ao path para importações
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import LOG_CONFIG, OUTPUT_CONFIG
from news_collector import NewsCollectionManager
from data_processor import DataProcessor
from scheduler import NewsScheduler, run_single_collection


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


def show_status():
    """Mostra status do sistema"""
    print("\n" + "="*60)
    print("📊 STATUS DO SISTEMA DE COLETA DE NOTÍCIAS")
    print("="*60)
    
    # Verifica diretórios
    output_dir = OUTPUT_CONFIG['output_directory']
    logs_dir = os.path.dirname(LOG_CONFIG['log_file'])
    
    print(f"📁 Diretório de saída: {output_dir}")
    print(f"📁 Diretório de logs: {logs_dir}")
    
    # Verifica arquivos existentes
    if os.path.exists(output_dir):
        files = [f for f in os.listdir(output_dir) if f.endswith(('.csv', '.json', '.html'))]
        print(f"📄 Arquivos de saída: {len(files)}")
        if files:
            print("   Últimos arquivos:")
            for file in sorted(files, key=lambda x: os.path.getmtime(os.path.join(output_dir, x)), reverse=True)[:5]:
                filepath = os.path.join(output_dir, file)
                mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                print(f"   - {file} (modificado: {mtime.strftime('%d/%m/%Y %H:%M')})")
    else:
        print("📄 Diretório de saída não existe")
    
    print("\n" + "="*60)


def run_test_collection():
    """Executa uma coleta de teste"""
    print("\n🧪 Executando coleta de teste...")
    
    try:
        # Inicializa componentes
        collection_manager = NewsCollectionManager()
        data_processor = DataProcessor()
        
        # Coleta notícias
        print("📡 Coletando notícias das fontes...")
        articles = collection_manager.collect_all_news()
        
        if not articles:
            print("❌ Nenhuma notícia foi coletada")
            return
        
        print(f"✅ Coletadas {len(articles)} notícias")
        
        # Mostra algumas notícias
        print("\n📰 Primeiras 5 notícias coletadas:")
        for i, article in enumerate(articles[:5], 1):
            print(f"{i}. {article.title}")
            print(f"   Fonte: {article.source}")
            print(f"   URL: {article.url}")
            if article.summary:
                print(f"   Resumo: {article.summary[:100]}...")
            print()
        
        # Salva resultados
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
        else:
            print("   ⚠️ Não foi possível gerar resumo")
        
        # Envia email se configurado
        if OUTPUT_CONFIG.get('save_to_email', False):
            print("\n📧 Enviando email...")
            if data_processor.send_email_report(articles):
                print("✅ Email enviado com sucesso!")
            else:
                print("❌ Erro ao enviar email")
        else:
            print("\n📧 Email não configurado para envio automático")
        
        print("\n🎉 Coleta de teste concluída com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro durante a coleta de teste: {e}")
        logging.error(f"Erro na coleta de teste: {e}")


def run_continuous_scheduler():
    """Executa o agendador contínuo"""
    print("\n🔄 Iniciando agendador contínuo...")
    print("   Pressione Ctrl+C para parar")
    
    try:
        scheduler = NewsScheduler()
        scheduler.start_scheduler()
    except KeyboardInterrupt:
        print("\n⏹️  Agendador interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro no agendador: {e}")
        logging.error(f"Erro no agendador: {e}")


def run_background_scheduler():
    """Executa o agendador em background"""
    print("\n🔄 Iniciando agendador em background...")
    print("   O sistema continuará rodando mesmo após fechar este terminal")
    
    try:
        from scheduler import BackgroundScheduler
        bg_scheduler = BackgroundScheduler()
        bg_scheduler.start()
        
        # Aguarda um pouco para garantir que iniciou
        import time
        time.sleep(3)
        
        print("✅ Agendador iniciado em background")
        print("   Para parar, use o comando: python main.py --stop-background")
        
    except Exception as e:
        print(f"❌ Erro ao iniciar agendador em background: {e}")
        logging.error(f"Erro ao iniciar agendador em background: {e}")


def stop_background_scheduler():
    """Para o agendador em background"""
    print("\n🛑 Parando agendador em background...")
    
    try:
        # Busca por processos Python rodando o scheduler
        import psutil
        import os
        
        current_pid = os.getpid()
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if (proc.info['name'] == 'python' and 
                    proc.info['pid'] != current_pid and
                    proc.info['cmdline'] and
                    any('scheduler' in cmd.lower() for cmd in proc.info['cmdline'])):
                    
                    print(f"   Parando processo {proc.info['pid']}")
                    proc.terminate()
                    proc.wait(timeout=5)
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                continue
        
        print("✅ Agendador em background parado")
        
    except ImportError:
        print("❌ Biblioteca psutil não encontrada. Instale com: pip install psutil")
    except Exception as e:
        print(f"❌ Erro ao parar agendador: {e}")


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description='Sistema de Coleta Automatizada de Notícias de Tecnologia',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py --test                    # Executa coleta de teste
  python main.py --scheduler               # Inicia agendador contínuo
  python main.py --background              # Inicia agendador em background
  python main.py --stop-background         # Para agendador em background
  python main.py --status                  # Mostra status do sistema
  python main.py                           # Mostra ajuda
        """
    )
    
    parser.add_argument('--test', action='store_true',
                       help='Executa uma coleta de teste')
    parser.add_argument('--scheduler', action='store_true',
                       help='Inicia o agendador contínuo')
    parser.add_argument('--background', action='store_true',
                       help='Inicia o agendador em background')
    parser.add_argument('--stop-background', action='store_true',
                       help='Para o agendador em background')
    parser.add_argument('--status', action='store_true',
                       help='Mostra status do sistema')
    
    args = parser.parse_args()
    
    # Configura logging
    setup_logging()
    
    # Banner
    print("\n" + "="*60)
    print("🚀 SISTEMA DE COLETA AUTOMATIZADA DE NOTÍCIAS")
    print("📰 Tecnologia e Inovação")
    print("="*60)
    
    try:
        if args.test:
            run_test_collection()
        elif args.scheduler:
            run_continuous_scheduler()
        elif args.background:
            run_background_scheduler()
        elif args.stop_background:
            stop_background_scheduler()
        elif args.status:
            show_status()
        else:
            # Mostra ajuda se nenhum argumento for fornecido
            parser.print_help()
            print("\n" + "="*60)
            print("💡 Dica: Use --test para executar uma coleta de teste")
            print("="*60)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Programa interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        logging.error(f"Erro inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
