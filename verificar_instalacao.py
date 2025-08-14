#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificador de Instalação do Sistema de Coleta de Notícias
==========================================================

Este script verifica se todas as dependências e módulos estão funcionando corretamente.
Execute este arquivo para diagnosticar problemas de instalação.
"""

import sys
import os
import subprocess
import importlib
from pathlib import Path

def verificar_python():
    """Verifica a versão do Python"""
    print("🐍 Verificando versão do Python...")
    
    version = sys.version_info
    print(f"  Versão: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  ❌ Python 3.8+ é necessário")
        return False
    else:
        print("  ✅ Versão do Python compatível")
        return True

def verificar_pip():
    """Verifica se o pip está disponível"""
    print("\n📦 Verificando pip...")
    
    try:
        import pip
        print(f"  ✅ pip disponível - versão {pip.__version__}")
        return True
    except ImportError:
        print("  ❌ pip não está disponível")
        return False

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    print("\n📚 Verificando dependências...")
    
    dependencias = [
        'requests',
        'beautifulsoup4',
        'lxml',
        'pandas',
        'schedule',
        'python-dotenv',
        'feedparser',
        'newspaper3k',
        'nltk',
        'textblob'
    ]
    
    faltando = []
    instaladas = []
    
    for dep in dependencias:
        try:
            module = importlib.import_module(dep)
            version = getattr(module, '__version__', 'versão desconhecida')
            print(f"  ✅ {dep} - {version}")
            instaladas.append(dep)
        except ImportError:
            print(f"  ❌ {dep} - não instalado")
            faltando.append(dep)
    
    if faltando:
        print(f"\n⚠️  Dependências faltando: {', '.join(faltando)}")
        print("Execute: pip install -r requirements.txt")
        return False
    else:
        print(f"\n✅ Todas as {len(instaladas)} dependências estão instaladas")
        return True

def verificar_modulos_locais():
    """Verifica se os módulos locais podem ser importados"""
    print("\n🏠 Verificando módulos locais...")
    
    modulos = [
        'config',
        'news_collector',
        'data_processor',
        'scheduler'
    ]
    
    faltando = []
    funcionando = []
    
    for modulo in modulos:
        try:
            module = importlib.import_module(modulo)
            print(f"  ✅ {modulo} - importado com sucesso")
            funcionando.append(modulo)
        except ImportError as e:
            print(f"  ❌ {modulo} - erro: {e}")
            faltando.append(modulo)
    
    if faltando:
        print(f"\n⚠️  Módulos com problema: {', '.join(faltando)}")
        return False
    else:
        print(f"\n✅ Todos os {len(funcionando)} módulos locais funcionando")
        return True

def verificar_diretorios():
    """Verifica se os diretórios necessários existem"""
    print("\n📁 Verificando estrutura de diretórios...")
    
    diretorios = ['output', 'logs', 'data']
    
    for dir_name in diretorios:
        if os.path.exists(dir_name):
            print(f"  ✅ {dir_name}/ - existe")
        else:
            print(f"  ❌ {dir_name}/ - não existe")
            try:
                os.makedirs(dir_name)
                print(f"  ✅ {dir_name}/ - criado")
            except Exception as e:
                print(f"  ❌ {dir_name}/ - erro ao criar: {e}")

def verificar_arquivos():
    """Verifica se os arquivos principais existem"""
    print("\n📄 Verificando arquivos principais...")
    
    arquivos = [
        'requirements.txt',
        'config.py',
        'news_collector.py',
        'data_processor.py',
        'scheduler.py',
        'main.py',
        'README.md'
    ]
    
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            size = os.path.getsize(arquivo)
            print(f"  ✅ {arquivo} - {size} bytes")
        else:
            print(f"  ❌ {arquivo} - não existe")

def testar_importacao_completa():
    """Testa a importação completa do sistema"""
    print("\n🧪 Testando importação completa...")
    
    try:
        # Importar módulos principais
        from config import NEWS_SOURCES, COLLECTION_CONFIG
        from news_collector import NewsCollectionManager
        from data_processor import DataProcessor
        from scheduler import NewsScheduler
        
        print("  ✅ Importação dos módulos principais bem-sucedida")
        
        # Testar criação de objetos
        collector = NewsCollectionManager()
        processor = DataProcessor()
        scheduler = NewsScheduler()
        
        print("  ✅ Criação de objetos bem-sucedida")
        
        # Testar configurações
        print(f"  ✅ Fontes configuradas: {list(NEWS_SOURCES.keys())}")
        print(f"  ✅ Intervalo de coleta: {COLLECTION_CONFIG['collection_interval_hours']} horas")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erro na importação completa: {e}")
        return False

def verificar_conectividade():
    """Verifica conectividade com as fontes de notícias"""
    print("\n🌐 Verificando conectividade...")
    
    try:
        import requests
        
        fontes = [
            'https://g1.globo.com/tecnologia/',
            'https://www1.folha.uol.com.br/tec/',
            'https://www.uol.com.br/tilt/'
        ]
        
        for fonte in fontes:
            try:
                response = requests.get(fonte, timeout=10)
                if response.status_code == 200:
                    print(f"  ✅ {fonte} - acessível")
                else:
                    print(f"  ⚠️  {fonte} - status {response.status_code}")
            except Exception as e:
                print(f"  ❌ {fonte} - erro: {e}")
                
    except ImportError:
        print("  ❌ requests não disponível para teste de conectividade")

def executar_teste_rapido():
    """Executa um teste rápido do sistema"""
    print("\n🚀 Executando teste rápido...")
    
    try:
        from test_quick import run_quick_test
        resultado = run_quick_test()
        if resultado:
            print("  ✅ Teste rápido bem-sucedido")
        else:
            print("  ❌ Teste rápido falhou")
        return resultado
    except ImportError:
        print("  ⚠️  test_quick.py não encontrado")
        return False

def main():
    """Função principal de verificação"""
    print("🔍 VERIFICADOR DE INSTALAÇÃO")
    print("=" * 50)
    print("Verificando se o sistema está funcionando corretamente...\n")
    
    resultados = []
    
    # Executar verificações
    resultados.append(verificar_python())
    resultados.append(verificar_pip())
    resultados.append(verificar_dependencias())
    resultados.append(verificar_modulos_locais())
    verificar_diretorios()
    verificar_arquivos()
    verificar_conectividade()
    resultados.append(testar_importacao_completa())
    resultados.append(executar_teste_rapido())
    
    # Resumo final
    print("\n" + "=" * 50)
    print("📊 RESUMO DA VERIFICAÇÃO")
    print("=" * 50)
    
    sucessos = sum(resultados)
    total = len(resultados)
    
    if sucessos == total:
        print("🎉 TODAS AS VERIFICAÇÕES PASSARAM!")
        print("✅ O sistema está funcionando corretamente")
        print("\n💡 Próximos passos:")
        print("  1. Execute 'python main.py --test' para testar a coleta")
        print("  2. Execute 'python main.py --scheduler' para iniciar o agendador")
        print("  3. Execute 'python exemplo_uso.py' para ver exemplos")
    else:
        print(f"⚠️  {sucessos}/{total} verificações passaram")
        print("❌ Existem problemas que precisam ser resolvidos")
        print("\n🔧 Soluções:")
        print("  1. Execute 'pip install -r requirements.txt'")
        print("  2. Verifique se está no diretório correto")
        print("  3. Verifique se o Python está configurado corretamente")
        print("  4. Execute 'python verificar_instalacao.py' novamente após resolver os problemas")

if __name__ == "__main__":
    main()
