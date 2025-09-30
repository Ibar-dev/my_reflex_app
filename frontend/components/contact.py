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
    
    def handle_name_change(self, value: str):
        self.name = value
        
    def handle_email_change(self, value: str):
        self.email = value
        
    def handle_phone_change(self, value: str):
        self.phone = value
        
    def handle_message_change(self, value: str):
        self.message = value
    
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
        rx.center(
            rx.vstack(
                rx.heading(
                    "Contacto",
                    size="7",
                    color="#FF6B35",
                    text_align="center",
                    mb="12",
                    font_weight="700",
                ),
                rx.grid(
                    # Columna izquierda: Información de contacto
                    rx.box(
                        rx.vstack(
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("map-pin", size=20, color="#FF6B35"),
                                    rx.heading(
                                        "Ubicación",
                                        size="3",
                                        color="#FF6B35",
                                        font_weight="600"
                                    ),
                                    spacing="4",
                                    align="center"
                                ),
                                rx.text(
                                    "Calle del Motor, 123\n28001 Madrid, España",
                                    color="#CCCCCC",
                                    line_height="1.5",
                                    font_size="1.1rem"
                                ),
                                spacing="4",
                                align="start"
                            ),
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("phone", size=20, color="#FF6B35"),
                                    rx.heading(
                                        "Teléfono",
                                        size="3",
                                        color="#FF6B35",
                                        font_weight="600"
                                    ),
                                    spacing="4",
                                    align="center"
                                ),
                                rx.text(
                                    "+34 91 123 45 67",
                                    color="#CCCCCC",
                                    line_height="1.5",
                                    font_size="1.1rem"
                                ),
                                spacing="4",
                                align="start"
                            ),
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("mail", size=20, color="#FF6B35"),
                                    rx.heading(
                                        "Email",
                                        size="3",
                                        color="#FF6B35",
                                        font_weight="600"
                                    ),
                                    spacing="4",
                                    align="center"
                                ),
                                rx.text(
                                    "info@astrotech.com",
                                    color="#CCCCCC",
                                    line_height="1.5",
                                    font_size="1.1rem"
                                ),
                                spacing="4",
                                align="start"
                            ),
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("clock", size=20, color="#FF6B35"),
                                    rx.heading(
                                        "Horarios",
                                        size="3",
                                        color="#FF6B35",
                                        font_weight="600"
                                    ),
                                    spacing="4",
                                    align="center"
                                ),
                                rx.text(
                                    "Lunes - Viernes: 9:00 - 18:00\nSábados: 9:00 - 14:00",
                                    color="#CCCCCC",
                                    line_height="1.5",
                                    font_size="1.1rem"
                                ),
                                spacing="4",
                                align="start"
                            ),
                            spacing="9",
                            align="start",
                            height="100%",
                            justify="start"
                        ),
                        bg="#2D2D2D",
                        border_radius="20px",
                        padding="2rem",
                        border="1px solid #404040",
                        height="100%",
                        min_height="550px"
                    ),
                    
                    # Columna derecha: Formulario de contacto
                    rx.box(
                        rx.cond(
                            ContactState.show_success,
                            rx.center(
                                rx.vstack(
                                    rx.icon("check_check", size=50, color="#FF6B35"),
                                    rx.heading(
                                        "¡Mensaje enviado!",
                                        size="4",
                                        color="#FF6B35",
                                        text_align="center"
                                    ),
                                    rx.text(
                                        "Te contactaremos pronto.",
                                        color="#CCCCCC",
                                        text_align="center"
                                    ),
                                    spacing="3",
                                    align="center"
                                ),
                                height="100%"
                            ),
                            rx.form(
                                rx.vstack(
                                    rx.input(
                                        placeholder="Nombre completo",
                                        value=ContactState.name,
                                        on_change=ContactState.handle_name_change,
                                        name="name",
                                        bg="#1A1A1A",
                                        border="2px solid #404040",
                                        border_radius="8px",
                                        color="white",
                                        p="4",
                                        font_size="1rem",
                                        height="50px",
                                        width="100%",
                                        _focus={
                                            "border_color": "#FF6B35",
                                            "outline": "none",
                                            "box_shadow": "0 0 0 2px rgba(255, 107, 53, 0.2)"
                                        },
                                        _placeholder={"color": "#999999"},
                                        transition="all 0.3s ease",
                                        required=True
                                    ),
                                    rx.input(
                                        placeholder="Email",
                                        type="email",
                                        value=ContactState.email,
                                        on_change=ContactState.handle_email_change,
                                        name="email",
                                        bg="#1A1A1A",
                                        border="2px solid #404040",
                                        border_radius="8px",
                                        color="white",
                                        p="4",
                                        font_size="1rem",
                                        height="50px",
                                        width="100%",
                                        _focus={
                                            "border_color": "#FF6B35",
                                            "outline": "none",
                                            "box_shadow": "0 0 0 2px rgba(255, 107, 53, 0.2)"
                                        },
                                        _placeholder={"color": "#999999"},
                                        transition="all 0.3s ease",
                                        required=True
                                    ),
                                    rx.input(
                                        placeholder="Teléfono",
                                        type="tel",
                                        value=ContactState.phone,
                                        on_change=ContactState.handle_phone_change,
                                        name="phone",
                                        bg="#1A1A1A",
                                        border="2px solid #404040",
                                        border_radius="8px",
                                        color="white",
                                        p="4",
                                        font_size="1rem",
                                        height="50px",
                                        width="100%",
                                        _focus={
                                            "border_color": "#FF6B35",
                                            "outline": "none",
                                            "box_shadow": "0 0 0 2px rgba(255, 107, 53, 0.2)"
                                        },
                                        _placeholder={"color": "#999999"},
                                        transition="all 0.3s ease"
                                    ),
                                    rx.text_area(
                                        placeholder="Mensaje",
                                        value=ContactState.message,
                                        on_change=ContactState.handle_message_change,
                                        name="message",
                                        bg="#1A1A1A",
                                        border="2px solid #404040",
                                        border_radius="8px",
                                        color="white",
                                        p="4",
                                        font_size="1rem",
                                        rows="4",
                                        height="120px",
                                        width="100%",
                                        resize="vertical",
                                        _focus={
                                            "border_color": "#FF6B35",
                                            "outline": "none",
                                            "box_shadow": "0 0 0 2px rgba(255, 107, 53, 0.2)"
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
                                                spacing="4",
                                                align="center"
                                            ),
                                            "Enviar Mensaje"
                                        ),
                                        bg="#FF6B35",
                                        color="white",
                                        border_radius="8px",
                                        p="4",
                                        font_weight="600",
                                        font_size="1rem",
                                        height="50px",
                                        width="100%",
                                        _hover={
                                            "bg": "#e55a2b",
                                            "transform": "translateY(-1px)",
                                            "box_shadow": "0 4px 12px rgba(255, 107, 53, 0.3)"
                                        },
                                        transition="all 0.3s ease",
                                        disabled=ContactState.is_loading,
                                        type="submit"
                                    ),
                                    spacing="6",
                                    width="100%"
                                ),
                                on_submit=ContactState.submit_form,
                                width="100%"
                            )
                        ),
                        bg="#2D2D2D",
                        border_radius="20px",
                        padding="2rem",
                        border="1px solid #404040",
                        height="100%",
                        min_height="550px"
                    ),
                    
                    columns={"base": "1", "lg": "2"},
                    spacing="9",
                    width="100%",
                    max_width="1300px",
                    mx="auto"
                ),
                spacing="9",
                align="center",
                width="100%",
                max_width="1400px"
            ),
            width="100%",
            px={"base": "6", "md": "8"},
            py={"base": "20", "md": "32"},
        ),
        bg="#1A1A1A",
        id="contacto"
    )
