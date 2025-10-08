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
    Cambia los valores aquí o usa variables de entorno para mayor seguridad.
    """
    # Configuración SMTP - Gmail por defecto (puedes cambiar por otro proveedor)
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    # Email del destinatario (dueño de la página)
    RECIPIENT_EMAIL = "Astrotechreprogramaciones@gmail.com"  # Cambia por tu email real
    # Configuración desde variables de entorno (más seguro)
    SENDER_EMAIL = os.getenv("SENDER_EMAIL", "noreply@astrotech.com")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")  # App password de Gmail

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
