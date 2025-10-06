# Script: vehicle_selector_corregido.py
import reflex as rx
from state.vehicle_state import VehicleState

def debug_panel() -> rx.Component:
    """Panel de depuración para ver el estado en tiempo real"""
    return rx.box(
        rx.vstack(
            rx.heading("🔍 Debug Panel", size="3", color="#FF6B35"),
            rx.text(f"Paso actual: {VehicleState.current_step}", color="white"),
            rx.text(f"Combustible: {VehicleState.selected_fuel}", color="white"),
            rx.text(f"Marca: {VehicleState.selected_brand}", color="white"),
            rx.text(f"Modelo: {VehicleState.selected_model}", color="white"),
            rx.text(f"Año: {VehicleState.selected_year}", color="white"),
            # NOTA: Estas ya están correctamente corregidas con .length()
            rx.text(f"Marcas disponibles: {VehicleState.available_brands.length()}", color="white"),
            rx.text(f"Modelos disponibles: {VehicleState.available_models.length()}", color="white"),
            rx.text(f"Años disponibles: {VehicleState.available_years.length()}", color="white"),
            spacing="2",
            align="start"
        ),
        bg="rgba(255, 107, 53, 0.1)",
        border="1px solid #FF6B35",
        border_radius="8px",
        p="4",
        mb="4",
        width="100%"
    )

