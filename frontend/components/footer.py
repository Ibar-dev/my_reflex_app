"""
Componente Footer - Pie de página moderno con enlaces y redes sociales
====================================================================

Footer completo con información de la empresa y enlaces estilizados.
"""

import reflex as rx

def footer() -> rx.Component:
    """Footer moderno con secciones organizadas y diseño coherente"""
    return rx.box(
        # Fondo con patrón de puntos y degradado para efecto visual
        rx.box(
            position="absolute",
            top="0",
            left="0",
            right="0",
            bottom="0",
            bg="radial-gradient(circle at 70% 80%, rgba(255, 107, 53, 0.03) 0%, rgba(30, 30, 30, 0) 70%)",
            z_index="0",
            # Patrón de puntos
            _after={
                "content": "''",
                "position": "absolute",
                "top": "0",
                "right": "0",
                "bottom": "0",
                "left": "0",
                "background": "radial-gradient(circle, rgba(255, 255, 255, 0.03) 1px, transparent 1px)",
                "background_size": "20px 20px",
                "z_index": "1",
                "opacity": "0.5",
            },
        ),
        rx.container(
            rx.box(
                rx.vstack(
                rx.grid(
                    # Sección de información de la empresa
                    rx.vstack(
                        rx.heading(
                            "AstroTech",
                            size="5",
                            color="white",
                            mb="4",
                            bg_image="linear-gradient(45deg, #FF6B35, #FF8C42)",
                            bg_clip="text",
                            text_fill_color="transparent",
                            font_weight="700",
                            class_name="fade-in-up",
                        ),
                        rx.text(
                            "Especialistas en reprogramación ECU con más de 10 años de experiencia. Potencia tu vehículo de forma segura y profesional.",
                            color="rgba(255, 255, 255, 0.8)",
                            line_height="1.7",
                            font_size="1rem",
                            class_name="fade-in-up",
                            animation_delay="0.1s",
                        ),
                        spacing="4",
                        align="start",
                        class_name="fade-in-up",
                    ),
                    
                    # Sección de servicios
                    rx.vstack(
                        rx.heading(
                            "Servicios",
                            size="4",
                            color="white",
                            mb="6",
                            font_weight="600",
                            class_name="fade-in-up",
                            animation_delay="0.2s",
                        ),
                        rx.vstack(
                            rx.link(
                                rx.hstack(
                                    rx.icon("arrow-right", size=14, color="#FF6B35"),
                                    rx.text("Reprogramación ECU"),
                                    spacing="2",
                                ),
                                href="/services",
                                color="white",
                                _hover={
                                    "color": "#FF6B35",
                                    "transform": "translateX(5px)"
                                },
                                transition="all 0.3s ease",
                                class_name="fade-in-up",
                                animation_delay="0.3s",
                            ),
                            rx.link(
                                rx.hstack(
                                    rx.icon("arrow-right", size=14, color="#FF6B35"),
                                    rx.text("Diagnóstico"),
                                    spacing="2",
                                ),
                                href="/services",
                                color="white",
                                _hover={
                                    "color": "#FF6B35",
                                    "transform": "translateX(5px)"
                                },
                                transition="all 0.3s ease",
                                class_name="fade-in-up",
                                animation_delay="0.4s",
                            ),
                            rx.link(
                                rx.hstack(
                                    rx.icon("arrow-right", size=14, color="#FF6B35"),
                                    rx.text("Backup Original"),
                                    spacing="2",
                                ),
                                href="/services",
                                color="white",
                                _hover={
                                    "color": "#FF6B35",
                                    "transform": "translateX(5px)"
                                },
                                transition="all 0.3s ease",
                                class_name="fade-in-up",
                                animation_delay="0.5s",
                            ),
                            rx.link(
                                rx.hstack(
                                    rx.icon("arrow-right", size=14, color="#FF6B35"),
                                    rx.text("Soporte Técnico"),
                                    spacing="2",
                                ),
                                href="/services",
                                color="white",
                                _hover={
                                    "color": "#FF6B35",
                                    "transform": "translateX(5px)"
                                },
                                transition="all 0.3s ease",
                                class_name="fade-in-up",
                                animation_delay="0.6s",
                            ),
                            spacing="4",
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
                            color="white",
                            mb="6",
                            font_weight="600",
                            class_name="fade-in-up",
                            animation_delay="0.2s",
                        ),
                        rx.vstack(
                            rx.link(
                                rx.hstack(
                                    rx.icon("arrow-right", size=14, color="#FF6B35"),
                                    rx.text("Inicio"),
                                    spacing="2",
                                ),
                                href="/#inicio",
                                color="white",
                                _hover={
                                    "color": "#FF6B35",
                                    "transform": "translateX(5px)"
                                },
                                transition="all 0.3s ease",
                                class_name="fade-in-up",
                                animation_delay="0.3s",
                            ),
                            rx.link(
                                rx.hstack(
                                    rx.icon("arrow-right", size=14, color="#FF6B35"),
                                    rx.text("Acerca de"),
                                    spacing="2",
                                ),
                                href="/#acerca",
                                color="white",
                                _hover={
                                    "color": "#FF6B35",
                                    "transform": "translateX(5px)"
                                },
                                transition="all 0.3s ease",
                                class_name="fade-in-up",
                                animation_delay="0.4s",
                            ),
                            rx.link(
                                rx.hstack(
                                    rx.icon("arrow-right", size=14, color="#FF6B35"),
                                    rx.text("Contacto"),
                                    spacing="2",
                                ),
                                href="/#contacto",
                                color="white",
                                _hover={
                                    "color": "#FF6B35",
                                    "transform": "translateX(5px)"
                                },
                                transition="all 0.3s ease",
                                class_name="fade-in-up",
                                animation_delay="0.5s",
                            ),
                            rx.link(
                                rx.hstack(
                                    rx.icon("arrow-right", size=14, color="#FF6B35"),
                                    rx.text("Beneficios"),
                                    spacing="2",
                                ),
                                href="/#beneficios",
                                color="white",
                                _hover={
                                    "color": "#FF6B35",
                                    "transform": "translateX(5px)"
                                },
                                transition="all 0.3s ease",
                                class_name="fade-in-up",
                                animation_delay="0.6s",
                            ),
                            spacing="4",
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
                            color="white",
                            mb="6",
                            font_weight="600",
                            class_name="fade-in-up",
                            animation_delay="0.2s",
                        ),
                        rx.hstack(
                            rx.link(
                                rx.box(
                                    rx.icon("facebook", size=24, color="white"),
                                    bg="linear-gradient(145deg, #252525, #1e1e1e)",
                                    p="3",
                                    border_radius="full",
                                    box_shadow="0 4px 10px rgba(0, 0, 0, 0.2)",
                                ),
                                href="https://facebook.com",
                                _hover={
                                    "transform": "translateY(-5px)",
                                    "color": "#1877F2"
                                },
                                transition="all 0.3s ease",
                                class_name="fade-in-up",
                                animation_delay="0.3s",
                            ),
                            rx.link(
                                rx.box(
                                    rx.icon("instagram", size=24, color="white"),
                                    bg="linear-gradient(145deg, #252525, #1e1e1e)",
                                    p="3",
                                    border_radius="full",
                                    box_shadow="0 4px 10px rgba(0, 0, 0, 0.2)",
                                ),
                                href="https://instagram.com",
                                _hover={
                                    "transform": "translateY(-5px)",
                                    "color": "#E4405F"
                                },
                                transition="all 0.3s ease",
                                class_name="fade-in-up",
                                animation_delay="0.4s",
                            ),
                            rx.link(
                                rx.box(
                                    rx.icon("youtube", size=24, color="white"),
                                    bg="linear-gradient(145deg, #252525, #1e1e1e)",
                                    p="3",
                                    border_radius="full",
                                    box_shadow="0 4px 10px rgba(0, 0, 0, 0.2)",
                                ),
                                href="https://youtube.com",
                                _hover={
                                    "transform": "translateY(-5px)",
                                    "color": "#FF0000"
                                },
                                transition="all 0.3s ease",
                                class_name="fade-in-up",
                                animation_delay="0.5s",
                            ),
                            rx.link(
                                rx.box(
                                    rx.icon("twitter", size=24, color="white"),
                                    bg="linear-gradient(145deg, #252525, #1e1e1e)",
                                    p="3",
                                    border_radius="full",
                                    box_shadow="0 4px 10px rgba(0, 0, 0, 0.2)",
                                ),
                                href="https://twitter.com",
                                _hover={
                                    "transform": "translateY(-5px)",
                                    "color": "#1DA1F2"
                                },
                                transition="all 0.3s ease",
                                class_name="fade-in-up",
                                animation_delay="0.6s",
                            ),
                            spacing="4"
                        ),
                        spacing="3",
                        align="start"
                    ),
                    
                    columns={"base": "1", "md": "2", "lg": "4"},
                    spacing="8",
                    width="100%",
                    mb="10",
                    p="6",
                ),
                
                # Línea de separación y copyright con diseño mejorado
                rx.box(
                    rx.hstack(
                        rx.text(
                            "© 2025 AstroTech.",
                            font_weight="500",
                            color="#FF6B35",
                            class_name="fade-in",
                        ),
                        rx.text(
                            "Todos los derechos reservados.",
                            color="rgba(255, 255, 255, 0.6)",
                            class_name="fade-in",
                            animation_delay="0.1s",
                        ),
                        justify="center",
                        spacing="2",
                    ),
                    border_top="1px solid rgba(255, 255, 255, 0.1)",
                    pt="8",
                    mt="4",
                    width="100%",
                ),
                
                spacing="8",
                align="center",
                width="100%"
                ),
                bg="linear-gradient(145deg, #1e1e1e, #212121)",
                border_radius="30px",
                border="1px solid #353535",
                overflow="hidden",
                padding="10",
                box_shadow="0 15px 40px rgba(0, 0, 0, 0.3)",
                class_name="card-shadow",
                position="relative",
                z_index="2",
            ),
            max_width="1400px",
            px="6",
            py="16",
            mx="auto"
        ),
        bg="linear-gradient(to bottom, #202020, #121212)",
        color="white",
        padding_top="8",
        position="relative",
        border_radius="30px 30px 0 0",
        overflow="hidden",
        margin_top="50px"
    )