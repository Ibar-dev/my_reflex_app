import reflex as rx
import os

config = rx.Config(
    app_name="app",
    db_url="sqlite:///reflex.db",
    
    # Configuración simple para desarrollo local
    frontend_port=3000,
    backend_port=8000,
    backend_host="127.0.0.1",  # Usar IP directamente en lugar de localhost
    
    # Desarrollo local
    env=rx.Env.DEV,
    
    # Opciones básicas
    backend_only=False,
    timeout=120,
    
    # Deshabilitar plugin problemático
    disable_plugins=['reflex.plugins.sitemap.SitemapPlugin']
)
