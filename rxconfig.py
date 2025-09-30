"""
Configuración de AstroTech - Reflex
==================================
Archivo de configuración para la aplicación AstroTech desarrollada con Reflex.
"""

import reflex as rx

config = rx.Config(
    app_name="app",
    db_url="sqlite:///reflex.db",
    
    # Puertos
    frontend_port=3000,
    backend_port=8000,
    
    # URLs
    api_url="http://localhost:8000",
    deploy_url="http://localhost:3000",
    
    # Entorno
    env=rx.Env.DEV,
    
    # Desactivar el plugin de sitemap para eliminar warnings
    # (puedes activarlo más tarde si necesitas generar un sitemap)
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
    
    # Configuración de compilación
    backend_only=False,
    
    # Timeout para el backend
    timeout=120,
)