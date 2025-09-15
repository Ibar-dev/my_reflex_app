"""
Componente VehicleSelector - Selector de vehículos para reprogramación ECU
=========================================================================

Selector interactivo paso a paso con animaciones y efectos visuales modernos.
"""

import reflex as rx

# Datos de vehículos (ampliados con más marcas y modelos)
vehicles_data = {
    "Audi": {
        "A3": [
            {"year": 2022, "fuel_type": "diesel", "original_power": 150, "tuned_power": 190, "consumption_reduction": 12, "price": 350, "description": "Audi A3 2.0 TDI - Incremento de potencia del 27%"},
            {"year": 2021, "fuel_type": "diesel", "original_power": 116, "tuned_power": 145, "consumption_reduction": 15, "price": 300, "description": "Audi A3 1.6 TDI - Incremento de potencia del 25%"},
            {"year": 2022, "fuel_type": "gasolina", "original_power": 140, "tuned_power": 175, "consumption_reduction": 8, "price": 320, "description": "Audi A3 1.4 TFSI - Incremento de potencia del 25%"}
        ],
        "A4": [
            {"year": 2022, "fuel_type": "diesel", "original_power": 190, "tuned_power": 240, "consumption_reduction": 15, "price": 450, "description": "Audi A4 2.0 TDI - Incremento de potencia del 26%"},
            {"year": 2021, "fuel_type": "gasolina", "original_power": 190, "tuned_power": 235, "consumption_reduction": 10, "price": 420, "description": "Audi A4 2.0 TFSI - Incremento de potencia del 24%"}
        ],
        "Q5": [
            {"year": 2022, "fuel_type": "diesel", "original_power": 190, "tuned_power": 245, "consumption_reduction": 10, "price": 480, "description": "Audi Q5 2.0 TDI - Incremento de potencia del 29%"},
            {"year": 2021, "fuel_type": "gasolina", "original_power": 265, "tuned_power": 320, "consumption_reduction": 7, "price": 550, "description": "Audi Q5 3.0 TFSI - Incremento de potencia del 21%"}
        ]
    },
    "BMW": {
        "Serie 3": [
            {"year": 2022, "fuel_type": "diesel", "original_power": 190, "tuned_power": 240, "consumption_reduction": 13, "price": 460, "description": "BMW Serie 3 320d - Incremento de potencia del 26%"},
            {"year": 2021, "fuel_type": "gasolina", "original_power": 184, "tuned_power": 230, "consumption_reduction": 8, "price": 420, "description": "BMW Serie 3 320i - Incremento de potencia del 25%"}
        ],
        "Serie 5": [
            {"year": 2022, "fuel_type": "diesel", "original_power": 235, "tuned_power": 290, "consumption_reduction": 10, "price": 520, "description": "BMW Serie 5 530d - Incremento de potencia del 23%"},
            {"year": 2021, "fuel_type": "gasolina", "original_power": 252, "tuned_power": 310, "consumption_reduction": 5, "price": 490, "description": "BMW Serie 5 530i - Incremento de potencia del 23%"}
        ],
        "X3": [
            {"year": 2022, "fuel_type": "diesel", "original_power": 190, "tuned_power": 245, "consumption_reduction": 14, "price": 480, "description": "BMW X3 xDrive20d - Incremento de potencia del 29%"},
            {"year": 2021, "fuel_type": "gasolina", "original_power": 184, "tuned_power": 230, "consumption_reduction": 7, "price": 450, "description": "BMW X3 xDrive20i - Incremento de potencia del 25%"}
        ]
    },
    "Mercedes-Benz": {
        "Clase A": [
            {"year": 2022, "fuel_type": "diesel", "original_power": 150, "tuned_power": 185, "consumption_reduction": 15, "price": 390, "description": "Mercedes Clase A 180d - Incremento de potencia del 23%"},
            {"year": 2021, "fuel_type": "gasolina", "original_power": 163, "tuned_power": 200, "consumption_reduction": 8, "price": 380, "description": "Mercedes Clase A 200 - Incremento de potencia del 23%"}
        ],
        "Clase C": [
            {"year": 2022, "fuel_type": "diesel", "original_power": 194, "tuned_power": 245, "consumption_reduction": 14, "price": 470, "description": "Mercedes Clase C 220d - Incremento de potencia del 26%"},
            {"year": 2021, "fuel_type": "gasolina", "original_power": 204, "tuned_power": 250, "consumption_reduction": 8, "price": 450, "description": "Mercedes Clase C 200 - Incremento de potencia del 23%"}
        ],
        "GLC": [
            {"year": 2022, "fuel_type": "diesel", "original_power": 194, "tuned_power": 240, "consumption_reduction": 12, "price": 510, "description": "Mercedes GLC 220d - Incremento de potencia del 24%"},
            {"year": 2021, "fuel_type": "gasolina", "original_power": 258, "tuned_power": 310, "consumption_reduction": 5, "price": 530, "description": "Mercedes GLC 300 - Incremento de potencia del 20%"}
        ]
    },
    "Volkswagen": {
        "Golf": [
            {"year": 2022, "fuel_type": "diesel", "original_power": 150, "tuned_power": 190, "consumption_reduction": 12, "price": 350, "description": "Volkswagen Golf 2.0 TDI - Incremento de potencia del 27%"},
            {"year": 2021, "fuel_type": "diesel", "original_power": 115, "tuned_power": 145, "consumption_reduction": 15, "price": 320, "description": "Volkswagen Golf 1.6 TDI - Incremento de potencia del 26%"},
            {"year": 2022, "fuel_type": "gasolina", "original_power": 150, "tuned_power": 185, "consumption_reduction": 8, "price": 330, "description": "Volkswagen Golf 1.5 TSI - Incremento de potencia del 23%"}
        ],
        "Tiguan": [
            {"year": 2022, "fuel_type": "diesel", "original_power": 150, "tuned_power": 195, "consumption_reduction": 10, "price": 380, "description": "Volkswagen Tiguan 2.0 TDI - Incremento de potencia del 30%"},
            {"year": 2021, "fuel_type": "gasolina", "original_power": 150, "tuned_power": 185, "consumption_reduction": 7, "price": 360, "description": "Volkswagen Tiguan 1.5 TSI - Incremento de potencia del 23%"}
        ],
        "Passat": [
            {"year": 2022, "fuel_type": "diesel", "original_power": 150, "tuned_power": 190, "consumption_reduction": 14, "price": 370, "description": "Volkswagen Passat 2.0 TDI - Incremento de potencia del 27%"},
            {"year": 2021, "fuel_type": "gasolina", "original_power": 190, "tuned_power": 230, "consumption_reduction": 6, "price": 390, "description": "Volkswagen Passat 2.0 TSI - Incremento de potencia del 21%"}
        ]
    },
    "Seat": {
        "León": [
            {"year": 2022, "fuel_type": "diesel", "original_power": 150, "tuned_power": 185, "consumption_reduction": 15, "price": 340, "description": "Seat León 2.0 TDI - Incremento de potencia del 23%"},
            {"year": 2021, "fuel_type": "gasolina", "original_power": 150, "tuned_power": 180, "consumption_reduction": 8, "price": 320, "description": "Seat León 1.5 TSI - Incremento de potencia del 20%"}
        ],
        "Ateca": [
            {"year": 2022, "fuel_type": "diesel", "original_power": 150, "tuned_power": 190, "consumption_reduction": 12, "price": 380, "description": "Seat Ateca 2.0 TDI - Incremento de potencia del 27%"},
            {"year": 2021, "fuel_type": "gasolina", "original_power": 150, "tuned_power": 185, "consumption_reduction": 7, "price": 360, "description": "Seat Ateca 1.5 TSI - Incremento de potencia del 23%"}
        ]
    },
    "Renault": {
        "Mégane": [
            {"year": 2022, "fuel_type": "diesel", "original_power": 115, "tuned_power": 145, "consumption_reduction": 15, "price": 300, "description": "Renault Mégane 1.5 dCi - Incremento de potencia del 26%"},
            {"year": 2021, "fuel_type": "gasolina", "original_power": 140, "tuned_power": 170, "consumption_reduction": 10, "price": 290, "description": "Renault Mégane 1.3 TCe - Incremento de potencia del 21%"}
        ],
        "Captur": [
            {"year": 2022, "fuel_type": "diesel", "original_power": 115, "tuned_power": 140, "consumption_reduction": 15, "price": 310, "description": "Renault Captur 1.5 dCi - Incremento de potencia del 22%"},
            {"year": 2021, "fuel_type": "gasolina", "original_power": 130, "tuned_power": 155, "consumption_reduction": 10, "price": 290, "description": "Renault Captur 1.3 TCe - Incremento de potencia del 19%"}
        ]
    }
}

