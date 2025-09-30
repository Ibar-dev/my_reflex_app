"""Selector de Vehículos Simple con Desplegables
===============================================

Selector simple y funcional con dropdowns.
"""

import reflex as rx


class SimpleVehicleState(rx.State):
    """Estado simple del selector"""
    
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
    
    # Opciones disponibles
    fuel_options: list[str] = ["Diesel", "Gasolina"]
    brand_options: list[str] = ["Toyota", "Ford", "Audi", "BMW", "Mercedes-Benz", "Volkswagen", "Honda", "Peugeot", "Renault", "Seat"]
    model_options: list[str] = ["Serie 1", "Serie 3", "Corolla", "Focus", "A3", "A4", "Golf", "Passat", "Civic", "Accord"]
    year_options: list[str] = ["2018", "2019", "2020", "2021", "2022", "2023", "2024"]
    
    def update_fuel(self, fuel: str):
        """Actualizar combustible seleccionado"""
        self.selected_fuel = fuel
        self.calculate_results()
    
    def update_brand(self, brand: str):
        """Actualizar marca seleccionada"""
        self.selected_brand = brand
        self.calculate_results()
    
    def update_model(self, model: str):
        """Actualizar modelo seleccionado"""
        self.selected_model = model
        self.calculate_results()
    
    def update_year(self, year: str):
        """Actualizar año seleccionado"""
        self.selected_year = year
        self.calculate_results()
    
    def calculate_results(self):
        """Calcular resultados basados en las selecciones"""
        if all([self.selected_fuel, self.selected_brand, self.selected_model, self.selected_year]):
            # Datos simulados basados en marca y combustible
            if self.selected_brand == "BMW":
                self.power_original = 190 if self.selected_fuel == "Diesel" else 150
            elif self.selected_brand == "Mercedes-Benz":
                self.power_original = 200 if self.selected_fuel == "Diesel" else 160
            elif self.selected_brand == "Audi":
                self.power_original = 180 if self.selected_fuel == "Diesel" else 140
            elif self.selected_brand == "Toyota":
                self.power_original = 150 if self.selected_fuel == "Diesel" else 120
            elif self.selected_brand == "Ford":
                self.power_original = 170 if self.selected_fuel == "Diesel" else 130
            else:
                self.power_original = 160 if self.selected_fuel == "Diesel" else 125
            
            # Cálculo de potencia optimizada (25-35% más)
            gain_percentage = 0.30 if self.selected_fuel == "Diesel" else 0.25
            self.power_gain = int(self.power_original * gain_percentage)
            self.power_optimized = self.power_original + self.power_gain
            self.show_results = True
        else:
            self.show_results = False
    
    def reset_all(self):
        """Resetear todo el selector"""
        self.selected_fuel = ""
        self.selected_brand = ""
        self.selected_model = ""
        self.selected_year = ""
        self.show_results = False


def vehicle_selector() -> rx.Component:
    """Selector principal simple con desplegables"""
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
                        rx.vstack(
                            rx.text("Tipo de Combustible", color="white", font_weight="600", font_size="1.1rem"),
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
                            rx.text("Marca del Vehículo", color="white", font_weight="600", font_size="1.1rem"),
                            rx.select(
                                SimpleVehicleState.brand_options,
                                placeholder="Selecciona marca",
                                value=SimpleVehicleState.selected_brand,
                                on_change=SimpleVehicleState.update_brand,
                                color_scheme="orange",
                                variant="filled",
                                size="lg",
                                width="100%",
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
                            ),
                            spacing="2", width="100%"
                        ),
                        
                        spacing="6", width="100%"
                    ),
                    
                    bg="linear-gradient(145deg, #252525, #1e1e1e)",
                    border_radius="20px",
                    p="8",
                    border="1px solid #3d3d3d",
                    width="100%",
                    max_width="500px"
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
                            
                            # Datos del vehículo
                            rx.text(
                                f"{SimpleVehicleState.selected_brand} {SimpleVehicleState.selected_model} ({SimpleVehicleState.selected_year}) - {SimpleVehicleState.selected_fuel}",
                                color="white",
                                font_weight="600",
                                font_size="1.2rem",
                                text_align="center",
                                margin_bottom="4"
                            ),
                            
                            # Comparativa de potencia
                            rx.grid(
                                rx.box(
                                    rx.vstack(
                                        rx.icon("gauge", size=40, color="#CCCCCC", mb="3"),
                                        rx.text("Potencia Original", color="#CCCCCC", font_weight="600"),
                                        rx.text(f"{SimpleVehicleState.power_original} CV", font_size="2rem", font_weight="700", color="white"),
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
                                        rx.text(f"{SimpleVehicleState.power_optimized} CV", font_size="2rem", font_weight="700", color="white"),
                                        rx.text(f"+{SimpleVehicleState.power_gain} CV", color="#4CAF50", font_weight="600", font_size="1.1rem"),
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
                                            size="lg",
                                            border_radius="full",
                                            px="6",
                                            py="3",
                                            _hover={"bg": "#e55a2b", "transform": "translateY(-2px)"},
                                            transition="all 0.3s ease",
                                            on_click=rx.redirect("mailto:Astrotechreprogramaciones@gmail.com?subject=Consulta Reprogramación ECU&body=Hola, estoy interesado en la reprogramación ECU para mi " + SimpleVehicleState.selected_brand + " " + SimpleVehicleState.selected_model)
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
