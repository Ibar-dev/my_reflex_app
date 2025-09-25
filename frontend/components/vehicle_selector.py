"""Selector de Vehículos con Datos Reales del JSON
================================================

Selector funcional que carga datos del JSON de vehículos.
"""

import reflex as rx
from typing import List, Dict


class VehicleState(rx.State):
    """Estado del selector con datos reales del JSON"""

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
    
    # Datos del vehículo seleccionado
    selected_vehicle_data: Dict = {}

    # Opciones dinámicas basadas en JSON
    fuel_options: List[str] = ["diesel", "gasolina"]
    brand_options: List[str] = []
    model_options: List[str] = []
    year_options: List[str] = []

    def load_brands_for_fuel(self, fuel: str):
        """Cargar marcas disponibles para el combustible seleccionado"""
        try:
            from utils.vehicle_data import get_brands_by_fuel
            self.brand_options = get_brands_by_fuel(fuel)
            print(f"Marcas cargadas para {fuel}: {len(self.brand_options)}")
        except Exception as e:
            print(f"Error cargando marcas: {e}")
            # Fallback básico
            self.brand_options = ["Ford", "Audi", "BMW", "Mercedes-Benz", "Volkswagen", "Toyota"]
    
    def load_models_for_brand(self, brand: str):
        """Cargar modelos disponibles para la marca seleccionada"""
        try:
            from utils.vehicle_data import get_models_by_brand
            self.model_options = get_models_by_brand(brand, self.selected_fuel)
            print(f"Modelos cargados para {brand}: {len(self.model_options)}")
        except Exception as e:
            print(f"Error cargando modelos: {e}")
            self.model_options = []
    
    def load_years_for_model(self, model: str):
        """Cargar años disponibles para el modelo seleccionado"""
        try:
            from utils.vehicle_data import get_vehicles_by_brand_model
            vehicles = get_vehicles_by_brand_model(self.selected_brand, model, self.selected_fuel)
            years = sorted(list(set([str(v.get('year', '')) for v in vehicles if v.get('year')])), reverse=True)
            self.year_options = years
            print(f"Años cargados para {self.selected_brand} {model}: {len(years)}")
        except Exception as e:
            print(f"Error cargando años: {e}")
            self.year_options = ["2023", "2022", "2021", "2020", "2019"]

    def update_fuel(self, fuel: str):
        """Actualizar combustible seleccionado"""
        self.selected_fuel = fuel
        # Limpiar selecciones posteriores
        self.selected_brand = ""
        self.selected_model = ""
        self.selected_year = ""
        self.model_options = []
        self.year_options = []
        self.show_results = False
        # Cargar marcas para este combustible
        self.load_brands_for_fuel(fuel)

    def update_brand(self, brand: str):
        """Actualizar marca seleccionada"""
        self.selected_brand = brand
        # Limpiar selecciones posteriores
        self.selected_model = ""
        self.selected_year = ""
        self.year_options = []
        self.show_results = False
        # Cargar modelos para esta marca
        self.load_models_for_brand(brand)

    def update_model(self, model: str):
        """Actualizar modelo seleccionado"""
        self.selected_model = model
        # Limpiar selecciones posteriores
        self.selected_year = ""
        self.show_results = False
        # Cargar años para este modelo
        self.load_years_for_model(model)

    def update_year(self, year: str):
        """Actualizar año seleccionado"""
        self.selected_year = year
        self.calculate_results()

    def calculate_results(self):
        """Calcular resultados con datos reales del JSON"""
        if all([self.selected_fuel, self.selected_brand, self.selected_model, self.selected_year]):
            try:
                from utils.vehicle_data import get_vehicles_by_brand_model
                vehicles = get_vehicles_by_brand_model(self.selected_brand, self.selected_model, self.selected_fuel)
                
                # Buscar el vehículo del año específico
                selected_vehicle = None
                for vehicle in vehicles:
                    if str(vehicle.get('year', '')) == self.selected_year:
                        selected_vehicle = vehicle
                        break
                
                if selected_vehicle:
                    self.selected_vehicle_data = selected_vehicle
                    self.power_original = selected_vehicle.get('power_stock', 150)
                    tuning_data = selected_vehicle.get('tuning_potential', {})
                    self.power_optimized = tuning_data.get('power_tuned', self.power_original + 30)
                    self.power_gain = tuning_data.get('power_gain', 30)
                    self.show_results = True
                    print(f"Datos cargados: {self.power_original} CV -> {self.power_optimized} CV (+{self.power_gain} CV)")
                else:
                    # Fallback con cálculos estimados
                    self.power_original = 150
                    gain_percentage = 0.30 if self.selected_fuel == "diesel" else 0.25
                    self.power_gain = int(self.power_original * gain_percentage)
                    self.power_optimized = self.power_original + self.power_gain
                    self.show_results = True
                    print(f"Usando datos estimados: {self.power_original} CV -> {self.power_optimized} CV")
                    
            except Exception as e:
                print(f"Error calculando resultados: {e}")
                # Fallback básico
                self.power_original = 150
                self.power_gain = 30
                self.power_optimized = 180
                self.show_results = True
        else:
            self.show_results = False

    def reset_all(self):
        """Resetear selector"""
        self.selected_fuel = ""
        self.selected_brand = ""
        self.selected_model = ""
        self.selected_year = ""
        self.brand_options = []
        self.model_options = []
        self.year_options = []
        self.selected_vehicle_data = {}
        self.show_results = False


