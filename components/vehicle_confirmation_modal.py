"""
Modal de Confirmación de Envío de Presupuesto
==============================================

Modal que aparece después de enviar la solicitud de presupuesto
desde el selector de vehículos.
"""

import reflex as rx
from state.vehicle_state_simple import VehicleState


def vehicle_confirmation_modal() -> rx.Component:
    """
    Modal de confirmación con diseño consistente con la web
    """
    return rx.cond(
        VehicleState.show_confirmation_modal,
        rx.box(
            # Overlay oscuro de fondo
            rx.box(
                bg="rgba(0, 0, 0, 0.85)",
                position="fixed",
                top="0",
                left="0",
                right="0",
                bottom="0",
                z_index="9998",
                on_click=VehicleState.close_confirmation_modal,
            ),

            # Modal centrado
            rx.center(
                rx.box(
                    rx.vstack(
                        # Icono y título
                        rx.cond(
                            VehicleState.confirmation_error,
                            # Error
                            rx.vstack(
                                rx.icon(
                                    "x_circle",
                                    size=60,
                                    color="#F44336"
                                ),
                                rx.heading(
                                    "Error al Enviar",
                                    size="7",
                                    color="#F44336",
                                    font_weight="700",
                                    text_align="center"
                                ),
                                spacing="4",
                                align="center"
                            ),
                            # Éxito
                            rx.vstack(
                                rx.icon(
                                    "check_circle",
                                    size=60,
                                    color="#FF6B35"
                                ),
                                rx.heading(
                                    "¡Solicitud Enviada!",
                                    size="7",
                                    color="#FF6B35",
                                    font_weight="700",
                                    text_align="center"
                                ),
                                spacing="4",
                                align="center"
                            )
                        ),

                        # Mensaje
                        rx.text(
                            VehicleState.confirmation_message,
                            color="#CCCCCC",
                            font_size="1.1rem",
                            text_align="center",
                            line_height="1.6"
                        ),

                        # Información adicional (solo en éxito)
                        rx.cond(
                            ~VehicleState.confirmation_error,
                            rx.vstack(
                                rx.divider(border_color="#404040"),
                                rx.vstack(
                                    rx.hstack(
                                        rx.icon("mail", size=20, color="#FF6B35"),
                                        rx.text(
                                            "Correo enviado a:",
                                            color="#999999",
                                            font_size="0.9rem"
                                        ),
                                        spacing="2",
                                        align="center"
                                    ),
                                    rx.text(
                                        "astrotechreprogramaciones@gmail.com",
                                        color="white",
                                        font_weight="600",
                                        font_size="1rem"
                                    ),
                                    spacing="2",
                                    align="center"
                                ),
                                rx.text(
                                    "Te contactaremos en las próximas 24-48 horas",
                                    color="#999999",
                                    font_size="0.9rem",
                                    text_align="center"
                                ),
                                spacing="4",
                                width="100%"
                            )
                        ),

                        # Botón de cerrar
                        rx.button(
                            rx.hstack(
                                rx.cond(
                                    VehicleState.confirmation_error,
                                    rx.icon("refresh_cw", size=20),
                                    rx.icon("check", size=20)
                                ),
                                rx.text(
                                    rx.cond(
                                        VehicleState.confirmation_error,
                                        "Reintentar",
                                        "Entendido"
                                    ),
                                    font_weight="600"
                                ),
                                spacing="2",
                                align="center"
                            ),
                            on_click=VehicleState.close_confirmation_modal,
                            bg=rx.cond(
                                VehicleState.confirmation_error,
                                "#F44336",
                                "linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%)"
                            ),
                            color="white",
                            width="100%",
                            padding="1rem",
                            border_radius="8px",
                            cursor="pointer",
                            _hover={
                                "transform": "translateY(-2px)",
                                "box_shadow": "0 6px 20px rgba(255, 107, 53, 0.4)"
                            },
                            transition="all 0.3s ease"
                        ),

                        spacing="6",
                        align="center",
                        width="100%"
                    ),
                    bg="#1A1A1A",
                    border="2px solid #FF6B35",
                    border_radius="20px",
                    padding="3rem",
                    max_width="500px",
                    width="90%",
                    box_shadow="0 10px 40px rgba(0, 0, 0, 0.5)",
                    position="relative",
                    z_index="9999"
                ),
                position="fixed",
                top="0",
                left="0",
                right="0",
                bottom="0",
                z_index="9999",
                pointer_events="none",
                style={
                    "& > div": {
                        "pointer-events": "auto"
                    }
                }
            ),
            width="100%",
            height="100%"
        )
    )