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

# Importar configuración centralizada
from config import settings

# Configurar logging usando settings centralizado
logging.basicConfig(level=getattr(logging, settings.LOGGING_LEVEL), format=settings.LOGGING_FORMAT)
logger = logging.getLogger(__name__)

class EmailConfig:
    """
    Configuración de correo electrónico centralizada.
    Usa settings.py para consistencia perfecta.
    """
    # Configuración SMTP desde settings
    SMTP_SERVER = settings.SMTP_SERVER
    SMTP_PORT = settings.SMTP_PORT

    # Emails desde settings
    SENDER_EMAIL = settings.SENDER_EMAIL
    SENDER_PASSWORD = settings.SENDER_PASSWORD
    RECIPIENT_EMAIL = settings.RECIPIENT_EMAIL

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
            contact_data: Diccionario con name, email, phone, message, is_registered, user_info

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

            # Extraer información de registro del usuario
            is_registered = contact_data.get("is_registered", False)
            user_info = contact_data.get("user_info", {})
            
            # Crear el mensaje de email
            msg = MIMEMultipart()
            msg['From'] = self.config["sender_email"]
            msg['To'] = self.config["recipient_email"]

            # Asunto personalizado según estado de registro
            if is_registered:
                msg['Subject'] = f"🎯 USUARIO REGISTRADO - Nuevo contacto - {contact_data['name']} (DESCUENTO 10%)"
            else:
                msg['Subject'] = f"Nuevo contacto desde web - {contact_data['name']}"

            # Cuerpo del email en HTML con información de registro
            body = self._create_email_body(contact_data, is_registered, user_info)
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
    
    def _create_email_body(self, contact_data: Dict[str, str], is_registered: bool = False, user_info: dict = None) -> str:
        """
        Crear el cuerpo del email en HTML con información de registro del usuario

        Args:
            contact_data: Datos del contacto
            is_registered: Si el usuario está registrado en la base de datos
            user_info: Información del usuario si está registrado
        """
        if user_info is None:
            user_info = {}

        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Banner especial para usuarios registrados
        registration_banner = ""
        if is_registered:
            registration_banner = f"""
            <div style="background: linear-gradient(135deg, #28a745, #20c997); color: white; padding: 20px; text-align: center; margin-bottom: 0; border-radius: 10px 10px 0 0;">
                <h2 style="margin: 0; font-size: 1.5rem;">🎯 ¡USUARIO REGISTRADO DETECTADO!</h2>
                <p style="margin: 8px 0 0 0; font-size: 1.1rem; font-weight: bold;">APLICAR DESCUENTO DEL 10% ✅</p>
                <div style="margin-top: 12px; padding: 10px; background-color: rgba(255,255,255,0.2); border-radius: 5px; font-size: 0.9rem;">
                    <strong>Usuario verificado:</strong> {user_info.get('nombre', 'N/A')}<br>
                    <strong>Registrado el:</strong> {user_info.get('created_at', 'N/A')[:10] if user_info.get('created_at') else 'N/A'}<br>
                    <strong>Teléfono registro:</strong> {user_info.get('telefono', 'N/A')}
                </div>
            </div>
            """
        else:
            registration_banner = """
            <div style="background: linear-gradient(135deg, #6c757d, #495057); color: white; padding: 20px; text-align: center; margin-bottom: 0; border-radius: 10px 10px 0 0;">
                <h2 style="margin: 0; font-size: 1.5rem;">👋 Nuevo Cliente Potencial</h2>
                <p style="margin: 8px 0 0 0; font-size: 1.1rem;">Usuario no registrado en la base de datos</p>
                <div style="margin-top: 12px; padding: 10px; background-color: rgba(255,255,255,0.2); border-radius: 5px; font-size: 0.9rem;">
                    💡 <strong>Oportunidad:</strong> Ofrecer registro para descuento del 10%
                </div>
            </div>
            """

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: white;
                    border-radius: 10px;
                    overflow: hidden;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                }}
                .content {{
                    padding: 20px;
                    background-color: #f9f9f9;
                }}
                .field {{
                    margin-bottom: 20px;
                    padding: 15px;
                    background-color: white;
                    border-radius: 8px;
                    border-left: 4px solid #FF6B35;
                }}
                .label {{
                    font-weight: bold;
                    color: #FF6B35;
                    display: block;
                    margin-bottom: 5px;
                    font-size: 1.1rem;
                }}
                .value {{
                    font-size: 1rem;
                    color: #333;
                }}
                .message-content {{
                    margin-top: 10px;
                    padding: 20px;
                    background-color: white;
                    border-left: 4px solid #FF6B35;
                    border-radius: 8px;
                    font-size: 1.05rem;
                    line-height: 1.7;
                    background-color: #fff8f6;
                }}
                .footer {{
                    padding: 20px;
                    text-align: center;
                    font-size: 0.9em;
                    color: #666;
                    background-color: #f0f0f0;
                    border-top: 1px solid #ddd;
                }}
                .action-buttons {{
                    margin: 20px;
                    text-align: center;
                }}
                .action-button {{
                    display: inline-block;
                    padding: 12px 24px;
                    margin: 5px;
                    border-radius: 6px;
                    text-decoration: none;
                    font-weight: bold;
                    font-size: 1rem;
                }}
                .button-registered {{
                    background-color: #28a745;
                    color: white;
                }}
                .button-new {{
                    background-color: #007bff;
                    color: white;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                {registration_banner}

                <div class="content">
                    <h3 style="color: #FF6B35; margin-bottom: 20px; text-align: center;">📧 Detalles del Mensaje de Contacto</h3>

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
                        <div class="message-content">
                            {contact_data['message'].replace('\n', '<br>')}
                        </div>
                    </div>
                </div>

                {'''
                <div class="action-buttons">
                    <a href="#" class="action-button button-registered" style="background-color: #28a745; color: white;">
                        ✅ Aplicar Descuento 10%
                    </a>
                    <a href="#" class="action-button" style="background-color: #007bff; color: white;">
                        📞 Contactar Ahora
                    </a>
                </div>
                ''' if is_registered else '''
                <div class="action-buttons">
                    <a href="#" class="action-button button-new" style="background-color: #007bff; color: white;">
                        🎯 Ofrecer Registro para Descuento
                    </a>
                    <a href="#" class="action-button" style="background-color: #6c757d; color: white;">
                        📞 Contactar Ahora
                    </a>
                </div>
                '''}

                <div class="footer">
                    <p>📅 <strong>Recibido el:</strong> {timestamp}</p>
                    <p>🌐 <strong>Enviado desde:</strong> www.astrotech.com</p>
                    <p style="margin-top: 10px; font-size: 0.85rem; color: #999;">
                        Este email fue generado automáticamente por el sistema de contacto de AstroTech
                    </p>
                </div>
            </div>
        </body>
        </html>
        """


# Instancia global del servicio
email_service = EmailService()


# Función de conveniencia para usar desde el estado
async def send_contact_form_email(name: str, email: str, phone: str, message: str, is_registered: bool = False, user_info: dict = None) -> Dict[str, any]:
    """
    Función helper para enviar email desde el formulario de contacto

    Args:
        name: Nombre del contacto
        email: Email del contacto
        phone: Teléfono del contacto (opcional)
        message: Mensaje del contacto
        is_registered: Si el usuario está registrado en la base de datos
        user_info: Información adicional del usuario si está registrado

    Returns:
        Dict con success (bool) y message (str)
    """
    if user_info is None:
        user_info = {}

    contact_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "message": message,
        "is_registered": is_registered,
        "user_info": user_info
    }

    return await email_service.send_contact_email(contact_data)
