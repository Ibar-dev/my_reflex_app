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
    """Configuración de correo electrónico"""
    
    # Configuración SMTP - Gmail por defecto (puedes cambiar por otro proveedor)
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    
    # Email del destinatario (dueño de la página)
    RECIPIENT_EMAIL = "Astrotechreprogramaciones@gmail.com"  # Cambiar por tu email real
    
    # Configuración desde variables de entorno (más seguro)
    SENDER_EMAIL = os.getenv("SENDER_EMAIL", "noreply@astrotech.com")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")  # App password de Gmail
    
    @classmethod
    def get_smtp_config(cls) -> Dict[str, any]:
        """Obtener configuración SMTP"""
        return {
            "server": cls.SMTP_SERVER,
            "port": cls.SMTP_PORT,
            "sender_email": cls.SENDER_EMAIL,
            "sender_password": cls.SENDER_PASSWORD,
            "recipient_email": cls.RECIPIENT_EMAIL
        }

class EmailSender:
    """Clase para envío de correos electrónicos"""
    
    def __init__(self):
        self.config = EmailConfig.get_smtp_config()
    
    def create_contact_email(self, name: str, email: str, phone: str, message: str) -> MIMEMultipart:
        """
        Crear el email de contacto con formato HTML
        
        Args:
            name: Nombre del contacto
            email: Email del contacto
            phone: Teléfono del contacto
            message: Mensaje del contacto
            
        Returns:
            MIMEMultipart: Email formateado
        """
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Nuevo contacto desde AstroTech - {name}"
        msg["From"] = self.config["sender_email"]
        msg["To"] = self.config["recipient_email"]
        
        # Crear contenido HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #FF6B35; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .field {{ margin-bottom: 15px; }}
                .label {{ font-weight: bold; color: #FF6B35; }}
                .value {{ margin-left: 10px; }}
                .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚗 AstroTech - Nuevo Contacto</h1>
                </div>
                <div class="content">
                    <p>Has recibido un nuevo mensaje de contacto desde tu página web:</p>
                    
                    <div class="field">
                        <span class="label">👤 Nombre:</span>
                        <span class="value">{name}</span>
                    </div>
                    
                    <div class="field">
                        <span class="label">📧 Email:</span>
                        <span class="value">{email}</span>
                    </div>
                    
                    <div class="field">
                        <span class="label">📱 Teléfono:</span>
                        <span class="value">{phone if phone else "No proporcionado"}</span>
                    </div>
                    
                    <div class="field">
                        <span class="label">💬 Mensaje:</span>
                        <div style="background: white; padding: 15px; border-left: 4px solid #FF6B35; margin-top: 10px;">
                            {message.replace('\n', '<br>')}
                        </div>
                    </div>
                </div>
                <div class="footer">
                    <p>Este mensaje fue enviado desde el formulario de contacto de AstroTech</p>
                    <p>Fecha: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Crear versión texto plano
        text_content = f"""
        Nuevo contacto desde AstroTech
        
        Nombre: {name}
        Email: {email}
        Teléfono: {phone if phone else "No proporcionado"}
        
        Mensaje:
        {message}
        
        ---
        Enviado desde el formulario de contacto de AstroTech
        """
        
        # Adjuntar ambas versiones
        text_part = MIMEText(text_content, "plain", "utf-8")
        html_part = MIMEText(html_content, "html", "utf-8")
        
        msg.attach(text_part)
        msg.attach(html_part)
        
        return msg
    
    def send_email(self, name: str, email: str, phone: str, message: str) -> bool:
        """
        Enviar email de contacto
        
        Args:
            name: Nombre del contacto
            email: Email del contacto  
            phone: Teléfono del contacto
            message: Mensaje del contacto
            
        Returns:
            bool: True si se envió correctamente, False en caso contrario
        """
        try:
            # Validar configuración
            if not self.config["sender_password"]:
                logger.warning("No se ha configurado la contraseña del email")
                return False
            
            # Crear el mensaje
            msg = self.create_contact_email(name, email, phone, message)
            
            # Configurar servidor SMTP
            with smtplib.SMTP(self.config["server"], self.config["port"]) as server:
                server.starttls()  # Habilitar encriptación
                server.login(self.config["sender_email"], self.config["sender_password"])
                
                # Enviar email
                text = msg.as_string()
                server.sendmail(
                    self.config["sender_email"],
                    self.config["recipient_email"],
                    text
                )
            
            logger.info(f"Email enviado correctamente desde {email}")
            return True
            
        except Exception as e:
            logger.error(f"Error al enviar email: {str(e)}")
            return False

# Instancia global para usar en el estado
email_sender = EmailSender()