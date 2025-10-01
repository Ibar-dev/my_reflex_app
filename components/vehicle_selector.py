def vehicle_selector() -> rx.Component:
"""Selector de Vehículos con Datos Reales del JSON (Wizard)"""
import reflex as rx
from state.vehicle_state import VehicleState

def vehicle_selector() -> rx.Component:
    """Selector de vehículos paso a paso (wizard) usando VehicleState"""
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
                # Paso 1: Selección de combustible
                rx.cond(
                    VehicleState.current_step == 1,
                    rx.vstack(
                        rx.text("Selecciona el tipo de combustible", color="white", font_weight="600", font_size="1.2rem", mb="3"),
                        rx.select(
                            ["diesel", "gasolina"],
                            placeholder="Selecciona combustible",
                            value=VehicleState.selected_fuel,
                            on_change=VehicleState.select_fuel,
                            color_scheme="orange",
                            variant="soft",
                            size="3",
                            width="100%",
                        ),
                        spacing="6", width="100%"
                    )
                ),
                # Paso 2: Selección de marca
                rx.cond(
                    VehicleState.current_step == 2,
                    rx.vstack(
                        rx.text("Selecciona la marca", color="white", font_weight="600", font_size="1.2rem", mb="3"),
                        rx.select(
                            VehicleState.available_brands,
                            placeholder="Selecciona marca",
                            value=VehicleState.selected_brand,
                            on_change=VehicleState.select_brand,
                            color_scheme="orange",
                            variant="soft",
                            size="3",
                            width="100%",
                        ),
                        rx.button("Atrás", on_click=VehicleState.go_back, color_scheme="gray", mt="4"),
                        spacing="6", width="100%"
                    )
                ),
                # Paso 3: Selección de modelo
                rx.cond(
                    VehicleState.current_step == 3,
                    rx.vstack(
                        rx.text("Selecciona el modelo", color="white", font_weight="600", font_size="1.2rem", mb="3"),
                        rx.select(
                            VehicleState.available_models,
                            placeholder="Selecciona modelo",
                            value=VehicleState.selected_model,
                            on_change=VehicleState.select_model,
                            color_scheme="orange",
                            variant="soft",
                            size="3",
                            width="100%",
                        ),
                        rx.button("Atrás", on_click=VehicleState.go_back, color_scheme="gray", mt="4"),
                        spacing="6", width="100%"
                    )
                ),
                # Paso 4: Selección de año
                rx.cond(
                    VehicleState.current_step == 4,
                    rx.vstack(
                        rx.text("Selecciona el año", color="white", font_weight="600", font_size="1.2rem", mb="3"),
                        rx.select(
                            VehicleState.available_years,
                            placeholder="Selecciona año",
                            value=VehicleState.selected_year,
                            on_change=VehicleState.select_year,
                            color_scheme="orange",
                            variant="soft",
                            size="3",
                            width="100%",
                        ),
                        rx.button("Atrás", on_click=VehicleState.go_back, color_scheme="gray", mt="4"),
                        spacing="6", width="100%"
                    )
                ),
                # Paso 5: Resultados
                rx.cond(
                    VehicleState.current_step == 5,
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
                                lambda: f"{VehicleState.selected_brand} {VehicleState.selected_model} ({VehicleState.selected_year}) - {VehicleState.selected_fuel}",
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
                                        rx.text("Potencia Original", color="#CCCCCC", font_weight="600", font_size="1.1rem"),
                                        rx.text(lambda: f"{VehicleState.vehicle_power_stock} CV", font_size="2.2rem", font_weight="700", color="white"),
                                        spacing="3", align="center"
                                    ),
                                    bg="linear-gradient(145deg, #2D2D2D, #232323)",
                                    border_radius="20px",
                                    p="8",
                                    border="2px solid #444444",
                                    width="100%",
                                    min_height="160px"
                                ),
                                rx.box(
                                    rx.vstack(
                                        rx.icon("zap", size=50, color="#FF6B35", mb="4"),
                                        rx.text("Potencia Optimizada", color="#FF6B35", font_weight="600", font_size="1.1rem"),
                                        rx.text(lambda: f"{VehicleState.vehicle_power_tuned} CV", font_size="2.2rem", font_weight="700", color="white"),
                                        rx.text(lambda: f"+{VehicleState.vehicle_power_gain} CV", color="#4CAF50", font_weight="600", font_size="1.3rem"),
                                        spacing="3", align="center"
                                    ),
                                    bg="linear-gradient(145deg, #2D2D2D, #232323)",
                                    border_radius="20px",
                                    p="8",
                                    border="2px solid #FF6B35",
                                    width="100%",
                                    min_height="160px"
                                ),
                                columns="2", spacing="6", width="100%"
                            ),
                            rx.box(
                                rx.vstack(
                                    rx.heading("¡Contacta con nosotros!", size="5", color="white", text_align="center", mb="4"),
                                    rx.hstack(
                                        rx.button(
                                            rx.hstack(
                                                rx.icon("mail", size=20),
                                                rx.text("Enviar Email"),
                                                spacing="2"
                                            ),
                                            bg="#FF6B35",
                                            color="white",
                                            size="3",
                                            border_radius="full",
                                            px="6",
                                            py="3",
                                            _hover={"bg": "#e55a2b", "transform": "translateY(-2px)"},
                                            transition="all 0.3s ease",
                                            on_click=rx.redirect(lambda: f"mailto:Astrotechreprogramaciones@gmail.com?subject=Consulta Reprogramación ECU&body=Hola, estoy interesado en la reprogramación ECU para mi {VehicleState.selected_brand} {VehicleState.selected_model}")
                                        ),
                                        rx.button(
                                            rx.hstack(
                                                rx.icon("phone", size=20),
                                                rx.text("Llamar"),
                                                spacing="2"
                                            ),
                                            bg="transparent",
                                            color="#FF6B35",
                                            border="2px solid #FF6B35",
                                            size="3",
                                            border_radius="full",
                                            px="6",
                                            py="3",
                                            _hover={"bg": "rgba(255, 107, 53, 0.1)", "transform": "translateY(-2px)"},
                                            transition="all 0.3s ease",
                                            on_click=rx.redirect("tel:+34123456789")
                                        ),
                                        spacing="4", justify="center"
                                    ),
                                    rx.text(
                                        "📧 Astrotechreprogramaciones@gmail.com | 📞 +34 123 456 789",
                                        color="#CCCCCC",
                                        text_align="center",
                                        font_size="0.9rem",
                                        mt="3"
                                    ),
                                    spacing="3", align="center"
                                ),
                                bg="linear-gradient(145deg, #2D2D2D, #232323)",
                                border_radius="15px",
                                p="6",
                                border="1px solid #444444",
                                width="100%",
                                mt="6"
                            ),
                            rx.button(
                                rx.hstack(
                                    rx.icon("refresh-cw", size=16),
                                    rx.text("Nueva Consulta"),
                                    spacing="2"
                                ),
                                bg="transparent",
                                color="#FF6B35",
                                border="1px solid #FF6B35",
                                border_radius="full",
                                px="6", py="3",
                                on_click=VehicleState.reset_selector,
                                _hover={"bg": "rgba(255, 107, 53, 0.1)", "transform": "translateY(-2px)"},
                                transition="all 0.3s ease",
                                mt="4"
                            ),
                            spacing="6", width="100%"
                        ),
                        bg="linear-gradient(145deg, #252525, #1e1e1e)",
                        border_radius="24px",
                        padding="2rem",
                        border="1px solid #3d3d3d",
                        width="100%",
                        max_width={"base": "100%", "md": "800px"},
                        mt="9"
                    )
                ),
                spacing="9", align="center", width="100%"
            ),
            max_width={"base": "100%", "md": "1000px"},
            px={"base": "4", "md": "6"},
            width="100%"
        ),
        width="100%",
        py="9"
    )