def vehicle_selector() -> rx.Component:
    """Selector de vehículos paso a paso con debugging"""
    return rx.center(
        rx.container(
            rx.vstack(
                rx.heading(
                    "Calculadora de Reprogramación ECU",
                    size="8",
                    color="white",
                    text_align="center",
                    margin_bottom="8",
                    bg_image="linear-gradient(45deg, #FF6B35, #FF8C42)",
                    bg_clip="text",
                    text_fill_color="transparent",
                ),
                
                # 🔍 Panel de debug (comentar en producción)
                debug_panel(),
                
                # Paso 1: Combustible - SIEMPRE VISIBLE
                rx.vstack(
                    rx.text(
                        "Paso 1: Selecciona el tipo de combustible",
                        color="white",
                        font_weight="600",
                        font_size="1.2rem",
                        mb="3"
                    ),
                    rx.select(
                        ["diesel", "gasolina"],
                        placeholder="¿Diesel o Gasolina?",
                        value=VehicleState.selected_fuel,
                        on_change=VehicleState.select_fuel,
                        size="3",
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                    p="6",
                    bg="rgba(45, 45, 45, 0.8)",
                    border_radius="12px",
                    border="1px solid #404040"
                ),
                
                # Paso 2: Marca (CORRECTO con .length())
                rx.cond(
                    VehicleState.current_step >= 2,
                    rx.vstack(
                        rx.text(
                            # Uso correcto: VehicleState.available_brands.length()
                            f"Paso 2: Selecciona la marca ({VehicleState.available_brands.length()} disponibles)",
                            color="white",
                            font_weight="600",
                            font_size="1.2rem",
                            mb="3"
                        ),
                        rx.cond(
                            VehicleState.available_brands.length() > 0,
                            rx.select(
                                VehicleState.available_brands,
                                placeholder="Selecciona la marca del vehículo",
                                value=VehicleState.selected_brand,
                                on_change=VehicleState.select_brand,
                                size="3",
                                width="100%",
                            ),
                            rx.text("Cargando marcas...", color="#CCCCCC")
                        ),
                        rx.button(
                            "← Volver",
                            on_click=VehicleState.go_back,
                            color_scheme="gray",
                            variant="soft",
                            size="2",
                            mt="2"
                        ),
                        spacing="4",
                        width="100%",
                        p="6",
                        bg="rgba(45, 45, 45, 0.8)",
                        border_radius="12px",
                        border="1px solid #404040"
                    )
                ),
                
                # Paso 3: Modelo (CORRECTO con .length())
                rx.cond(
                    VehicleState.current_step >= 3,
                    rx.vstack(
                        rx.text(
                            # Uso correcto: VehicleState.available_models.length()
                            f"Paso 3: Selecciona el modelo ({VehicleState.available_models.length()} disponibles)",
                            color="white",
                            font_weight="600",
                            font_size="1.2rem",
                            mb="3"
                        ),
                        rx.cond(
                            VehicleState.available_models.length() > 0,
                            rx.select(
                                VehicleState.available_models,
                                placeholder="Selecciona el modelo",
                                value=VehicleState.selected_model,
                                on_change=VehicleState.select_model,
                                size="3",
                                width="100%",
                            ),
                            rx.text("Cargando modelos...", color="#CCCCCC")
                        ),
                        rx.button(
                            "← Volver",
                            on_click=VehicleState.go_back,
                            color_scheme="gray",
                            variant="soft",
                            size="2",
                            mt="2"
                        ),
                        spacing="4",
                        width="100%",
                        p="6",
                        bg="rgba(45, 45, 45, 0.8)",
                        border_radius="12px",
                        border="1px solid #404040"
                    )
                ),
                
                # Paso 4: Año (AHORA CORREGIDO)
                rx.cond(
                    VehicleState.current_step >= 4,
                    rx.vstack(
                        rx.text(
                            # CORRECCIÓN AQUÍ: Cambiado de len() a .length()
                            f"Paso 4: Selecciona el año ({VehicleState.available_years.length()} disponibles)", 
                            color="white",
                            font_weight="600",
                            font_size="1.2rem",
                            mb="3"
                        ),
                        rx.cond(
                            VehicleState.available_years.length() > 0,
                            rx.select(
                                VehicleState.available_years,
                                placeholder="Selecciona el año",
                                value=VehicleState.selected_year,
                                on_change=VehicleState.select_year,
                                size="3",
                                width="100%",
                            ),
                            rx.text("Cargando años...", color="#CCCCCC")
                        ),
                        rx.button(
                            "← Volver",
                            on_click=VehicleState.go_back,
                            color_scheme="gray",
                            variant="soft",
                            size="2",
                            mt="2"
                        ),
                        spacing="4",
                        width="100%",
                        p="6",
                        bg="rgba(45, 45, 45, 0.8)",
                        border_radius="12px",
                        border="1px solid #404040"
                    )
                ),
                
                # Paso 5: Resultados (sin cambios, el que ya tienes)
                rx.cond(
                    VehicleState.current_step == 5,
                    # ... (El resto del código del Paso 5 que ya estaba bien)
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Resultados de la Optimización",
                                size="7",
                                color="#FF6B35",
                                text_align="center",
                                margin_bottom="8"
                            ),
                            rx.text(
                                VehicleState.vehicle_display_name,
                                color="white",
                                font_weight="600",
                                font_size="1.4rem",
                                text_align="center",
                                margin_bottom="6"
                            ),
                            rx.grid(
                                rx.box(
                                    rx.vstack(
                                        rx.icon("gauge", size=50, color="#CCCCCC", mb="4"),
                                        rx.text("Potencia Original", color="#CCCCCC", font_weight="600"),
                                        rx.text(
                                            f"{VehicleState.vehicle_power_stock} CV",
                                            font_size="2.2rem",
                                            font_weight="700",
                                            color="white"
                                        ),
                                        spacing="3", align="center"
                                    ),
                                    bg="linear-gradient(145deg, #2D2D2D, #232323)",
                                    border_radius="20px",
                                    p="8",
                                    border="2px solid #444444"
                                ),
                                rx.box(
                                    rx.vstack(
                                        rx.icon("zap", size=50, color="#FF6B35", mb="4"),
                                        rx.text("Potencia Optimizada", color="#FF6B35", font_weight="600"),
                                        rx.text(
                                            f"{VehicleState.vehicle_power_tuned} CV",
                                            font_size="2.2rem",
                                            font_weight="700",
                                            color="white"
                                        ),
                                        rx.text(
                                            f"+{VehicleState.vehicle_power_gain} CV",
                                            color="#4CAF50",
                                            font_weight="600",
                                            font_size="1.3rem"
                                        ),
                                        spacing="3", align="center"
                                    ),
                                    bg="linear-gradient(145deg, #2D2D2D, #232323)",
                                    border_radius="20px",
                                    p="8",
                                    border="2px solid #FF6B35"
                                ),
                                columns="2", spacing="6", width="100%"
                            ),
                            rx.button(
                                "🔄 Nueva Consulta",
                                on_click=VehicleState.reset_selector,
                                bg="#FF6B35",
                                color="white",
                                size="3",
                                mt="6"
                            ),
                            spacing="6", width="100%"
                        ),
                        bg="linear-gradient(145deg, #252525, #1e1e1e)",
                        border_radius="24px",
                        p="8",
                        width="100%"
                    )
                ),
                
                spacing="6",
                align="center",
                width="100%"
            ),
            max_width={"base": "100%", "md": "800px"},
            px={"base": "4", "md": "6"},
            width="100%"
        ),
        width="100%",
        py="9"
    )