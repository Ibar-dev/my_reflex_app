"""
Estado del selector de vehículos AstroTech
=========================================

Maneja toda la lógica del selector de vehículos paso a paso.
"""

import reflex as rx


class VehicleState(rx.State):
    """Estado del selector de vehículos"""
    
    # Datos de selección
    selected_fuel: str = ""
    selected_brand: str = ""
    selected_model: str = ""
    selected_year: str = ""
    current_step: int = 1
    
    # Listas disponibles
    available_brands: list[str] = []
    available_models: list[str] = []
    available_years: list[str] = []
    available_vehicles: list = []
    selected_vehicle: dict = {}
    
    def select_fuel(self, fuel: str):
        """Selecciona el tipo de combustible"""
        print(f"DEBUG: select_fuel llamado con {fuel}")
        self.selected_fuel = fuel
        self.selected_brand = ""
        self.selected_model = ""
        self.selected_year = ""
        
        # Cargar marcas disponibles desde JSON
        try:
            from utils.vehicle_data import get_brands_by_fuel
            self.available_brands = get_brands_by_fuel(fuel)
            print(f"DEBUG: Marcas cargadas desde JSON: {self.available_brands}")
        except Exception as e:
            print(f"DEBUG: Error cargando desde JSON: {e}")
            # Fallback con marcas europeas populares
            self.available_brands = ["Toyota", "Ford", "Audi", "BMW", "Mercedes-Benz", "Volkswagen", "SEAT"]
            
        self.available_models = []
        self.available_years = []
        self.current_step = 2
        print(f"DEBUG: current_step cambiado a {self.current_step}")
    
    def select_brand(self, brand: str):
        """Seleccionar marca"""
        print(f"DEBUG: select_brand llamado con {brand}")
        self.selected_brand = brand
        self.selected_model = "Modelo General"  # Usar modelo genérico
        self.selected_year = "2023"  # Usar año genérico
        
        # Crear vehículo de ejemplo basado en la marca y combustible
        try:
            # Intentar cargar datos reales del JSON
            from utils.vehicle_data import get_models_by_brand, get_vehicles_by_brand_model
            models = get_models_by_brand(brand, self.selected_fuel)
            
            if models:
                # Usar el primer modelo disponible
                self.selected_model = models[0]
                vehicles = get_vehicles_by_brand_model(brand, self.selected_model, self.selected_fuel)
                if vehicles:
                    self.selected_vehicle = vehicles[0]
                else:
                    self._create_default_vehicle(brand)
            else:
                self._create_default_vehicle(brand)
                
        except Exception as e:
            print(f"DEBUG: Error cargando desde JSON: {e}")
            self._create_default_vehicle(brand)
            
        self.current_step = 5  # Ir directamente a resultados
        print(f"DEBUG: Vehículo seleccionado: {brand} {self.selected_model}")
    
    def _create_default_vehicle(self, brand: str):
        """Crear vehículo por defecto para demo"""
        # Datos específicos por marca
        brand_specs = {
            "Toyota": {"power_stock": 116, "torque_stock": 270, "power_tuned": 145, "torque_tuned": 320, "gain": 29, "torque_gain": 50, "fuel_reduction": 10},
            "Ford": {"power_stock": 150, "torque_stock": 370, "power_tuned": 190, "torque_tuned": 420, "gain": 40, "torque_gain": 50, "fuel_reduction": 12},
            "Audi": {"power_stock": 150, "torque_stock": 320, "power_tuned": 190, "torque_tuned": 380, "gain": 40, "torque_gain": 60, "fuel_reduction": 15},
            "BMW": {"power_stock": 150, "torque_stock": 320, "power_tuned": 190, "torque_tuned": 380, "gain": 40, "torque_gain": 60, "fuel_reduction": 12},
            "Mercedes-Benz": {"power_stock": 170, "torque_stock": 360, "power_tuned": 220, "torque_tuned": 440, "gain": 50, "torque_gain": 80, "fuel_reduction": 15},
            "Volkswagen": {"power_stock": 150, "torque_stock": 320, "power_tuned": 190, "torque_tuned": 380, "gain": 40, "torque_gain": 60, "fuel_reduction": 15},
            "Honda": {"power_stock": 120, "torque_stock": 300, "power_tuned": 150, "torque_tuned": 360, "gain": 30, "torque_gain": 60, "fuel_reduction": 12},
            "Chevrolet": {"power_stock": 136, "torque_stock": 320, "power_tuned": 170, "torque_tuned": 380, "gain": 34, "torque_gain": 60, "fuel_reduction": 12},
            "Hyundai": {"power_stock": 136, "torque_stock": 280, "power_tuned": 170, "torque_tuned": 340, "gain": 34, "torque_gain": 60, "fuel_reduction": 12},
            "Nissan": {"power_stock": 115, "torque_stock": 260, "power_tuned": 145, "torque_tuned": 320, "gain": 30, "torque_gain": 60, "fuel_reduction": 12}
        }
        
        specs = brand_specs.get(brand, {"power_stock": 150, "torque_stock": 300, "power_tuned": 190, "torque_tuned": 380, "gain": 40, "torque_gain": 80, "fuel_reduction": 12})
        
        self.selected_vehicle = {
            "make": brand,
            "model": self.selected_model,
            "year": 2023,
            "fuel_type": self.selected_fuel,
            "power_stock": specs["power_stock"],
            "torque_stock": specs["torque_stock"],
            "engine_name": f"Motor {self.selected_fuel.title()}",
            "displacement": "2.0L",
            "ecu_brand": "Bosch",
            "tuning_potential": {
                "power_tuned": specs["power_tuned"],
                "torque_tuned": specs["torque_tuned"],
                "power_gain": specs["gain"],
                "torque_gain": specs["torque_gain"],
                "fuel_reduction": specs["fuel_reduction"]
            }
        }
    
    def select_model(self, model: str):
        """Seleccionar modelo"""
        print(f"DEBUG: select_model llamado con {model}")
        self.selected_model = model
        self.selected_year = ""
        
        # Cargar vehículos disponibles desde JSON
        try:
            from utils.vehicle_data import get_vehicles_by_brand_model
            vehicles = get_vehicles_by_brand_model(self.selected_brand, model, self.selected_fuel)
            # Extraer años únicos
            years = list(set([str(v.get('year', '')) for v in vehicles if v.get('year')]))
            self.available_years = sorted(years, reverse=True)
            self.available_vehicles = vehicles
            print(f"DEBUG: Años encontrados: {self.available_years}")
        except Exception as e:
            print(f"DEBUG: Error cargando años desde JSON: {e}")
            # Fallback con años estáticos
            self.available_years = ["2023", "2022", "2021", "2020", "2019", "2018"]
            self.available_vehicles = []
            
        self.current_step = 4
    
    def select_year(self, year: str):
        """Seleccionar año"""
        print(f"DEBUG: select_year llamado con {year}")
        self.selected_year = year
        
        # Buscar el vehículo específico
        try:
            selected_vehicles = [v for v in self.available_vehicles if str(v.get('year', '')) == year]
            if selected_vehicles:
                self.selected_vehicle = selected_vehicles[0]  # Tomar el primero
                print(f"DEBUG: Vehículo seleccionado: {self.selected_vehicle.get('make', '')} {self.selected_vehicle.get('model', '')} {self.selected_vehicle.get('year', '')}")
            else:
                # Crear vehículo de ejemplo
                self.selected_vehicle = {
                    "make": self.selected_brand,
                    "model": self.selected_model,
                    "year": int(year),
                    "fuel_type": self.selected_fuel,
                    "power_stock": 150,
                    "torque_stock": 300,
                    "engine_name": f"{self.selected_fuel.title()} Engine",
                    "displacement": "2.0L",
                    "ecu_brand": "Bosch",
                    "tuning_potential": {
                        "power_tuned": 190,
                        "torque_tuned": 380,
                        "power_gain": 40,
                        "torque_gain": 80,
                        "fuel_reduction": 12
                    }
                }
        except Exception as e:
            print(f"DEBUG: Error seleccionando vehículo: {e}")
            
        self.current_step = 5
    
    def go_back(self):
        """Volver al paso anterior"""
        print(f"DEBUG: go_back llamado desde step {self.current_step}")
        if self.current_step > 1:
            self.current_step -= 1
            if self.current_step == 1:
                self.selected_fuel = ""
                self.available_brands = []
                self.available_models = []
                self.available_years = []
            elif self.current_step == 2:
                self.selected_brand = ""
                self.available_models = []
                self.available_years = []
            elif self.current_step == 3:
                self.selected_model = ""
                self.available_years = []
            elif self.current_step == 4:
                self.selected_year = ""
                self.selected_vehicle = {}
        print(f"DEBUG: Nuevo step: {self.current_step}")
    
    def reset_selector(self):
        """Reiniciar selector"""
        print("DEBUG: reset_selector llamado")
        self.selected_fuel = ""
        self.selected_brand = ""
        self.selected_model = ""
        self.selected_year = ""
        self.available_brands = []
        self.available_models = []
        self.available_years = []
        self.available_vehicles = []
        self.selected_vehicle = {}
        self.current_step = 1
    
    @rx.var
    def vehicle_power_stock(self) -> int:
        """Potencia original del vehículo"""
        if not self.selected_vehicle:
            return 150
        return self.selected_vehicle.get('power_stock', 150)
    
    @rx.var
    def vehicle_power_tuned(self) -> int:
        """Potencia optimizada del vehículo"""
        if not self.selected_vehicle:
            return 190
        return self.selected_vehicle.get('tuning_potential', {}).get('power_tuned', 190)
    
    @rx.var
    def vehicle_power_gain(self) -> int:
        """Incremento de potencia"""
        if not self.selected_vehicle:
            return 40
        return self.selected_vehicle.get('tuning_potential', {}).get('power_gain', 40)
    
    @rx.var
    def vehicle_torque_gain(self) -> int:
        """Incremento de par"""
        if not self.selected_vehicle:
            return 80
        return self.selected_vehicle.get('tuning_potential', {}).get('torque_gain', 80)
    
    @rx.var
    def vehicle_fuel_reduction(self) -> int:
        """Reducción de combustible"""
        if not self.selected_vehicle:
            return 12
        return self.selected_vehicle.get('tuning_potential', {}).get('fuel_reduction', 12)
    
    @rx.var
    def vehicle_price(self) -> int:
        """Precio calculado según potencia"""
        base_price = 250
        gain = self.vehicle_power_gain if self.selected_vehicle else 40
        return base_price + (gain * 8)
