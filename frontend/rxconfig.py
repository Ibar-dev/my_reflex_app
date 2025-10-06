import reflex as rx
import os

IS_RENDER = os.getenv("RENDER") is not None
PORT = int(os.getenv("PORT", 8000))

config = rx.Config(
    app_name="app",
    db_url="sqlite:///reflex.db",
    frontend_port=PORT if IS_RENDER else 3000,
    backend_port=PORT if IS_RENDER else 8000,
    backend_host="0.0.0.0" if IS_RENDER else "localhost",
    api_url=os.getenv("RENDER_EXTERNAL_URL") if IS_RENDER else None,
    deploy_url=os.getenv("RENDER_EXTERNAL_URL") if IS_RENDER else None,
    env=rx.Env.PROD if IS_RENDER else rx.Env.DEV,
    backend_only=False,
    timeout=120,
)
