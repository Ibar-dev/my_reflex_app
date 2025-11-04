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
            # Overlay oscuro de fondo - MÁS OPACO
            rx.box(
                bg="rgba(0, 0, 0, 0.95)",  # Aumentado de 0.85 a 0.95
                position="fixed",
                top="0",
                left="0",
                right="0",
                bottom="0",
                z_index="99999",  # Aumentado a 99999 para asegurar capa superior
                on_click=VehicleState.close_confirmation_modal,
                backdrop_filter="blur(4px)",  # Añadido efecto de desenfoque
            ),

            # Modal centrado
            rx.center(
                rx.box(
                    rx.vstack(
                        # Icono y título
                        rx.cond(
                            VehicleState.confirmation_error,
                            # Error - CON FONDO MÁS VISIBLE
                            rx.vstack(
                                rx.box(
                                    rx.icon(
                                        "x_circle",
                                        size=60,
                                        color="white"
                                    ),
                                    bg="linear-gradient(135deg, #F44336 0%, #D32F2F 100%)",
                                    border_radius="50%",
                                    padding="1.5rem",
                                    box_shadow="0 0 30px rgba(244, 67, 54, 0.5)",
                                ),
                                rx.heading(
                                    "Error al Enviar",
                                    size="7",
                                    color="white",  # Cambiado a blanco
                                    font_weight="700",
                                    text_align="center"
                                ),
                                spacing="4",
                                align="center"
                            ),
                            # Éxito
                            rx.vstack(
                                rx.box(
                                    rx.icon(
                                        "check_circle",
                                        size=60,
                                        color="white"
                                    ),
                                    bg="linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%)",
                                    border_radius="50%",
                                    padding="1.5rem",
                                    box_shadow="0 0 30px rgba(255, 107, 53, 0.5)",
                                ),
                                rx.heading(
                                    "¡Solicitud Enviada!",
                                    size="7",
                                    color="white",  # Cambiado a blanco
                                    font_weight="700",
                                    text_align="center"
                                ),
                                spacing="4",
                                align="center"
                            )
                        ),

                        # Mensaje - CON MEJOR CONTRASTE
                        rx.box(
                            rx.text(
                                VehicleState.confirmation_message,
                                color="white",  # Cambiado de #CCCCCC a white
                                font_size="1.1rem",
                                text_align="center",
                                line_height="1.6",
                                font_weight="500"
                            ),
                            bg=rx.cond(
                                VehicleState.confirmation_error,
                                "rgba(244, 67, 54, 0.1)",  # Fondo rojizo suave para errores
                                "rgba(255, 107, 53, 0.1)"   # Fondo naranja suave para éxito
                            ),
                            border_left=rx.cond(
                                VehicleState.confirmation_error,
                                "4px solid #F44336",
                                "4px solid #FF6B35"
                            ),
                            padding="1.5rem",
                            border_radius="8px",
                            width="100%"
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
                                            color="#BBBBBB",
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
                                    color="#BBBBBB",
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
                                        "Cerrar",
                                        "Entendido"
                                    ),
                                    font_weight="600",
                                    font_size="1rem"
                                ),
                                spacing="2",
                                align="center"
                            ),
                            on_click=VehicleState.close_confirmation_modal,
                            bg=rx.cond(
                                VehicleState.confirmation_error,
                                "linear-gradient(135deg, #F44336 0%, #D32F2F 100%)",
                                "linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%)"
                            ),
                            color="white",
                            width="100%",
                            padding="1rem",
                            border_radius="8px",
                            cursor="pointer",
                            _hover={
                                "transform": "translateY(-2px)",
                                "box_shadow": rx.cond(
                                    VehicleState.confirmation_error,
                                    "0 6px 20px rgba(244, 67, 54, 0.6)",
                                    "0 6px 20px rgba(255, 107, 53, 0.6)"
                                )
                            },
                            transition="all 0.3s ease"
                        ),

                        spacing="6",
                        align="center",
                        width="100%"
                    ),
                    bg="#1A1A1A",
                    border=rx.cond(
                        VehicleState.confirmation_error,
                        "2px solid #F44336",
                        "2px solid #FF6B35"
                    ),
                    border_radius="20px",
                    padding="3rem",
                    max_width="550px",
                    width="90%",
                    box_shadow=rx.cond(
                        VehicleState.confirmation_error,
                        "0 10px 60px rgba(244, 67, 54, 0.3), 0 0 0 1px rgba(244, 67, 54, 0.2)",
                        "0 10px 60px rgba(255, 107, 53, 0.3), 0 0 0 1px rgba(255, 107, 53, 0.2)"
                    ),
                    position="relative",
                    z_index="100001"  # Z-index más alto para el modal en sí
                ),
                position="fixed",
                top="0",
                left="0",
                right="0",
                bottom="0",
                z_index="100000",  # Aumentado a 100000 para asegurar que esté por encima de todo
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