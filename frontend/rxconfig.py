"""
Configuración de AstroTech - Reflex
==================================

Archivo de configuración para la aplicación AstroTech desarrollada con Reflex.
"""

import reflex as rx

config = rx.Config(
    app_name="app",
    db_url="sqlite:///reflex.db",
    frontend_port=3000,
    backend_port=8000,
    # Configuración adicional
    api_url="http://localhost:8000",
    deploy_url="http://localhost:3000",
    # Configuración de desarrollo
    env=rx.Env.DEV,
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
)
