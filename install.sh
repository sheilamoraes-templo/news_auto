#!/bin/bash

echo "========================================"
echo " Sistema de Coleta de Noticias"
echo " Instalacao e Configuracao"
echo "========================================"
echo

echo "[1/4] Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "ERRO: Python3 nao encontrado!"
    echo "Instale Python 3.8+ com: sudo apt install python3 python3-pip"
    exit 1
fi
echo "Python encontrado!"

echo
echo "[2/4] Instalando dependencias..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERRO: Falha na instalacao das dependencias"
    exit 1
fi
echo "Dependencias instaladas com sucesso!"

echo
echo "[3/4] Criando diretorios..."
mkdir -p output logs
echo "Diretorios criados!"

echo
echo "[4/4] Testando sistema..."
python3 main.py --status
if [ $? -ne 0 ]; then
    echo "ERRO: Falha no teste do sistema"
    exit 1
fi

echo
echo "========================================"
echo " Instalacao concluida com sucesso!"
echo "========================================"
echo
echo "Para testar o sistema:"
echo "  python3 main.py --test"
echo
echo "Para ver ajuda:"
echo "  python3 main.py --help"
echo
