#!/usr/bin/env python3
"""
Teste rápido do sistema de coleta de notícias
Executa verificações básicas para garantir que tudo está funcionando
"""

import sys
import os
import importlib
from datetime import datetime

def test_imports():
    """Testa se todos os módulos podem ser importados"""
    print("🔍 Testando importações...")
    
    required_modules = [
        'requests',
        'beautifulsoup4',
        'pandas',
        'schedule',
        'lxml'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Falha na importação: {', '.join(failed_imports)}")
        print("Execute: pip install -r requirements.txt")
        return False
    
    print("✅ Todas as importações funcionaram!")
    return True


def test_local_modules():
    """Testa se os módulos locais podem ser importados"""
    print("\n🔍 Testando módulos locais...")
    
    local_modules = [
        'config',
        'news_collector',
        'data_processor',
        'scheduler'
    ]
    
    failed_imports = []
    
    for module in local_modules:
        try:
            importlib.import_module(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Falha na importação de módulos locais: {', '.join(failed_imports)}")
        return False
    
    print("✅ Todos os módulos locais funcionaram!")
    return True


def test_directories():
    """Testa se os diretórios necessários existem ou podem ser criados"""
    print("\n🔍 Testando diretórios...")
    
    required_dirs = ['output', 'logs']
    
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            try:
                os.makedirs(dir_name)
                print(f"  ✅ Criado: {dir_name}/")
            except Exception as e:
                print(f"  ❌ Erro ao criar {dir_name}/: {e}")
                return False
        else:
            print(f"  ✅ Existe: {dir_name}/")
    
    return True


def test_config():
    """Testa se as configurações estão válidas"""
    print("\n🔍 Testando configurações...")
    
    try:
        from config import NEWS_SOURCES, COLLECTION_CONFIG, OUTPUT_CONFIG
        
        # Verifica fontes de notícias
        if not NEWS_SOURCES:
            print("  ❌ Nenhuma fonte de notícias configurada")
            return False
        
        print(f"  ✅ Fontes configuradas: {len(NEWS_SOURCES)}")
        
        # Verifica configurações de coleta
        if not COLLECTION_CONFIG:
            print("  ❌ Configurações de coleta não encontradas")
            return False
        
        print(f"  ✅ Intervalo de coleta: {COLLECTION_CONFIG.get('collection_interval_hours', 'N/A')} horas")
        
        # Verifica configurações de saída
        if not OUTPUT_CONFIG:
            print("  ❌ Configurações de saída não encontradas")
            return False
        
        print(f"  ✅ Formato de saída: {OUTPUT_CONFIG.get('file_format', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erro ao testar configurações: {e}")
        return False


def test_basic_functionality():
    """Testa funcionalidades básicas do sistema"""
    print("\n🔍 Testando funcionalidades básicas...")
    
    try:
        from news_collector import NewsCollectionManager
        from data_processor import DataProcessor
        
        # Testa criação dos objetos
        collection_manager = NewsCollectionManager()
        data_processor = DataProcessor()
        
        print("  ✅ Objetos criados com sucesso")
        
        # Testa se os coletores estão configurados
        if hasattr(collection_manager, 'collectors') and collection_manager.collectors:
            print(f"  ✅ Coletores configurados: {len(collection_manager.collectors)}")
        else:
            print("  ❌ Nenhum coletor configurado")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erro ao testar funcionalidades: {e}")
        return False


def run_quick_test():
    """Executa teste rápido de uma fonte"""
    print("\n🧪 Executando teste rápido de coleta...")
    
    try:
        from news_collector import NewsCollectionManager
        
        collection_manager = NewsCollectionManager()
        
        # Testa apenas uma fonte para ser mais rápido
        if 'g1_tecnologia' in collection_manager.collectors:
            print("  📡 Testando coleta do G1 Tecnologia...")
            
            collector = collection_manager.collectors['g1_tecnologia']
            articles = collector.collect_news()
            
            if articles:
                print(f"  ✅ Coletadas {len(articles)} notícias do G1")
                print(f"  📰 Exemplo: {articles[0].title[:50]}...")
                return True
            else:
                print("  ⚠️  Nenhuma notícia coletada (pode ser normal)")
                return True
        else:
            print("  ❌ Coletor G1 não encontrado")
            return False
            
    except Exception as e:
        print(f"  ❌ Erro no teste rápido: {e}")
        return False


def main():
    """Função principal do teste"""
    print("🚀 TESTE RÁPIDO DO SISTEMA DE COLETA DE NOTÍCIAS")
    print("=" * 60)
    print(f"⏰ Iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    tests = [
        ("Importações de bibliotecas", test_imports),
        ("Módulos locais", test_local_modules),
        ("Diretórios", test_directories),
        ("Configurações", test_config),
        ("Funcionalidades básicas", test_basic_functionality),
        ("Teste rápido de coleta", run_quick_test)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 40)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSOU")
            else:
                print(f"❌ {test_name}: FALHOU")
        except Exception as e:
            print(f"❌ {test_name}: ERRO - {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 RESULTADO: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 SISTEMA FUNCIONANDO PERFEITAMENTE!")
        print("\n💡 Próximos passos:")
        print("   python main.py --test          # Coleta completa de teste")
        print("   python main.py --scheduler     # Iniciar agendador")
        print("   python main.py --help          # Ver todas as opções")
    else:
        print("⚠️  ALGUNS TESTES FALHARAM")
        print("\n🔧 Verifique:")
        print("   1. Se todas as dependências estão instaladas")
        print("   2. Se está no diretório correto")
        print("   3. Se os arquivos de configuração estão válidos")
        print("   4. Os logs para mais detalhes")
    
    print("=" * 60)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