class VehicleState(rx.State):
    """Estado del selector de vehículos"""
    selected_fuel: str = ""
    selected_brand: str = ""
    selected_model: str = ""
    selected_vehicle: dict = {}
    current_step: int = 1
    power_increase: int = 0
    brand_search: str = ""
    model_search: str = ""
    
    @rx.var
    def filtered_brands(self) -> list[str]:
        if not self.brand_search:
            return list(vehicles_data.keys())
        return [brand for brand in vehicles_data.keys() 
                if self.brand_search.lower() in brand.lower()]
    
    @rx.var
    def filtered_models(self) -> list[str]:
        if not self.selected_brand:
            return []
        models = list(vehicles_data.get(self.selected_brand, {}).keys())
        if not self.model_search:
            return models
        return [model for model in models 
                if self.model_search.lower() in model.lower()]
    
    def select_fuel(self, fuel: str):
        """Selecciona el tipo de combustible"""
        self.selected_fuel = fuel
        self.selected_brand = ""
        self.selected_model = ""
        self.selected_vehicle = {}
        self.brand_search = ""
        self.model_search = ""
        self.current_step = 2
        
    def set_brand_search(self, value: str):
        self.brand_search = value
        
    def set_model_search(self, value: str):
        self.model_search = value
    
    def select_brand(self, brand: str):
        self.selected_brand = brand
        self.selected_model = ""
        self.selected_vehicle = {}
        self.model_search = ""
        self.current_step = 3
    
    def select_model(self, model: str):
        self.selected_model = model
        self.selected_vehicle = {}
        self.current_step = 4
    
    def select_vehicle(self, vehicle: dict):
        self.selected_vehicle = vehicle
        self.power_increase = int((vehicle['tuned_power'] / vehicle['original_power'] - 1) * 100)
        self.current_step = 5
    
    def reset_selector(self):
        self.selected_fuel = ""
        self.selected_brand = ""
        self.selected_model = ""
        self.selected_vehicle = {}
        self.current_step = 1
    
    def go_back(self):
        if self.current_step > 1:
            self.current_step -= 1
            if self.current_step == 1:
                self.selected_fuel = ""
            elif self.current_step == 2:
                self.selected_brand = ""
            elif self.current_step == 3:
                self.selected_model = ""
            elif self.current_step == 4:
                self.selected_vehicle = {}

