"""
Componente Footer - Pie de página moderno con enlaces y redes sociales
====================================================================

Footer completo con información de la empresa y enlaces estilizados.
"""

import reflex as rx

def footer() -> rx.Component:
    """Footer completo con secciones organizadas"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.grid(
                    # Sección de información de la empresa
                    rx.vstack(
                        rx.heading(
                            "AstroTech",
                            size="5",
                            color="#FF6B35",
                            mb="4"
                        ),
                        rx.text(
                            "Especialistas en reprogramación ECU con más de 10 años de experiencia. Potencia tu vehículo de forma segura y profesional.",
                            color="white",
                            line_height="1.6"
                        ),
                        spacing="3",
                        align="start"
                    ),
                    
                    # Sección de servicios
                    rx.vstack(
                        rx.heading(
                            "Servicios",
                            size="4",
                            color="#FF6B35",
                            mb="4"
                        ),
                        rx.vstack(
                            rx.link(
                                "Reprogramación ECU",
                                href="/services",
                                color="white",
                                _hover={"color": "#FF6B35"},
                                transition="color 0.3s ease"
                            ),
                            rx.link(
                                "Diagnóstico",
                                href="/services",
                                color="white",
                                _hover={"color": "#FF6B35"},
                                transition="color 0.3s ease"
                            ),
                            rx.link(
                                "Backup Original",
                                href="/services",
                                color="white",
                                _hover={"color": "#FF6B35"},
                                transition="color 0.3s ease"
                            ),
                            rx.link(
                                "Soporte Técnico",
                                href="/services",
                                color="white",
                                _hover={"color": "#FF6B35"},
                                transition="color 0.3s ease"
                            ),
                            spacing="2",
                            align="start"
                        ),
                        spacing="3",
                        align="start"
                    ),
                    
                    # Sección de enlaces de navegación
                    rx.vstack(
                        rx.heading(
                            "Enlaces",
                            size="4",
                            color="#FF6B35",
                            mb="4"
                        ),
                        rx.vstack(
                            rx.link(
                                "Inicio",
                                href="/",
                                color="white",
                                _hover={"color": "#FF6B35"},
                                transition="color 0.3s ease"
                            ),
                            rx.link(
                                "Acerca de",
                                href="/about",
                                color="white",
                                _hover={"color": "#FF6B35"},
                                transition="color 0.3s ease"
                            ),
                            rx.link(
                                "Contacto",
                                href="/contact",
                                color="white",
                                _hover={"color": "#FF6B35"},
                                transition="color 0.3s ease"
                            ),
                            rx.link(
                                "Beneficios",
                                href="/#beneficios",
                                color="white",
                                _hover={"color": "#FF6B35"},
                                transition="color 0.3s ease"
                            ),
                            spacing="2",
                            align="start"
                        ),
                        spacing="3",
                        align="start"
                    ),
                    
                    # Sección de redes sociales
                    rx.vstack(
                        rx.heading(
                            "Redes Sociales",
                            size="4",
                            color="#FF6B35",
                            mb="4"
                        ),
                        rx.hstack(
                            rx.link(
                                rx.icon("facebook", size=24, color="white"),
                                href="https://facebook.com",
                                _hover={
                                    "transform": "translateY(-3px)",
                                    "color": "#1877F2"
                                },
                                transition="all 0.3s ease"
                            ),
                            rx.link(
                                rx.icon("instagram", size=24, color="white"),
                                href="https://instagram.com",
                                _hover={
                                    "transform": "translateY(-3px)",
                                    "color": "#E4405F"
                                },
                                transition="all 0.3s ease"
                            ),
                            rx.link(
                                rx.icon("youtube", size=24, color="white"),
                                href="https://youtube.com",
                                _hover={
                                    "transform": "translateY(-3px)",
                                    "color": "#FF0000"
                                },
                                transition="all 0.3s ease"
                            ),
                            rx.link(
                                rx.icon("twitter", size=24, color="white"),
                                href="https://twitter.com",
                                _hover={
                                    "transform": "translateY(-3px)",
                                    "color": "#1DA1F2"
                                },
                                transition="all 0.3s ease"
                            ),
                            spacing="6"
                        ),
                        spacing="3",
                        align="start"
                    ),
                    
                    columns={"base": "1", "md": "2", "lg": "4"},
                    spacing="8",
                    width="100%",
                    mb="8"
                ),
                
                # Línea de separación y copyright
                rx.box(
                    rx.text(
                        "© 2025 AstroTech. Todos los derechos reservados.",
                        color="#666666",
                        text_align="center"
                    ),
                    border_top="1px solid #666666",
                    pt="6",
                    width="100%"
                ),
                
                spacing="6",
                align="center"
            ),
            max_width="1200px",
            px="6",
            py="16"
        ),
        bg="#2D2D2D",
        color="white"
    )