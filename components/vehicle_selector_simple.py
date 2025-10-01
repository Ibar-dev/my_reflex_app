"""Selector de Vehículos Simple con Desplegables
===============================================

Selector simple y funcional con dropdowns, conectado a la base de datos JSON.
"""


import reflex as rx
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))
from utils import vehicle_data


class SimpleVehicleState(rx.State):
    """Estado simple del selector conectado a datos reales"""

    # Selecciones del usuario
    selected_fuel: str = ""
    selected_brand: str = ""
    selected_model: str = ""
    selected_year: str = ""

    # Datos calculados
    power_original: int = 0
    power_optimized: int = 0
    power_gain: int = 0
    show_results: bool = False

    # Opciones disponibles (dinámicas)
    @property
    def fuel_options(self) -> list[str]:
        return ["gasolina", "diesel"]

    @property
    def brand_options(self) -> list[str]:
        if not self.selected_fuel:
            return []
        return vehicle_data.get_brands_by_fuel(self.selected_fuel)

    @property
    def model_options(self) -> list[str]:
        if not self.selected_brand or not self.selected_fuel:
            return []
        return vehicle_data.get_models_by_brand(self.selected_brand, self.selected_fuel)

    @property
    def year_options(self) -> list[str]:
        if not self.selected_brand or not self.selected_model or not self.selected_fuel:
            return []
        vehicles = vehicle_data.get_vehicles_by_brand_model(self.selected_brand, self.selected_model, self.selected_fuel)
        years = sorted({str(v.get('year')) for v in vehicles if v.get('year')}, reverse=True)
        return years

    def update_fuel(self, fuel: str):
        self.selected_fuel = fuel
        self.selected_brand = ""
        self.selected_model = ""
        self.selected_year = ""
        self.show_results = False

    def update_brand(self, brand: str):
        self.selected_brand = brand
        self.selected_model = ""
        self.selected_year = ""
        self.show_results = False

    def update_model(self, model: str):
        self.selected_model = model
        self.selected_year = ""
        self.show_results = False

    def update_year(self, year: str):
        self.selected_year = year
        self.show_results = False

    def calculate_results(self):
        if not (self.selected_brand and self.selected_model and self.selected_year and self.selected_fuel):
            self.show_results = False
            return
        vehicles = vehicle_data.get_vehicles_by_brand_model(self.selected_brand, self.selected_model, self.selected_fuel)
        vehicle = next((v for v in vehicles if str(v.get('year')) == self.selected_year), None)
        if vehicle:
            self.power_original = vehicle.get('power_stock', 0)
            tuning = vehicle.get('tuning_potential', {})
            self.power_optimized = tuning.get('power_tuned', 0)
            self.power_gain = tuning.get('power_gain', 0)
            self.show_results = True
        else:
            self.power_original = 0
            self.power_optimized = 0
            self.power_gain = 0
            self.show_results = False

    def reset_all(self):
        self.selected_fuel = ""
        self.selected_brand = ""
        self.selected_model = ""
        self.selected_year = ""
        self.power_original = 0
        self.power_optimized = 0
        self.power_gain = 0
        self.show_results = False


