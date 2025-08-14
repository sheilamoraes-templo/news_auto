# 📧 CONFIGURAR EMAIL - Guia Rápido

## 🎯 **O QUE FOI ALTERADO**

✅ **Coleta**: Mudou de 4x por dia para **1x por dia**  
✅ **Armazenamento**: Não salva mais no computador  
✅ **Envio**: Envia notícias por email automaticamente  

## 🚀 **PASSO A PASSO PARA CONFIGURAR EMAIL**

### **1️⃣ Editar Configuração**

Abra o arquivo `config_email.py` e altere:

```python
'smtp_username': 'seu_email@gmail.com',  # ⚠️ ALTERE AQUI
'smtp_password': 'sua_senha_app',       # ⚠️ ALTERE AQUI
```

E também:

```python
EMAIL_RECIPIENTS = [
    'seu_email@gmail.com',  # ⚠️ ALTERE AQUI
]
```

### **2️⃣ Obter Senha de Aplicativo do Gmail**

1. Acesse: https://myaccount.google.com/
2. Vá em **"Segurança"**
3. Ative **"Verificação em duas etapas"** (se não estiver ativa)
4. Vá em **"Senhas de app"**
5. Gere uma nova senha para **"Email"**
6. **Copie a senha** (exemplo: `abcd efgh ijkl mnop`)

### **3️⃣ Testar Configuração**

```cmd
python testar_email.py
```

Se funcionar, você receberá um email de teste!

### **4️⃣ Iniciar Sistema**

```cmd
python main.py --scheduler
```

## 📅 **AGORA O SISTEMA FUNCIONA ASSIM:**

- **⏰ Coleta**: 1 vez por dia às 12:00
- **📧 Envio**: Email automático com resumo das notícias
- **💾 Armazenamento**: Nada salvo no computador
- **🔄 Automático**: Funciona sozinho, sem intervenção

## 🔧 **EXEMPLO DE CONFIGURAÇÃO COMPLETA**

```python
# Seu email real
'smtp_username': 'joao.silva@gmail.com',

# Sua senha de aplicativo (16 caracteres)
'smtp_password': 'abcd efgh ijkl mnop',

# Destinatários
EMAIL_RECIPIENTS = [
    'joao.silva@gmail.com',
    'maria.santos@empresa.com',  # Opcional: enviar para outro email
]
```

## ⚠️ **IMPORTANTE**

- ✅ **Use sempre senha de aplicativo** (nunca senha principal)
- ✅ **Verificação em duas etapas deve estar ativa**
- ✅ **Teste sempre antes de usar em produção**

## 🎉 **RESULTADO FINAL**

Após configurar, você receberá **diariamente às 12:00** um email com:

- 📰 **Resumo das principais notícias** de tecnologia
- 🔗 **Links para ler as notícias completas**
- 📊 **Estatísticas** da coleta
- 🎨 **Formato HTML** bonito e organizado

## 🆘 **PROBLEMAS COMUNS**

### **Erro: "Authentication failed"**
- Verifique se a senha de aplicativo está correta
- Verifique se a verificação em duas etapas está ativa

### **Erro: "SMTP connection failed"**
- Verifique se o email está correto
- Verifique se o Gmail está acessível

### **Email não chega**
- Verifique a pasta de spam
- Verifique se o email está correto

---

**🎯 Configure o email e teste! O sistema ficará ainda mais prático!**
