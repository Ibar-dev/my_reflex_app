"""
Cookie Banner Component para AstroTech
=====================================

Banner de cookies conforme al RGPD con opciones de aceptar/rechazar
y configuración personalizada.
"""

import reflex as rx
from state.cookie_state import CookieState


def cookie_banner() -> rx.Component:
    """
    Banner de cookies que aparece en la parte inferior de la página.
    Se oculta automáticamente cuando el usuario acepta las cookies.
    """
    return rx.box(
        # Contenedor principal del banner
        rx.box(
            rx.hstack(
                # Información sobre cookies
                rx.vstack(
                    rx.hstack(
                        rx.icon("cookie", size=24, color="#FF6B35"),
                        rx.heading(
                            "🍪 Uso de Cookies",
                            size="4",
                            color="white",
                            font_weight="600",
                        ),
                        spacing="2",
                        align="center",
                    ),
                    rx.text(
                        "Utilizamos cookies esenciales para el funcionamiento del sitio y cookies de análisis "
                        "para mejorar nuestros servicios. Los datos de contacto que proporcionas (nombre, email, teléfono) "
                        "se almacenan localmente para procesar tu solicitud de presupuesto de reprogramación ECU. "
                        "Puedes gestionar tus preferencias de cookies a continuación.",
                        color="#CCCCCC",
                        font_size="0.9rem",
                        line_height="1.4",
                        max_width="600px",
                    ),
                    rx.hstack(
                        rx.link(
                            "Política de Privacidad",
                            href="/privacy",
                            color="#FF6B35",
                            font_size="0.8rem",
                            _hover={"color": "#FF8C42", "text_decoration": "underline"},
                        ),
                        rx.text("•", color="#666666", font_size="0.8rem"),
                        rx.link(
                            "Gestión de Datos",
                            href="/data-management", 
                            color="#FF6B35",
                            font_size="0.8rem",
                            _hover={"color": "#FF8C42", "text_decoration": "underline"},
                        ),
                        spacing="2",
                        mt="2",
                    ),
                    spacing="2",
                    align="start",
                    flex="1",
                ),
                
                # Botones de acción
                rx.vstack(
                    rx.hstack(
                        # Botón configurar
                        rx.button(
                            "Configurar",
                            size="2",
                            variant="outline",
                            color_scheme="gray",
                            on_click=CookieState.open_config,
                            _hover={"bg": "#3A3A3A"},
                        ),
                        # Botón rechazar
                        rx.button(
                            "Solo Esenciales",
                            size="2",
                            variant="outline",
                            color_scheme="gray",
                            on_click=CookieState.accept_essential_only,
                            _hover={"bg": "#3A3A3A", "color": "white"},
                        ),
                        # Botón aceptar
                        rx.button(
                            "Aceptar todas",
                            size="2",
                            bg="linear-gradient(45deg, #FF6B35, #FF8C42)",
                            color="white",
                            on_click=CookieState.accept_all,
                            _hover={
                                "bg": "linear-gradient(45deg, #FF8C42, #FFAB66)",
                                "transform": "translateY(-1px)",
                            },
                            transition="all 0.2s ease",
                        ),
                        spacing="2",
                        wrap="wrap",
                        justify="end",
                    ),
                    spacing="2",
                    align="end",
                ),
                spacing="4",
                align="start",
                justify="between",
                width="100%",
                flex_direction={"base": "column", "md": "row"},
            ),
            
            # Modal de configuración de cookies
            rx.cond(
                CookieState.show_settings,
                rx.box(
                    rx.box(
                        # Overlay
                        position="fixed",
                        top="0",
                        left="0",
                        width="100vw",
                        height="100vh",
                        bg="rgba(0, 0, 0, 0.5)",
                        z_index="1000",
                        on_click=lambda: CookieState.set_show_settings(False),
                    ),
                    rx.box(
                        # Modal content
                        rx.vstack(
                            rx.hstack(
                                rx.heading(
                                    "⚙️ Configuración de Cookies",
                                    size="5",
                                    color="white",
                                ),
                                rx.button(
                                    rx.icon("x", size=20),
                                    size="1",
                                    variant="ghost",
                                    on_click=lambda: CookieState.set_show_settings(False),
                                ),
                                justify="between",
                                width="100%",
                            ),
                            
                            rx.text(
                                "Gestiona qué tipos de cookies y datos quieres permitir. "
                                "Ten en cuenta que rechazar cookies esenciales puede afectar la funcionalidad del sitio:",
                                color="#CCCCCC",
                                font_size="1rem",
                            ),
                            
                            # Tipos de cookies
                            rx.vstack(
                                # Cookies esenciales
                                rx.hstack(
                                    rx.box(
                                        rx.text("✅", font_size="1.2rem"),
                                        width="30px",
                                    ),
                                    rx.vstack(
                                        rx.text(
                                            "Cookies Esenciales",
                                            font_weight="600",
                                            color="white",
                                        ),
                                        rx.text(
                                            "Necesarias para formularios de contacto, selector de vehículos y funcionamiento básico del sitio. "
                                            "Incluye almacenamiento de preferencias de cookies.",
                                            color="#CCCCCC",
                                            font_size="0.9rem",
                                        ),
                                        spacing="1",
                                        align="start",
                                        flex="1",
                                    ),
                                    spacing="3",
                                    align="start",
                                    width="100%",
                                ),
                                
                                # Cookies de análisis
                                rx.hstack(
                                    rx.box(
                                        rx.checkbox(
                                            checked=CookieState.analytics_cookies,
                                            on_change=CookieState.toggle_analytics,
                                            color_scheme="orange",
                                        ),
                                        width="30px",
                                    ),
                                    rx.vstack(
                                        rx.text(
                                            "Cookies de Análisis",
                                            font_weight="600",
                                            color="white",
                                        ),
                                        rx.text(
                                            "Nos ayudan a entender cómo interactúas con nuestro selector de vehículos y formularios "
                                            "para mejorar nuestros servicios de reprogramación ECU. Datos anonimizados.",
                                            color="#CCCCCC",
                                            font_size="0.9rem",
                                        ),
                                        spacing="1",
                                        align="start",
                                        flex="1",
                                    ),
                                    spacing="3",
                                    align="start",
                                    width="100%",
                                ),
                                
                                # Cookies de marketing
                                rx.hstack(
                                    rx.box(
                                        rx.checkbox(
                                            checked=CookieState.marketing_cookies,
                                            on_change=CookieState.toggle_marketing,
                                            color_scheme="orange",
                                        ),
                                        width="30px",
                                    ),
                                    rx.vstack(
                                        rx.text(
                                            "Cookies de Marketing",
                                            font_weight="600",
                                            color="white",
                                        ),
                                        rx.text(
                                            "Para mostrar ofertas relevantes de servicios de reprogramación ECU "
                                            "basadas en tu tipo de vehículo y preferencias expresadas.",
                                            color="#CCCCCC",
                                            font_size="0.9rem",
                                        ),
                                        spacing="1",
                                        align="start",
                                        flex="1",
                                    ),
                                    spacing="3",
                                    align="start",
                                    width="100%",
                                ),
                                spacing="4",
                                width="100%",
                            ),
                            
                            # Botones del modal
                            rx.hstack(
                                rx.button(
                                    "Solo Esenciales",
                                    size="3",
                                    variant="outline",
                                    color_scheme="gray",
                                    on_click=CookieState.accept_essential_only,
                                    flex="1",
                                ),
                                rx.button(
                                    "Guardar Configuración",
                                    size="3",
                                    bg="linear-gradient(45deg, #FF6B35, #FF8C42)",
                                    color="white",
                                    on_click=CookieState.save_custom_settings,
                                    flex="1",
                                ),
                                spacing="2",
                                width="100%",
                            ),
                            
                            spacing="4",
                            width="100%",
                        ),
                        position="fixed",
                        top="50%",
                        left="50%",
                        transform="translate(-50%, -50%)",
                        bg="linear-gradient(145deg, #2A2A2A, #1E1E1E)",
                        border="1px solid #3A3A3A",
                        border_radius="15px",
                        p="6",
                        max_width="500px",
                        width="90%",
                        box_shadow="0 20px 40px rgba(0, 0, 0, 0.4)",
                        z_index="1001",
                    ),
                    position="fixed",
                    top="0",
                    left="0",
                    width="100%",
                    height="100%",
                ),
            ),
            
            bg="linear-gradient(145deg, #2A2A2A, #1E1E1E)",
            border="1px solid #3A3A3A",
            border_radius="15px",
            p={"base": "4", "md": "6"},
            box_shadow="0 10px 30px rgba(0, 0, 0, 0.3)",
            max_width="1200px",
            width="100%",
            mx="auto",
        ),
        
        # Posicionamiento del banner
        position="fixed",
        bottom="20px",
        left="20px",
        right="20px",
        z_index="999",
        px={"base": "4", "md": "6"},
        
        # Animación de entrada
        animation="slideInUp 0.5s ease-out",
        
        # Media queries para responsive
        _mobile={
            "bottom": "10px",
            "left": "10px",
            "right": "10px",
        },
    )


# Estilos adicionales para animaciones
def cookie_banner_styles():
    """Estilos CSS adicionales para el cookie banner."""
    return {
        "@keyframes slideInUp": {
            "from": {
                "transform": "translateY(100%)",
                "opacity": "0",
            },
            "to": {
                "transform": "translateY(0)",
                "opacity": "1",
            },
        },
    }

