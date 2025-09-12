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
                    mb="12"
                ),
                rx.grid(
                    # Tarjeta 1: Mayor Potencia
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "⚡",
                                font_size="3rem",
                                mb="4"
                            ),
                            rx.heading(
                                "Mayor Potencia",
                                size="5",
                                color="white",
                                mb="3"
                            ),
                            rx.text(
                                "Aumenta la potencia de tu motor hasta un 30% manteniendo la fiabilidad del vehículo.",
                                color="#666666",
                                line_height="1.6",
                                text_align="center"
                            ),
                            spacing="2",
                            align="center"
                        ),
                        bg="#2D2D2D",
                        border_radius="15px",
                        p="8",
                        border="1px solid #666666",
                        _hover={
                            "transform": "translateY(-10px)",
                            "box_shadow": "0 8px 15px rgba(0, 0, 0, 0.2)"
                        },
                        transition="all 0.3s ease",
                        cursor="pointer"
                    ),
                    
                    # Tarjeta 2: Menor Consumo
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "💰",
                                font_size="3rem",
                                mb="4"
                            ),
                            rx.heading(
                                "Menor Consumo",
                                size="5",
                                color="white",
                                mb="3"
                            ),
                            rx.text(
                                "Reduce el consumo de combustible hasta un 15% con una conducción eficiente.",
                                color="#666666",
                                line_height="1.6",
                                text_align="center"
                            ),
                            spacing="2",
                            align="center"
                        ),
                        bg="#2D2D2D",
                        border_radius="15px",
                        p="8",
                        border="1px solid #666666",
                        _hover={
                            "transform": "translateY(-10px)",
                            "box_shadow": "0 8px 15px rgba(0, 0, 0, 0.2)"
                        },
                        transition="all 0.3s ease",
                        cursor="pointer"
                    ),
                    
                    # Tarjeta 3: Proceso Reversible
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "🔧",
                                font_size="3rem",
                                mb="4"
                            ),
                            rx.heading(
                                "Proceso Reversible",
                                size="5",
                                color="white",
                                mb="3"
                            ),
                            rx.text(
                                "La reprogramación es completamente reversible. Puedes volver a la configuración original cuando quieras.",
                                color="#666666",
                                line_height="1.6",
                                text_align="center"
                            ),
                            spacing="2",
                            align="center"
                        ),
                        bg="#2D2D2D",
                        border_radius="15px",
                        p="8",
                        border="1px solid #666666",
                        _hover={
                            "transform": "translateY(-10px)",
                            "box_shadow": "0 8px 15px rgba(0, 0, 0, 0.2)"
                        },
                        transition="all 0.3s ease",
                        cursor="pointer"
                    ),
                    
                    # Tarjeta 4: Garantía Incluida
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "🛡️",
                                font_size="3rem",
                                mb="4"
                            ),
                            rx.heading(
                                "Garantía Incluida",
                                size="5",
                                color="white",
                                mb="3"
                            ),
                            rx.text(
                                "Ofrecemos garantía completa en todos nuestros servicios de reprogramación ECU.",
                                color="#666666",
                                line_height="1.6",
                                text_align="center"
                            ),
                            spacing="2",
                            align="center"
                        ),
                        bg="#2D2D2D",
                        border_radius="15px",
                        p="8",
                        border="1px solid #666666",
                        _hover={
                            "transform": "translateY(-10px)",
                            "box_shadow": "0 8px 15px rgba(0, 0, 0, 0.2)"
                        },
                        transition="all 0.3s ease",
                        cursor="pointer"
                    ),
                    
                    columns={"base": "1", "md": "2", "lg": "4"},
                    spacing="6",
                    width="100%"
                ),
                spacing="8",
                align="center"
            ),
            max_width="1200px",
            px="6",
            py="20"
        ),
        bg="#1A1A1A"
    )
