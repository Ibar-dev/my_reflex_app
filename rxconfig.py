import reflex as rx
import os

# Obtener configuración desde variables de entorno
env = os.getenv("RX_ENV", rx.Env.DEV)

# Configuración de base de datos según entorno
if env == rx.Env.PROD:
    # En producción no usamos base de datos SQL local, solo Supabase
    db_url = None
else:
    # En desarrollo mantener compatibilidad (aunque ya no se usa)
    db_url = "sqlite:///data/astrotech.db"

config = rx.Config(
    app_name="app",
    db_url=db_url,

    # Configuración de puertos
    frontend_port=3000,
    backend_port=8000,
    backend_host="127.0.0.1",

    # Entorno (automático en producción)
    env=env,

    # Opciones básicas
    backend_only=False,
    timeout=120,

    # Deshabilitar plugin problemático
    disable_plugins=['reflex.plugins.sitemap.SitemapPlugin']
)
