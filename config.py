# Configurações do sistema de coleta de notícias (versão para GitHub Actions)
import os
from datetime import datetime

# URLs das fontes de notícias
NEWS_SOURCES = {
    'g1_tecnologia': {
        'url': 'https://g1.globo.com/tecnologia/',
        'name': 'G1 Tecnologia',
        'type': 'html'
    },
    'folha_tec': {
        'url': 'https://www1.folha.uol.com.br/tec/',
        'name': 'Folha de S.Paulo - Tec',
        'type': 'html'
    },
    'uol_tilt': {
        'url': 'https://www.uol.com.br/tilt/',
        'name': 'UOL Tilt',
        'type': 'html'
    }
}

# Configurações de coleta
COLLECTION_CONFIG = {
    'max_articles_per_source': 20,
    'collection_interval_hours': 24,   # Coleta 1 vez por dia
    'daily_summary_time': '13:00',     # Resumo diário às 13h (coerente com BR)
    'remove_duplicates': True,
    'min_title_length': 10,
    'keywords_filter': [
        'tecnologia', 'inovação', 'startup', 'IA', 'inteligência artificial',
        'machine learning', 'blockchain', 'fintech', 'edtech', 'healthtech',
        'sustentabilidade', 'energia renovável', 'carro elétrico', '5G',
        'metaverso', 'NFT', 'cryptocurrency', 'robótica', 'automação'
    ]
}

# Configurações de saída
OUTPUT_CONFIG = {
    # Em GitHub Actions: deixe False (só e-mail) ou ative com SAVE_TO_FILE=true
    'save_to_file': os.getenv('SAVE_TO_FILE', 'False').lower() == 'true',
    'save_to_email': True,                  # Enviar por e-mail
    'output_directory': 'output',
    'file_format': os.getenv('FILE_FORMAT', 'html'),  # 'html' é ideal p/ e-mail
    'email_recipients': [os.getenv('EMAIL_TO', 'sheila.moraes@templo.cc')],
    'email_subject_prefix': os.getenv('EMAIL_SUBJECT_PREFIX', '[News Auto] Resumo Diário de Tecnologia')
}

# Configurações de e-mail (lidas de variáveis de ambiente / Secrets no GitHub)
EMAIL_CONFIG = {
    'smtp_server': os.getenv('SMTP_HOST', 'smtp.gmail.com'),
    'smtp_port': int(os.getenv('SMTP_PORT', '587')),
    'smtp_username': os.getenv('SMTP_USER', ''),        # setado via Secret
    'smtp_password': os.getenv('SMTP_PASS', ''),        # setado via Secret
    'use_tls': True,
    'from_name': os.getenv('EMAIL_FROM_NAME', 'Sistema de Coleta de Notícias')
}

# Configurações de log
LOG_CONFIG = {
    'log_level': 'INFO',
    'log_file': 'logs/news_collector.log',
    'max_log_size_mb': 10,
    'backup_count': 5
}

# Diretórios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, OUTPUT_CONFIG['output_directory'])
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# Criar diretórios se não existirem
for directory in [OUTPUT_DIR, LOGS_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)
