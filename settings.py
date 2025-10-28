"""
Configuración Centralizada Simple - AstroTech
============================================

Archivo de configuración principal para toda la aplicación.
Evita imports circulares y asegura consistencia.
"""

import os
from pathlib import Path

# Rutas del proyecto
PROJECT_ROOT = Path(__file__).parent
DATABASE_PATH = PROJECT_ROOT / "astrotech.db"

# Configuración de Base de Datos
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Configuración de Email
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "astrotechreprogramaciones@gmail.com"
RECIPIENT_EMAIL = "astrotechreprogramaciones@gmail.com"

# Intentar cargar contraseña desde .env
try:
    from dotenv import load_dotenv
    load_dotenv()
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")
except ImportError:
    SENDER_PASSWORD = ""

# Configuración de la aplicación
APP_CONFIG = {
    "name": "AstroTech Reprogramaciones",
    "version": "1.0.0",
    "debug": True,
    "contact_discount": 10,  # Descuento para usuarios registrados
    "max_form_submissions_per_hour": 10
}

# Logging
LOGGING_LEVEL = "INFO"
LOGGING_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

def is_email_configured():
    """Verificar si el email está configurado correctamente"""
    return bool(SENDER_PASSWORD and SENDER_EMAIL and RECIPIENT_EMAIL)

def get_database_info():
    """Obtener información de la base de datos"""
    return {
        "path": str(DATABASE_PATH),
        "url": DATABASE_URL,
        "exists": DATABASE_PATH.exists(),
        "size": DATABASE_PATH.stat().st_size if DATABASE_PATH.exists() else 0
    }

def print_startup_info():
    """Imprimir información de inicio"""
    print("=" * 50)
    print(f"🚗 {APP_CONFIG['name']} v{APP_CONFIG['version']}")
    print("=" * 50)
    print(f"📊 Base de Datos: {DATABASE_URL}")
    print(f"📧 Email: {'Configurado' if is_email_configured() else 'Modo Simulación'}")
    print(f"🔧 Debug: {'Activado' if APP_CONFIG['debug'] else 'Desactivado'}")
    print(f"💰 Descuento Contacto: {APP_CONFIG['contact_discount']}%")
    print("=" * 50)

if __name__ == "__main__":
    print_startup_info()