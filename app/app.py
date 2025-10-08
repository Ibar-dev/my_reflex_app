"""
Aplicación AstroTech - Reprogramación ECU
===============================

Aplicación web moderna para servicios de reprogramación ECU con diseño profesional,
animaciones suaves y experiencia de usuario optimizada.
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
from state.vehicle_state import VehicleState

# Importar estados para que Reflex los reconozca
from state.contact_state import ContactState


# Estado global de la aplicación
class AppState(rx.State):
    """Estado global de la aplicación."""
    show_scroll_top: bool = False

    def toggle_scroll_top(self, show: bool):
        """Muestra u oculta el botón de volver arriba."""
        self.show_scroll_top = show

# Estilos personalizados
def custom_styles() -> dict:
    """Estilos personalizados para toda la aplicación."""
    return {
        "global": {
            "html, body": {
                "scrollBehavior": "smooth",
                "backgroundColor": "#121212",
                "color": "white",
                "fontFamily": "'Inter', sans-serif"
            },
            ".fade-in": {
                "opacity": "0",
                "animation": "fadeIn 0.8s ease forwards"
            },
            ".fade-in-up": {
                "opacity": "0",
                "transform": "translateY(20px)",
                "animation": "fadeInUp 0.8s ease forwards"
            },
            ".fade-in-left": {
                "opacity": "0",
                "transform": "translateX(-20px)",
                "animation": "fadeInLeft 0.8s ease forwards"
            },
            ".fade-in-right": {
                "opacity": "0",
                "transform": "translateX(20px)",
                "animation": "fadeInRight 0.8s ease forwards"
            },
            ".hover-raise": {
                "transition": "transform 0.3s ease, box-shadow 0.3s ease",
            },
            ".hover-raise:hover": {
                "transform": "translateY(-5px)",
                "boxShadow": "0 10px 20px rgba(0, 0, 0, 0.2)"
            },
            ".section": {
                "scrollMarginTop": "70px",
                "paddingTop": "80px",
                "paddingBottom": "80px",
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center",
            },
            ".gradient-text": {
                "background": "linear-gradient(45deg, #FF6B35, #FF8C42)",
                "backgroundClip": "text",
                "WebkitBackgroundClip": "text",
                "color": "transparent",
                "WebkitTextFillColor": "transparent"
            },
            ".card-shadow": {
                "boxShadow": "0 8px 30px rgba(0, 0, 0, 0.12), 0 4px 10px rgba(0, 0, 0, 0.06)"
            },
            "@keyframes fadeIn": {
                "from": {"opacity": "0"},
                "to": {"opacity": "1"}
            },
            "@keyframes fadeInUp": {
                "from": {"opacity": "0", "transform": "translateY(20px)"},
                "to": {"opacity": "1", "transform": "translateY(0)"}
            },
            "@keyframes fadeInLeft": {
                "from": {"opacity": "0", "transform": "translateX(-20px)"},
                "to": {"opacity": "1", "transform": "translateX(0)"}
            },
            "@keyframes fadeInRight": {
                "from": {"opacity": "0", "transform": "translateX(20px)"},
                "to": {"opacity": "1", "transform": "translateX(0)"}
            },
            "@keyframes pulse": {
                "0%": {"transform": "scale(1)"},
                "50%": {"transform": "scale(1.05)"},
                "100%": {"transform": "scale(1)"}
            },
            "@media (max-width: 768px)": {
                ".section": {
                    "paddingTop": "40px",
                    "paddingBottom": "40px",
                    "paddingLeft": "1rem",
                    "paddingRight": "1rem",
                },
                ".hero-title": {
                    "fontSize": "2.2rem !important",
                    "textAlign": "center",
                    "lineHeight": "1.2",
                },
                ".hero-text": {
                    "fontSize": "1rem !important",
                    "textAlign": "center",
                    "padding": "0 0.5rem",
                },
                ".benefit-card": {
                    "minHeight": "200px",
                    "padding": "1rem",
                    "margin": "0 0.5rem",
                },
                ".service-card": {
                    "minHeight": "160px",
                    "padding": "1rem",
                },
                ".vehicle-selector": {
                    "padding": "1rem !important",
                    "margin": "0.5rem",
                },
                ".faq-container": {
                    "padding": "1rem",
                },
                "h1, h2, h3": {
                    "fontSize": "1.8rem !important",
                    "textAlign": "center",
                },
                ".grid": {
                    "gap": "1rem !important",
                }
            }
        }
    }

# Botón para volver arriba
def scroll_to_top() -> rx.Component:
    """Botón para volver al inicio de la página."""
    return rx.cond(
        AppState.show_scroll_top,
        rx.button(
            rx.icon("arrow-up", size=24),
            position="fixed",
            bottom="30px",
            right="30px",
            size="3",
            border_radius="full",
            bg="rgba(255, 107, 53, 0.9)",
            color="white",
            _hover={"bg": "#FF6B35", "transform": "translateY(-5px)"},
            transition="all 0.3s ease",
            z_index="999",
            box_shadow="0 4px 20px rgba(255, 107, 53, 0.4)",
            on_click=rx.redirect("/#"),
            opacity={"base": "0.8", "_hover": "1"}
        ),
        rx.box()  # No mostrar nada si show_scroll_top es False
    )

def index() -> rx.Component:
    """Página principal completa con diseño moderno y consistente."""
    return rx.box(
        # Header fijo en la parte superior
        header(),
        
        # Main content - Centralized layout
        rx.center(
            rx.vstack(
                rx.box(
                    hero(),
                    class_name="section scroll-target",
                    id="inicio",
                    padding_top="0px",
                    width="100%",
                ),
                rx.box(
                    vehicle_selector(),
                    class_name="scroll-target",
                    width="100%",
                ),
                rx.box(
                    benefits(),
                    class_name="section scroll-target",
                    id="beneficios",
                    width="100%",
                ),
                rx.box(
                    services(),
                    class_name="section scroll-target",
                    id="servicios",
                    width="100%",
                ),
            
                # Espaciado adicional antes de la sección Acerca de
                rx.box(height={"base": "3rem", "md": "4rem"}),
                
                # Sección Acerca de con diseño moderno y fondo
                rx.box(
                # Background image with overlay and effects
                rx.box(
                    # Dark overlay with gradient
                    rx.box(
                        position="absolute",
                        top="0",
                        left="0",
                        right="0",
                        bottom="0",
                        bg="linear-gradient(135deg, rgba(18, 18, 18, 0.95) 0%, rgba(30, 30, 30, 0.9) 100%)",
                        z_index="1",
                    ),
                    # Animated glow effect 1
                    rx.box(
                        position="absolute",
                        top="20%",
                        right="-20%",
                        width="50%",
                        height="50%",
                        border_radius="full",
                        bg="radial-gradient(circle, rgba(255,107,53,0.15) 0%, rgba(255,107,53,0) 70%)",
                        z_index="1",
                        animation="pulse 8s infinite ease-in-out",
                    ),
                    # Animated glow effect 2
                    rx.box(
                        position="absolute",
                        bottom="-10%",
                        left="-5%",
                        width="40%",
                        height="40%",
                        border_radius="full",
                        bg="radial-gradient(circle, rgba(255,140,66,0.1) 0%, rgba(255,140,66,0) 60%)",
                        z_index="1",
                        animation="pulse 10s infinite ease-in-out",
                        animation_delay="2s",
                    ),
                    # Background image
                    position="absolute",
                    top="0",
                    left="0",
                    right="0",
                    bottom="0",
                    background_image="url('/images/centralita-coche.jpg')",
                    background_size="cover",
                    background_position="center",
                    background_repeat="no-repeat",
                    background_attachment="fixed",
                    filter="blur(1px)",
                    z_index="0",
                    class_name="parallax-bg",
                ),
                
                # Main content container
                rx.center(
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "¿Qué es la reprogramación ECU?",
                                size="8",
                                color="#FF6B35",
                                text_align="center",
                                mb="6",
                                mt="9",
                                pt="9",
                                font_weight="700",
                                class_name="fade-in",
                            ),
                            rx.text(
                                "Optimización profesional del software para maximizar el rendimiento de tu vehículo",
                                color="#CCCCCC",
                                font_size="1.3rem",
                                text_align="center",
                                mb="8",
                                line_height="1.6",
                                class_name="fade-in",
                                font_weight="500",
                            ),
                            rx.text(
                                "La reprogramación ECU (Unidad de Control del Motor) es un proceso técnico que consiste en modificar el software que controla el funcionamiento del motor de tu vehículo. Esta optimización permite:",
                                color="#CCCCCC",
                                mb="8",
                                line_height="1.7",
                                font_size="1.1rem",
                                text_align="center",
                                max_width="900px"
                            ),
                            rx.vstack(
                                rx.hstack(
                                    rx.box(
                                        rx.icon("check", size=18, color="white"),
                                        bg="#FF6B35",
                                        border_radius="full",
                                        p="2",
                                    ),
                                    rx.text("Aumentar la potencia del motor", color="white", font_weight="500", font_size="1.05rem"),
                                    spacing="3",
                                    align="center",
                                ),
                                rx.hstack(
                                    rx.box(
                                        rx.icon("check", size=18, color="white"),
                                        bg="#FF6B35",
                                        border_radius="full",
                                        p="2",
                                    ),
                                    rx.text("Reducir el consumo de combustible", color="white", font_weight="500", font_size="1.05rem"),
                                    spacing="3",
                                    align="center",
                                ),
                                rx.hstack(
                                    rx.box(
                                        rx.icon("check", size=18, color="white"),
                                        bg="#FF6B35",
                                        border_radius="full",
                                        p="2",
                                    ),
                                    rx.text("Mejorar la respuesta del acelerador", color="white", font_weight="500", font_size="1.05rem"),
                                    spacing="3",
                                    align="center",
                                ),
                                rx.hstack(
                                    rx.box(
                                        rx.icon("check", size=18, color="white"),
                                        bg="#FF6B35",
                                        border_radius="full",
                                        p="2",
                                    ),
                                    rx.text("Optimizar el par motor", color="white", font_weight="500", font_size="1.05rem"),
                                    spacing="3",
                                    align="center",
                                ),
                                spacing="4",
                                align="center",
                                mb="8",
                            ),
                            rx.text(
                                "Nuestro equipo de técnicos especializados utiliza equipos de última generación para garantizar resultados óptimos y seguros para tu vehículo.",
                                color="#CCCCCC",
                                line_height="1.7",
                                font_size="1.1rem",
                                text_align="center",
                                max_width="800px"
                            ),
                            spacing="6",
                            align="center",
                            width="100%",
                        ),
                        max_width="1000px",
                        width="100%",
                        mx="auto",
                        class_name="scroll-target",
                        position="relative",
                        z_index="10",
                    ),
                    width="100%",
                    px={"base": "6", "md": "8"},
                    py={"base": "8", "md": "12"},
                    id="acerca"
                ),
                position="relative",
                overflow="hidden",
                min_height="60vh",  # Reducido aún más para menos espacio
                width="100%",
                ),
                
                rx.box(
                    faq(),
                    class_name="section scroll-target",
                    id="faq",
                    width="100%",
                ),
                rx.box(
                    contact(),
                    class_name="section scroll-target",
                    id="contacto",
                    width="100%",
                ),
                footer(),
                
                # Botón para volver arriba
                scroll_to_top(),
                
                spacing="0",
                align="center",
                width="100%",
            ),
            width="100%",
        ),
        
        bg="#121212",
        min_height="100vh",
        width="100%",
    )

def services_page() -> rx.Component:
    """Página de servicios dedicada con diseño moderno."""
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
                        mb="8",
                        class_name="gradient-text fade-in"
                    ),
                    rx.grid(
                        rx.box(
                            rx.vstack(
                                rx.box(
                                    rx.text("1", font_size="2rem", color="white", font_weight="bold"),
                                    bg="linear-gradient(45deg, #FF6B35, #FF8C42)",
                                    width="50px",
                                    height="50px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                    border_radius="full",
                                    mb="4",
                                ),
                                rx.heading("Diagnóstico", size="5", color="white"),
                                rx.text("Análisis completo del vehículo", color="#CCCCCC"),
                                spacing="3",
                                align="center",
                                class_name="fade-in-up hover-raise"
                            ),
                            text_align="center",
                            p="6",
                            bg="linear-gradient(145deg, #252525, #1e1e1e)",
                            border_radius="20px",
                            border="1px solid #3d3d3d",
                            box_shadow="0 15px 35px rgba(0, 0, 0, 0.3)",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.box(
                                    rx.text("2", font_size="2rem", color="white", font_weight="bold"),
                                    bg="linear-gradient(45deg, #FF6B35, #FF8C42)",
                                    width="50px",
                                    height="50px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                    border_radius="full",
                                    mb="4",
                                ),
                                rx.heading("Backup", size="5", color="white"),
                                rx.text("Copia de seguridad original", color="#CCCCCC"),
                                spacing="3",
                                align="center",
                                class_name="fade-in-up hover-raise"
                            ),
                            text_align="center",
                            p="6",
                            bg="linear-gradient(145deg, #252525, #1e1e1e)",
                            border_radius="20px",
                            border="1px solid #3d3d3d",
                            box_shadow="0 15px 35px rgba(0, 0, 0, 0.3)",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.box(
                                    rx.text("3", font_size="2rem", color="white", font_weight="bold"),
                                    bg="linear-gradient(45deg, #FF6B35, #FF8C42)",
                                    width="50px",
                                    height="50px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                    border_radius="full",
                                    mb="4",
                                ),
                                rx.heading("Reprogramación", size="5", color="white"),
                                rx.text("Optimización del software", color="#CCCCCC"),
                                spacing="3",
                                align="center",
                                class_name="fade-in-up hover-raise"
                            ),
                            text_align="center",
                            p="6",
                            bg="linear-gradient(145deg, #252525, #1e1e1e)",
                            border_radius="20px",
                            border="1px solid #3d3d3d",
                            box_shadow="0 15px 35px rgba(0, 0, 0, 0.3)",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.box(
                                    rx.text("4", font_size="2rem", color="white", font_weight="bold"),
                                    bg="linear-gradient(45deg, #FF6B35, #FF8C42)",
                                    width="50px",
                                    height="50px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                    border_radius="full",
                                    mb="4",
                                ),
                                rx.heading("Verificación", size="5", color="white"),
                                rx.text("Pruebas y validación final", color="#CCCCCC"),
                                spacing="3",
                                align="center",
                                class_name="fade-in-up hover-raise"
                            ),
                            text_align="center",
                            p="6",
                            bg="linear-gradient(145deg, #252525, #1e1e1e)",
                            border_radius="20px",
                            border="1px solid #3d3d3d",
                            box_shadow="0 15px 35px rgba(0, 0, 0, 0.3)",
                        ),
                        columns={"base": "1", "md": "2", "lg": "4"},
                        spacing="6",
                    ),
                    spacing="8",
                    align="center",
                ),
                max_width="1200px",
                px="6",
                py="20",
            ),
            bg="#1A1A1A",
            class_name="section"
        ),
        footer(),
        bg="#121212",
        min_height="100vh",
        width="100%",
    )

def about_page() -> rx.Component:
    """Página acerca de dedicada."""
    return rx.box(
        header(active="about"),
        rx.box(height="70px"),  # Spacer for fixed header
        # Main content with background image
        rx.box(
            # Background image with overlay and effects
            rx.box(
                # Dark overlay with gradient
                rx.box(
                    position="absolute",
                    top="0",
                    left="0",
                    right="0",
                    bottom="0",
                    bg="linear-gradient(135deg, rgba(18, 18, 18, 0.95) 0%, rgba(30, 30, 30, 0.9) 100%)",
                    z_index="1",
                ),
                # Animated glow effect 1
                rx.box(
                    position="absolute",
                    top="20%",
                    right="-20%",
                    width="50%",
                    height="50%",
                    border_radius="full",
                    bg="radial-gradient(circle, rgba(255,107,53,0.15) 0%, rgba(255,107,53,0) 70%)",
                    z_index="1",
                    animation="pulse 8s infinite ease-in-out",
                ),
                # Animated glow effect 2
                rx.box(
                    position="absolute",
                    bottom="-10%",
                    left="-5%",
                    width="40%",
                    height="40%",
                    border_radius="full",
                    bg="radial-gradient(circle, rgba(255,140,66,0.1) 0%, rgba(255,140,66,0) 60%)",
                    z_index="1",
                    animation="pulse 10s infinite ease-in-out",
                    animation_delay="2s",
                ),
                # Background image
                position="absolute",
                top="0",
                left="0",
                right="0",
                bottom="0",
                background_image="url('/images/centralita-coche.jpg')",
                background_size="cover",
                background_position="center",
                background_repeat="no-repeat",
                background_attachment="fixed",
                filter="blur(1px)",
                z_index="0",
                class_name="parallax-bg",
            ),
            
            # Main content container
            rx.box(
                # Hero section
                rx.container(
                    rx.vstack(
                        rx.heading(
                            "Acerca de AstroTech",
                            size="8",
                            color="white",
                            text_align="center",
                            mb="12",
                            class_name="gradient-text fade-in",
                            position="relative",
                            z_index="2",
                            text_shadow="0 2px 4px rgba(0,0,0,0.8)",
                            font_weight="800"
                        ),
                        spacing="8",
                        align="center",
                        position="relative",
                        z_index="2",
                    ),
                    max_width="1200px",
                    px="6",
                    py={"base": "100px", "md": "150px"},
                    position="relative",
                    z_index="1",
                ),
                
                # Content section with semi-transparent background
                rx.box(
                    rx.container(
                        rx.vstack(
                            rx.heading(
                                "Nuestra Experiencia",
                                size="6",
                                color="#FF6B35",
                                mb="6",
                                class_name="fade-in-left",
                                width="100%",
                                text_align={"base": "center", "md": "left"}
                            ),
                            rx.text(
                                "Con más de 10 años de experiencia en reprogramación ECU, hemos trabajado con miles de vehículos de todas las marcas principales. Nuestro equipo de técnicos certificados utiliza las herramientas más avanzadas del mercado.",
                                color="white",
                                line_height="1.6",
                                mb="6",
                                class_name="fade-in-left",
                                width="100%"
                            ),
                            rx.text(
                                "Garantizamos un servicio profesional, seguro y con resultados medibles. Cada reprogramación se realiza de forma personalizada según las características específicas de tu vehículo.",
                                color="#CCCCCC",
                                line_height="1.6",
                                class_name="fade-in-left",
                                width="100%"
                            ),
                            spacing="4",
                            align="start",
                            width="100%",
                            max_width="800px",
                            mx="auto"
                        ),
                        max_width="1200px",
                        px="6",
                        py="20",
                        bg="rgba(26, 26, 26, 0.85)",
                        borderRadius="lg",
                        boxShadow="xl"
                    ),
                    position="relative",
                    z_index="2"
                ),
                
                # Benefits section with semi-transparent background
                rx.box(
                    benefits(),
                    bg="rgba(18, 18, 18, 0.9)",
                    py="12",
                    position="relative",
                    z_index="2"
                ),
                
                # Footer
                rx.box(
                    footer(),
                    position="relative",
                    z_index="2"
                ),
                
                position="relative",
                z_index="2"
            ),
            min_height="100vh",
            width="100%",
            position="relative",
            overflow="hidden"
        ),
        min_height="100vh",
        width="100%",
    )

def contact_page() -> rx.Component:
    """Página de contacto dedicada."""
    return rx.box(
        header(active="contact"),
        rx.box(height="70px"),  # Spacer for fixed header
        contact(),
        footer(),
        bg="#121212",
        min_height="100vh",
        width="100%",
    )

# Crear la aplicación
app = rx.App(
    stylesheets=["/styles.css", "/selector-fix.css"],  # ✅ CORRECTO
    style=custom_styles(),
)

app.add_page(
    index,
    route="/",
    title="AstroTech - Potencia el coche de tus sueños",
    description="Reprogramación ECU profesional para maximizar el rendimiento de tu vehículo",
    meta=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0, maximum-scale=5.0"},
    ]
)


app.add_page(services_page, route="/services", title="Servicios - AstroTech")
app.add_page(about_page, route="/about", title="Acerca de - AstroTech")
app.add_page(contact_page, route="/contact", title="Contacto - AstroTech")
