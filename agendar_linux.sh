#!/bin/bash

# Agendador de Tarefas para Linux/macOS
# ======================================
# Este script configura o agendamento automático
# do sistema de coleta de notícias usando cron

set -e  # Para o script se houver erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir com cores
print_status() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️  ${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ️  ${NC} $1"
}

echo "========================================"
echo "  AGENDADOR DE TAREFAS LINUX/MACOS"
echo "========================================"
echo
echo "Este script configura o agendamento automático"
echo "do sistema de coleta de notícias usando cron."
echo

# Verificar se está rodando como root (opcional)
if [[ $EUID -eq 0 ]]; then
    print_warning "Executando como root (recomendado para cron)"
else
    print_warning "Executando como usuário normal"
    print_info "Para agendamento global, execute como root"
fi

# Obter o diretório atual
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$CURRENT_DIR/main.py"
CRON_JOB_NAME="coleta_automatica_noticias"

echo "📍 Diretório atual: $CURRENT_DIR"
echo "🐍 Script Python: $PYTHON_SCRIPT"
echo "📅 Nome da tarefa: $CRON_JOB_NAME"
echo

# Verificar se o script Python existe
if [[ ! -f "$PYTHON_SCRIPT" ]]; then
    print_error "Arquivo main.py não encontrado em $CURRENT_DIR"
    echo
    exit 1
fi

print_status "Arquivo main.py encontrado"

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        print_error "Python não está instalado"
        echo
        echo "Soluções:"
        echo "1. Ubuntu/Debian: sudo apt install python3 python3-pip"
        echo "2. CentOS/RHEL: sudo yum install python3 python3-pip"
        echo "3. macOS: brew install python3"
        echo "4. Ou baixe de https://python.org"
        echo
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

print_status "Python encontrado"
$PYTHON_CMD --version

# Verificar se as dependências estão instaladas
echo
print_info "Verificando dependências..."
cd "$CURRENT_DIR"

if ! $PYTHON_CMD -m pip install -r requirements.txt &> /dev/null; then
    print_warning "Erro ao instalar dependências automaticamente"
    print_info "Execute manualmente: $PYTHON_CMD -m pip install -r requirements.txt"
else
    print_status "Dependências instaladas/verificadas"
fi

# Criar diretórios necessários
mkdir -p output logs data
print_status "Diretórios criados/verificados"

# Verificar se cron está disponível
if ! command -v crontab &> /dev/null; then
    print_error "crontab não está disponível"
    echo
    echo "Soluções:"
    echo "1. Ubuntu/Debian: sudo apt install cron"
    echo "2. CentOS/RHEL: sudo yum install cronie"
    echo "3. macOS: cron já vem instalado por padrão"
    echo
    exit 1
fi

print_status "crontab disponível"

# Criar arquivo de log para cron
CRON_LOG="$CURRENT_DIR/logs/cron.log"
touch "$CRON_LOG"

# Função para criar o comando cron
create_cron_command() {
    local schedule="$1"
    local description="$2"
    
    # Comando para executar o script
    local command="$PYTHON_CMD \"$PYTHON_SCRIPT\" --scheduler"
    
    # Adicionar redirecionamento de output para log
    local full_command="$command >> \"$CRON_LOG\" 2>&1"
    
    echo "$schedule $full_command # $description"
}

# Criar entradas cron
echo
print_info "Configurando agendamentos cron..."

# Coleta diária às 8:00
CRON_DAILY="0 8 * * *"
CRON_DAILY_DESC="Coleta diária de notícias às 8:00"

# Coleta a cada 4 horas (opcional)
CRON_HOURLY="0 */4 * * *"
CRON_HOURLY_DESC="Coleta a cada 4 horas"

# Backup semanal aos domingos às 2:00
CRON_BACKUP="0 2 * * 0"
CRON_BACKUP_DESC="Backup semanal aos domingos às 2:00"

# Criar arquivo temporário com as entradas cron
TEMP_CRON=$(mktemp)

# Adicionar comentário de cabeçalho
cat > "$TEMP_CRON" << EOF
# ========================================
# AGENDAMENTO DO SISTEMA DE COLETA DE NOTÍCIAS
# ========================================
# Gerado automaticamente em: $(date)
# Diretório: $CURRENT_DIR
# Log: $CRON_LOG
# ========================================

EOF

# Adicionar entradas cron
create_cron_command "$CRON_DAILY" "$CRON_DAILY_DESC" >> "$TEMP_CRON"
create_cron_command "$CRON_HOURLY" "$CRON_HOURLY_DESC" >> "$TEMP_CRON"
create_cron_command "$CRON_BACKUP" "$CRON_BACKUP_DESC" >> "$TEMP_CRON"

# Adicionar linha em branco
echo "" >> "$TEMP_CRON"

# Mostrar o que será adicionado ao cron
echo "📋 Entradas cron que serão adicionadas:"
echo "----------------------------------------"
cat "$TEMP_CRON"
echo "----------------------------------------"
echo

# Perguntar confirmação
read -p "Deseja continuar e adicionar estas entradas ao cron? (s/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Ss]$ ]]; then
    # Fazer backup do cron atual
    print_info "Fazendo backup do cron atual..."
    crontab -l > "$CURRENT_DIR/cron_backup_$(date +%Y%m%d_%H%M%S).txt" 2>/dev/null || true
    
    # Adicionar novas entradas ao cron
    print_info "Adicionando entradas ao cron..."
    if crontab "$TEMP_CRON"; then
        print_status "Entradas cron adicionadas com sucesso!"
        
        echo
        echo "📋 Agendamentos configurados:"
        echo "  • Coleta diária: 8:00"
        echo "  • Coleta a cada 4 horas"
        echo "  • Backup semanal: Domingos às 2:00"
        echo
        
        echo "📁 Arquivos e diretórios:"
        echo "  • Script: $PYTHON_SCRIPT"
        echo "  • Log cron: $CRON_LOG"
        echo "  • Backup cron: $CURRENT_DIR/cron_backup_*.txt"
        echo
        
        echo "🔧 Comandos úteis:"
        echo "  • Ver cron atual: crontab -l"
        echo "  • Editar cron: crontab -e"
        echo "  • Remover cron: crontab -r"
        echo "  • Ver logs: tail -f $CRON_LOG"
        echo
        
    else
        print_error "Falha ao adicionar entradas ao cron"
        exit 1
    fi
else
    print_info "Operação cancelada pelo usuário"
fi

# Limpar arquivo temporário
rm -f "$TEMP_CRON"

echo "========================================"
echo "  CONFIGURAÇÃO CONCLUÍDA"
echo "========================================"
echo
echo "💡 Próximos passos:"
echo "1. Teste o sistema: $PYTHON_CMD main.py --test"
echo "2. Execute manualmente: $PYTHON_CMD main.py --scheduler"
echo "3. Verifique os logs em: logs/"
echo "4. Verifique os dados em: output/"
echo "5. Monitore o cron: tail -f $CRON_LOG"
echo
echo "🚀 O sistema está configurado para rodar automaticamente!"
echo
