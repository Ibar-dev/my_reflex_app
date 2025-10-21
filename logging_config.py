"""
Configuración de logging centralizado para toda la app Reflex
============================================================

Este archivo configura el logging para backend y puede ser importado en cualquier módulo.
"""
import logging
import sys

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
LOG_LEVEL = "INFO"
LOG_FILE = "app.log"

logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

def get_logger(name: str = None):
    """Devuelve un logger configurado con el formato global."""
    return logging.getLogger(name)
