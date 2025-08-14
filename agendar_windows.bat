@echo off
chcp 65001 >nul
echo ========================================
echo  AGENDADOR DE TAREFAS DO WINDOWS
echo ========================================
echo.
echo Este script configura o agendamento automático
echo do sistema de coleta de notícias no Windows.
echo.

REM Verificar se está rodando como administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ ERRO: Este script precisa ser executado como Administrador!
    echo.
    echo Para executar como administrador:
    echo 1. Clique com o botão direito no arquivo
    echo 2. Selecione "Executar como administrador"
    echo.
    pause
    exit /b 1
)

echo ✅ Executando como administrador
echo.

REM Obter o diretório atual
set "CURRENT_DIR=%~dp0"
set "PYTHON_SCRIPT=%CURRENT_DIR%main.py"
set "TASK_NAME=Coleta_Automatica_Noticias"
set "TASK_DESCRIPTION=Sistema automatizado de coleta de notícias sobre tecnologia e inovação"

echo 📍 Diretório atual: %CURRENT_DIR%
echo 🐍 Script Python: %PYTHON_SCRIPT%
echo 📅 Nome da tarefa: %TASK_NAME%
echo.

REM Verificar se o script Python existe
if not exist "%PYTHON_SCRIPT%" (
    echo ❌ ERRO: Arquivo main.py não encontrado em %CURRENT_DIR%
    echo.
    pause
    exit /b 1
)

echo ✅ Arquivo main.py encontrado
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ ERRO: Python não está instalado ou não está no PATH
    echo.
    echo Soluções:
    echo 1. Instale o Python de https://python.org
    echo 2. Adicione Python ao PATH durante a instalação
    echo 3. Reinicie o terminal após a instalação
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado
python --version
echo.

REM Verificar se as dependências estão instaladas
echo 📦 Verificando dependências...
cd /d "%CURRENT_DIR%"
pip install -r requirements.txt >nul 2>&1
if %errorLevel% neq 0 (
    echo ⚠️  AVISO: Erro ao instalar dependências
    echo Execute manualmente: pip install -r requirements.txt
    echo.
)

echo ✅ Dependências verificadas
echo.

REM Criar diretórios necessários
if not exist "output" mkdir output
if not exist "logs" mkdir logs
if not exist "data" mkdir data

echo ✅ Diretórios criados/verificados
echo.

REM Remover tarefa existente se houver
echo 🗑️  Removendo tarefa existente (se houver)...
schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1

REM Criar nova tarefa
echo 📅 Criando nova tarefa agendada...
schtasks /create /tn "%TASK_NAME%" /tr "python \"%CURRENT_DIR%coleta_agendada.py\"" /sc daily /st 12:00 /ru "SYSTEM" /f

if %errorLevel% equ 0 (
    echo ✅ Tarefa criada com sucesso!
    echo.
    echo 📋 Detalhes da tarefa:
    echo    Nome: %TASK_NAME%
    echo    Descrição: %TASK_DESCRIPTION%
    echo    Execução: Diariamente às 12:00
    echo    Script: %PYTHON_SCRIPT%
    echo.
    echo 🔧 Para modificar o agendamento:
    echo    1. Abra "Agendador de Tarefas" (taskschd.msc)
    echo    2. Procure por "%TASK_NAME%"
    echo    3. Clique com botão direito e selecione "Propriedades"
    echo.
    echo 🚀 Para executar manualmente:
    echo    schtasks /run /tn "%TASK_NAME%"
    echo.
    echo 📊 Para ver o status:
    echo    schtasks /query /tn "%TASK_NAME%"
    echo.
) else (
    echo ❌ ERRO: Falha ao criar a tarefa
    echo.
    echo 🔧 Soluções:
    echo 1. Verifique se o Windows Task Scheduler está funcionando
    echo 2. Execute o script como administrador
    echo 3. Verifique as permissões do usuário
    echo.
)

echo ========================================
echo  CONFIGURAÇÃO CONCLUÍDA
echo ========================================
echo.
echo 💡 Próximos passos:
echo 1. Teste o sistema: python main.py --test
echo 2. Execute manualmente: python main.py --scheduler
echo 3. Verifique os logs em: logs/
echo 4. Verifique os dados em: output/
echo.
pause