def fuel_selection() -> rx.Component:
    """Paso 1: Selección de combustible con diseño mejorado."""
    return rx.center(
        rx.vstack(
            # Título con gradiente y animación
            rx.heading(
                "Elige el tipo de combustible de tu vehículo para continuar", 
                size="5", 
                color="white", 
                text_align="center", 
                margin_bottom="6",
                font_weight="600",
                class_name="fade-in",
            ),
        rx.center(
            rx.hstack(
                # Botón Diésel con efecto 3D y animación
                rx.button(
                    rx.vstack(
                        rx.box(
                            rx.icon("fuel", size=80, color="#FF6B35"),
                            mb="4",
                            animation="pulse 3s infinite",
                            p="3",
                            border_radius="full",
                            bg="rgba(255, 107, 53, 0.1)",
                            box_shadow="0 0 30px rgba(255, 107, 53, 0.2)",
                        ),
                        rx.text(
                            "Diésel", 
                            font_weight="700", 
                            color="white", 
                            font_size="1.25rem",
                        ),
                        spacing="6",
                        align="center",
                        width="100%",
                    ),
                    bg="linear-gradient(145deg, #252525, #1e1e1e)",
                    border="2px solid #3d3d3d",
                    border_radius="30px",
                    p="8",
                    width={"base": "220px", "md": "240px"},
                    height={"base": "250px", "md": "280px"},
                    _hover={
                        "border_color": "#FF6B35",
                        "transform": "translateY(-10px) scale(1.03)",
                        "box_shadow": "0 15px 30px rgba(255, 107, 53, 0.4)",
                        "bg": "linear-gradient(145deg, #272727, #1c1c1c)"
                    },
                    _active={
                        "transform": "translateY(-5px)",
                        "box_shadow": "0 10px 15px rgba(255, 107, 53, 0.3)",
                    },
                    transition="all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)",
                    on_click=lambda: VehicleState.select_fuel("diesel"),
                    class_name="fuel-btn fade-in-up",
                ),
                # Botón Gasolina con efecto 3D y animación
                rx.button(
                    rx.vstack(
                        rx.box(
                            rx.icon("fuel", size=80, color="#FF6B35"),
                            mb="4",
                            animation="pulse 3s infinite",
                            animation_delay="1.5s",
                            p="3",
                            border_radius="full",
                            bg="rgba(255, 107, 53, 0.1)",
                            box_shadow="0 0 30px rgba(255, 107, 53, 0.2)",
                        ),
                        rx.text(
                            "Gasolina", 
                            font_weight="700", 
                            color="white", 
                            font_size="1.25rem",
                        ),
                        spacing="6",
                        align="center",
                        width="100%",
                    ),
                    bg="linear-gradient(145deg, #252525, #1e1e1e)",
                    border="2px solid #3d3d3d",
                    border_radius="30px",
                    p="8",
                    width={"base": "220px", "md": "240px"},
                    height={"base": "250px", "md": "280px"},
                    _hover={
                        "border_color": "#FF6B35",
                        "transform": "translateY(-10px) scale(1.03)",
                        "box_shadow": "0 15px 30px rgba(255, 107, 53, 0.4)",
                        "bg": "linear-gradient(145deg, #272727, #1c1c1c)"
                    },
                    _active={
                        "transform": "translateY(-5px)",
                        "box_shadow": "0 10px 15px rgba(255, 107, 53, 0.3)",
                    },
                    transition="all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)",
                    on_click=lambda: VehicleState.select_fuel("gasolina"),
                    class_name="fuel-btn fade-in-up",
                    animation_delay="0.2s",
                ),
                spacing="8",
                justify="center",
                wrap="wrap"
            ),
            width="100%"
            ),
            spacing="8",
            align="center",
            class_name="vehicle-selector-step",
            width="100%",
            max_width="600px"
        ),
        width="100%"
    )

