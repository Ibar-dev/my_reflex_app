"""
Componente de contacto simplificado para debugging
"""

import reflex as rx
from simple_contact_state import SimpleContactState

def simple_contact() -> rx.Component:
    """Componente simplificado para probar inputs"""
    return rx.box(
        rx.center(
            rx.vstack(
                rx.heading("PRUEBA DE INPUTS", size="6", color="white", mb="4"),
                
                # Mostrar valores actuales
                rx.box(
                    rx.text(f"Nombre: '{SimpleContactState.test_name}'", color="white"),
                    rx.text(f"Email: '{SimpleContactState.test_email}'", color="white"),
                    rx.text(f"Mensaje: '{SimpleContactState.test_message}'", color="white"),
                    bg="#333",
                    p="4",
                    border_radius="8px",
                    mb="4",
                    width="400px"
                ),
                
                # Inputs de prueba
                rx.vstack(
                    rx.input(
                        placeholder="Escribe tu nombre aquí",
                        value=SimpleContactState.test_name,
                        on_change=SimpleContactState.update_name,
                        width="400px",
                        height="50px",
                        bg="white",
                        color="black",
                        border="2px solid #FF6B35"
                    ),
                    rx.input(
                        placeholder="Escribe tu email aquí",
                        value=SimpleContactState.test_email,
                        on_change=SimpleContactState.update_email,
                        width="400px",
                        height="50px",
                        bg="white",
                        color="black",
                        border="2px solid #FF6B35"
                    ),
                    rx.text_area(
                        placeholder="Escribe tu mensaje aquí",
                        value=SimpleContactState.test_message,
                        on_change=SimpleContactState.update_message,
                        width="400px",
                        height="100px",
                        bg="white",
                        color="black",
                        border="2px solid #FF6B35"
                    ),
                    spacing="4",
                    width="100%"
                ),
                
                rx.text(
                    "Si puedes escribir aquí, el problema NO es del estado",
                    color="#FF6B35",
                    font_weight="bold",
                    mt="4"
                ),
                
                spacing="4",
                align="center",
                width="100%"
            ),
            width="100%",
            height="100vh"
        ),
        bg="#121212",
        width="100%",
        height="100vh"
    )