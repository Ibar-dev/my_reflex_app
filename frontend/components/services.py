"""
Componente Services - Sección de servicios con estilo moderno
==========================================================

Tarjetas de servicios con efectos hover y diseño profesional.
"""

import reflex as rx

def services() -> rx.Component:
    """Sección de servicios con tarjetas estilizadas"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading(
                    "Nuestros Servicios",
                    size="8",
                    color="white",
                    text_align="center",
                    mb="12"
                ),
                rx.grid(
                    # Servicio 1: Reprogramación ECU
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Reprogramación ECU",
                                size="5",
                                color="#FF6B35",
                                mb="4"
                            ),
                            rx.text(
                                "Optimización completa del software del motor para maximizar el rendimiento y eficiencia.",
                                color="#666666",
                                line_height="1.6"
                            ),
                            spacing="3",
                            align="start"
                        ),
                        bg="#1A1A1A",
                        border_radius="15px",
                        p="8",
                        border="1px solid #666666",
                        box_shadow="0 4px 6px rgba(0, 0, 0, 0.1)",
                        _hover={
                            "transform": "translateY(-5px)",
                            "box_shadow": "0 8px 15px rgba(0, 0, 0, 0.2)"
                        },
                        transition="all 0.3s ease"
                    ),
                    
                    # Servicio 2: Diagnóstico Avanzado
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Diagnóstico Avanzado",
                                size="5",
                                color="#FF6B35",
                                mb="4"
                            ),
                            rx.text(
                                "Análisis completo del sistema de gestión del motor antes de cualquier modificación.",
                                color="#666666",
                                line_height="1.6"
                            ),
                            spacing="3",
                            align="start"
                        ),
                        bg="#1A1A1A",
                        border_radius="15px",
                        p="8",
                        border="1px solid #666666",
                        box_shadow="0 4px 6px rgba(0, 0, 0, 0.1)",
                        _hover={
                            "transform": "translateY(-5px)",
                            "box_shadow": "0 8px 15px rgba(0, 0, 0, 0.2)"
                        },
                        transition="all 0.3s ease"
                    ),
                    
                    # Servicio 3: Backup Original
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Backup Original",
                                size="5",
                                color="#FF6B35",
                                mb="4"
                            ),
                            rx.text(
                                "Guardamos una copia de seguridad de la configuración original de tu vehículo.",
                                color="#666666",
                                line_height="1.6"
                            ),
                            spacing="3",
                            align="start"
                        ),
                        bg="#1A1A1A",
                        border_radius="15px",
                        p="8",
                        border="1px solid #666666",
                        box_shadow="0 4px 6px rgba(0, 0, 0, 0.1)",
                        _hover={
                            "transform": "translateY(-5px)",
                            "box_shadow": "0 8px 15px rgba(0, 0, 0, 0.2)"
                        },
                        transition="all 0.3s ease"
                    ),
                    
                    # Servicio 4: Soporte Técnico
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Soporte Técnico",
                                size="5",
                                color="#FF6B35",
                                mb="4"
                            ),
                            rx.text(
                                "Asistencia técnica especializada durante todo el proceso y posterior seguimiento.",
                                color="#666666",
                                line_height="1.6"
                            ),
                            spacing="3",
                            align="start"
                        ),
                        bg="#1A1A1A",
                        border_radius="15px",
                        p="8",
                        border="1px solid #666666",
                        box_shadow="0 4px 6px rgba(0, 0, 0, 0.1)",
                        _hover={
                            "transform": "translateY(-5px)",
                            "box_shadow": "0 8px 15px rgba(0, 0, 0, 0.2)"
                        },
                        transition="all 0.3s ease"
                    ),
                    
                    columns={"base": "1", "md": "2"},
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
        bg="#2D2D2D"
    )