def brand_selection() -> rx.Component:
    """Paso 2: Selección de marca con buscador"""
    return rx.vstack(
        rx.heading(
            "2. Selecciona la marca", 
            size="6", 
            color="white", 
            margin_bottom="6",
            font_weight="700",
            bg_image="linear-gradient(45deg, #FF6B35, #FF8C42)",
            bg_clip="text",
            text_fill_color="transparent",
        ),
        # Campo de búsqueda mejorado
        rx.vstack(
            rx.hstack(
                rx.icon(
                    "search",
                    color="#FF6B35",
                    size=22
                ),
                rx.input(
                    placeholder="Buscar marca...",
                    value=VehicleState.brand_search,
                    on_change=VehicleState.set_brand_search,
                    bg="rgba(26, 26, 26, 0.8)",
                    border="2px solid #444444",
                    border_radius="full",
                    p="4",
                    color="white",
                    width="100%",
                    _focus={
                        "border_color": "#FF6B35", 
                        "box_shadow": "0 0 0 2px rgba(255, 107, 53, 0.3)"
                    },
                    font_size="1.1rem",
                ),
                width="100%",
                align="center",
                spacing="3",
                bg="linear-gradient(145deg, #252525, #1e1e1e)",
                border_radius="full",
                p="2",
                ps="4",
            ),
            width="100%",
            mb="6"
        ),
        # Rejilla de marcas con diseño mejorado
        rx.box(
            rx.cond(
                VehicleState.filtered_brands.length() > 0,
                rx.grid(
                    rx.foreach(
                        VehicleState.filtered_brands,
                        lambda brand: rx.button(
                            rx.vstack(
                                rx.box(
                                    rx.icon("car", size=32, color="#FF6B35", mb="2"),
                                ),
                                rx.text(
                                    brand, 
                                    font_weight="600", 
                                    font_size="1.1rem",
                                    color="white",
                                ),
                                spacing="2",
                                align="center",
                                width="100%",
                            ),
                            bg="linear-gradient(145deg, #252525, #1e1e1e)",
                            border="2px solid #3d3d3d",
                            border_radius="20px",
                            p="5",
                            height="100px",
                            width="100%",
                            _hover={
                                "border_color": "#FF6B35",
                                "transform": "translateY(-5px)",
                                "box_shadow": "0 10px 20px rgba(255, 107, 53, 0.4)",
                                "bg": "linear-gradient(145deg, #2a2a2a, #202020)"
                            },
                            transition="all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275)",
                            on_click=lambda b=brand: VehicleState.select_brand(b),
                            class_name="brand-btn"
                        )
                    ),
                    columns={"base": "1", "sm": "2", "md": "3", "lg": "4"},
                    spacing="4",
                    width="100%"
                ),
                rx.vstack(
                    rx.icon("circle_alert", size=40, color="#FF6B35", mb="3"),
                    rx.text(
                        "No se encontraron marcas", 
                        color="#CCCCCC", 
                        font_size="1.1rem"
                    ),
                    align="center",
                    pt="6",
                    pb="10",
                )
            ),
            width="100%",
            overflow_y="auto",
            max_height="500px",
            bg="linear-gradient(145deg, rgba(30, 30, 30, 0.3), rgba(35, 35, 35, 0.2))",
            border_radius="20px",
            p="4",
        ),
        rx.button(
            rx.hstack(
                rx.icon("arrow-left", size=16),
                rx.text("Volver"),
                spacing="2"
            ),
            bg="transparent",
            color="#FF6B35",
            border="1px solid #FF6B35",
            border_radius="full",
            px="6",
            py="3",
            margin_top="6",
            on_click=VehicleState.go_back,
            _hover={
                "bg": "rgba(255, 107, 53, 0.1)", 
                "transform": "translateY(-2px)",
                "box_shadow": "0 5px 15px rgba(255, 107, 53, 0.2)"
            },
            transition="all 0.3s ease",
        ),
        spacing="4",
        align="center",
        width="100%"
    )

