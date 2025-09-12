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
    """Sección de contacto con formulario e información"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading(
                    "Contacto",
                    size="8",
                    color="white",
                    text_align="center",
                    mb="12"
                ),
                rx.grid(
                    # Información de contacto
                    rx.vstack(
                        rx.box(
                            rx.heading(
                                "📍 Ubicación",
                                size="4",
                                color="#FF6B35",
                                mb="2"
                            ),
                            rx.text(
                                "Calle del Motor, 123\n28001 Madrid, España",
                                color="#666666",
                                line_height="1.6"
                            ),
                            mb="6"
                        ),
                        rx.box(
                            rx.heading(
                                "📞 Teléfono",
                                size="4",
                                color="#FF6B35",
                                mb="2"
                            ),
                            rx.text(
                                "+34 91 123 45 67",
                                color="#666666",
                                line_height="1.6"
                            ),
                            mb="6"
                        ),
                        rx.box(
                            rx.heading(
                                "✉️ Email",
                                size="4",
                                color="#FF6B35",
                                mb="2"
                            ),
                            rx.text(
                                "info@astrotech.com",
                                color="#666666",
                                line_height="1.6"
                            ),
                            mb="6"
                        ),
                        rx.box(
                            rx.heading(
                                "🕒 Horarios",
                                size="4",
                                color="#FF6B35",
                                mb="2"
                            ),
                            rx.text(
                                "Lunes - Viernes: 9:00 - 18:00\nSábados: 9:00 - 14:00",
                                color="#666666",
                                line_height="1.6"
                            )
                        ),
                        spacing="4",
                        align="start"
                    ),
                    
                    # Formulario de contacto
                    rx.box(
                        rx.cond(
                            ContactState.show_success,
                            rx.box(
                                rx.vstack(
                                    rx.text("✅", font_size="3rem"),
                                    rx.heading(
                                        "¡Mensaje enviado!",
                                        size="5",
                                        color="#FF6B35"
                                    ),
                                    rx.text(
                                        "Te contactaremos pronto.",
                                        color="white"
                                    ),
                                    spacing="3",
                                    align="center"
                                ),
                                text_align="center",
                                p="8"
                            ),
                            rx.form(
                                rx.vstack(
                                    rx.input(
                                        placeholder="Nombre completo",
                                        value=ContactState.name,
                                        on_change=ContactState.set_name,
                                        bg="#1A1A1A",
                                        border="2px solid #666666",
                                        border_radius="8px",
                                        color="white",
                                        p="3",
                                        _focus={
                                            "border_color": "#FF6B35",
                                            "outline": "none"
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
                                        border="2px solid #666666",
                                        border_radius="8px",
                                        color="white",
                                        p="3",
                                        _focus={
                                            "border_color": "#FF6B35",
                                            "outline": "none"
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
                                        border="2px solid #666666",
                                        border_radius="8px",
                                        color="white",
                                        p="3",
                                        _focus={
                                            "border_color": "#FF6B35",
                                            "outline": "none"
                                        },
                                        _placeholder={"color": "#999999"},
                                        transition="all 0.3s ease"
                                    ),
                                    rx.text_area(
                                        placeholder="Mensaje",
                                        value=ContactState.message,
                                        on_change=ContactState.set_message,
                                        bg="#1A1A1A",
                                        border="2px solid #666666",
                                        border_radius="8px",
                                        color="white",
                                        p="3",
                                        rows="5",
                                        _focus={
                                            "border_color": "#FF6B35",
                                            "outline": "none"
                                        },
                                        _placeholder={"color": "#999999"},
                                        transition="all 0.3s ease",
                                        required=True
                                    ),
                                    rx.button(
                                        rx.cond(
                                            ContactState.is_loading,
                                            rx.hstack(
                                                rx.spinner(size="1"),
                                                rx.text("Enviando..."),
                                                spacing="2",
                                                align="center"
                                            ),
                                            "Enviar Mensaje"
                                        ),
                                        bg="#FF6B35",
                                        color="white",
                                        border_radius="8px",
                                        p="3",
                                        font_weight="600",
                                        width="100%",
                                        _hover={
                                            "bg": "#e55a2b",
                                            "transform": "translateY(-2px)"
                                        },
                                        transition="all 0.3s ease",
                                        disabled=ContactState.is_loading,
                                        type="submit"
                                    ),
                                    spacing="4",
                                    width="100%"
                                ),
                                on_submit=ContactState.submit_form,
                                width="100%"
                            )
                        ),
                        bg="#2D2D2D",
                        border_radius="15px",
                        p="8",
                        border="1px solid #666666"
                    ),
                    
                    columns={"base": "1", "md": "2"},
                    spacing="9",
                    width="100%"
                ),
                spacing="8",
                align="center"
            ),
            max_width="1200px",
            px="6",
            py="20"
        ),
        bg="#1A1A1A",
        id="contacto"
    )
