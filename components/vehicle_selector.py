import reflex as rx
from state.vehicle_state import VehicleState


def vehicle_selector() -> rx.Component:
    """Selector de vehículos FUNCIONAL con rx.select estándar"""
    return rx.container(
        rx.vstack(
            rx.heading("🚗 Configurador de Centralitas", size="8", color="#FF6B35", margin_bottom="2rem"),
            
            # Selector de Combustible
            rx.vstack(
                rx.text("Paso 1: Tipo de Combustible", weight="bold", size="4", color="white"),
                rx.select(
                    ["diesel", "gasolina"],
                    placeholder="Selecciona el tipo de combustible", 
                    value=VehicleState.selected_fuel,
                    on_change=VehicleState.select_fuel,
                    width="100%",
                    size="3",
                    style={
                        "pointer_events": "auto",
                        "z_index": "100",
                        "position": "relative"
                    }
                ),
                width="100%",
                spacing="2",
            ),
            
            # Selector de Marca
            rx.vstack(
                rx.text("Paso 2: Marca", weight="bold", size="4", color="white"),
                rx.select(
                    VehicleState.available_brands,
                    placeholder="Selecciona la marca",
                    value=VehicleState.selected_brand,
                    on_change=VehicleState.select_brand,
                    disabled=VehicleState.selected_fuel == "",
                    width="100%",
                    size="3",
                    style={
                        "pointer_events": "auto",
                        "z_index": "100",
                        "position": "relative"
                    }
                ),
                width="100%",
                spacing="2",
            ),
            
            # Selector de Modelo
            rx.vstack(
                rx.text("Paso 3: Modelo", weight="bold", size="4", color="white"),
                rx.select(
                    VehicleState.available_models,
                    placeholder="Selecciona el modelo",
                    value=VehicleState.selected_model,
                    on_change=VehicleState.select_model,
                    disabled=VehicleState.selected_brand == "",
                    width="100%",
                    size="3",
                    style={
                        "pointer_events": "auto",
                        "z_index": "100",
                        "position": "relative"
                    }
                ),
                width="100%",
                spacing="2",
            ),
            
            # Selector de Año
            rx.vstack(
                rx.text("Paso 4: Año", weight="bold", size="4", color="white"),
                rx.select(
                    VehicleState.available_years,
                    placeholder="Selecciona el año",
                    value=VehicleState.selected_year,
                    on_change=VehicleState.select_year,
                    disabled=VehicleState.selected_model == "",
                    width="100%",
                    size="3",
                    style={
                        "pointer_events": "auto",
                        "z_index": "100",
                        "position": "relative"
                    }
                ),
                width="100%",
                spacing="2",
            ),
            
            # Resumen de selección
            rx.cond(
                VehicleState.selected_year != "",
                rx.card(
                    rx.vstack(
                        rx.heading("✅ Vehículo Seleccionado", size="6", color="#FF6B35"),
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
            
            # Panel de debug
            rx.card(
                rx.vstack(
                    rx.heading("🔍 Debug Info", size="4", color="#FF6B35"),
                    rx.text(f"Combustibles disponibles: {VehicleState.available_fuel_types.length()}", color="white", size="2"),
                    rx.text(f"Marcas disponibles: {VehicleState.available_brands.length()}", color="white", size="2"),
                    rx.text(f"Modelos disponibles: {VehicleState.available_models.length()}", color="white", size="2"),
                    rx.text(f"Años disponibles: {VehicleState.available_years.length()}", color="white", size="2"),
                    spacing="2",
                    align_items="start",
                ),
                margin_top="2rem",
                width="100%",
                bg="#0d1117",
                border="1px solid #30363d",
            ),
            
            spacing="5",
            width="100%",
            max_width="600px",
        ),
        padding="2rem",
        center_content=True,
        bg="linear-gradient(135deg, #0d1117 0%, #161b22 100%)",
        min_height="100vh",
    )