def model_selection() -> rx.Component:
    """Paso 3: Selección de modelo con buscador"""
    return rx.vstack(
        rx.heading(
            rx.cond(
                VehicleState.selected_brand,
                f"3. Selecciona el modelo {VehicleState.selected_brand}",
                "3. Selecciona un modelo"
            ),
            size="6", 
            color="white", 
            margin_bottom="6",
            font_weight="700",
            bg_image="linear-gradient(45deg, #FF6B35, #FF8C42)",
            bg_clip="text",
            text_fill_color="transparent",
        ),
        
        # Campo de búsqueda mejorado
        rx.vstack(
            rx.hstack(
                rx.icon(
                    "search",
                    color="#FF6B35",
                    size=22
                ),
                rx.input(
                    placeholder="Buscar modelo...",
                    value=VehicleState.model_search,
                    on_change=VehicleState.set_model_search,
                    bg="rgba(26, 26, 26, 0.8)",
                    border="2px solid #444444",
                    border_radius="full",
                    p="4",
                    color="white",
                    width="100%",
                    _focus={
                        "border_color": "#FF6B35", 
                        "box_shadow": "0 0 0 2px rgba(255, 107, 53, 0.3)"
                    },
                    font_size="1.1rem",
                ),
                width="100%",
                align="center",
                spacing="3",
                bg="linear-gradient(145deg, #252525, #1e1e1e)",
                border_radius="full",
                p="2",
                ps="4",
            ),
            width="100%",
            mb="6"
        ),
        
        # Rejilla de modelos con diseño mejorado
        rx.box(
            rx.cond(
                VehicleState.filtered_models.length() > 0,
                rx.grid(
                    rx.foreach(
                        VehicleState.filtered_models,
                        lambda model: rx.button(
                            rx.vstack(
                                rx.box(
                                    rx.icon("settings-2", size=30, color="#FF6B35", mb="2"),
                                ),
                                rx.text(
                                    model, 
                                    font_weight="600", 
                                    font_size="1.1rem",
                                    color="white",
                                ),
                                spacing="2",
                                align="center",
                                width="100%",
                            ),
                            bg="linear-gradient(145deg, #252525, #1e1e1e)",
                            border="2px solid #3d3d3d",
                            border_radius="20px",
                            p="5",
                            height="100px",
                            width="100%",
                            _hover={
                                "border_color": "#FF6B35",
                                "transform": "translateY(-5px)",
                                "box_shadow": "0 10px 20px rgba(255, 107, 53, 0.4)",
                                "bg": "linear-gradient(145deg, #2a2a2a, #202020)"
                            },
                            transition="all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275)",
                            on_click=lambda m=model: VehicleState.select_model(m),
                            class_name="model-btn"
                        )
                    ),
                    columns={"base": "1", "sm": "2", "md": "3"},
                    spacing="4",
                    width="100%"
                ),
                rx.vstack(
                    rx.icon("circle_alert", size=40, color="#FF6B35", mb="3"),
                    rx.text(
                        "No se encontraron modelos", 
                        color="#CCCCCC", 
                        font_size="1.1rem"
                    ),
                    align="center",
                    pt="6",
                    pb="10",
                )
            ),
            width="100%",
            overflow_y="auto",
            max_height="500px",
            bg="linear-gradient(145deg, rgba(30, 30, 30, 0.3), rgba(35, 35, 35, 0.2))",
            border_radius="20px",
            p="4",
        ),
        
        rx.button(
            rx.hstack(
                rx.icon("arrow-left", size=16),
                rx.text("Volver"),
                spacing="2"
            ),
            bg="transparent",
            color="#FF6B35",
            border="1px solid #FF6B35",
            border_radius="full",
            px="6",
            py="3",
            margin_top="6",
            on_click=VehicleState.go_back,
            _hover={
                "bg": "rgba(255, 107, 53, 0.1)", 
                "transform": "translateY(-2px)",
                "box_shadow": "0 5px 15px rgba(255, 107, 53, 0.2)"
            },
            transition="all 0.3s ease",
        ),
        spacing="4",
        align="center",
        width="100%"
    )

