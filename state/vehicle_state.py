"""
Estado simplificado del selector de vehículos - Compatible con rx.select
========================================================================
"""

import reflex as rx


class VehicleState(rx.State):
    """Estado simplificado del selector de vehículos con soporte para API externa"""

    # Valores seleccionados
    selected_fuel: str = ""
    selected_brand: str = ""
    selected_model: str = ""
    selected_year: str = ""
    selected_version: str = ""

    # Opciones disponibles para cada dropdown - Inicializadas con valores por defecto
    available_fuel_types: list[str] = ["gasolina", "diesel"]
    available_brands: list[str] = []
    available_models: list[str] = []
    available_years: list[str] = []
    available_versions: list[str] = []

    # Nuevas variables para API
    api_loading: bool = False
    api_last_sync: str = ""
    api_total_vehicles: int = 0
    api_data_source: str = "local"  # "local" | "api" | "cache"

    # Flag para saber si ya se cargaron los datos
    _data_loaded: bool = False
    _api_data: dict = {}

    def on_load(self):
        """Inicializa los datos cuando el estado se carga en la aplicación"""
        if not self._data_loaded:
            try:
                from services.vehicle_api_service import get_fuel_types
                fuel_types = get_fuel_types()
                self.available_fuel_types = fuel_types
                self._data_loaded = True
                print(f"[VEHICLE_STATE] Datos cargados con {len(fuel_types)} tipos de combustible")
            except Exception as e:
                print(f"[VEHICLE_STATE] Error cargando datos: {str(e)}")
                self.available_fuel_types = ["gasolina", "diesel"]
                self._data_loaded = True

    def select_fuel(self, fuel: str):
        print(f"[FUEL] [SELECT] Combustible seleccionado: '{fuel}'")
        self.selected_fuel = fuel
        self.selected_brand = ""
        self.selected_model = ""
        self.selected_year = ""
        self.selected_version = ""
        from services.vehicle_api_service import get_brands
        self.available_brands = get_brands(fuel)
        self.available_models = []
        self.available_years = []
        self.available_versions = []

    def select_brand(self, brand: str):
        print(f"[BRAND] [SELECT] Marca seleccionada: '{brand}'")
        self.selected_brand = brand
        self.selected_model = ""
        self.selected_year = ""
        self.selected_version = ""
        from services.vehicle_api_service import get_models
        self.available_models = get_models(self.selected_fuel, brand)
        self.available_years = []
        self.available_versions = []

    def select_model(self, model: str):
        print(f"[MODEL] [SELECT] Modelo seleccionado: '{model}'")
        self.selected_model = model
        self.selected_year = ""
        self.selected_version = ""
        from services.vehicle_api_service import get_years
        self.available_years = get_years(self.selected_fuel, self.selected_brand, model)
        self.available_versions = []

    def select_year(self, year: str):
        print(f"[YEAR] [SELECT] Año seleccionado: '{year}'")
        self.selected_year = year
        self.selected_version = ""
        from services.vehicle_api_service import get_versions
        self.available_versions = get_versions(self.selected_fuel, self.selected_brand, self.selected_model, year)

    def select_version(self, version: str):
        print(f"[VERSION] [SELECT] Versión seleccionada: '{version}'")
        self.selected_version = version
    
    async def sync_vehicles_from_api(self):
        """Sincronizar vehículos desde APIs externas"""
        self.api_loading = True
        
        try:
            print("[SYNC] Iniciando sincronización desde APIs externas...")
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
                
                print(f"OK Sincronización completada: {len(self.available_brands)} marcas")
            else:
                print("AVISO No se pudieron obtener datos de API")
                
        except Exception as e:
            print(f"ERROR Error sincronizando desde API: {e}")
        finally:
            self.api_loading = False
    
    def get_api_stats(self) -> dict:
        """Obtener estadísticas de la API"""
        from services.vehicle_api_service import get_api_cache_stats
        return get_api_cache_stats()
    
    def select_fuel(self, fuel: str):
        """Cuando se selecciona un tipo de combustible"""
        print(f"[FUEL] [SELECT] Combustible seleccionado: '{fuel}'")
        
        self.selected_fuel = fuel
        self.selected_brand = ""
        self.selected_model = ""
        self.selected_year = ""
        self.selected_version = ""

        # Cargar marcas disponibles para este combustible
        if self.api_data_source in ["api", "cache"] and self._api_data:
            # Usar datos de API
            self.available_brands = sorted(list(self._api_data.keys()))
            print(f"OK Marcas cargadas desde API: {len(self.available_brands)}")
        else:
            # Fallback a datos locales
            try:
                from utils.vehicle_data import get_brands_by_fuel
                self.available_brands = get_brands_by_fuel(fuel)
                print(f"OK Marcas cargadas desde local: {len(self.available_brands)}")
            except Exception as e:
                print(f"ERROR Error cargando marcas: {e}")
                self.available_brands = []
        
        # Limpiar opciones posteriores
        self.available_models = []
        self.available_years = []
        self.available_versions = []
    
    def select_brand(self, brand: str):
        """Cuando se selecciona una marca"""
        print(f"[BRAND] [SELECT] Marca seleccionada: '{brand}'")
        
        self.selected_brand = brand
        self.selected_model = ""
        self.selected_year = ""
        self.selected_version = ""

        # Cargar modelos disponibles para esta marca
        if self.api_data_source in ["api", "cache"] and self._api_data and brand in self._api_data:
            # Usar datos de API
            models_data = self._api_data[brand]
            self.available_models = [model_info["model"] for model_info in models_data]
            print(f"OK Modelos cargados desde API: {len(self.available_models)}")
        else:
            # Fallback a datos locales
            try:
                from utils.vehicle_data import get_models_by_fuel_and_brand
                self.available_models = get_models_by_fuel_and_brand(self.selected_fuel, brand)
                print(f"OK Modelos cargados desde local: {len(self.available_models)}")
            except Exception as e:
                print(f"ERROR Error cargando modelos: {e}")
                self.available_models = []
        
        # Limpiar opciones posteriores
        self.available_years = []
        self.available_versions = []
    
    def select_model(self, model: str):
        """Cuando se selecciona un modelo"""
        print(f"[MODEL] [SELECT] Modelo seleccionado: '{model}'")
        
        self.selected_model = model
        self.selected_year = ""
        self.selected_version = ""

        # Usar datos de API cache si están disponibles
        if self.api_data_source in ["api", "cache"] and self._api_data:
            try:
                print(f"[SEARCH] [API] Buscando años para {self.selected_brand} {model}")
                
                # Buscar la marca en los datos de API
                brand_models = self._api_data.get(self.selected_brand, [])
                
                # Buscar el modelo específico
                api_years = []
                for vehicle_model in brand_models:
                    if vehicle_model.get('model', '').lower() == model.lower():
                        # Obtener años del modelo
                        years_list = vehicle_model.get('years', [])
                        
                        # Filtrar por combustible si está seleccionado
                        if self.selected_fuel:
                            fuel_types = vehicle_model.get('fuel_types', [])
                            if self.selected_fuel in fuel_types:
                                api_years = years_list
                                print(f"OK [API] Combustible '{self.selected_fuel}' compatible")
                        else:
                            api_years = years_list
                        
                        break
                
                # Convertir a strings y ordenar
                if api_years:
                    self.available_years = sorted([str(y) for y in api_years], reverse=True)
                    print(f"OK Años cargados desde API: {len(self.available_years)} → {self.available_years[:5]}")
                    return
                else:
                    print(f"AVISO [API] No se encontraron años para {self.selected_brand} {model}")
                    
            except Exception as e:
                print(f"ERROR Error procesando años de API: {e}")
        
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
            print(f"OK Años cargados desde datos locales: {len(self.available_years)} → {self.available_years[:5]}")
        except Exception as e:
            print(f"ERROR Error cargando años: {e}")
            self.available_years = []
            self.available_versions = []
    
    def select_year(self, year: str):
        """Cuando se selecciona un año"""
        # Debug detallado
        print(f"[DATA] [DEBUG] select_year llamado con: tipo={type(year)}, valor='{year}', repr={repr(year)}")

        # Convertir a string y limpiar
        year_str = str(year).strip()

        # Validar - solo rechazar None, vacío o "None" literal
        if not year_str or year_str == "None" or year_str == "null":
            print(f"AVISO [SELECT] Año inválido recibido: '{year_str}', ignorando...")
            return

        print(f"[YEAR] [SELECT] Año seleccionado: '{year_str}'")

        self.selected_year = year_str
        self.selected_version = ""  # Resetear versión

        # Cargar versiones disponibles para este año
        if self.api_data_source in ["api", "cache"] and self._api_data:
            # Usar datos de API cache si están disponibles
            try:
                print(f"[SEARCH] [API] Buscando versiones para {self.selected_brand} {self.selected_model} {year_str}")

                # Buscar la marca en los datos de API
                brand_models = self._api_data.get(self.selected_brand, [])

                # Buscar el modelo específico
                api_versions = []
                for vehicle_model in brand_models:
                    if vehicle_model.get('model', '').lower() == self.selected_model.lower():
                        # Obtener años del modelo
                        years_list = vehicle_model.get('years', [])

                        # Filtrar por año si coincide
                        if year_str in [str(y) for y in years_list]:
                            # Obtener versiones disponibles
                            versions_list = vehicle_model.get('versions', [])

                            # Filtrar por combustible si está seleccionado
                            if self.selected_fuel:
                                fuel_types = vehicle_model.get('fuel_types', [])
                                if self.selected_fuel in fuel_types:
                                    api_versions = versions_list
                                    print(f"OK [API] Combustible '{self.selected_fuel}' compatible")
                            else:
                                api_versions = versions_list

                            break

                # Convertir a strings y ordenar
                if api_versions:
                    self.available_versions = sorted([str(v) for v in api_versions])
                    print(f"OK Versiones cargadas desde API: {len(self.available_versions)} → {self.available_versions}")
                    return
                else:
                    print(f"AVISO [API] No se encontraron versiones para {self.selected_brand} {self.selected_model} {year_str}")

            except Exception as e:
                print(f"ERROR Error procesando versiones de API: {e}")

        # Fallback a datos locales
        try:
            from utils.vehicle_data import get_versions_by_fuel_brand_model_year
            versions_local = get_versions_by_fuel_brand_model_year(
                self.selected_fuel,
                self.selected_brand,
                self.selected_model,
                year_str
            )
            # Asegurar que todos sean strings
            self.available_versions = [str(v) for v in versions_local]
            print(f"OK Versiones cargadas desde datos locales: {len(self.available_versions)} → {self.available_versions[:5]}")
        except Exception as e:
            print(f"ERROR Error cargando versiones: {e}")
            self.available_versions = []

    def select_version(self, version: str):
        """Cuando se selecciona una versión"""
        # Debug detallado
        print(f"[VERSION] [DEBUG] select_version llamado con: tipo={type(version)}, valor='{version}', repr={repr(version)}")

        # Convertir a string y limpiar
        version_str = str(version).strip()

        # Validar
        if not version_str or version_str == "None" or version_str == "null":
            print(f"AVISO [SELECT] Versión inválida recibida: '{version_str}', ignorando...")
            return

        print(f"[VERSION] [SELECT] Versión seleccionada: '{version_str}'")

        self.selected_version = version_str

        print(f"[SUCCESS] Selección completa:")
        print(f"   Combustible: {self.selected_fuel}")
        print(f"   Marca: {self.selected_brand}")
        print(f"   Modelo: {self.selected_model}")
        print(f"   Año: {self.selected_year}")
        print(f"   Versión: {self.selected_version}")

    def submit_vehicle_selection(self):
        """
        AVISO MÉTODO PARA BACKEND AVISO
        
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
            print("OK Datos enviados correctamente")
            # Mostrar mensaje de éxito al usuario
        else:
            print("ERROR Error al enviar los datos")
            # Mostrar mensaje de error al usuario
        """
        # 1) Log informativo (útil en desarrollo)
        print("\n" + "="*60)
        print("[SEND] DATOS LISTOS PARA ENVIAR AL BACKEND:")
        print("="*60)
        print(f"[FUEL] Combustible: {self.selected_fuel}")
        print(f"[BRAND] Marca: {self.selected_brand}")
        print(f"[MODEL] Modelo: {self.selected_model}")
        print(f"[YEAR] Año: {self.selected_year}")
        print(f"[VERSION] Versión: {self.selected_version}")
        print("="*60)
        
        # 2) Prefill del mensaje de contacto y scroll a la sección "Contacto"
        try:
            from state.contact_state import ContactState
        except Exception as e:
            print(f"ERROR No se pudo importar ContactState: {e}")
            ContactState = None  # fallback para evitar crash

        # Componer un mensaje claro para el usuario
        resumen = (
            "Hola, me gustaría solicitar presupuesto para mi "
            f"{self.selected_brand} {self.selected_model} {self.selected_version} ({self.selected_year}, {self.selected_fuel}). "
            "¿Podríais confirmarme disponibilidad y precio? Gracias."
        )

        actions = []
        if ContactState is not None:
            # Usamos el handler existente para fijar el valor del textarea
            actions.append(ContactState.handle_message_change(resumen))
        
        # Opcional: marcar la sección de contacto como activa en el header si el estado está disponible
        try:
            from components.header import HeaderState
            actions.append(HeaderState.set_active_section("contacto"))
        except Exception as e:
            print(f"[INFO] HeaderState no disponible para actualizar sección activa: {e}")
        
        # Desplazar suavemente hasta la sección de contacto y enfocar el textarea
        scroll_and_focus = """
        (function(){
            const section = document.getElementById('contacto');
            if(section){ section.scrollIntoView({behavior:'smooth'}); }
            setTimeout(()=>{
                const ta = document.querySelector('#contacto textarea[name="message"]');
                if(ta){ ta.focus(); }
            }, 350);
        })();
        """
        actions.append(rx.call_script(scroll_and_focus))

        # 3) Devolver acciones para que Reflex las ejecute en el cliente
        return actions