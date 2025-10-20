"""
Configuración de correo electrónico para AstroTech
=================================================

Configuración centralizada para el envío de correos desde el formulario de contacto.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Optional
import logging
from datetime import datetime

# Cargar variables de entorno
try:
    from dotenv import load_dotenv
    load_dotenv()  # Cargar archivo .env
except ImportError:
    pass  # python-dotenv no instalado, usar variables de entorno del sistema

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailConfig:
    """
    Configuración de correo electrónico centralizada.
    Lee la configuración desde variables de entorno (.env)
    """
    # Configuración SMTP desde .env
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    
    # Emails desde .env
    SENDER_EMAIL = os.getenv("SENDER_EMAIL", "astrotechreprogramaciones@gmail.com")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")
    RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "Astrotechreprogramaciones@gmail.com")

    @classmethod
    def get_smtp_config(cls) -> Dict[str, any]:
        """Obtener configuración SMTP."""
        return {
            "server": cls.SMTP_SERVER,
            "port": cls.SMTP_PORT,
            "sender_email": cls.SENDER_EMAIL,
            "sender_password": cls.SENDER_PASSWORD,
            "recipient_email": cls.RECIPIENT_EMAIL
        }
    
    @classmethod
    def is_configured(cls) -> bool:
        """Verificar si la configuración SMTP está completa."""
        return bool(cls.SENDER_EMAIL and cls.SENDER_PASSWORD and cls.RECIPIENT_EMAIL)


class EmailService:
    """
    Servicio de envío de correos electrónicos para AstroTech
    """
    
    def __init__(self):
        self.config = EmailConfig.get_smtp_config()
        
        # Log de configuración al inicializar
        if EmailConfig.is_configured():
            logger.info("[EMAIL] Configuración SMTP activada - emails se enviarán realmente")
            logger.info(f"[EMAIL] Servidor: {self.config['server']}:{self.config['port']}")
            logger.info(f"[EMAIL] Desde: {self.config['sender_email']}")
            logger.info(f"[EMAIL] Para: {self.config['recipient_email']}")
        else:
            logger.info("[EMAIL] MODO SIMULACIÓN - Falta configuración SMTP en .env")
            logger.info("[EMAIL] Ver GMAIL_SETUP_INSTRUCTIONS.md para configurar")
    
    async def send_contact_email(self, contact_data: Dict[str, str]) -> Dict[str, any]:
        """
        Enviar email de contacto desde el formulario
        
        Args:
            contact_data: Diccionario con name, email, phone, message
            
        Returns:
            Dict con success (bool) y message (str)
        """
        try:
            # Validar datos requeridos
            required_fields = ["name", "email", "message"]
            for field in required_fields:
                if not contact_data.get(field, "").strip():
                    return {
                        "success": False,
                        "message": f"Campo requerido faltante: {field}"
                    }
            
            # Crear el mensaje de email
            msg = MIMEMultipart()
            msg['From'] = self.config["sender_email"]
            msg['To'] = self.config["recipient_email"]
            msg['Subject'] = f"Nuevo contacto desde web - {contact_data['name']}"
            
            # Cuerpo del email en HTML
            body = self._create_email_body(contact_data)
            msg.attach(MIMEText(body, 'html'))
            
            # Enviar el email
            if not EmailConfig.is_configured():
                # Modo simulación - solo logging
                logger.info("[EMAIL] MODO SIMULACIÓN - Email no enviado (falta configuración SMTP)")
                logger.info("[EMAIL] Ver GMAIL_SETUP_INSTRUCTIONS.md para configurar el envío real")
                logger.info(f"[EMAIL] Para: {self.config['recipient_email']}")
                logger.info(f"[EMAIL] Asunto: {msg['Subject']}")
                logger.info(f"[EMAIL] Contenido:\n{body}")
                
                return {
                    "success": True,
                    "message": "Email simulado enviado correctamente (revisar logs)"
                }
            
            # Envío real
            with smtplib.SMTP(self.config["server"], self.config["port"]) as server:
                server.starttls()
                server.login(self.config["sender_email"], self.config["sender_password"])
                server.send_message(msg)
            
            logger.info(f"[EMAIL] Email enviado correctamente a {self.config['recipient_email']}")
            
            return {
                "success": True,
                "message": "Email enviado correctamente"
            }
            
        except Exception as e:
            logger.error(f"❌ Error enviando email: {str(e)}")
            return {
                "success": False,
                "message": f"Error al enviar email: {str(e)}"
            }
    
    def _create_email_body(self, contact_data: Dict[str, str]) -> str:
        """
        Crear el cuerpo del email en HTML
        """
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #FF6B35; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .field {{ margin-bottom: 15px; }}
                .label {{ font-weight: bold; color: #FF6B35; }}
                .value {{ margin-left: 10px; }}
                .footer {{ padding: 20px; text-align: center; font-size: 0.9em; color: #666; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚗 Nuevo Contacto - AstroTech</h1>
            </div>
            <div class="content">
                <p>Has recibido un nuevo mensaje de contacto desde la web:</p>
                
                <div class="field">
                    <span class="label">👤 Nombre:</span>
                    <span class="value">{contact_data['name']}</span>
                </div>
                
                <div class="field">
                    <span class="label">📧 Email:</span>
                    <span class="value">{contact_data['email']}</span>
                </div>
                
                <div class="field">
                    <span class="label">📱 Teléfono:</span>
                    <span class="value">{contact_data.get('phone', 'No proporcionado')}</span>
                </div>
                
                <div class="field">
                    <span class="label">💬 Mensaje:</span>
                    <div class="value" style="margin-top: 10px; padding: 15px; background-color: white; border-left: 4px solid #FF6B35;">
                        {contact_data['message'].replace('\n', '<br>')}
                    </div>
                </div>
            </div>
            <div class="footer">
                <p>📅 Recibido el: {timestamp}</p>
                <p>🌐 Enviado desde: www.astrotech.com</p>
            </div>
        </body>
        </html>
        """


# Instancia global del servicio
email_service = EmailService()


# Función de conveniencia para usar desde el estado
async def send_contact_form_email(name: str, email: str, phone: str, message: str) -> Dict[str, any]:
    """
    Función helper para enviar email desde el formulario de contacto
    
    Args:
        name: Nombre del contacto
        email: Email del contacto  
        phone: Teléfono del contacto (opcional)
        message: Mensaje del contacto
        
    Returns:
        Dict con success (bool) y message (str)
    """
    contact_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "message": message
    }
    
    return await email_service.send_contact_email(contact_data)
