# 🎯 CONTROLE DO SISTEMA DE COLETA AUTOMÁTICA DE NOTÍCIAS

## 🚀 **COMO USAR O SISTEMA**

### **1️⃣ INICIAR O SISTEMA**
```cmd
# Opção 1: Rodar em segundo plano (temporário)
python main.py --scheduler

# Opção 2: Configurar agendamento automático (RECOMENDADO)
agendar_windows.bat
```

### **2️⃣ TESTAR O SISTEMA**
```cmd
# Teste completo (coleta + email)
python main.py --test

# Teste apenas do email
python testar_email.py

# Teste da coleta agendada
python coleta_agendada.py

# Verificar status
python main.py --status
```

### **3️⃣ PARAR O SISTEMA**
```cmd
# Se estiver rodando com --scheduler
Ctrl+C (no terminal)

# Se estiver com agendamento do Windows
schtasks /delete /tn "Coleta_Automatica_Noticias" /f

# Ou usar o script de parada
python main.py --stop
```

## 📁 **ESTRUTURA LIMPA DO PROJETO**

### **📄 ARQUIVOS PRINCIPAIS (NÃO DELETAR)**
- `main.py` - Sistema principal
- `config.py` - Configurações básicas
- `config_email.py` - Configurações de email
- `news_collector.py` - Coleta de notícias
- `data_processor.py` - Processamento de dados
- `scheduler.py` - Agendamento
- `coleta_agendada.py` - Script para execução agendada
- `requirements.txt` - Dependências

### **🧪 ARQUIVOS DE TESTE (NÃO DELETAR)**
- `testar_email.py` - Teste de email
- `test_quick.py` - Teste rápido do sistema
- `verificar_instalacao.py` - Verificação de instalação

### **📚 DOCUMENTAÇÃO (NÃO DELETAR)**
- `README.md` - Documentação principal
- `CONFIGURAR_EMAIL.md` - Guia de email
- `INSTRUCOES_FINAIS.md` - Instruções completas
- `CONTROLE_SISTEMA.md` - Este arquivo

### **⚙️ SCRIPTS DE INSTALAÇÃO (NÃO DELETAR)**
- `install.bat` - Instalação Windows
- `install.sh` - Instalação Linux/macOS
- `agendar_windows.bat` - Agendamento Windows (12:00)
- `agendar_linux.sh` - Agendamento Linux/macOS

### **🔒 CONTROLE DE VERSÃO (NÃO DELETAR)**
- `.gitignore` - Arquivos ignorados pelo Git

## 🎯 **VERSÃO FINAL LIMPA**

### **ARQUIVOS ESSENCIAIS (MANTENHA):**
```
news_auto/
├── 📄 Sistema Principal
│   ├── main.py
│   ├── config.py
│   ├── config_email.py
│   ├── news_collector.py
│   ├── data_processor.py
│   ├── scheduler.py
│   └── coleta_agendada.py
│
├── 🧪 Testes
│   ├── testar_email.py
│   ├── test_quick.py
│   └── verificar_instalacao.py
│
├── 📚 Documentação
│   ├── README.md
│   ├── CONFIGURAR_EMAIL.md
│   ├── INSTRUCOES_FINAIS.md
│   └── CONTROLE_SISTEMA.md
│
├── ⚙️ Instalação
│   ├── requirements.txt
│   ├── install.bat
│   ├── install.sh
│   ├── agendar_windows.bat
│   └── agendar_linux.sh
│
└── 🔒 Controle
    └── .gitignore
```

## 🚀 **COMO FUNCIONA AGORA**

### **✅ CONFIGURAÇÃO ATUAL:**
- **Coleta**: 1 vez por dia às 12:00 (meio-dia)
- **Email**: Envio automático após coleta
- **Armazenamento**: Nada salvo no computador (apenas logs)
- **Agendamento**: Windows Task Scheduler às 12:00

### **📧 EMAIL CONFIGURADO:**
- **De**: Sistema de Coleta de Notícias
- **Para**: sheila.moraes@templo.cc
- **Assunto**: [News Auto] Resumo Diário de Tecnologia
- **Formato**: HTML bonito e organizado

## 🔍 **TROUBLESHOOTING**

### **Problema: Não recebeu email de teste**
1. Verifique se `config_email.py` está configurado
2. Execute: `python testar_email.py`
3. Verifique pasta de spam

### **Problema: Sistema não coleta**
1. Verifique se agendamento está ativo
2. Execute: `python main.py --test`
3. Verifique logs em `logs/`

### **Problema: Erro de autenticação**
1. Verifique senha de aplicativo
2. Verifique verificação em duas etapas
3. Teste conexão: `python testar_email.py`

### **Problema: Agendamento não funciona**
1. Execute `agendar_windows.bat` como administrador
2. Verifique: `schtasks /query /tn "Coleta_Automatica_Noticias"`
3. Confirme horário: 12:00 (meio-dia)

## 🎉 **SISTEMA PRONTO!**

**O sistema está configurado e funcionando!**
- ✅ Email configurado e testado
- ✅ Coleta automática configurada para 12:00
- ✅ Agendamento do Windows configurado
- ✅ Documentação completa
- ✅ Scripts de teste funcionando

**🎯 Use os comandos acima para controlar o sistema!** 🚀

## 📅 **HORÁRIO DE EXECUÇÃO**

**🕛 DIARIAMENTE ÀS 12:00 (MEIO-DIA)**
- ✅ Horário ideal (computador sempre ligado)
- ✅ Internet estável (horário comercial)
- ✅ Fácil de monitorar
- ✅ Execução automática via Windows Task Scheduler