def vehicle_selector() -> rx.Component:
    """Selector principal simple con desplegables"""

    def dropdown_field(label: str, options: list[str], value, on_change, placeholder: str) -> rx.Component:
        return rx.vstack(
            rx.text(label, color="white", font_weight="600", font_size="1.2rem", mb="3"),
            rx.select(
                options,
                placeholder=placeholder,
                value=value,
                on_change=on_change,
                variant="soft",
                size="3",
                width="100%",
                color_scheme="orange",
                height="60px",
                bg="#1f1f1f",
                color="white",
                border_color="#FF6B35",
                _hover={"border_color": "#FF6B35"},
                _focus={"border_color": "#FF6B35", "box_shadow": "0 0 0 1px #FF6B35"},
                px="4",
                py="3"
            ),
            spacing="3",
            width="100%",
            mb="4"
        )

    return rx.center(
        rx.container(
            rx.vstack(
                # Título
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

                # Formulario con desplegables
                rx.box(
                    rx.vstack(
                        # Combustible
                        dropdown_field(
                            "Tipo de Combustible",
                            VehicleState.fuel_options,
                            VehicleState.selected_fuel,
                            VehicleState.update_fuel,
                            "Selecciona combustible"
                        ),

                        # Marca
                        dropdown_field(
                            "Marca del Vehículo",
                            VehicleState.brand_options,
                            VehicleState.selected_brand,
                            VehicleState.update_brand,
                            "Selecciona marca"
                        ),

                        # Modelo
                        dropdown_field(
                            "Modelo",
                            VehicleState.model_options,
                            VehicleState.selected_model,
                            VehicleState.update_model,
                            "Selecciona modelo"
                        ),

                        # Año
                        dropdown_field(
                            "Año",
                            VehicleState.year_options,
                            VehicleState.selected_year,
                            VehicleState.update_year,
                            "Selecciona año"
                        ),

                        spacing="8", width="100%"
                    ),

                    bg="linear-gradient(145deg, #252525, #1e1e1e)",
                    border_radius="24px",
                    padding="2rem",
                    border="1px solid #3d3d3d",
                    width="100%",
                    max_width="800px",
                    min_height="420px",
                    z_index="10",
                    position="relative",
                ),

                # Resultados
                rx.cond(
                    VehicleState.show_results,
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Resultados de la Optimización",
                                size="7",
                                color="#FF6B35",
                                text_align="center",
                                margin_bottom="8"
                            ),

                            # Datos del vehículo
                            rx.text(
                                f"{VehicleState.selected_brand} {VehicleState.selected_model} ({VehicleState.selected_year}) - {VehicleState.selected_fuel}",
                                color="white",
                                font_weight="600",
                                font_size="1.4rem",
                                text_align="center",
                                margin_bottom="6"
                            ),

                            # Comparativa de potencia
                            rx.grid(
                                rx.box(
                                    rx.vstack(
                                        rx.icon("gauge", size=50, color="#CCCCCC", mb="4"),
                                        rx.text("Potencia Original", color="#CCCCCC", font_weight="600", font_size="1.1rem"),
                                        rx.text(f"{VehicleState.power_original} CV", font_size="2.2rem", font_weight="700", color="white"),
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
                                        rx.text(f"{VehicleState.power_optimized} CV", font_size="2.2rem", font_weight="700", color="white"),
                                        rx.text(f"+{VehicleState.power_gain} CV", color="#4CAF50", font_weight="600", font_size="1.3rem"),
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

                            # Contacto
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
                                            on_click=rx.redirect(f"mailto:info@astrotech.com?subject=Consulta Reprogramación ECU&body=Hola, estoy interesado en la reprogramación ECU para mi {VehicleState.selected_brand} {VehicleState.selected_model}")
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
                                        "📧 info@astrotech.com | 📞 +34 123 456 789",
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

                            # Botón reset
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
                                on_click=VehicleState.reset_all,
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
                        max_width="800px",
                        mt="9"
                    )
                ),

                spacing="9", align="center", width="100%"
            ),
            max_width="1000px",
            px="6"
        ),
        width="100%",
        py="9"
    )
