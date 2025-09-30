#!/usr/bin/env python3
"""
Script de verificación del formulario de contacto
===============================================

Verifica que el componente de contacto se renderice correctamente.
"""

import reflex as rx
from components.contact import contact
from state.contact_state import ContactState

def test_page() -> rx.Component:
    """Página de prueba del formulario de contacto"""
    return rx.box(
        rx.heading("Prueba del Formulario de Contacto", size="6", color="white", mb="8"),
        contact(),
        bg="#121212",
        min_height="100vh",
        p="4"
    )

# Configuración de la app de prueba
app = rx.App(
    style={
        "font_family": "Inter",
        "background_color": "#121212"
    }
)

app.add_page(test_page, route="/")

if __name__ == "__main__":
    print("🧪 Iniciando prueba del formulario de contacto...")
    print("📝 Componente de contacto cargado correctamente")
    print("🎯 Estado ContactState importado correctamente")
    print("✅ Todo listo para ejecutar: reflex run")