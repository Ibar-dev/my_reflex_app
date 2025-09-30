#!/usr/bin/env python3
"""
Script de prueba para el sistema de envío de emails
==================================================

Prueba el servicio de email sin necesidad de ejecutar toda la aplicación.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.email_service import email_sender, EmailConfig

def test_email_configuration():
    """Prueba la configuración de email"""
    print("🧪 Probando configuración de email...")
    print("=" * 50)
    
    config = EmailConfig.get_smtp_config()
    
    print(f"📧 Email remitente: {config['sender_email']}")
    print(f"📨 Email destinatario: {config['recipient_email']}")
    print(f"🌐 Servidor SMTP: {config['server']}:{config['port']}")
    
    if config['sender_password']:
        print("✅ Contraseña configurada")
    else:
        print("❌ Contraseña NO configurada")
        print("⚠️  Configura SENDER_PASSWORD en el archivo .env")
        return False
    
    return True

def test_email_sending():
    """Prueba el envío de un email de prueba"""
    print("\n📬 Enviando email de prueba...")
    print("=" * 50)
    
    try:
        success = email_sender.send_email(
            name="Usuario de Prueba",
            email="test@ejemplo.com", 
            phone="+34 612 345 678",
            message="Este es un mensaje de prueba del formulario de contacto de AstroTech.\n\n¡El sistema está funcionando correctamente! 🎉"
        )
        
        if success:
            print("✅ Email enviado correctamente!")
            print("📧 Revisa tu bandeja de entrada")
            return True
        else:
            print("❌ Error al enviar el email")
            print("💡 Revisa la configuración y credenciales")
            return False
            
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False

def main():
    """Función principal de prueba"""
    print("🚀 Iniciando pruebas del sistema de email AstroTech")
    print("=" * 60)
    
    # Verificar que existe el archivo .env
    if not os.path.exists('.env'):
        print("⚠️  No se encontró el archivo .env")
        print("📋 Crea el archivo .env basado en .env.example")
        print("💡 Instrucciones completas en EMAIL_SETUP.md")
        return False
    
    # Probar configuración
    if not test_email_configuration():
        return False
    
    # Preguntar si enviar email de prueba
    print("\n❓ ¿Deseas enviar un email de prueba? (y/n): ", end="")
    respuesta = input().lower().strip()
    
    if respuesta in ['y', 'yes', 'sí', 's']:
        success = test_email_sending()
        
        if success:
            print("\n🎉 ¡Prueba completada exitosamente!")
            print("🚀 El formulario de contacto está listo para usar")
        else:
            print("\n❌ Hay problemas con el envío de emails")
            print("📖 Revisa EMAIL_SETUP.md para más información")
        
        return success
    else:
        print("\n✅ Configuración verificada (email no enviado)")
        return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)