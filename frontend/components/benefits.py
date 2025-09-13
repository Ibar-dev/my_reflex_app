"""
Componente Benefits - Sección de beneficios con tarjetas animadas
===============================================================

Tarjetas con efectos hover, iconos y animaciones basadas en la maqueta.
"""

import reflex as rx

def benefits() -> rx.Component:
    """Sección de beneficios con tarjetas animadas"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading(
                    "Más potencia, menos consumo",
                    size="8",
                    color="white",
                    text_align="center",
                    mb="16",
                    font_weight="700"
                ),
                rx.center(
                    rx.grid(
                        # Tarjeta 1: Mayor Potencia
                        rx.box(
                            rx.vstack(
                                rx.center(
                                    rx.icon("zap", size=48, color="#FF6B35")
                                ),
                                rx.heading(
                                    "Mayor Potencia",
                                    size="5",
                                    color="white",
                                    mb="3",
                                    text_align="center"
                                ),
                                rx.text(
                                    "Aumenta la potencia de tu motor hasta un 30% manteniendo la fiabilidad del vehículo.",
                                    color="#CCCCCC",
                                    line_height="1.6",
                                    text_align="center",
                                    font_size="0.95rem"
                                ),
                                spacing="4",
                                align="center",
                                height="100%"
                            ),
                            bg="#2D2D2D",
                            border_radius="20px",
                            p="10",
                            border="1px solid #404040",
                            min_height="220px",
                            _hover={
                                "transform": "translateY(-10px)",
                                "box_shadow": "0 10px 25px rgba(255, 107, 53, 0.15)",
                                "border_color": "#FF6B35"
                            },
                            transition="all 0.4s ease",
                            cursor="pointer",
                            class_name="benefit-card fade-in-up hover-raise"
                        ),
                        
                        # Tarjeta 2: Menor Consumo
                        rx.box(
                            rx.vstack(
                                rx.center(
                                    rx.icon("dollar-sign", size=48, color="#FF6B35")
                                ),
                                rx.heading(
                                    "Menor Consumo",
                                    size="5",
                                    color="white",
                                    mb="3",
                                    text_align="center"
                                ),
                                rx.text(
                                    "Reduce el consumo de combustible hasta un 15% con una conducción eficiente.",
                                    color="#CCCCCC",
                                    line_height="1.6",
                                    text_align="center",
                                    font_size="0.95rem"
                                ),
                                spacing="4",
                                align="center",
                                height="100%"
                            ),
                            bg="#2D2D2D",
                            border_radius="20px",
                            p="10",
                            border="1px solid #404040",
                            min_height="220px",
                            _hover={
                                "transform": "translateY(-10px)",
                                "box_shadow": "0 10px 25px rgba(255, 107, 53, 0.15)",
                                "border_color": "#FF6B35"
                            },
                            transition="all 0.4s ease",
                            cursor="pointer",
                            class_name="benefit-card fade-in-up hover-raise"
                        ),
                        
                        # Tarjeta 3: Proceso Reversible
                        rx.box(
                            rx.vstack(
                                rx.center(
                                    rx.icon("wrench", size=48, color="#FF6B35")
                                ),
                                rx.heading(
                                    "Proceso Reversible",
                                    size="5",
                                    color="white",
                                    mb="3",
                                    text_align="center"
                                ),
                                rx.text(
                                    "La reprogramación es completamente reversible. Puedes volver a la configuración original cuando quieras.",
                                    color="#CCCCCC",
                                    line_height="1.6",
                                    text_align="center",
                                    font_size="0.95rem"
                                ),
                                spacing="4",
                                align="center",
                                height="100%"
                            ),
                            bg="#2D2D2D",
                            border_radius="20px",
                            p="10",
                            border="1px solid #404040",
                            min_height="220px",
                            _hover={
                                "transform": "translateY(-10px)",
                                "box_shadow": "0 10px 25px rgba(255, 107, 53, 0.15)",
                                "border_color": "#FF6B35"
                            },
                            transition="all 0.4s ease",
                            cursor="pointer",
                            class_name="benefit-card fade-in-up hover-raise"
                        ),
                        
                        # Tarjeta 4: Garantía Incluida
                        rx.box(
                            rx.vstack(
                                rx.center(
                                    rx.icon("shield-check", size=48, color="#FF6B35")
                                ),
                                rx.heading(
                                    "Garantía Incluida",
                                    size="5",
                                    color="white",
                                    mb="3",
                                    text_align="center"
                                ),
                                rx.text(
                                    "Ofrecemos garantía completa en todos nuestros servicios de reprogramación ECU.",
                                    color="#CCCCCC",
                                    line_height="1.6",
                                    text_align="center",
                                    font_size="0.95rem"
                                ),
                                spacing="4",
                                align="center",
                                height="100%"
                            ),
                            bg="#2D2D2D",
                            border_radius="20px",
                            p="10",
                            border="1px solid #404040",
                            min_height="220px",
                            _hover={
                                "transform": "translateY(-10px)",
                                "box_shadow": "0 10px 25px rgba(255, 107, 53, 0.15)",
                                "border_color": "#FF6B35"
                            },
                            transition="all 0.4s ease",
                            cursor="pointer",
                            class_name="benefit-card fade-in-up hover-raise"
                        ),
                        
                        columns={"base": "1", "md": "2", "lg": "4"},
                        spacing={"base": "6", "md": "8"},
                        width="100%",
                        class_name="fade-in-up",
                        justify="center"
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
        bg="#1A1A1A"
    )
