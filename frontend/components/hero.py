"""
Componente Hero - Sección principal con título, texto, CTA e imagen
===================================================================

Se inspira en la maqueta HTML/CSS y utiliza componentes y estilos de Reflex
para un look moderno, limpio y responsivo.
"""

import reflex as rx


def hero() -> rx.Component:
    return rx.box(
        rx.container(
            rx.grid(
                # Columna izquierda: contenido de texto
                rx.vstack(
                    rx.heading(
                        "Potencia el coche de tus sueños", 
                        size="8", 
                        color="white",
                        font_weight="800",
                        line_height="1.2",
                        mb="4"
                    ),
                    rx.text(
                        "Reprogramación ECU profesional para maximizar el rendimiento de tu vehículo sin comprometer su fiabilidad.",
                        color="#CCCCCC",
                        font_size="1.1rem",
                        mb="8"
                    ),
                    rx.button(
                        "Selecciona tu vehículo",
                        size="3",
                        px="8",
                        py="6",
                        bg="#FF6B35",
                        color="white",
                        _hover={"bg": "#FF5A1F"},
                        on_click=rx.redirect("/#selector")
                    ),
                    spacing="6",
                    align="start",
                    justify="center",
                    height="100%",
                    padding_y="2rem",
                    class_name="fade-in-up"
                ),
                # Columna derecha: imagen
                rx.box(
                    rx.image(
                        src="/centralita-coche.jpg", 
                        width="100%", 
                        height="auto",
                        border_radius="20px",
                        box_shadow="0 10px 30px rgba(0, 0, 0, 0.3)"
                    ),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    height="100%",
                    padding_y="2rem",
                    class_name="hero-image fade-in-up"
                ),
                columns={"base": "1", "md": "2"},
                spacing="8",
                width="100%",
                height="100%"
            ),
            max_width="1200px",
            height="100%"
        ),
        bg="linear-gradient(45deg, #1A1A1A 0%, #2D2D2D 100%)",
        padding_x="1rem",
        padding_y="4rem",
        width="100%",
        class_name="parallax-section"
    )
