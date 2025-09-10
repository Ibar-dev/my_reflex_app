"""
Aplicación básica de AstroTech - Reflex
======================================

Aplicación básica para probar que Reflex funciona correctamente.
"""

import reflex as rx

def index() -> rx.Component:
    """Página principal básica"""
    return rx.vstack(
        rx.heading("AstroTech", size="8"),
        rx.text("Bienvenido a AstroTech - Reprogramación ECU"),
        spacing="4",
    )

# Crear la aplicación
app = rx.App()
app.add_page(index, route="/", title="AstroTech")