def year_selection() -> rx.Component:
    """Paso 4: Selección de año y motor con mejor presentación"""
    vehicle_options = [vehicle for vehicle in vehicles_data.get(VehicleState.selected_brand, {}).get(VehicleState.selected_model, [])
                      if vehicle["fuel_type"] == VehicleState.selected_fuel]
    
    return rx.vstack(
        rx.heading(
            f"4. Selecciona el año para {VehicleState.selected_brand} {VehicleState.selected_model}", 
            size="6", 
            color="white", 
            margin_bottom="6"
        ),
        rx.box(
            rx.cond(
                len(vehicle_options) > 0,
                rx.grid(
                    [rx.button(
                            rx.vstack(
                                rx.heading(
                                    str(vehicle["year"]), 
                                    size="4", 
                                    color="white",
                                    mb="2"
                                ),
                                rx.hstack(
                                    rx.vstack(
                                        rx.text("Original", color="#CCCCCC", font_size="0.8rem"),
                                        rx.text(
                                            f"{vehicle['original_power']} CV", 
                                            font_weight="bold", 
                                            color="white", 
                                            font_size="1.1rem"
                                        ),
                                        align="center",
                                    ),
                                    rx.icon("arrow-right", color="#FF6B35", size=20),
                                    rx.vstack(
                                        rx.text("Optimizado", color="#CCCCCC", font_size="0.8rem"),
                                        rx.text(
                                            f"{vehicle['tuned_power']} CV", 
                                            font_weight="bold", 
                                            color="#FF6B35", 
                                            font_size="1.1rem"
                                        ),
                                        align="center",
                                    ),
                                    justify="center",
                                    spacing="6",
                                    width="100%"
                                ),
                                rx.text(
                                    f"Consumo: -{vehicle['consumption_reduction']}%",
                                    color="#AAAAAA",
                                    font_size="0.9rem",
                                    mt="2"
                                ),
                                spacing="3",
                                align="center",
                                width="100%"
                            ),
                            bg="linear-gradient(145deg, #303030, #232323)",
                            border="2px solid #444444",
                            border_radius="20px",
                            p="6",
                            height="180px",
                            color="white",
                            width="100%",
                            _hover={
                                "border_color": "#FF6B35",
                                "transform": "translateY(-5px)",
                                "box_shadow": "0 8px 15px rgba(255, 107, 53, 0.3)",
                                "bg": "linear-gradient(145deg, #343434, #272727)"
                            },
                            transition="all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275)",
                            on_click=lambda v=vehicle: VehicleState.select_vehicle(v),
                        )
                        for vehicle in vehicle_options
                    ],
                    columns={"base": "1", "md": "2"},
                    spacing="6",
                    width="100%"
                ),
                rx.box(
                    rx.vstack(
                        rx.icon("triangle_alert", size=40, color="#FF6B35", mb="4"),
                        rx.text(
                            "No hay vehículos disponibles con estas características",
                            color="#CCCCCC"
                        ),
                        align="center",
                        p="8"
                    )
                )
            ),
            width="100%",
            overflow_y="auto",
            max_height="500px"
        ),
        rx.button(
            rx.hstack(
                rx.icon("arrow-left", size=16),
                rx.text("Volver"),
                spacing="2"
            ),
            bg="transparent",
            color="#FF6B35",
            border="1px solid #FF6B35",
            border_radius="full",
            px="6",
            py="3",
            margin_top="6",
            on_click=VehicleState.go_back,
            _hover={
                "bg": "rgba(255, 107, 53, 0.1)", 
                "transform": "translateY(-2px)",
                "box_shadow": "0 5px 15px rgba(255, 107, 53, 0.2)"
            },
            transition="all 0.3s ease",
        ),
        spacing="6",
        align="center",
        width="100%",
    )

