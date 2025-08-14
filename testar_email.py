#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de Envio de Email - Sistema de Coleta de Notícias
=======================================================

Este script testa o envio de email com as configurações atuais.
Execute para verificar se o email está funcionando.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import sys

def testar_configuracao_email():
    """Testa a configuração de email"""
    print("🧪 TESTANDO CONFIGURAÇÃO DE EMAIL")
    print("=" * 50)
    
    try:
        # Importar configurações
        from config_email import EMAIL_CONFIG, EMAIL_RECIPIENTS
        
        print("✅ Configurações de email carregadas")
        print(f"📧 Servidor SMTP: {EMAIL_CONFIG['smtp_server']}:{EMAIL_CONFIG['smtp_port']}")
        print(f"👤 Usuário: {EMAIL_CONFIG['smtp_username']}")
        print(f"📨 Destinatários: {EMAIL_RECIPIENTS}")
        
        # Verificar se as configurações foram alteradas
        if 'seu_email@gmail.com' in EMAIL_CONFIG['smtp_username']:
            print("\n❌ ERRO: Configure seu email primeiro!")
            print("Edite o arquivo config_email.py e altere:")
            print("  - seu_email@gmail.com → seu email real")
            print("  - sua_senha_app → sua senha de aplicativo")
            return False
        
        if 'sua_senha_app' in EMAIL_CONFIG['smtp_password']:
            print("\n❌ ERRO: Configure sua senha primeiro!")
            print("Edite o arquivo config_email.py e altere:")
            print("  - sua_senha_app → sua senha de aplicativo do Gmail")
            return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro ao importar configurações: {e}")
        return False

def testar_conexao_smtp():
    """Testa a conexão com o servidor SMTP"""
    print("\n🔌 TESTANDO CONEXÃO SMTP")
    print("=" * 50)
    
    try:
        from config_email import EMAIL_CONFIG
        
        print(f"🔗 Conectando ao servidor {EMAIL_CONFIG['smtp_server']}...")
        
        # Criar conexão SMTP
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        
        print("✅ Conexão TLS estabelecida")
        
        # Fazer login
        print("🔐 Fazendo login...")
        server.login(EMAIL_CONFIG['smtp_username'], EMAIL_CONFIG['smtp_password'])
        
        print("✅ Login realizado com sucesso!")
        
        # Fechar conexão
        server.quit()
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão SMTP: {e}")
        return False

def enviar_email_teste():
    """Envia um email de teste"""
    print("\n📧 ENVIANDO EMAIL DE TESTE")
    print("=" * 50)
    
    try:
        from config_email import EMAIL_CONFIG, EMAIL_RECIPIENTS
        
        # Criar mensagem
        msg = MIMEMultipart()
        msg['From'] = f"{EMAIL_CONFIG['from_name']} <{EMAIL_CONFIG['smtp_username']}>"
        msg['To'] = ', '.join(EMAIL_RECIPIENTS)
        msg['Subject'] = '[TESTE] Sistema de Coleta de Notícias'
        
        # Corpo do email
        body = """
        <html>
        <body>
            <h2>🧪 Email de Teste - Sistema de Coleta de Notícias</h2>
            <p>Este é um email de teste para verificar se o sistema está funcionando.</p>
            <p><strong>✅ Se você recebeu este email, a configuração está funcionando!</strong></p>
            <hr>
            <p><em>Configurações atuais:</em></p>
            <ul>
                <li>Servidor SMTP: {smtp_server}</li>
                <li>Usuário: {username}</li>
                <li>Destinatários: {recipients}</li>
            </ul>
            <hr>
            <p>A partir de agora, você receberá um resumo diário de notícias sobre tecnologia e inovação!</p>
        </body>
        </html>
        """.format(
            smtp_server=EMAIL_CONFIG['smtp_server'],
            username=EMAIL_CONFIG['smtp_username'],
            recipients=', '.join(EMAIL_RECIPIENTS)
        )
        
        msg.attach(MIMEText(body, 'html'))
        
        # Enviar email
        print("📤 Enviando email de teste...")
        
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['smtp_username'], EMAIL_CONFIG['smtp_password'])
        
        text = msg.as_string()
        server.sendmail(EMAIL_CONFIG['smtp_username'], EMAIL_RECIPIENTS, text)
        server.quit()
        
        print("✅ Email de teste enviado com sucesso!")
        print(f"📨 Verifique a caixa de entrada de: {', '.join(EMAIL_RECIPIENTS)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 TESTE DE EMAIL - SISTEMA DE COLETA DE NOTÍCIAS")
    print("=" * 60)
    print("Este script testa se o envio de email está funcionando.\n")
    
    # Verificar configurações
    if not testar_configuracao_email():
        print("\n🔧 Para configurar o email:")
        print("1. Edite o arquivo config_email.py")
        print("2. Configure seu email e senha de aplicativo")
        print("3. Execute este script novamente")
        return
    
    # Testar conexão SMTP
    if not testar_conexao_smtp():
        print("\n🔧 Possíveis soluções:")
        print("1. Verifique se a senha de aplicativo está correta")
        print("2. Verifique se a verificação em duas etapas está ativa")
        print("3. Verifique se o email está correto")
        return
    
    # Enviar email de teste
    if enviar_email_teste():
        print("\n🎉 SUCESSO! O sistema de email está funcionando!")
        print("\n💡 Próximos passos:")
        print("1. O sistema agora enviará notícias por email 1 vez por dia")
        print("2. Execute 'python main.py --scheduler' para iniciar o agendador")
        print("3. Verifique seu email diariamente às 12:00")
    else:
        print("\n❌ Falha no envio do email de teste")
        print("Verifique as configurações e tente novamente")

if __name__ == "__main__":
    main()
