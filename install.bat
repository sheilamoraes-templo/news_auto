@echo off
echo ========================================
echo  Sistema de Coleta de Noticias
echo  Instalacao e Configuracao
echo ========================================
echo.

echo [1/4] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.8+ de https://python.org
    pause
    exit /b 1
)
echo Python encontrado!

echo.
echo [2/4] Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERRO: Falha na instalacao das dependencias
    pause
    exit /b 1
)
echo Dependencias instaladas com sucesso!

echo.
echo [3/4] Criando diretorios...
if not exist "output" mkdir output
if not exist "logs" mkdir logs
echo Diretorios criados!

echo.
echo [4/4] Testando sistema...
python main.py --status
if errorlevel 1 (
    echo ERRO: Falha no teste do sistema
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Instalacao concluida com sucesso!
echo ========================================
echo.
echo Para testar o sistema:
echo   python main.py --test
echo.
echo Para ver ajuda:
echo   python main.py --help
echo.
pause
