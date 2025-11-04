"""
Estado simplificado del selector de vehículos - Versión optimizada
==============================================================

Funciona con la base de datos unificada astrotech.db
"""

import reflex as rx
import logging
import asyncio

# Variable global para compartir información del vehículo entre estados
_shared_vehicle_message = ""

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

    # Estados para el modal de confirmación
    show_confirmation_modal: bool = False
    confirmation_message: str = ""
    confirmation_error: bool = False

  
    
    def load_fuel_types(self):
        """Cargar tipos de combustible desde la base de datos"""
        logger.info("[VEHICLE] Iniciando carga de tipos de combustible")

        # Agregar diagnóstico de entorno
        import os
        env_type = os.getenv("RX_ENV", "DEV")
        logger.info(f"[VEHICLE] Entorno actual: {env_type}")

        # Verificar variables de Supabase
        supabase_url = os.getenv("SUPABASE_URL")
        if supabase_url:
            logger.info(f"[VEHICLE] SUPABASE_URL configurada: {supabase_url[:20]}...")
        else:
            logger.warning("[VEHICLE] SUPABASE_URL no configurada")

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

    async def submit_vehicle_selection(self):
        """Enviar selección de vehículo al formulario de contacto"""
        if self.is_complete_selection():
            selection = self.get_current_selection()
            logger.info(f"[VEHICLE] 🚀 Iniciando envío de presupuesto")
            logger.info(f"[VEHICLE] 📋 Datos: {selection}")

            # Preparar mensaje con datos del vehículo
            vehicle_message = (
                f"VEHÍCULO SELECCIONADO:\n"
                f"• Combustible: {selection['fuel_type']}\n"
                f"• Marca: {selection['brand']}\n"
                f"• Modelo: {selection['model']}\n"
                f"• Versión: {selection['version']}"
            )

            # Almacenar en el estado y en la variable global
            self.selected_vehicle_message = vehicle_message
            global _shared_vehicle_message
            _shared_vehicle_message = vehicle_message

            logger.info("[VEHICLE] 📝 Mensaje preparado correctamente")
            logger.info("[VEHICLE] 🔄 Notificando al formulario de contacto...")

            try:
                # Importar el servicio de email
                from utils.email_service import send_contact_form_email

                logger.info("[VEHICLE] 📧 Preparando envío de email...")
                logger.info("[VEHICLE] 📬 Destinatario: astrotechreprogramaciones@gmail.com")

                # Enviar email con la información del vehículo
                email_result = await send_contact_form_email(
                    name="Cliente - Solicitud desde Selector",
                    email="info@astrotech.com",  # Email temporal
                    phone="",
                    message=vehicle_message,
                    is_registered=False,
                    user_info={}
                )

                if email_result["success"]:
                    logger.info("[VEHICLE] ✅ EMAIL ENVIADO EXITOSAMENTE")
                    logger.info(f"[VEHICLE] 📨 Detalles: {email_result['message']}")

                    # Actualizar ContactState
                    from state.contact_state import ContactState
                    ContactState.update_vehicle_info()
                    ContactState.confirm_budget_sent()

                    logger.info("[VEHICLE] ✅ Estado del formulario actualizado")

                    # Mostrar modal de éxito
                    self.confirmation_message = "¡Solicitud enviada exitosamente! Nos pondremos en contacto contigo pronto."
                    self.confirmation_error = False
                    self.show_confirmation_modal = True

                    logger.info("[VEHICLE] 🎉 Proceso completado exitosamente")

                    # Limpiar selectores después de 2 segundos
                    await asyncio.sleep(2)
                    self.reset_selection()
                    logger.info("[VEHICLE] 🧹 Selectores limpiados")

                else:
                    logger.error(f"[VEHICLE] ❌ ERROR AL ENVIAR EMAIL: {email_result['message']}")
                    logger.error("[VEHICLE] 🔍 Verifica la configuración de SMTP en settings.py")

                    # Mostrar modal de error
                    self.confirmation_message = f"Error al enviar: {email_result['message']}"
                    self.confirmation_error = True
                    self.show_confirmation_modal = True

            except Exception as e:
                logger.error(f"[VEHICLE] ❌ EXCEPCIÓN CRÍTICA: {str(e)}")
                logger.error("[VEHICLE] 🔧 Posibles causas:")
                logger.error("[VEHICLE]    • Configuración de email incorrecta")
                logger.error("[VEHICLE]    • Sin conexión a internet")
                logger.error("[VEHICLE]    • Credenciales SMTP inválidas")

                import traceback
                logger.error(f"[VEHICLE] 📋 Stack trace: {traceback.format_exc()}")

                # Mostrar modal de error
                self.confirmation_message = f"Error al procesar la solicitud: {str(e)}"
                self.confirmation_error = True
                self.show_confirmation_modal = True

            return
        else:
            logger.warning("[VEHICLE] ⚠️ Selección incompleta - no se puede enviar")
            return

    def close_confirmation_modal(self):
        """Cerrar el modal de confirmación"""
        self.show_confirmation_modal = False
        self.confirmation_message = ""
        logger.info("[VEHICLE] 🔒 Modal de confirmación cerrado")

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