"""
Configuración Centralizada - AstroTech
=====================================

Archivo principal de configuración para toda la aplicación.
Asegura consistencia y sinergia entre todos los componentes.
"""

# Importar gestor de base de datos
from utils.database_manager import db_manager

# Configuración de Base de Datos
DATABASE_CONFIG = {
    "url": f"sqlite:///astrotech.db",
    "path": db_manager.engine.url.database if hasattr(db_manager.engine.url, 'database') else "astrotech.db",
    "echo": False,  # Set to True for SQL debugging
    "pool_pre_ping": True,
    "pool_recycle": 3600
}

# Configuración de Email
try:
    from utils.email_service import EmailConfig
    EMAIL_CONFIG = EmailConfig.get_smtp_config()
    EMAIL_CONFIG["configured"] = EmailConfig.is_configured()
except Exception:
    EMAIL_CONFIG = {
        "configured": False,
        "server": "smtp.gmail.com",
        "port": 587,
        "sender_email": "",
        "sender_password": "",
        "recipient_email": ""
    }

# Configuración de la Aplicación
APP_CONFIG = {
    "name": "AstroTech Reprogramaciones",
    "version": "1.0.0",
    "debug": True,
    "timezone": "Europe/Madrid",
    "contact_form": {
        "max_message_length": 1000,
        "required_fields": ["name", "email", "message"],
        "optional_fields": ["phone"]
    },
    "user_registration": {
        "discount_percentage": 10,
        "min_phone_length": 9,
        "source_options": ["discount_popup", "contact_form", "manual"]
    }
}

# Configuración de Logging
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    "date_format": "%Y-%m-%d %H:%M:%S",
    "file": "astrotech.log" if not APP_CONFIG["debug"] else None
}

# Configuración de Caché
CACHE_CONFIG = {
    "vehicle_data": {
        "enabled": True,
        "expire_days": 30,
        "auto_update": True
    },
    "user_lookup": {
        "enabled": True,
        "cache_minutes": 30
    }
}

# Configuración de Seguridad
SECURITY_CONFIG = {
    "email_validation": True,
    "phone_validation": True,
    "max_form_submissions_per_hour": 10,
    "enable_rate_limiting": True
}

def get_full_config() -> dict:
    """Obtener configuración completa de la aplicación"""
    return {
        "database": DATABASE_CONFIG,
        "email": EMAIL_CONFIG,
        "app": APP_CONFIG,
        "logging": LOGGING_CONFIG,
        "cache": CACHE_CONFIG,
        "security": SECURITY_CONFIG
    }

def is_production_ready() -> bool:
    """Verificar si la configuración está lista para producción"""
    checks = [
        DATABASE_CONFIG.get("url") is not None,
        EMAIL_CONFIG.get("configured", False),
        not APP_CONFIG.get("debug", True),
        len(SECURITY_CONFIG) > 0
    ]
    return all(checks)

def print_config_summary():
    """Imprimir resumen de configuración"""
    config = get_full_config()

    print("=== RESUMEN DE CONFIGURACIÓN ASTROTECH ===")
    print(f"📊 Base de Datos: {config['database']['url']}")
    print(f"📧 Email: {'Configurado' if config['email']['configured'] else 'Modo Simulación'}")
    print(f"🔧 Debug: {'Activado' if config['app']['debug'] else 'Desactivado'}")
    print(f"🚗 Caché Vehículos: {'Activado' if config['cache']['vehicle_data']['enabled'] else 'Desactivado'}")
    print(f"🛡️ Modo Producción: {'Listo' if is_production_ready() else 'En Desarrollo'}")
    print("=" * 45)

# Verificación al importar
if __name__ == "__main__":
    print_config_summary()