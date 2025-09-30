#!/usr/bin/env python3
"""
Prueba simple del formulario de contacto
======================================

Verifica que los inputs sean editables y el estado funcione.
"""

import reflex as rx
from state.contact_state import ContactState

def simple_contact_test() -> rx.Component:
    """Versión simplificada del formulario para debugging"""
    return rx.box(
        rx.vstack(
            rx.heading("Prueba de Formulario de Contacto", size="6", color="white", mb="4"),
            
            # Mostrar valores actuales del estado
            rx.box(
                rx.heading("Estado Actual:", size="4", color="#FF6B35", mb="2"),
                rx.text(f"Nombre: '{ContactState.name}'", color="white"),
                rx.text(f"Email: '{ContactState.email}'", color="white"),
                rx.text(f"Teléfono: '{ContactState.phone}'", color="white"),
                rx.text(f"Mensaje: '{ContactState.message}'", color="white"),
                bg="#2D2D2D",
                p="4",
                border_radius="8px",
                mb="4"
            ),
            
            # Inputs de prueba
            rx.vstack(
                rx.input(
                    placeholder="Escribe tu nombre",
                    value=ContactState.name,
                    on_change=ContactState.handle_name_change,
                    bg="white",
                    color="black",
                    width="300px"
                ),
                rx.input(
                    placeholder="Escribe tu email",
                    value=ContactState.email,
                    on_change=ContactState.handle_email_change,
                    bg="white",
                    color="black",
                    width="300px"
                ),
                rx.input(
                    placeholder="Escribe tu teléfono",
                    value=ContactState.phone,
                    on_change=ContactState.handle_phone_change,
                    bg="white",
                    color="black",
                    width="300px"
                ),
                rx.text_area(
                    placeholder="Escribe tu mensaje",
                    value=ContactState.message,
                    on_change=ContactState.handle_message_change,
                    bg="white",
                    color="black",
                    width="300px",
                    height="100px"
                ),
                spacing="3"
            ),
            
            # Botón de prueba
            rx.button(
                "Probar Envío",
                on_click=ContactState.submit_form,
                bg="#FF6B35",
                color="white",
                size="3"
            ),
            
            # Mostrar estado de éxito
            rx.cond(
                ContactState.show_success,
                rx.box(
                    rx.text("¡Formulario enviado con éxito!", color="green", font_weight="bold"),
                    bg="rgba(0, 255, 0, 0.1)",
                    p="3",
                    border_radius="8px"
                )
            ),
            
            # Mostrar errores
            rx.cond(
                ContactState.form_error != "",
                rx.box(
                    rx.text(ContactState.form_error, color="red", font_weight="bold"),
                    bg="rgba(255, 0, 0, 0.1)",
                    p="3",
                    border_radius="8px"
                )
            ),
            
            spacing="4",
            align="center",
            width="100%",
            max_width="600px"
        ),
        bg="#121212",
        min_height="100vh",
        p="8",
        display="flex",
        justify_content="center",
        align_items="center"
    )

# Crear app de prueba
app = rx.App()
app.add_page(simple_contact_test, route="/test")

if __name__ == "__main__":
    print("🧪 Ejecuta: reflex run --port 3001")
    print("📱 Ve a: http://localhost:3001/test")
    print("✏️  Prueba escribir en los campos")