def vehicle_details() -> rx.Component:
    """Paso 5: Detalles del vehículo seleccionado"""
    return rx.vstack(
        rx.heading(
            f"{VehicleState.selected_brand} {VehicleState.selected_model} {VehicleState.selected_vehicle.get('year', '')}",
            size="6",
            color="#FF6B35",
            margin_bottom="4"
        ),
        rx.text(
            VehicleState.selected_vehicle.get("description", ""),
            color="white",
            margin_bottom="6"
        ),
        rx.grid(
            rx.box(
                rx.vstack(
                    rx.text("Potencia Original", color="white", font_weight="600"),
                    rx.text(f"{VehicleState.selected_vehicle.get('original_power', 0)} CV", 
                            font_size="2rem", font_weight="700", color="#FF6B35"),
                    spacing="2",
                    align="center"
                ),
                bg="#2D2D2D",
                border_radius="20px",
                p="6",
                border="1px solid #666666"
            ),
            rx.box(
                rx.vstack(
                    rx.text("Potencia Optimizada", color="white", font_weight="600"),
                    rx.text(f"{VehicleState.selected_vehicle.get('tuned_power', 0)} CV", 
                            font_size="2rem", font_weight="700", color="#FF6B35"),
                    spacing="2",
                    align="center"
                ),
                bg="#2D2D2D",
                border_radius="20px",
                p="6",
                border="1px solid #666666"
            ),
            columns="2",
            spacing="6",
            margin_bottom="6"
        ),
        rx.vstack(
            rx.text("Beneficios de la reprogramación:", color="white", font_weight="600", margin_bottom="3"),
            rx.vstack(
                rx.text(f"⚡ Incremento de potencia: +{VehicleState.power_increase} CV", color="white"),
                rx.text("💰 Reducción de consumo: hasta -15%", color="white"),
                rx.text("🔧 Proceso completamente reversible", color="white"),
                rx.text("🛡️ Garantía incluida", color="white"),
                spacing="2",
                align="start"
            ),
            spacing="2",
            align="start",
            margin_bottom="6"
        ),
        rx.box(
            rx.vstack(
                rx.text(f"€{VehicleState.selected_vehicle.get('price', 0)}", 
                        font_size="2.5rem", font_weight="700", color="#FF6B35"),
                rx.text("Precio incluye: Reprogramación + Backup + Garantía", color="#666666"),
                rx.button(
                    "Solicitar Información",
                    bg="#FF6B35",
                    color="white",
                    size="3",
                    border_radius="20px",
                    margin_bottom="4",
                    _hover={"bg": "#e55a2b", "transform": "translateY(-2px)"},
                    transition="all 0.3s ease"
                ),
                spacing="3",
                align="center"
            ),
            text_align="center"
        ),
        rx.hstack(
            rx.button(
                "← Volver",
                bg="transparent",
                color="#FF6B35",
                border="1px solid #FF6B35",
                border_radius="20px",
                p="2",
                on_click=VehicleState.go_back,
                _hover={"bg": "rgba(255, 107, 53, 0.1)"}
            ),
            rx.button(
                "Nuevo Cálculo",
                bg="transparent",
                color="#FF6B35",
                border="1px solid #FF6B35",
                border_radius="20px",
                p="2",
                on_click=VehicleState.reset_selector,
                _hover={"bg": "rgba(255, 107, 53, 0.1)"}
            ),
            spacing="4",
            justify="center",
            mt="6"
        ),
        spacing="6",
        align="center",
        class_name="vehicle-selector-step",
        max_width="600px"
    )

