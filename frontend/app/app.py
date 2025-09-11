"""
Aplicación básica de AstroTech - Reflex
======================================

Aplicación básica para probar que Reflex funciona correctamente.
"""

import reflex as rx
from components.header import header
from components.hero import hero

def index() -> rx.Component:
    """Página principal básica"""
    return rx.box(
        header(active="home"),
        hero(),
        bg="#1A1A1A",
        min_height="100vh",
    )


# Páginas de marcador de posición para la navegación
def services() -> rx.Component:
    return rx.box(
        header(active="services"),
        rx.container(
            rx.vstack(
                rx.heading("Servicios", size="7", color="#FF6B35"),
                rx.text("Página en construcción.", color="white"),
                spacing="4",
                py="8",
            )
        ),
        bg="#1A1A1A",
        min_height="100vh",
    )


def about() -> rx.Component:
    return rx.box(
        header(active="about"),
        rx.container(
            rx.vstack(
                rx.heading("Acerca de", size="7", color="#FF6B35"),
                rx.text("Página en construcción.", color="white"),
                spacing="4",
                py="8",
            )
        ),
        bg="#1A1A1A",
        min_height="100vh",
    )


def contact() -> rx.Component:
    return rx.box(
        header(active="contact"),
        rx.container(
            rx.vstack(
                rx.heading("Contacto", size="7", color="#FF6B35"),
                rx.text("Página en construcción.", color="white"),
                spacing="4",
                py="8",
            )
        ),
        bg="#1A1A1A",
        min_height="100vh",
    )

# Crear la aplicación
# Nota: Los estilos en la carpeta `assets/` se referencian como "/styles.css"
# para evitar que Reflex resuelva la ruta como "assets/assets/styles.css".
app = rx.App(stylesheets=["/styles.css"])
app.add_page(index, route="/", title="AstroTech")
app.add_page(services, route="/services", title="Servicios - AstroTech")
app.add_page(about, route="/about", title="Acerca de - AstroTech")
app.add_page(contact, route="/contact", title="Contacto - AstroTech")