import reflex as rx
from state.vehicle_state_simple import VehicleState


def vehicle_selector() -> rx.Component:
    """Selector de vehículos FUNCIONAL con estilos de interacción mejorados y CENTRADO COMPLETO"""

    return rx.box(
        # Contenedor principal con centrado completo
        rx.container(
            rx.vstack(
                # Header centrado
                rx.hstack(
                    rx.icon("car", size=32, color="#FF6B35"),
                    rx.heading(
                        "Configurador de Centralitas",
                        size="8",
                        color="#FF6B35",
                        font_weight="700"
                    ),
                    align="center",
                    spacing="3",
                    justify="center",
                    width="100%"
                ),

                # Selector de Combustible
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            "Paso 1: Tipo de Combustible",
                            weight="bold",
                            size="4",
                            color="white"
                        ),
                        # Botón de inicialización para forzar carga de datos
                        rx.button(
                            rx.icon("refresh_cw", size=16),
                            "Cargar Datos",
                            on_click=VehicleState.load_fuel_types,
                            size="1",
                            bg="#FF6B35",
                            color="white",
                            border_radius="6px",
                            _hover={"bg": "#e55a2b"}
                        ),
                        justify="between",
                        align="center",
                        width="100%"
                    ),
                    rx.cond(
                        VehicleState.available_fuel_types != [],
                        rx.select(
                            VehicleState.available_fuel_types,
                            placeholder="Selecciona el tipo de combustible",
                            value=VehicleState.selected_fuel,
                            on_change=VehicleState.select_fuel,
                            width="100%",
                            size="3",
                        ),
                        rx.vstack(
                            rx.spinner(size="3", color="#FF6B35"),
                            rx.text("Cargando tipos de combustible...", color="#CCCCCC"),
                            rx.text("O haz clic en 'Cargar Datos'", color="#999999", font_size="0.85rem"),
                            spacing="2",
                            align="center",
                            padding="2rem"
                        )
                    ),
                    width="100%",
                    spacing="2",
                    align="center"
                ),

                # Selector de Marca
                rx.vstack(
                    rx.text(
                        "Paso 2: Marca",
                        weight="bold",
                        size="4",
                        color="white"
                    ),
                    rx.select(
                        VehicleState.available_brands,
                        placeholder="Selecciona la marca",
                        value=VehicleState.selected_brand,
                        on_change=lambda value: VehicleState.select_brand(value),
                        disabled=VehicleState.selected_fuel == "",
                        width="100%",
                        size="3",
                    ),
                    width="100%",
                    spacing="2",
                    align="center"
                ),

                # Selector de Modelo
                rx.vstack(
                    rx.text(
                        "Paso 3: Modelo",
                        weight="bold",
                        size="4",
                        color="white"
                    ),
                    rx.select(
                        VehicleState.available_models,
                        placeholder="Selecciona el modelo",
                        value=VehicleState.selected_model,
                        on_change=lambda value: VehicleState.select_model(value),
                        disabled=VehicleState.selected_brand == "",
                        width="100%",
                        size="3",
                    ),
                    width="100%",
                    spacing="2",
                    align="center"
                ),

                # Selector de Versión
                rx.vstack(
                    rx.text(
                        "Paso 4: Versión",
                        weight="bold",
                        size="4",
                        color="white"
                    ),
                    rx.select(
                        VehicleState.available_versions,
                        placeholder="Selecciona la versión",
                        value=VehicleState.selected_version,
                        on_change=lambda value: VehicleState.select_version(value),
                        disabled=VehicleState.selected_model == "",
                        width="100%",
                        size="3",
                    ),
                    width="100%",
                    spacing="2",
                    align="center"
                ),

                # Resumen de selección
                rx.cond(
                    VehicleState.selected_version != "",
                    rx.vstack(
                        rx.card(
                            rx.vstack(
                                rx.heading(
                                    "✅ Vehículo Seleccionado",
                                    size="6",
                                    color="#FF6B35"
                                ),
                                rx.divider(),
                                rx.hstack(
                                    rx.text("Combustible:", weight="bold", color="white"),
                                    rx.text(VehicleState.selected_fuel, color="#FF6B35"),
                                    spacing="2",
                                ),
                                rx.hstack(
                                    rx.text("Marca:", weight="bold", color="white"),
                                    rx.text(VehicleState.selected_brand, color="#FF6B35"),
                                    spacing="2",
                                ),
                                rx.hstack(
                                    rx.text("Modelo:", weight="bold", color="white"),
                                    rx.text(VehicleState.selected_model, color="#FF6B35"),
                                    spacing="2",
                                ),
                                rx.hstack(
                                    rx.text("Versión:", weight="bold", color="white"),
                                    rx.text(VehicleState.selected_version, color="#FF6B35"),
                                    spacing="2",
                                ),
                                spacing="3",
                                align_items="center",
                            ),
                            width="100%",
                            bg="#1a1a1a",
                            border="1px solid #FF6B35",
                        ),

                        # Botón para enviar selección al formulario de contacto
                        rx.button(
                            rx.hstack(
                                rx.icon("send", size=20),
                                rx.text("Solicitar Presupuesto", font_size="1.1rem", font_weight="600"),
                                spacing="2",
                                align="center",
                            ),
                            on_click=VehicleState.submit_vehicle_selection,
                            bg="linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%)",
                            color="white",
                            size="4",
                            width="100%",
                            padding="1.5rem",
                            border_radius="12px",
                            cursor="pointer",
                            _hover={
                                "transform": "translateY(-2px)",
                                "box_shadow": "0 10px 30px rgba(255, 107, 53, 0.4)",
                                "bg": "linear-gradient(135deg, #FF8C42 0%, #FFA55E 100%)",
                            },
                            transition="all 0.3s ease",
                            box_shadow="0 4px 15px rgba(255, 107, 53, 0.3)",
                        ),

                        spacing="4",
                        width="100%",
                    ),
                ),

                spacing="5",
                width="100%",
                align="center",
            ),

            # Parámetros de centrado del contenedor
            max_width="600px",
            margin="0 auto",
            padding="40px 20px",
            center_content=True,
        ),

        # Parámetros del box principal para centrado completo
        width="100%",
        min_height="80vh",
        display="flex",
        justify_content="center",
        align_items="center",
        bg="#1A1A1A",
        padding="20px",
        id="selector",
        on_mount=VehicleState.load_fuel_types,  # Carga automática al montar componente
    )