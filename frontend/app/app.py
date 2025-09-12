"""
Aplicación ReproTuning - Reflex
===============================

Aplicación completa de reprogramación ECU con componentes modernos y animaciones.
"""

import reflex as rx
from components.header import header
from components.hero import hero
from components.vehicle_selector import vehicle_selector
from components.benefits import benefits
from components.services import services
from components.faq import faq
from components.contact import contact
from components.footer import footer

def index() -> rx.Component:
    """Página principal completa con todos los componentes"""
    return rx.box(
        header(active="home"),
        hero(),
        vehicle_selector(),
        benefits(),
        services(),
        rx.box(
            rx.container(
                rx.vstack(
                    rx.heading(
                        "¿Qué es la reprogramación ECU?",
                        size="8",
                        color="white",
                        text_align="center",
                        mb="8"
                    ),
                    rx.grid(
                        rx.vstack(
                            rx.text(
                                "La reprogramación ECU (Unidad de Control del Motor) es un proceso técnico que consiste en modificar el software que controla el funcionamiento del motor de tu vehículo. Esta optimización permite:",
                                color="white",
                                mb="6",
                                line_height="1.6"
                            ),
                            rx.vstack(
                                rx.text("• Aumentar la potencia del motor", color="#666666"),
                                rx.text("• Reducir el consumo de combustible", color="#666666"),
                                rx.text("• Mejorar la respuesta del acelerador", color="#666666"),
                                rx.text("• Optimizar el par motor", color="#666666"),
                                spacing="2",
                                align="start",
                                mb="6"
                            ),
                            rx.text(
                                "Nuestro equipo de técnicos especializados utiliza equipos de última generación para garantizar resultados óptimos y seguros para tu vehículo.",
                                color="white",
                                line_height="1.6"
                            ),
                            spacing="4",
                            align="start"
                        ),
                        rx.box(
                            height={"base": "280px", "md": "340px", "lg": "400px"},
                            bg="#2D2D2D",
                            border_radius="20px",
                            box_shadow="0 20px 40px rgba(0, 0, 0, 0.2)",
                            border="1px solid #666666"
                        ),
                        columns={"base": "1", "lg": "2"},
                        spacing="9",
                        align="center"
                    ),
                    spacing="8",
                    align="center"
                ),
                max_width="1200px",
                px="6",
                py="20"
            ),
            bg="#1A1A1A",
            id="acerca"
        ),
        faq(),
        contact(),
        footer(),
        bg="#1A1A1A",
        min_height="100vh",
    )


def services_page() -> rx.Component:
    """Página de servicios dedicada"""
    return rx.box(
        header(active="services"),
        rx.box(height="70px"),  # Spacer for fixed header
        services(),
        rx.box(
            rx.container(
                rx.vstack(
                    rx.heading(
                        "Proceso de Reprogramación",
                        size="7",
                        color="white",
                        text_align="center",
                        mb="8"
                    ),
                    rx.grid(
                        rx.box(
                            rx.vstack(
                                rx.text("1", font_size="2rem", color="#FF6B35", font_weight="bold"),
                                rx.heading("Diagnóstico", size="5", color="white"),
                                rx.text("Análisis completo del vehículo", color="#666666"),
                                spacing="3",
                                align="center"
                            ),
                            text_align="center",
                            p="6",
                            bg="#2D2D2D",
                            border_radius="15px",
                            border="1px solid #666666"
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text("2", font_size="2rem", color="#FF6B35", font_weight="bold"),
                                rx.heading("Backup", size="5", color="white"),
                                rx.text("Copia de seguridad original", color="#666666"),
                                spacing="3",
                                align="center"
                            ),
                            text_align="center",
                            p="6",
                            bg="#2D2D2D",
                            border_radius="15px",
                            border="1px solid #666666"
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text("3", font_size="2rem", color="#FF6B35", font_weight="bold"),
                                rx.heading("Reprogramación", size="5", color="white"),
                                rx.text("Optimización del software", color="#666666"),
                                spacing="3",
                                align="center"
                            ),
                            text_align="center",
                            p="6",
                            bg="#2D2D2D",
                            border_radius="15px",
                            border="1px solid #666666"
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text("4", font_size="2rem", color="#FF6B35", font_weight="bold"),
                                rx.heading("Verificación", size="5", color="white"),
                                rx.text("Pruebas y validación final", color="#666666"),
                                spacing="3",
                                align="center"
                            ),
                            text_align="center",
                            p="6",
                            bg="#2D2D2D",
                            border_radius="15px",
                            border="1px solid #666666"
                        ),
                        columns={"base": "1", "md": "2", "lg": "4"},
                        spacing="6"
                    ),
                    spacing="8",
                    align="center"
                ),
                max_width="1200px",
                px="6",
                py="20"
            ),
            bg="#1A1A1A"
        ),
        footer(),
        bg="#1A1A1A",
        min_height="100vh",
    )


def about_page() -> rx.Component:
    """Página acerca de dedicada"""
    return rx.box(
        header(active="about"),
        rx.box(height="70px"),  # Spacer for fixed header
        rx.box(
            rx.container(
                rx.vstack(
                    rx.heading(
                        "Acerca de AstroTech",
                        size="8",
                        color="white",
                        text_align="center",
                        mb="12"
                    ),
                    rx.grid(
                        rx.vstack(
                            rx.heading(
                                "Nuestra Experiencia",
                                size="6",
                                color="#FF6B35",
                                mb="6"
                            ),
                            rx.text(
                                "Con más de 10 años de experiencia en reprogramación ECU, hemos trabajado con miles de vehículos de todas las marcas principales. Nuestro equipo de técnicos certificados utiliza las herramientas más avanzadas del mercado.",
                                color="white",
                                line_height="1.6",
                                mb="6"
                            ),
                            rx.text(
                                "Garantizamos un servicio profesional, seguro y con resultados medibles. Cada reprogramación se realiza de forma personalizada según las características específicas de tu vehículo.",
                                color="#666666",
                                line_height="1.6"
                            ),
                            spacing="4",
                            align="start"
                        ),
                        rx.box(
                            height={"base": "300px", "md": "400px"},
                            bg="#2D2D2D",
                            border_radius="20px",
                            box_shadow="0 20px 40px rgba(0, 0, 0, 0.2)",
                            border="1px solid #666666"
                        ),
                        columns={"base": "1", "lg": "2"},
                        spacing="9",
                        align="center"
                    ),
                    spacing="8",
                    align="center"
                ),
                max_width="1200px",
                px="6",
                py="20"
            ),
            bg="#1A1A1A"
        ),
        benefits(),
        footer(),
        bg="#1A1A1A",
        min_height="100vh",
    )


def contact_page() -> rx.Component:
    """Página de contacto dedicada"""
    return rx.box(
        header(active="contact"),
        rx.box(height="70px"),  # Spacer for fixed header
        contact(),
        footer(),
        bg="#1A1A1A",
        min_height="100vh",
    )


# Crear la aplicación
app = rx.App(stylesheets=["/styles.css"])
app.add_page(index, route="/", title="AstroTech - Potencia el coche de tus sueños")
app.add_page(services_page, route="/services", title="Servicios - AstroTech")
app.add_page(about_page, route="/about", title="Acerca de - AstroTech")
app.add_page(contact_page, route="/contact", title="Contacto - AstroTech")