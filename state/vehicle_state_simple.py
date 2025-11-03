"""
Estado simplificado del selector de vehículos - Versión optimizada
==============================================================

Funciona con la base de datos unificada astrotech.db
"""

import reflex as rx
import logging

# Obtener logger para este módulo
logger = logging.getLogger(__name__)

class VehicleState(rx.State):
    """Estado del selector de vehículos optimizado para base de datos unificada"""

    # Valores seleccionados
    selected_fuel: str = ""
    selected_brand: str = ""
    selected_model: str = ""
    selected_version: str = ""

    # Opciones disponibles
    available_fuel_types: list[str] = []
    available_brands: list[str] = []
    available_models: list[str] = []
    available_versions: list[str] = []

    # Estado de carga
    loading: bool = False
    data_loaded: bool = False

    # Mensaje del vehículo seleccionado para contacto
    selected_vehicle_message: str = ""

  
    
    def load_fuel_types(self):
        """Cargar tipos de combustible desde la base de datos"""
        logger.info("[VEHICLE] Iniciando carga de tipos de combustible")

        try:
            from utils.vehicle_data_supabase import get_vehicle_fuel_types
            fuel_types = get_vehicle_fuel_types()
            logger.info(f"[VEHICLE] Tipos obtenidos de Supabase: {fuel_types}")

            if fuel_types and len(fuel_types) > 0:
                self.available_fuel_types = list(fuel_types)  # Crear nueva lista para forzar re-render
                logger.info(f"[VEHICLE] Tipos de combustible cargados: {len(self.available_fuel_types)}")
                logger.info(f"[VEHICLE] Opciones disponibles: {self.available_fuel_types}")
                print(f"[VEHICLE] ✅ Tipos de combustible cargados desde BD: {len(self.available_fuel_types)}")
                print(f"[VEHICLE] Opciones: {self.available_fuel_types}")
            else:
                # Si no hay datos, dejar la lista vacía para mostrar el error real
                self.available_fuel_types = list()
                logger.warning("[VEHICLE] Base de datos sin tipos de combustible")
                print(f"[VEHICLE] ⚠️ Base de datos sin tipos de combustible")

        except Exception as e:
            logger.error(f"[VEHICLE] Error cargando tipos de combustible: {e}", exc_info=True)
            # Dejar vacío para mostrar si hay un error real
            self.available_fuel_types = list()
            print(f"[VEHICLE] ❌ Error cargando tipos de combustible: {e}")
            print(f"[VEHICLE] ❌ Base de datos no disponible")

        # Marcar como cargado para evitar recargas innecesarias
        self.data_loaded = True
        logger.info(f"[VEHICLE] Estado data_loaded: {self.data_loaded}")

    def select_fuel(self, fuel: str):
        """Seleccionar tipo de combustible y cargar marcas"""
        print(f"[VEHICLE] Combustible seleccionado: {fuel}")
        self.selected_fuel = fuel
        self.selected_brand = ""
        self.selected_model = ""
        self.selected_version = ""

        # Cargar marcas para este tipo de combustible
        self.load_brands(fuel)

    def load_brands(self, fuel_type: str = None):
        """Cargar marcas disponibles"""
        try:
            from utils.vehicle_data_supabase import get_vehicle_brands
            brands = get_vehicle_brands(fuel_type or self.selected_fuel)
            self.available_brands = list(brands)  # Crear nueva lista para forzar re-render
            print(f"[VEHICLE] Marcas cargadas: {len(self.available_brands)}")
        except Exception as e:
            print(f"[VEHICLE] Error cargando marcas: {e}")
            self.available_brands = list()  # Lista vacía nueva

    def select_brand(self, brand: str):
        """Seleccionar marca y cargar modelos"""
        print(f"[VEHICLE] Marca seleccionada: {brand}")
        self.selected_brand = brand
        self.selected_model = ""
        self.selected_version = ""

        # Cargar modelos para esta marca
        self.load_models(self.selected_fuel, brand)

    def load_models(self, fuel_type: str = None, brand: str = None):
        """Cargar modelos disponibles"""
        try:
            from utils.vehicle_data_supabase import get_vehicle_models
            models = get_vehicle_models(
                fuel_type or self.selected_fuel,
                brand or self.selected_brand
            )
            self.available_models = list(models)  # Crear nueva lista para forzar re-render
            print(f"[VEHICLE] Modelos cargados: {len(self.available_models)}")
        except Exception as e:
            print(f"[VEHICLE] Error cargando modelos: {e}")
            self.available_models = list()  # Lista vacía nueva

    def select_model(self, model: str):
        """Seleccionar modelo y cargar versiones"""
        print(f"[VEHICLE] Modelo seleccionado: {model}")
        self.selected_model = model
        self.selected_version = ""

        # Cargar versiones para este modelo
        self.load_versions(self.selected_fuel, self.selected_brand, model)

    def load_versions(self, fuel_type: str = None, brand: str = None, model: str = None):
        """Cargar versiones disponibles"""
        try:
            from utils.vehicle_data_supabase import get_vehicle_versions
            versions = get_vehicle_versions(
                fuel_type or self.selected_fuel,
                brand or self.selected_brand,
                model or self.selected_model
            )
            self.available_versions = list(versions)  # Crear nueva lista para forzar re-render
            print(f"[VEHICLE] Versiones cargadas: {len(self.available_versions)}")
        except Exception as e:
            print(f"[VEHICLE] Error cargando versiones: {e}")
            self.available_versions = list()  # Lista vacía nueva

    def select_version(self, version: str):
        """Seleccionar versión final"""
        print(f"[VEHICLE] Versión seleccionada: {version}")
        self.selected_version = version

    def submit_vehicle_selection(self):
        """Enviar selección de vehículo al formulario de contacto"""
        if self.is_complete_selection():
            selection = self.get_current_selection()
            print(f"[VEHICLE] Enviando selección: {selection}")

            # Preparar mensaje con datos del vehículo
            vehicle_message = (
                f"VEHÍCULO SELECCIONADO:\n"
                f"• Combustible: {selection['fuel_type']}\n"
                f"• Marca: {selection['brand']}\n"
                f"• Modelo: {selection['model']}\n"
                f"• Versión: {selection['version']}"
            )

            # Almacenar en el estado para que el formulario de contacto lo use
            self.selected_vehicle_message = vehicle_message
            print(f"[VEHICLE] Mensaje preparado: {vehicle_message}")

            return vehicle_message
        else:
            print("[VEHICLE] Error: Selección incompleta")
            return None

    def reset_selection(self):
        """Reiniciar todas las selecciones"""
        print("[VEHICLE] Reiniciando selección")
        self.selected_fuel = ""
        self.selected_brand = ""
        self.selected_model = ""
        self.selected_version = ""
        self.available_brands = list()
        self.available_models = list()
        self.available_versions = list()

    def get_current_selection(self) -> dict:
        """Obtener la selección actual"""
        return {
            "fuel_type": self.selected_fuel,
            "brand": self.selected_brand,
            "model": self.selected_model,
            "version": self.selected_version
        }

    def is_complete_selection(self) -> bool:
        """Verificar si se ha completado la selección"""
        return all([
            self.selected_fuel,
            self.selected_brand,
            self.selected_model,
            self.selected_version
        ])

# Para compatibilidad con código existente
def get_vehicle_state_methods():
    """Obtener métodos disponibles para compatibilidad"""
    state_methods = [
        'select_fuel', 'select_brand', 'select_model', 'select_version',
        'load_fuel_types', 'load_brands', 'load_models', 'load_versions',
        'reset_selection', 'get_current_selection', 'is_complete_selection'
    ]
    return state_methods

# Verificación al importar
if __name__ == "__main__":
    print("=== VERIFICACIÓN DE VEHICLE_STATE_SIMPLE ===")
    print("Estado de vehículos optimizado creado correctamente")
    print(f"Métodos disponibles: {get_vehicle_state_methods()}")