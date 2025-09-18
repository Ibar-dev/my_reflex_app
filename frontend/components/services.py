"""
Componente Services - Sección de servicios con estilo moderno
==========================================================

Tarjetas de servicios con efectos hover y diseño profesional.
"""

import reflex as rx

def services() -> rx.Component:
    """Sección de servicios con tarjetas estilizadas y centrado mejorado"""
    return rx.center(
        rx.container(
            rx.vstack(
                rx.heading(
                    "Nuestros Servicios",
                    size="8",
                    color="white",
                    text_align="center",
                    mb="16",
                    font_weight="700",
                    bg_image="linear-gradient(45deg, #FF6B35, #FF8C42)",
                    bg_clip="text",
                    text_fill_color="transparent",
                ),
                rx.center(
                    rx.grid(
                        # Servicio 1: Reprogramación ECU
                        rx.box(
                            rx.vstack(
                                rx.heading(
                                    "Reprogramación ECU",
                                    size="5",
                                    color="#FF6B35",
                                    mb="6",
                                    text_align="center"
                                ),
                                rx.text(
                                    "Optimización completa del software del motor para maximizar el rendimiento y eficiencia.",
                                    color="#CCCCCC",
                                    line_height="1.7",
                                    text_align="center",
                                    font_size="0.95rem"
                                ),
                                spacing="4",
                                align="center",
                                height="100%",
                                justify="center"
                            ),
                            bg="#2D2D2D",
                            border_radius="20px",
                            p="12",
                            border="1px solid #404040",
                            box_shadow="0 8px 20px rgba(0, 0, 0, 0.25)",
                            min_height="200px",
                            _hover={
                                "transform": "translateY(-8px)",
                                "box_shadow": "0 12px 30px rgba(255, 107, 53, 0.2)",
                                "border_color": "#FF6B35"
                            },
                            transition="all 0.4s ease",
                            class_name="hover-raise fade-in-up"
                        ),
                        
                        # Servicio 2: Diagnóstico Avanzado
                        rx.box(
                            rx.vstack(
                                rx.heading(
                                    "Diagnóstico Avanzado",
                                    size="5",
                                    color="#FF6B35",
                                    mb="6",
                                    text_align="center"
                                ),
                                rx.text(
                                    "Análisis completo del sistema de gestión del motor antes de cualquier modificación.",
                                    color="#CCCCCC",
                                    line_height="1.7",
                                    text_align="center",
                                    font_size="0.95rem"
                                ),
                                spacing="4",
                                align="center",
                                height="100%",
                                justify="center"
                            ),
                            bg="#2D2D2D",
                            border_radius="20px",
                            p="12",
                            border="1px solid #404040",
                            box_shadow="0 8px 20px rgba(0, 0, 0, 0.25)",
                            min_height="200px",
                            _hover={
                                "transform": "translateY(-8px)",
                                "box_shadow": "0 12px 30px rgba(255, 107, 53, 0.2)",
                                "border_color": "#FF6B35"
                            },
                            transition="all 0.4s ease"
                        ),
                        
                        # Servicio 3: Backup Original
                        rx.box(
                            rx.vstack(
                                rx.heading(
                                    "Backup Original",
                                    size="5",
                                    color="#FF6B35",
                                    mb="6",
                                    text_align="center"
                                ),
                                rx.text(
                                    "Guardamos una copia de seguridad de la configuración original de tu vehículo.",
                                    color="#CCCCCC",
                                    line_height="1.7",
                                    text_align="center",
                                    font_size="0.95rem"
                                ),
                                spacing="4",
                                align="center",
                                height="100%",
                                justify="center"
                            ),
                            bg="#2D2D2D",
                            border_radius="20px",
                            p="12",
                            border="1px solid #404040",
                            box_shadow="0 8px 20px rgba(0, 0, 0, 0.25)",
                            min_height="200px",
                            _hover={
                                "transform": "translateY(-8px)",
                                "box_shadow": "0 12px 30px rgba(255, 107, 53, 0.2)",
                                "border_color": "#FF6B35"
                            },
                            transition="all 0.4s ease"
                        ),
                        
                        # Servicio 4: Soporte Técnico
                        rx.box(
                            rx.vstack(
                                rx.heading(
                                    "Soporte Técnico",
                                    size="5",
                                    color="#FF6B35",
                                    mb="6",
                                    text_align="center"
                                ),
                                rx.text(
                                    "Asistencia técnica especializada durante todo el proceso y posterior seguimiento.",
                                    color="#CCCCCC",
                                    line_height="1.7",
                                    text_align="center",
                                    font_size="0.95rem"
                                ),
                                spacing="4",
                                align="center",
                                height="100%",
                                justify="center"
                            ),
                            bg="#2D2D2D",
                            border_radius="20px",
                            p="12",
                            border="1px solid #404040",
                            box_shadow="0 8px 20px rgba(0, 0, 0, 0.25)",
                            min_height="200px",
                            _hover={
                                "transform": "translateY(-8px)",
                                "box_shadow": "0 12px 30px rgba(255, 107, 53, 0.2)",
                                "border_color": "#FF6B35"
                            },
                            transition="all 0.4s ease"
                        ),
                        
                        columns={"base": "1", "md": "2", "lg": "4"},
                        spacing="8",
                        width="100%",
                        class_name="fade-in-up",
                        justify="center",
                        max_width="1200px",
                        mx="auto"
                    ),
                    width="100%",
                    mx="auto"
                ),
                spacing="6",
                align="center",
                width="100%",
                max_width="1200px"
            ),
            max_width="1400px",
            px={"base": "6", "md": "8"},
            py={"base": "16", "md": "24"},
            mx="auto"
        ),
        width="100%",
        bg="#1A1A1A"
    )
