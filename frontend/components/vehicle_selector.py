"""
Componente VehicleSelector - Selector de vehículos para reprogramación ECU
=========================================================================

Selector interactivo paso a paso con animaciones y efectos visuales modernos.
"""

import reflex as rx

# Datos de vehículos (simulados)
vehicles_data = {
    "Audi": {
        "A3": [
            {"year": 2020, "fuel_type": "diesel", "original_power": 150, "tuned_power": 190, "consumption_reduction": 12, "price": 350, "description": "Audi A3 2.0 TDI - Incremento de potencia del 27%"},
            {"year": 2021, "fuel_type": "gasolina", "original_power": 140, "tuned_power": 175, "consumption_reduction": 8, "price": 320, "description": "Audi A3 1.4 TFSI - Incremento de potencia del 25%"}
        ],
        "A4": [
            {"year": 2021, "fuel_type": "diesel", "original_power": 190, "tuned_power": 240, "consumption_reduction": 15, "price": 450, "description": "Audi A4 2.0 TDI - Incremento de potencia del 26%"},
            {"year": 2021, "fuel_type": "gasolina", "original_power": 190, "tuned_power": 235, "consumption_reduction": 10, "price": 420, "description": "Audi A4 2.0 TFSI - Incremento de potencia del 24%"}
        ]
    },
    "BMW": {
        "Serie 3": [
            {"year": 2021, "fuel_type": "diesel", "original_power": 190, "tuned_power": 240, "consumption_reduction": 13, "price": 460, "description": "BMW Serie 3 320d - Incremento de potencia del 26%"},
            {"year": 2021, "fuel_type": "gasolina", "original_power": 184, "tuned_power": 230, "consumption_reduction": 8, "price": 420, "description": "BMW Serie 3 320i - Incremento de potencia del 25%"}
        ],
        "X3": [
            {"year": 2021, "fuel_type": "diesel", "original_power": 190, "tuned_power": 245, "consumption_reduction": 14, "price": 480, "description": "BMW X3 xDrive20d - Incremento de potencia del 29%"}
        ]
    },
    "Mercedes-Benz": {
        "Clase C": [
            {"year": 2021, "fuel_type": "diesel", "original_power": 194, "tuned_power": 245, "consumption_reduction": 14, "price": 470, "description": "Mercedes Clase C 220d - Incremento de potencia del 26%"}
        ]
    },
    "Volkswagen": {
        "Golf": [
            {"year": 2021, "fuel_type": "diesel", "original_power": 150, "tuned_power": 190, "consumption_reduction": 12, "price": 350, "description": "Volkswagen Golf 2.0 TDI - Incremento de potencia del 27%"},
            {"year": 2020, "fuel_type": "gasolina", "original_power": 150, "tuned_power": 185, "consumption_reduction": 8, "price": 320, "description": "Volkswagen Golf 1.5 TSI - Incremento de potencia del 23%"}
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
    
    def select_fuel(self, fuel: str):
        self.selected_fuel = fuel
        self.selected_brand = ""
        self.selected_model = ""
        self.selected_vehicle = {}
        self.current_step = 2
    
    def select_brand(self, brand: str):
        self.selected_brand = brand
        self.selected_model = ""
        self.selected_vehicle = {}
        self.current_step = 3
    
    def select_model(self, model: str):
        self.selected_model = model
        self.selected_vehicle = {}
        self.current_step = 4
    
    def select_vehicle(self, vehicle: dict):
        self.selected_vehicle = vehicle
        self.power_increase = vehicle.get('tuned_power', 0) - vehicle.get('original_power', 0)
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
    """Paso 1: Selección de combustible"""
    return rx.vstack(
        rx.heading("1. Selecciona el tipo de combustible", size="6", color="white", text_align="center", margin_bottom="8"),
        rx.center(
            rx.hstack(
                rx.button(
                    rx.vstack(
                        rx.icon("fuel", size=32, color="#FF6B35"),
                        rx.text("Diésel", font_weight="600", color="white", font_size="1.1rem"),
                        spacing="3",
                        align="center"
                    ),
                    bg="#2D2D2D",
                    border="2px solid #666666",
                    border_radius="15px",
                    p="6",
                    width={"base": "140px", "md": "160px"},
                    height={"base": "120px", "md": "140px"},
                    _hover={
                        "border_color": "#FF6B35",
                        "transform": "translateY(-5px)",
                        "box_shadow": "0 8px 15px rgba(255, 107, 53, 0.3)",
                        "bg": "rgba(255, 107, 53, 0.05)"
                    },
                    transition="all 0.3s ease",
                    on_click=VehicleState.select_fuel("diesel"),
                ),
                rx.button(
                    rx.vstack(
                        rx.icon("fuel", size=32, color="#FF6B35"),
                        rx.text("Gasolina", font_weight="600", color="white", font_size="1.1rem"),
                        spacing="3",
                        align="center"
                    ),
                    bg="#2D2D2D",
                    border="2px solid #666666",
                    border_radius="15px",
                    p="6",
                    width={"base": "140px", "md": "160px"},
                    height={"base": "120px", "md": "140px"},
                    _hover={
                        "border_color": "#FF6B35",
                        "transform": "translateY(-5px)",
                        "box_shadow": "0 8px 15px rgba(255, 107, 53, 0.3)",
                        "bg": "rgba(255, 107, 53, 0.05)"
                    },
                    transition="all 0.3s ease",
                    on_click=VehicleState.select_fuel("gasolina"),
                ),
                spacing={"base": "6", "md": "8"},
                justify="center",
                wrap="wrap"
            ),
            width="100%"
        ),
        spacing="8",
        align="center",
        class_name="vehicle-selector-step",
        width="100%"
    )

def brand_selection() -> rx.Component:
    """Paso 2: Selección de marca"""
    return rx.vstack(
        rx.heading("2. Selecciona la marca", size="6", color="white", margin_bottom="6"),
        rx.grid(
            *[
                rx.button(
                    brand,
                    bg="#1A1A1A",
                    border="2px solid #666666",
                    border_radius="10px",
                    p="4",
                    color="white",
                    font_weight="500",
                    _hover={
                        "border_color": "#FF6B35",
                        "bg": "rgba(255, 107, 53, 0.1)"
                    },
                    transition="all 0.3s ease",
                    on_click=VehicleState.select_brand(brand),
                )
                for brand in vehicles_data.keys()
            ],
            columns="4",
            spacing="4",
            width="100%"
        ),
        rx.button(
            "← Volver",
            bg="transparent",
            color="#FF6B35",
            border="1px solid #FF6B35",
            border_radius="8px",
            p="2",
            margin_bottom="4",
            on_click=VehicleState.go_back,
            _hover={"bg": "rgba(255, 107, 53, 0.1)"}
        ),
        spacing="6",
        align="center",
    )

def model_selection() -> rx.Component:
    """Paso 3: Selección de modelo"""
    return rx.vstack(
        rx.heading("3. Selecciona el modelo", size="6", color="white", margin_bottom="6"),
        rx.grid(
            *[
                rx.button(
                    model,
                    bg="#1A1A1A",
                    border="2px solid #666666",
                    border_radius="10px",
                    p="4",
                    color="white",
                    font_weight="500",
                    _hover={
                        "border_color": "#FF6B35",
                        "bg": "rgba(255, 107, 53, 0.1)"
                    },
                    transition="all 0.3s ease",
                    on_click=VehicleState.select_model(model),
                )
                for model in vehicles_data.get(VehicleState.selected_brand, {}).keys()
            ],
            columns="3",
            spacing="4",
            width="100%"
        ),
        rx.button(
            "← Volver",
            bg="transparent",
            color="#FF6B35",
            border="1px solid #FF6B35",
            border_radius="8px",
            p="2",
            margin_bottom="4",
            on_click=VehicleState.go_back,
            _hover={"bg": "rgba(255, 107, 53, 0.1)"}
        ),
        spacing="6",
        align="center",
    )

def year_selection() -> rx.Component:
    """Paso 4: Selección de año y motor"""
    return rx.vstack(
        rx.heading("4. Selecciona el año y motor", size="6", color="white", margin_bottom="6"),
        rx.grid(
            *[
                rx.button(
                    rx.vstack(
                        rx.text(str(vehicle["year"]), font_weight="bold", font_size="1.2rem"),
                        rx.text(f"{vehicle['original_power']}CV → {vehicle['tuned_power']}CV", font_size="0.9rem", color="#FF6B35"),
                        spacing="1",
                        align="center"
                    ),
                    bg="#1A1A1A",
                    border="2px solid #666666",
                    border_radius="10px",
                    p="4",
                    color="white",
                    _hover={
                        "border_color": "#FF6B35",
                        "bg": "rgba(255, 107, 53, 0.1)"
                    },
                    transition="all 0.3s ease",
                    on_click=VehicleState.select_vehicle(vehicle),
                )
                for vehicle in vehicles_data.get(VehicleState.selected_brand, {}).get(VehicleState.selected_model, [])
                if vehicle["fuel_type"] == VehicleState.selected_fuel
            ],
            columns="2",
            spacing="4",
            width="100%"
        ),
        rx.button(
            "← Volver",
            bg="transparent",
            color="#FF6B35",
            border="1px solid #FF6B35",
            border_radius="8px",
            p="2",
            margin_bottom="4",
            on_click=VehicleState.go_back,
            _hover={"bg": "rgba(255, 107, 53, 0.1)"}
        ),
        spacing="6",
        align="center",
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
                border_radius="10px",
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
                border_radius="10px",
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
                    border_radius="8px",
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
                border_radius="8px",
                p="2",
                on_click=VehicleState.go_back,
                _hover={"bg": "rgba(255, 107, 53, 0.1)"}
            ),
            rx.button(
                "Nuevo Cálculo",
                bg="transparent",
                color="#FF6B35",
                border="1px solid #FF6B35",
                border_radius="8px",
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
                rx.heading("Encuentra tu vehículo", size="8", color="white", text_align="center", mb="12"),
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
                    width="100%"
                ),
                spacing="6",
                align="center",
                width="100%"
            ),
            max_width="1200px",
            px={"base": "6", "md": "8"},
            py={"base": "16", "md": "20"}
        ),
        bg="#1A1A1A",
        id="selector"
    )