def vehicle_selector() -> rx.Component:
    """Selector principal simple con desplegables"""
    return rx.center(
        rx.container(
            rx.vstack(
                rx.heading(
                    "Calculadora de Reprogramación ECU",
                    size="8",
                ),
                # Combustible
                rx.vstack(
                    rx.text("Combustible", color="white", font_weight="600", font_size="1.1rem"),
                    rx.select(
                        SimpleVehicleState.fuel_options,
                        placeholder="Selecciona combustible",
                        value=SimpleVehicleState.selected_fuel,
                        on_change=SimpleVehicleState.update_fuel,
                        color_scheme="orange",
                        variant="filled",
                        size="lg",
                        width="100%",
                    ),
                    spacing="2", width="100%"
                ),
                # Marca
                rx.vstack(
                    rx.text("Marca", color="white", font_weight="600", font_size="1.1rem"),
                    rx.select(
                        SimpleVehicleState.brand_options,
                        placeholder="Selecciona marca",
                        value=SimpleVehicleState.selected_brand,
                        on_change=SimpleVehicleState.update_brand,
                        color_scheme="orange",
                        variant="filled",
                        size="lg",
                        width="100%",
                        is_disabled=rx.cond(SimpleVehicleState.selected_fuel == "", True, False),
                    ),
                    spacing="2", width="100%"
                ),
                # Modelo
                rx.vstack(
                    rx.text("Modelo", color="white", font_weight="600", font_size="1.1rem"),
                    rx.select(
                        SimpleVehicleState.model_options,
                        placeholder="Selecciona modelo",
                        value=SimpleVehicleState.selected_model,
                        on_change=SimpleVehicleState.update_model,
                        color_scheme="orange",
                        variant="filled",
                        size="lg",
                        width="100%",
                        is_disabled=rx.cond(SimpleVehicleState.selected_brand == "", True, False),
                    ),
                    spacing="2", width="100%"
                ),
                # Año
                rx.vstack(
                    rx.text("Año", color="white", font_weight="600", font_size="1.1rem"),
                    rx.select(
                        SimpleVehicleState.year_options,
                        placeholder="Selecciona año",
                        value=SimpleVehicleState.selected_year,
                        on_change=SimpleVehicleState.update_year,
                        color_scheme="orange",
                        variant="filled",
                        size="lg",
                        width="100%",
                        is_disabled=rx.cond(SimpleVehicleState.selected_model == "", True, False),
                    ),
                    spacing="2", width="100%"
                ),
                # Botón calcular
                rx.button(
                    "Calcular Potencia",
                    on_click=SimpleVehicleState.calculate_results,
                    color_scheme="orange",
                    size="lg",
                    width="100%",
                    is_disabled=rx.cond(
                        (SimpleVehicleState.selected_fuel == "") |
                        (SimpleVehicleState.selected_brand == "") |
                        (SimpleVehicleState.selected_model == "") |
                        (SimpleVehicleState.selected_year == ""),
                        True, False
                    ),
                    mt="4"
                ),
                # Resultados
                rx.cond(
                    SimpleVehicleState.show_results,
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Resultados de la Optimización",
                                size="6",
                                color="#FF6B35",
                                text_align="center",
                                margin_bottom="6"
                            ),
                            rx.text(
                                lambda: f"{SimpleVehicleState.selected_brand} {SimpleVehicleState.selected_model} ({SimpleVehicleState.selected_year}) - {SimpleVehicleState.selected_fuel}",
                                color="white",
                                font_weight="600",
                                font_size="1.2rem",
                                text_align="center",
                                margin_bottom="4"
                            ),
                            rx.grid(
                                rx.box(
                                    rx.vstack(
                                        rx.icon("gauge", size=40, color="#CCCCCC", mb="3"),
                                        rx.text("Potencia Original", color="#CCCCCC", font_weight="600"),
                                        rx.text(lambda: f"{SimpleVehicleState.power_original} CV", font_size="2rem", font_weight="700", color="white"),
                                        spacing="2", align="center"
                                    ),
                                    bg="linear-gradient(145deg, #2D2D2D, #232323)",
                                    border_radius="15px",
                                    p="6",
                                    border="2px solid #444444",
                                    width="100%"
                                ),
                                rx.box(
                                    rx.vstack(
                                        rx.icon("zap", size=40, color="#FF6B35", mb="3"),
                                        rx.text("Potencia Optimizada", color="#FF6B35", font_weight="600"),
                                        rx.text(lambda: f"{SimpleVehicleState.power_optimized} CV", font_size="2rem", font_weight="700", color="white"),
                                        rx.text(lambda: f"+{SimpleVehicleState.power_gain} CV", color="#4CAF50", font_weight="600", font_size="1.1rem"),
                                        spacing="2", align="center"
                                    ),
                                    bg="linear-gradient(145deg, #2D2D2D, #232323)",
                                    border_radius="15px",
                                    p="6",
                                    border="2px solid #FF6B35",
                                    width="100%"
                                ),
                                columns="2", spacing="4", width="100%"
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
                                            size="lg",
                                            border_radius="full",
                                            px="6",
                                            py="3",
                                            _hover={"bg": "#e55a2b", "transform": "translateY(-2px)"},
                                            transition="all 0.3s ease",
                                            on_click=rx.redirect(lambda: "mailto:Astrotechreprogramaciones@gmail.com?subject=Consulta Reprogramación ECU&body=Hola, estoy interesado en la reprogramación ECU para mi " + SimpleVehicleState.selected_brand + " " + SimpleVehicleState.selected_model)
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
                                            size="lg",
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
                                on_click=SimpleVehicleState.reset_all,
                                _hover={"bg": "rgba(255, 107, 53, 0.1)", "transform": "translateY(-2px)"},
                                transition="all 0.3s ease",
                                mt="4"
                            ),
                            spacing="6", width="100%"
                        ),
                        bg="linear-gradient(145deg, #252525, #1e1e1e)",
                        border_radius="20px",
                        p="8",
                        border="1px solid #3d3d3d",
                        width="100%",
                        max_width="600px",
                        mt="8"
                    )
                ),
                spacing="8", align="center", width="100%"
            ),
            max_width="800px",
            px="4"
        ),
        width="100%",
        py="10"
    )