def vehicle_selector() -> rx.Component:
    """Selector principal de vehículos con pasos dinámicos"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading(
                    "Encuentra tu vehículo", 
                    size="8", 
                    color="white", 
                    text_align="center", 
                    mb="12",
                    bg_image="linear-gradient(45deg, #FF6B35, #FF8C42)",
                    bg_clip="text",
                    text_fill_color="transparent",
                ),
                rx.center(
                    rx.box(
                        rx.cond(
                            VehicleState.current_step == 1,
                            fuel_selection(),
                            rx.cond(
                                VehicleState.current_step == 2,
                                brand_selection(),
                                rx.cond(
                                    VehicleState.current_step == 3,
                                    model_selection(),
                                    rx.cond(
                                        VehicleState.current_step == 4,
                                        year_selection(),
                                        vehicle_details()
                                    )
                                )
                            )
                        ),
                        bg="#1A1A1A",
                        border_radius="20px",
                        p={"base": "8", "md": "12"},
                        box_shadow="0 8px 25px rgba(0, 0, 0, 0.3)",
                        border="1px solid #404040",
                        max_width="900px",
                        width="100%",
                        min_height="300px"
                    ),
                    width="100%",
                    mx="auto"
                ),
                spacing="6",
                align="center",
                width="100%",
                mx="auto"
            ),
            max_width="1000px",
            mx="auto",
            px={"base": "6", "md": "8"},
            py={"base": "16", "md": "20"}
        ),
        bg="#1A1A1A",
        id="selector"
    )