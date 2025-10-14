"""
Estado simplificado del selector de vehículos - Compatible con rx.select
========================================================================
"""

import reflex as rx
import asyncio


class VehicleState(rx.State):
    """Estado simplificado del selector de vehículos con soporte para API externa"""
    
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
    
    # Nuevas variables para API
    api_loading: bool = False
    api_last_sync: str = ""
    api_total_vehicles: int = 0
    api_data_source: str = "local"  # "local" | "api" | "cache"
    
    # Flag para saber si ya se cargaron los datos
    _data_loaded: bool = False
    _api_data: dict = {}
    
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
            # Intentar cargar desde API cache primero
            from services.vehicle_api_service import get_api_cache_stats
            cache_stats = get_api_cache_stats()
            
            if cache_stats.get("cached") and cache_stats.get("cache_valid"):
                print("✅ Usando datos de API (cache válido)")
                self._load_from_api_cache()
                self.api_data_source = "cache"
            else:
                # Fallback a datos locales
                print("⚠️ Cache API no válido, usando datos locales")
                self._load_from_local_json()
                self.api_data_source = "local"
            
        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            # Fallback seguro a datos locales
            self._load_from_local_json()
            self.api_data_source = "local"
        
        self._data_loaded = True
    
    def _load_from_local_json(self):
        """Cargar desde JSON local (fallback)"""
        try:
            from utils.vehicle_data import get_fuel_types, load_vehicle_data
            
            vehicles = load_vehicle_data()
            print(f"✅ Cargados {len(vehicles)} vehículos desde JSON local")
            
            self.available_fuel_types = get_fuel_types()
            print(f"🔥 Tipos de combustible: {self.available_fuel_types}")
            
            # Extraer marcas únicas
            brands = set()
            for vehicle in vehicles:
                brands.add(vehicle.get("marca", ""))
            
            self.available_brands = sorted(list(brands))
            print(f"🚗 Marcas disponibles: {len(self.available_brands)}")
            
        except Exception as e:
            print(f"❌ Error cargando datos locales: {e}")
    
    def _load_from_api_cache(self):
        """Cargar desde cache de API"""
        try:
            from services.vehicle_api_service import VehicleAPIService
            service = VehicleAPIService()
            cached_data = service._load_cache()
            
            if cached_data and 'data' in cached_data:
                self._api_data = cached_data['data']
                self.available_brands = sorted(list(self._api_data.keys()))
                self.api_total_vehicles = sum(len(models) for models in self._api_data.values())
                self.api_last_sync = cached_data.get('cached_at', 'Desconocido')
                
                print(f"✅ Cargados {len(self.available_brands)} marcas desde API cache")
                print(f"📊 Total vehículos API: {self.api_total_vehicles}")
                
        except Exception as e:
            print(f"❌ Error cargando desde API cache: {e}")
    
    async def sync_vehicles_from_api(self):
        """Sincronizar vehículos desde APIs externas"""
        self.api_loading = True
        
        try:
            print("🔄 Iniciando sincronización desde APIs externas...")
            from services.vehicle_api_service import sync_vehicles_from_api
            
            # Sincronizar datos
            api_data = await sync_vehicles_from_api()
            
            if api_data:
                self._api_data = api_data
                self.available_brands = sorted(list(api_data.keys()))
                self.api_total_vehicles = sum(len(models) for models in api_data.values())
                self.api_last_sync = "Ahora mismo"
                self.api_data_source = "api"
                
                # Limpiar selecciones actuales para forzar actualización
                self.selected_brand = ""
                self.selected_model = ""
                self.selected_year = ""
                self.available_models = []
                self.available_years = []
                
                print(f"✅ Sincronización completada: {len(self.available_brands)} marcas")
            else:
                print("⚠️ No se pudieron obtener datos de API")
                
        except Exception as e:
            print(f"❌ Error sincronizando desde API: {e}")
        finally:
            self.api_loading = False
    
    def get_api_stats(self) -> dict:
        """Obtener estadísticas de la API"""
        from services.vehicle_api_service import get_api_cache_stats
        return get_api_cache_stats()
    
    def select_fuel(self, fuel: str):
        """Cuando se selecciona un tipo de combustible"""
        print(f"🔥 [SELECT] Combustible seleccionado: '{fuel}'")
        
        self.selected_fuel = fuel
        self.selected_brand = ""
        self.selected_model = ""
        self.selected_year = ""
        
        # Cargar marcas disponibles para este combustible
        if self.api_data_source in ["api", "cache"] and self._api_data:
            # Usar datos de API
            self.available_brands = sorted(list(self._api_data.keys()))
            print(f"✅ Marcas cargadas desde API: {len(self.available_brands)}")
        else:
            # Fallback a datos locales
            try:
                from utils.vehicle_data import get_brands_by_fuel
                self.available_brands = get_brands_by_fuel(fuel)
                print(f"✅ Marcas cargadas desde local: {len(self.available_brands)}")
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
        
        # Cargar modelos disponibles para esta marca
        if self.api_data_source in ["api", "cache"] and self._api_data and brand in self._api_data:
            # Usar datos de API
            models_data = self._api_data[brand]
            self.available_models = [model_info["model"] for model_info in models_data]
            print(f"✅ Modelos cargados desde API: {len(self.available_models)}")
        else:
            # Fallback a datos locales
            try:
                from utils.vehicle_data import get_models_by_fuel_and_brand
                self.available_models = get_models_by_fuel_and_brand(self.selected_fuel, brand)
                print(f"✅ Modelos cargados desde local: {len(self.available_models)}")
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
        
        # Usar datos de API si están disponibles
        if self.api_data_source == "api" and hasattr(self, '_vehicle_api_data'):
            try:
                # Filtrar años de los datos de API
                api_years = set()
                for vehicle in self._vehicle_api_data.get('vehicles', []):
                    if (vehicle.get('brand', '').lower() == self.selected_brand.lower() and 
                        vehicle.get('model', '').lower() == model.lower()):
                        year = vehicle.get('year')
                        if year:
                            api_years.add(str(year))  # Convertir a string
                
                # Asegurar que todos sean strings y ordenar
                self.available_years = sorted([str(y) for y in api_years], reverse=True)
                print(f"✅ Años cargados desde API: {len(self.available_years)} → {self.available_years[:5]}")
                return
            except Exception as e:
                print(f"❌ Error procesando años de API: {e}")
        
        # Fallback a datos locales
        try:
            from utils.vehicle_data import get_years_by_fuel_brand_model
            years_local = get_years_by_fuel_brand_model(
                self.selected_fuel, 
                self.selected_brand, 
                model
            )
            # Asegurar que todos sean strings
            self.available_years = [str(y) for y in years_local]
            print(f"✅ Años cargados desde datos locales: {len(self.available_years)} → {self.available_years[:5]}")
        except Exception as e:
            print(f"❌ Error cargando años: {e}")
            self.available_years = []
    
    def select_year(self, year: str):
        """Cuando se selecciona un año"""
        # Debug detallado
        print(f"📊 [DEBUG] select_year llamado con: tipo={type(year)}, valor='{year}', repr={repr(year)}")
        
        # Convertir a string y limpiar
        year_str = str(year).strip()
        
        # Validar - solo rechazar None, vacío o "None" literal
        if not year_str or year_str == "None" or year_str == "null":
            print(f"⚠️ [SELECT] Año inválido recibido: '{year_str}', ignorando...")
            return
            
        print(f"📅 [SELECT] Año seleccionado: '{year_str}'")
        
        self.selected_year = year_str
        
        print(f"🎉 Selección completa:")
        print(f"   Combustible: {self.selected_fuel}")
        print(f"   Marca: {self.selected_brand}")
        print(f"   Modelo: {self.selected_model}")
        print(f"   Año: {self.selected_year}")
    
    def submit_vehicle_selection(self):
        """
        ⚠️ MÉTODO PARA BACKEND ⚠️
        
        Envía la selección del vehículo al backend.
        
        TODO BACKEND: Implementar la llamada a la API aquí
        
        Datos disponibles:
        - self.selected_fuel: Tipo de combustible (diesel/gasolina)
        - self.selected_brand: Marca del vehículo
        - self.selected_model: Modelo del vehículo
        - self.selected_year: Año del vehículo
        
        Ejemplo de implementación:
        
        import requests
        
        response = requests.post(
            "https://tu-api.com/vehicle/submit",
            json={
                "fuel": self.selected_fuel,
                "brand": self.selected_brand,
                "model": self.selected_model,
                "year": self.selected_year
            }
        )
        
        if response.status_code == 200:
            print("✅ Datos enviados correctamente")
            # Mostrar mensaje de éxito al usuario
        else:
            print("❌ Error al enviar los datos")
            # Mostrar mensaje de error al usuario
        """
        
        # Log temporal - ELIMINAR cuando se implemente el backend
        print("\n" + "="*60)
        print("📤 DATOS LISTOS PARA ENVIAR AL BACKEND:")
        print("="*60)
        print(f"🔥 Combustible: {self.selected_fuel}")
        print(f"🏭 Marca: {self.selected_brand}")
        print(f"🚗 Modelo: {self.selected_model}")
        print(f"📅 Año: {self.selected_year}")
        print("="*60)
        print("⚠️  TODO: Implementar llamada al backend aquí")
        print("="*60 + "\n")
        
        # TODO BACKEND: Implementar aquí la lógica de envío
        # Ejemplo:
        # try:
        #     response = tu_api_call(
        #         fuel=self.selected_fuel,
        #         brand=self.selected_brand,
        #         model=self.selected_model,
        #         year=self.selected_year
        #     )
        #     return {"success": True, "message": "Datos enviados correctamente"}
        # except Exception as e:
        #     return {"success": False, "message": str(e)}