import reflex as rx
from state.vehicle_state import VehicleState


def vehicle_selector() -> rx.Component:
    """Selector de vehículos FUNCIONAL con estilos de interacción mejorados"""
    return rx.center(
        rx.box(
            rx.vstack(
                rx.heading(
                    "🚗 Configurador de Centralitas", 
                    size="8", 
                    color="#FF6B35", 
                    margin_bottom="2rem",
                    text_align="center"
                ),
                
                # Selector de Combustible
                rx.box(
                    rx.vstack(
                        rx.text(
                            "Paso 1: Tipo de Combustible", 
                            weight="bold", 
                            size="4", 
                            color="white"
                        ),
                        rx.select(
                            VehicleState.fuel_options,
                            placeholder="Selecciona el tipo de combustible", 
                            value=VehicleState.selected_fuel,
                            on_change=VehicleState.select_fuel,
                            width="100%",
                            size="3",
                        ),
                        width="100%",
                        spacing="2",
                    ),
                    position="relative",
                    z_index="10",
                    width="100%",
                ),
                
                # Selector de Marca
                rx.box(
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
                            on_change=VehicleState.select_brand,
                            disabled=VehicleState.selected_fuel == "",
                            width="100%",
                            size="3",
                        ),
                        width="100%",
                        spacing="2",
                    ),
                    position="relative",
                    z_index="9",
                    width="100%",
                ),
                
                # Selector de Modelo
                rx.box(
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
                            on_change=VehicleState.select_model,
                            disabled=VehicleState.selected_brand == "",
                            width="100%",
                            size="3",
                        ),
                        width="100%",
                        spacing="2",
                    ),
                    position="relative",
                    z_index="8",
                    width="100%",
                ),
                
                # Selector de Año
                rx.box(
                    rx.vstack(
                        rx.text(
                            "Paso 4: Año", 
                            weight="bold", 
                            size="4", 
                            color="white"
                        ),
                        rx.select(
                            VehicleState.available_years,
                            placeholder="Selecciona el año",
                            value=VehicleState.selected_year,
                            on_change=VehicleState.select_year,
                            disabled=VehicleState.selected_model == "",
                            width="100%",
                            size="3",
                        ),
                        width="100%",
                        spacing="2",
                    ),
                    position="relative",
                    z_index="7",
                    width="100%",
                ),
                
                # Resumen de selección
                rx.cond(
                    VehicleState.selected_year != "",
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
                                rx.text("Año:", weight="bold", color="white"),
                                rx.text(VehicleState.selected_year, color="#FF6B35"),
                                spacing="2",
                            ),
                            spacing="3",
                            align_items="start",
                        ),
                        margin_top="2rem",
                        width="100%",
                        bg="#1a1a1a",
                        border="1px solid #FF6B35",
                    ),
                ),
                
                spacing="5",
                width="100%",
                max_width="600px",
            ),
            padding="2rem",
            bg="#2D2D2D",
            border_radius="20px",
            border="1px solid #404040",
            box_shadow="0 8px 30px rgba(0, 0, 0, 0.3)",
            width="100%",
            max_width="700px",
            position="relative",
            z_index="1",
        ),
        width="100%",
        id="selector",
    )