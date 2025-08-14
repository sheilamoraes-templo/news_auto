# 🚀 Sistema de Coleta Automatizada de Notícias de Tecnologia

Um sistema completo e automatizado para coleta, processamento e análise de notícias sobre tecnologia e inovação de múltiplas fontes brasileiras.

## 📋 Características Principais

- **Coleta Automatizada**: Coleta notícias de 3 fontes principais de tecnologia
- **Remoção de Duplicatas**: Sistema inteligente de detecção e remoção de notícias repetidas
- **Filtragem por Palavras-chave**: Foca em notícias relevantes de tecnologia e inovação
- **Múltiplos Formatos de Saída**: CSV, JSON e HTML formatado
- **Agendamento Automático**: Execução em intervalos configuráveis
- **Relatórios Diários**: Resumos automáticos com estatísticas
- **Logs Detalhados**: Sistema completo de monitoramento e debug

## 🗞️ Fontes de Notícias

- **G1 Tecnologia**: https://g1.globo.com/tecnologia/
- **Folha de S.Paulo - Tec**: https://www1.folha.uol.com.br/tec/
- **UOL Tilt**: https://www.uol.com.br/tilt/

## 🛠️ Requisitos

- Python 3.8+
- Bibliotecas listadas em `requirements.txt`

## 📦 Instalação

1. **Clone ou baixe o projeto**:
```bash
cd news_auto
```

2. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

3. **Verifique a instalação**:
```bash
python main.py --status
```

## 🚀 Como Usar

### 1. Coleta de Teste (Recomendado para começar)

Execute uma coleta única para testar o sistema:

```bash
python main.py --test
```

Este comando irá:
- Coletar notícias de todas as fontes
- Processar e filtrar os dados
- Salvar em múltiplos formatos
- Gerar um relatório HTML visual

### 2. Agendador Contínuo

Para executar o sistema continuamente (coleta a cada 6 horas):

```bash
python main.py --scheduler
```

**Para parar**: Pressione `Ctrl+C`

### 3. Agendador em Background

Para executar o sistema em background (continua rodando mesmo após fechar o terminal):

```bash
python main.py --background
```

**Para parar o agendador em background**:
```bash
python main.py --stop-background
```

### 4. Verificar Status

Para ver o status atual do sistema:

```bash
python main.py --status
```

## 📁 Estrutura de Arquivos

```
news_auto/
├── main.py                 # Arquivo principal e interface CLI
├── config.py              # Configurações do sistema
├── news_collector.py      # Módulo de coleta de notícias
├── data_processor.py      # Processamento e geração de relatórios
├── scheduler.py           # Agendamento automático
├── requirements.txt       # Dependências Python
├── README.md             # Esta documentação
├── output/               # Arquivos gerados (CSV, JSON, HTML)
└── logs/                 # Logs do sistema
```

## ⚙️ Configuração

### Personalizar Fontes

Edite `config.py` para adicionar ou modificar fontes:

```python
NEWS_SOURCES = {
    'nova_fonte': {
        'url': 'https://exemplo.com/tecnologia/',
        'name': 'Nova Fonte',
        'type': 'html'
    }
}
```

### Ajustar Intervalos

Modifique as configurações de coleta:

```python
COLLECTION_CONFIG = {
    'collection_interval_hours': 4,  # Coleta a cada 4 horas
    'daily_summary_time': '09:00',   # Resumo diário às 9h
    'max_articles_per_source': 30,   # Máximo de artigos por fonte
}
```

### Palavras-chave de Filtro

Personalize as palavras-chave para focar em tópicos específicos:

```python
'keywords_filter': [
    'tecnologia', 'inovação', 'startup', 'IA', 'blockchain',
    'fintech', 'sustentabilidade', 'energia renovável'
]
```

## 📊 Formatos de Saída

### 1. CSV
- Formato tabular para análise em Excel/Google Sheets
- Inclui todas as informações coletadas
- Codificação UTF-8 para caracteres especiais

### 2. JSON
- Formato estruturado para processamento programático
- Ideal para integração com outras aplicações
- Mantém toda a estrutura de dados

### 3. HTML
- Relatório visual formatado e responsivo
- Estatísticas e gráficos
- Links diretos para as notícias originais

## 🔍 Monitoramento e Logs

### Logs do Sistema

Os logs são salvos em `logs/news_collector.log` e incluem:
- Informações de coleta
- Erros e avisos
- Estatísticas de performance
- Timestamps detalhados

### Verificar Logs

```bash
# Ver logs em tempo real
tail -f logs/news_collector.log

# Últimas 50 linhas
tail -n 50 logs/news_collector.log
```

## 🚨 Solução de Problemas

### Erro de Conexão

Se houver problemas de conexão com as fontes:

1. Verifique sua conexão com a internet
2. As fontes podem estar temporariamente indisponíveis
3. Verifique os logs para detalhes específicos

### Poucas Notícias Coletadas

1. Verifique se as URLs das fontes ainda estão válidas
2. As fontes podem ter mudado sua estrutura HTML
3. Ajuste as palavras-chave de filtro se necessário

### Erro de Importação

Se houver erros de módulos não encontrados:

```bash
# Reinstale as dependências
pip install -r requirements.txt

# Verifique se está no diretório correto
pwd
ls -la
```

## 🔧 Desenvolvimento

### Adicionar Nova Fonte

1. Crie uma nova classe coletora em `news_collector.py`
2. Implemente os métodos necessários
3. Adicione a fonte em `config.py`
4. Teste com `python main.py --test`

### Estrutura de uma Classe Coletora

```python
class NovaFonteCollector(BaseNewsCollector):
    def collect_news(self) -> List[NewsArticle]:
        # Implementar lógica de coleta
        pass
    
    def _is_news_link(self, href: str) -> bool:
        # Implementar filtro de links
        pass
```

## 📈 Estatísticas e Métricas

O sistema coleta automaticamente:
- Total de notícias por fonte
- Palavras-chave mais frequentes
- Tempo de coleta e processamento
- Taxa de sucesso das coletas

## 🔒 Considerações de Uso

- **Respeite os termos de uso** das fontes de notícias
- **Não sobrecarregue** os servidores (pausas automáticas implementadas)
- **Use para fins educacionais e de pesquisa**
- **Atribua crédito** às fontes originais

## 📞 Suporte

Para problemas ou sugestões:

1. Verifique os logs primeiro
2. Consulte esta documentação
3. Teste com `--test` para isolar problemas
4. Verifique se as dependências estão atualizadas

## 🎯 Exemplos de Uso

### Coleta Diária para Pesquisa

```bash
# Iniciar agendador em background às 8h
python main.py --background

# Verificar status
python main.py --status

# Parar quando necessário
python main.py --stop-background
```

### Análise Manual

```bash
# Coleta única para análise
python main.py --test

# Ver arquivos gerados
ls -la output/

# Abrir relatório HTML
start output/noticias_tecnologia_*.html
```

### Integração com Outros Sistemas

Os arquivos JSON podem ser facilmente integrados com:
- Dashboards (Power BI, Tableau)
- Análise de dados (Python, R)
- Sistemas de alerta
- APIs personalizadas

## 🚀 Próximos Passos

- [ ] Adicionar mais fontes de notícias
- [ ] Implementar análise de sentimento
- [ ] Adicionar notificações por email
- [ ] Dashboard web em tempo real
- [ ] API REST para integração
- [ ] Suporte a feeds RSS

---

**🎉 Sistema desenvolvido para coleta automatizada de notícias de tecnologia e inovação!**

*Última atualização: Dezembro 2024*
