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
        # Header fuera del contenedor para que ocupe todo el ancho
        header(),
        rx.container(
            rx.box(hero(), class_name="section scroll-target", id="inicio"),
            rx.box(vehicle_selector(), class_name="scroll-target", id="selector"),
            rx.box(benefits(), class_name="scroll-target", id="beneficios"),
            rx.box(services(), class_name="scroll-target", id="servicios"),
            rx.box(
                rx.container(
                    rx.vstack(
                        rx.heading(
                            "¿Qué es la reprogramación ECU?",
                            size="8",
                            color="white",
                            text_align="center",
                            mb="12",
                            font_weight="700"
                        ),
                        rx.center(
                            rx.grid(
                                # Columna de texto
                                rx.vstack(
                                    rx.text(
                                        "La reprogramación ECU (Unidad de Control del Motor) es un proceso técnico que consiste en modificar el software que controla el funcionamiento del motor de tu vehículo. Esta optimización permite:",
                                        color="#CCCCCC",
                                        mb="6",
                                        line_height="1.7",
                                        font_size="1.05rem"
                                    ),
                                    rx.vstack(
                                        rx.hstack(
                                            rx.icon("check_check", size=16, color="#FF6B35"),
                                            rx.text("Aumentar la potencia del motor", color="white"),
                                            spacing="3",
                                            align="center"
                                        ),
                                        rx.hstack(
                                            rx.icon("check_check", size=16, color="#FF6B35"),
                                            rx.text("Reducir el consumo de combustible", color="white"),
                                            spacing="3",
                                            align="center"
                                        ),
                                        rx.hstack(
                                            rx.icon("check_check", size=16, color="#FF6B35"),
                                            rx.text("Mejorar la respuesta del acelerador", color="white"),
                                            spacing="3",
                                            align="center"
                                        ),
                                        rx.hstack(
                                            rx.icon("check_check", size=16, color="#FF6B35"),
                                            rx.text("Optimizar el par motor", color="white"),
                                            spacing="3",
                                            align="center"
                                        ),
                                        spacing="3",
                                        align="start",
                                        mb="6"
                                    ),
                                    rx.text(
                                        "Nuestro equipo de técnicos especializados utiliza equipos de última generación para garantizar resultados óptimos y seguros para tu vehículo.",
                                        color="#CCCCCC",
                                        line_height="1.7",
                                        font_weight="500"
                                    ),
                                    spacing="4",
                                    align="start",
                                    justify="center"
                                ),
                                # Columna de imagen
                                rx.box(
                                    rx.center(
                                        rx.vstack(
                                            rx.icon("cpu", size=60, color="#FF6B35"),
                                            rx.text(
                                                "Imagen ECU",
                                                color="#666666",
                                                font_size="0.9rem",
                                                text_align="center"
                                            ),
                                            spacing="4"
                                        )
                                    ),
                                    height={"base": "300px", "md": "350px", "lg": "400px"},
                                    bg="#2D2D2D",
                                    border_radius="20px",
                                    border="2px solid #404040",
                                    box_shadow="0 10px 30px rgba(0, 0, 0, 0.3)",
                                    position="relative",
                                    overflow="hidden",
                                    _before={
                                        "content": "''",
                                        "position": "absolute",
                                        "top": "0",
                                        "left": "0",
                                        "right": "0",
                                        "bottom": "0",
                                        "background": "linear-gradient(45deg, transparent 40%, rgba(255, 107, 53, 0.05) 50%, transparent 60%)",
                                        "z_index": "1"
                                    }
                                ),
                                columns={"base": "1", "lg": "2"},
                                spacing={"base": "6", "lg": "8"},
                                align="center",
                                width="100%"
                            ),
                            width="100%"
                        ),
                        spacing="6",
                        align="center",
                        width="100%"
                    ),
                    max_width="1200px",
                    px={"base": "6", "md": "8"},
                    py={"base": "16", "md": "24"}
                ),
                bg="#2D2D2D",
                class_name="scroll-target",
                id="acerca"
            ),
            rx.box(faq(), class_name="scroll-target", id="faq"),
            rx.box(contact(), class_name="scroll-target", id="contacto"),
            footer(),
            spacing="8",
            width="100%",
            max_width="1200px",
            padding_x="1rem",
        ),
        bg="#1A1A1A",
        min_height="100vh",
        display="flex",
        justify_content="center",
        align_items="center",
        flex_direction="column",
    )


def services_page() -> rx.Component:
    """Página de servicios dedicada"""
    return rx.box(
        rx.container(
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
            display="flex",
            justify_content="center",
            align_items="center",
            flex_direction="column",
        ),
        bg="#1A1A1A",
        min_height="100vh",
        display="flex",
        justify_content="center",
        align_items="center",
        flex_direction="column",
    )


def about_page() -> rx.Component:
    """Página acerca de dedicada"""
    return rx.box(
        rx.container(
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
            display="flex",
            justify_content="center",
            align_items="center",
            flex_direction="column",
        ),
        bg="#1A1A1A",
        min_height="100vh",
        display="flex",
        justify_content="center",
        align_items="center",
        flex_direction="column",
    )


def contact_page() -> rx.Component:
    """Página de contacto dedicada"""
    return rx.box(
        rx.container(
            header(active="contact"),
            rx.box(height="70px"),  # Spacer for fixed header
            contact(),
            footer(),
            bg="#1A1A1A",
            min_height="100vh",
            display="flex",
            justify_content="center",
            align_items="center",
            flex_direction="column",
        ),
        bg="#1A1A1A",
        min_height="100vh",
        display="flex",
        justify_content="center",
        align_items="center",
        flex_direction="column",
    )


# Crear la aplicación
app = rx.App(stylesheets=["/styles.css"])
app.add_page(index, route="/", title="AstroTech - Potencia el coche de tus sueños")
app.add_page(services_page, route="/services", title="Servicios - AstroTech")
app.add_page(about_page, route="/about", title="Acerca de - AstroTech")
app.add_page(contact_page, route="/contact", title="Contacto - AstroTech")