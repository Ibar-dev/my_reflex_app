# """
# Configuración de AstroTech - Reflex
# ==================================
# Archivo de configuración para la aplicación AstroTech desarrollada con Reflex.
# """

# import reflex as rx

# config = rx.Config(
#     app_name="app",
#     db_url="sqlite:///reflex.db",
    
#     # Puertos
#     frontend_port=3000,
#     backend_port=8000,
    
#     # URLs
#     api_url="http://localhost:8000",
#     deploy_url="http://localhost:3000",
    
#     # Entorno
#     env=rx.Env.DEV,
    
#     # Desactivar el plugin de sitemap para eliminar warnings
#     # (puedes activarlo más tarde si necesitas generar un sitemap)
#     disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
    
#     # Configuración de compilación
#     backend_only=False,
    
#     # Timeout para el backend
#     timeout=120,
# )

import reflex as rx
import os

config = rx.Config(
    app_name="app",
    db_url="sqlite:///reflex.db",
    
    # Usar variables de entorno en producción
    frontend_port=int(os.getenv("PORT", 3000)),
    backend_port=int(os.getenv("PORT", 8000)),
    
    # Detectar entorno automáticamente
    env=rx.Env.PROD if os.getenv("RENDER") else rx.Env.DEV,
    
    # Configuración de producción
    api_url=os.getenv("RENDER_EXTERNAL_URL", "http://localhost:8000"),
    
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
    backend_only=False,
    timeout=120,
)