"""
Componente Contact - Formulario de contacto con validación y estilo moderno
========================================================================

Formulario estilizado con información de contacto y validación.
"""

import reflex as rx

class ContactState(rx.State):
    """Estado del formulario de contacto"""
    name: str = ""
    email: str = ""
    phone: str = ""
    message: str = ""
    is_loading: bool = False
    show_success: bool = False
    
    def submit_form(self):
        self.is_loading = True
        # Simular envío del formulario
        yield rx.sleep(1)
        self.is_loading = False
        self.show_success = True
        # Limpiar formulario
        self.name = ""
        self.email = ""
        self.phone = ""
        self.message = ""
        yield rx.sleep(3)
        self.show_success = False

def contact() -> rx.Component:
    """Sección de contacto reorganizada: info izquierda, formulario derecha"""
    return rx.box(
        rx.container(
            rx.center(
                rx.vstack(
                rx.heading(
                    "Contacto",
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
                        # Columna izquierda: Información de contacto
                        rx.box(
                            rx.vstack(
                                rx.vstack(
                                    rx.hstack(
                                        rx.icon("map-pin", size=24, color="#FF6B35"),
                                        rx.heading(
                                            "Ubicación",
                                            size="4",
                                            color="#FF6B35",
                                            font_weight="600"
                                        ),
                                        spacing="3",
                                        align="center"
                                    ),
                                    rx.text(
                                        "Calle del Motor, 123\n28001 Madrid, España",
                                        color="#CCCCCC",
                                        line_height="1.7",
                                        font_size="0.95rem"
                                    ),
                                    spacing="3",
                                    align="start"
                                ),
                                rx.vstack(
                                    rx.hstack(
                                        rx.icon("phone", size=24, color="#FF6B35"),
                                        rx.heading(
                                            "Teléfono",
                                            size="4",
                                            color="#FF6B35",
                                            font_weight="600"
                                        ),
                                        spacing="3",
                                        align="center"
                                    ),
                                    rx.text(
                                        "+34 91 123 45 67",
                                        color="#CCCCCC",
                                        line_height="1.7",
                                        font_size="0.95rem"
                                    ),
                                    spacing="3",
                                    align="start"
                                ),
                                rx.vstack(
                                    rx.hstack(
                                        rx.icon("mail", size=24, color="#FF6B35"),
                                        rx.heading(
                                            "Email",
                                            size="4",
                                            color="#FF6B35",
                                            font_weight="600"
                                        ),
                                        spacing="3",
                                        align="center"
                                    ),
                                    rx.text(
                                        "info@astrotech.com",
                                        color="#CCCCCC",
                                        line_height="1.7",
                                        font_size="0.95rem"
                                    ),
                                    spacing="3",
                                    align="start"
                                ),
                                rx.vstack(
                                    rx.hstack(
                                        rx.icon("clock", size=24, color="#FF6B35"),
                                        rx.heading(
                                            "Horarios",
                                            size="4",
                                            color="#FF6B35",
                                            font_weight="600"
                                        ),
                                        spacing="3",
                                        align="center"
                                    ),
                                    rx.text(
                                        "Lunes - Viernes: 9:00 - 18:00\nSábados: 9:00 - 14:00",
                                        color="#CCCCCC",
                                        line_height="1.7",
                                        font_size="0.95rem"
                                    ),
                                    spacing="3",
                                    align="start"
                                ),
                                spacing="8",
                                align="start",
                                height="100%",
                                justify="start"
                            ),
                            bg="#2D2D2D",
                            border_radius="20px",
                            p="10",
                            border="1px solid #404040",
                            height="100%",
                            min_height="500px"
                        ),
                        
                        # Columna derecha: Formulario de contacto
                        rx.box(
                            rx.cond(
                                ContactState.show_success,
                                rx.center(
                                    rx.vstack(
                                        rx.icon("check_check", size=60, color="#FF6B35"),
                                        rx.heading(
                                            "¡Mensaje enviado!",
                                            size="5",
                                            color="#FF6B35",
                                            text_align="center"
                                        ),
                                        rx.text(
                                            "Te contactaremos pronto.",
                                            color="#CCCCCC",
                                            text_align="center"
                                        ),
                                        spacing="4",
                                        align="center"
                                    ),
                                    height="100%"
                                ),
                                rx.form(
                                    rx.vstack(
                                        rx.input(
                                            placeholder="Nombre completo",
                                            value=ContactState.name,
                                            on_change=ContactState.set_name,
                                            bg="#1A1A1A",
                                            border="2px solid #404040",
                                            border_radius="10px",
                                            color="white",
                                            p="4",
                                            font_size="0.95rem",
                                            _focus={
                                                "border_color": "#FF6B35",
                                                "outline": "none",
                                                "box_shadow": "0 0 0 3px rgba(255, 107, 53, 0.1)"
                                            },
                                            _placeholder={"color": "#999999"},
                                            transition="all 0.3s ease",
                                            required=True
                                        ),
                                        rx.input(
                                            placeholder="Email",
                                            type="email",
                                            value=ContactState.email,
                                            on_change=ContactState.set_email,
                                            bg="#1A1A1A",
                                            border="2px solid #404040",
                                            border_radius="10px",
                                            color="white",
                                            p="4",
                                            font_size="0.95rem",
                                            _focus={
                                                "border_color": "#FF6B35",
                                                "outline": "none",
                                                "box_shadow": "0 0 0 3px rgba(255, 107, 53, 0.1)"
                                            },
                                            _placeholder={"color": "#999999"},
                                            transition="all 0.3s ease",
                                            required=True
                                        ),
                                        rx.input(
                                            placeholder="Teléfono",
                                            type="tel",
                                            value=ContactState.phone,
                                            on_change=ContactState.set_phone,
                                            bg="#1A1A1A",
                                            border="2px solid #404040",
                                            border_radius="10px",
                                            color="white",
                                            p="4",
                                            font_size="0.95rem",
                                            _focus={
                                                "border_color": "#FF6B35",
                                                "outline": "none",
                                                "box_shadow": "0 0 0 3px rgba(255, 107, 53, 0.1)"
                                            },
                                            _placeholder={"color": "#999999"},
                                            transition="all 0.3s ease"
                                        ),
                                        rx.text_area(
                                            placeholder="Mensaje",
                                            value=ContactState.message,
                                            on_change=ContactState.set_message,
                                            bg="#1A1A1A",
                                            border="2px solid #404040",
                                            border_radius="10px",
                                            color="white",
                                            p="4",
                                            font_size="0.95rem",
                                            rows="6",
                                            resize="vertical",
                                            _focus={
                                                "border_color": "#FF6B35",
                                                "outline": "none",
                                                "box_shadow": "0 0 0 3px rgba(255, 107, 53, 0.1)"
                                            },
                                            _placeholder={"color": "#999999"},
                                            transition="all 0.3s ease",
                                            required=True
                                        ),
                                        rx.button(
                                            rx.cond(
                                                ContactState.is_loading,
                                                rx.hstack(
                                                    rx.spinner(size="1", color="white"),
                                                    rx.text("Enviando...", color="white"),
                                                    spacing="3",
                                                    align="center"
                                                ),
                                                "Enviar Mensaje"
                                            ),
                                            bg="#FF6B35",
                                            color="white",
                                            border_radius="10px",
                                            p="4",
                                            font_weight="600",
                                            font_size="1rem",
                                            width="100%",
                                            _hover={
                                                "bg": "#e55a2b",
                                                "transform": "translateY(-2px)",
                                                "box_shadow": "0 8px 20px rgba(255, 107, 53, 0.3)"
                                            },
                                            transition="all 0.3s ease",
                                            disabled=ContactState.is_loading,
                                            type="submit"
                                        ),
                                        spacing="5",
                                        width="100%"
                                    ),
                                    on_submit=ContactState.submit_form,
                                    width="100%"
                                )
                            ),
                            bg="#2D2D2D",
                            border_radius="20px",
                            p="10",
                            border="1px solid #404040",
                            height="100%",
                            min_height="500px"
                        ),
                        
                        columns={"base": "1", "lg": "2"},
                        spacing="6",
                        width="100%",
                        class_name="fade-in-up",
                        justify="center",
                        max_width="1000px",
                        mx="auto"
                    ),
                    width="100%",
                    mx="auto"
                ),
                    spacing="6",
                    align="center",
                    width="100%",
                    max_width="1000px"
                ),
                width="100%"
            ),
            max_width="1200px",
            px={"base": "6", "md": "8"},
            py={"base": "16", "md": "24"},
            mx="auto"
        ),
        bg="#1A1A1A",
        id="contacto"
    )
