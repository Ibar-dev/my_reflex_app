"""
Estado simplificado del selector de vehículos - Compatible con rx.select
========================================================================
"""

import reflex as rx


class VehicleState(rx.State):
    """Estado simplificado del selector de vehículos"""
    
    # Valores seleccionados
    selected_fuel: str = ""
    selected_brand: str = ""
    selected_model: str = ""
    selected_year: str = ""
    
    # Opciones disponibles para cada dropdown - Inicializadas con valores por defecto
    available_fuel_types: list[str] = ["diesel", "gasolina"]
    available_brands: list[str] = []
    available_models: list[str] = []
    available_years: list[str] = []
    
    # Flag para saber si ya se cargaron los datos
    _data_loaded: bool = False
    
    @rx.var
    def fuel_options(self) -> list[str]:
        """Opciones de combustible disponibles"""
        if not self._data_loaded:
            self._load_initial_data()
        return self.available_fuel_types
    
    def _load_initial_data(self):
        """Cargar datos iniciales una sola vez"""
        if self._data_loaded:
            return
            
        print("🚀 VehicleState cargando datos iniciales...")
        
        try:
            from utils.vehicle_data import get_fuel_types, load_vehicle_data
            
            # Cargar datos para verificar conexión
            vehicles = load_vehicle_data()
            print(f"✅ Cargados {len(vehicles)} vehículos")
            
            # Cargar tipos de combustible
            self.available_fuel_types = get_fuel_types()
            print(f"🔥 Tipos de combustible: {self.available_fuel_types}")
            
            self._data_loaded = True
            
        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            self.available_fuel_types = ["diesel", "gasolina"]
            self._data_loaded = True
    
    def select_fuel(self, fuel: str):
        """Cuando se selecciona un tipo de combustible"""
        print(f"🔥 [SELECT] Combustible seleccionado: '{fuel}'")
        
        self.selected_fuel = fuel
        self.selected_brand = ""
        self.selected_model = ""
        self.selected_year = ""
        
        # Cargar marcas disponibles para este combustible
        try:
            from utils.vehicle_data import get_brands_by_fuel
            self.available_brands = get_brands_by_fuel(fuel)
            print(f"✅ Marcas cargadas: {len(self.available_brands)}")
        except Exception as e:
            print(f"❌ Error cargando marcas: {e}")
            self.available_brands = []
        
        # Limpiar opciones posteriores
        self.available_models = []
        self.available_years = []
    
    def select_brand(self, brand: str):
        """Cuando se selecciona una marca"""
        print(f"🏭 [SELECT] Marca seleccionada: '{brand}'")
        
        self.selected_brand = brand
        self.selected_model = ""
        self.selected_year = ""
        
        # Cargar modelos disponibles para esta marca y combustible
        try:
            from utils.vehicle_data import get_models_by_fuel_and_brand
            self.available_models = get_models_by_fuel_and_brand(self.selected_fuel, brand)
            print(f"✅ Modelos cargados: {len(self.available_models)}")
        except Exception as e:
            print(f"❌ Error cargando modelos: {e}")
            self.available_models = []
        
        # Limpiar opciones posteriores
        self.available_years = []
    
    def select_model(self, model: str):
        """Cuando se selecciona un modelo"""
        print(f"🚗 [SELECT] Modelo seleccionado: '{model}'")
        
        self.selected_model = model
        self.selected_year = ""
        
        # Cargar años disponibles para este modelo, marca y combustible
        try:
            from utils.vehicle_data import get_years_by_fuel_brand_model
            self.available_years = get_years_by_fuel_brand_model(
                self.selected_fuel, 
                self.selected_brand, 
                model
            )
            print(f"✅ Años cargados: {len(self.available_years)}")
        except Exception as e:
            print(f"❌ Error cargando años: {e}")
            self.available_years = []
    
    def select_year(self, year: str):
        """Cuando se selecciona un año"""
        print(f"📅 [SELECT] Año seleccionado: '{year}'")
        
        self.selected_year = year
        
        print(f"🎉 Selección completa:")
        print(f"   Combustible: {self.selected_fuel}")
        print(f"   Marca: {self.selected_brand}")
        print(f"   Modelo: {self.selected_model}")
        print(f"   Año: {self.selected_year}")