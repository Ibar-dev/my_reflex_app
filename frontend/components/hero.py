"""
Componente Hero - Sección principal con título, texto, CTA e imagen
===================================================================

Se inspira en la maqueta HTML/CSS y utiliza componentes y estilos de Reflex
para un look moderno, limpio y responsivo.
"""

import reflex as rx


def hero() -> rx.Component:
    return rx.box(
        # Fondo degradado y espacio para la barra fija
        rx.container(
            rx.grid(
                # Columna izquierda: contenido
                rx.vstack(
                    rx.heading(
                        "Potencia el coche de tus sueños",
                        color="white",
                        line_height="1.05",
                        letter_spacing="-0.8px",
                        font_size={"base": "2.8rem", "md": "3.6rem", "lg": "4.2rem"},
                        font_weight="800",
                        animation="fadeInUp 0.6s ease-out",
                    ),
                    rx.text(
                        "Reprogramación profesional de ECU para aumentar la potencia y reducir el consumo de combustible. Servicio garantizado con más de 10 años de experiencia.",
                        color="rgba(255,255,255,0.88)",
                        font_size={"base": "1rem", "md": "1.05rem", "lg": "1.08rem"},
                        line_height="1.7",
                        max_width="56ch",
                        animation="fadeInUp 0.7s ease-out",
                    ),
                    rx.hstack(
                        rx.link(
                            rx.button(
                                "SELECCIONA TU VEHÍCULO",
                                bg="#FF6B35",
                                color="white",
                                size="3",
                                border_radius="10px",
                                px="18px",
                                _hover={"bg": "#e55a2b", "transform": "translateY(-2px)"},
                                transition="all 0.2s ease",
                            ),
                            href="/services",  # Temporal hasta tener el selector
                            _hover={"text_decoration": "none"},
                        ),
                        mt="5",
                        animation="fadeInUp 0.8s ease-out",
                    ),
                    spacing="6",
                    align="start",
                    max_width="640px",
                ),
                # Columna derecha: placeholder en blanco para imagen futura
                rx.box(
                    width="100%",
                    height={"base": "280px", "md": "340px", "lg": "380px"},
                    bg="#2D2D2D",
                    border_radius="20px",
                    box_shadow="0 20px 40px rgba(255, 107, 53, 0.25)",
                    class_name="hero-image",
                ),
                columns={"base": "1", "md": "1", "lg": "2"},
                gap={"base": "8", "lg": "12"},
                align="center",
            ),
            max_width="1200px",
            px={"base": "20px", "md": "24px"},
            py={"base": "16", "md": "18", "lg": "24"},
            min_height={"lg": "560px"},
        ),
        bg="linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%)",
        pt="90px",  # separa del header fijo
    )
