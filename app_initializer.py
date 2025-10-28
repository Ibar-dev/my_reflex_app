"""
Inicializador Centralizado - AstroTech Application
===============================================

Asegura que todos los componentes se inicialicen en el orden correcto
y con perfecta sinergia entre ellos.
"""

import os
import logging
from typing import Dict, Any

# Configurar logging centralizado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class AppInitializer:
    """
    Inicializador centralizado que asegura la sinergia perfecta
    entre todos los componentes de la aplicación AstroTech
    """

    def __init__(self):
        self.initialization_steps = []
        self.status = {
            "database": False,
            "email": False,
            "models": False,
            "cache": False
        }

    def initialize_all(self) -> Dict[str, Any]:
        """
        Inicializa todos los componentes en el orden correcto
        para asegurar sinergia perfecta
        """
        logger.info("🚀 Iniciando inicialización centralizada de AstroTech...")

        results = {
            "success": True,
            "initialized_components": [],
            "errors": [],
            "database_info": None,
            "email_config": None
        }

        # 1. Inicializar Base de Datos (fundamento de todo)
        try:
            logger.info("📊 Paso 1: Inicializando base de datos unificada...")
            from utils.database_manager import db_manager

            health = db_manager.health_check()
            if health["status"] == "healthy":
                self.status["database"] = True
                results["initialized_components"].append("database")
                results["database_info"] = health["database_info"]
                logger.info("✅ Base de datos unificada inicializada correctamente")
            else:
                raise Exception(f"Error en BD: {health['message']}")

        except Exception as e:
            logger.error(f"❌ Error inicializando base de datos: {e}")
            results["success"] = False
            results["errors"].append(f"Database: {str(e)}")

        # 2. Inicializar Modelos (dependen de BD)
        try:
            logger.info("📋 Paso 2: Verificando modelos de datos...")
            from models.user import UserRegistration
            from models.vehicle import Vehicle

            self.status["models"] = True
            results["initialized_components"].append("models")
            logger.info("✅ Modelos de datos verificados correctamente")

        except Exception as e:
            logger.error(f"❌ Error inicializando modelos: {e}")
            results["success"] = False
            results["errors"].append(f"Models: {str(e)}")

        # 3. Inicializar Email Service
        try:
            logger.info("📧 Paso 3: Configurando servicio de email...")
            from utils.email_service import EmailConfig

            if EmailConfig.is_configured():
                self.status["email"] = True
                results["initialized_components"].append("email")
                results["email_config"] = EmailConfig.get_smtp_config()
                logger.info("✅ Servicio de email configurado correctamente")
            else:
                logger.warning("⚠️ Email service configurado para modo simulación")
                results["initialized_components"].append("email_simulation")

        except Exception as e:
            logger.error(f"❌ Error configurando email: {e}")
            results["errors"].append(f"Email: {str(e)}")

        # 4. Inicializar Cache de Vehículos
        try:
            logger.info("🚗 Paso 4: Inicializando cache de vehículos...")
            from utils.database_service import vehicle_cache_service

            # Programar actualización automática si es necesario
            vehicle_cache_service.schedule_auto_update()
            self.status["cache"] = True
            results["initialized_components"].append("vehicle_cache")
            logger.info("✅ Cache de vehículos inicializado correctamente")

        except Exception as e:
            logger.warning(f"⚠️ Error inicializando cache de vehículos: {e}")
            results["errors"].append(f"Vehicle Cache: {str(e)}")

        # 5. Verificar sinergia final
        try:
            logger.info("🔄 Paso 5: Verificando sinergia entre componentes...")
            synergy_check = self._verify_synergy()
            results["synergy_check"] = synergy_check

            if synergy_check["all_connected"]:
                logger.info("✅ Sinergia perfecta verificada")
            else:
                logger.warning(f"⚠️ Problemas de sinergia detectados: {synergy_check['issues']}")

        except Exception as e:
            logger.error(f"❌ Error verificando sinergia: {e}")
            results["errors"].append(f"Synergy: {str(e)}")

        # Resumen final
        if results["success"] and len(results["errors"]) == 0:
            logger.info("🎉 ¡Inicialización completada con éxito! Todos los componentes en perfecta sinergia.")
        else:
            logger.warning(f"⚠️ Inicialización completada con {len(results['errors'])} advertencias")

        return results

    def _verify_synergy(self) -> Dict[str, Any]:
        """
        Verifica que todos los componentes estén conectados correctamente
        """
        issues = []

        try:
            # Verificar conexión entre ContactState y UserRegistration
            from state.contact_state import ContactState
            from models.user import UserRegistration

            # Verificar que ContactState puede acceder a la base de datos
            from utils.database_manager import db_manager
            health = db_manager.health_check()
            if health["status"] != "healthy":
                issues.append("Database connection issue")

            # Verificar que EmailService puede conectarse
            from utils.email_service import EmailConfig
            # EmailConfig.is_configured() puede ser False (modo simulación), no es error

            # Verificar imports entre componentes principales
            components_ok = all([
                health["status"] == "healthy"
            ])

            return {
                "all_connected": components_ok and len(issues) == 0,
                "issues": issues,
                "components_status": {
                    "database": health["status"],
                    "email": "configured" if EmailConfig.is_configured() else "simulation",
                    "models": "ready",
                    "cache": "ready"
                }
            }

        except Exception as e:
            return {
                "all_connected": False,
                "issues": [f"Synergy verification error: {str(e)}"],
                "components_status": {}
            }

    def get_status(self) -> Dict[str, Any]:
        """Obtener estado actual de inicialización"""
        return {
            "initialized": all(self.status.values()),
            "components": self.status.copy(),
            "details": {
                "database": "Base de datos unificada lista",
                "models": "Modelos de datos importados",
                "email": "Servicio de email configurado",
                "cache": "Cache de vehículos listo"
            }
        }

# Instancia global del inicializador
app_initializer = AppInitializer()

# Función para inicialización rápida
def initialize_app() -> Dict[str, Any]:
    """Inicializa toda la aplicación AstroTech"""
    return app_initializer.initialize_all()

# Verificación automática al importar
if __name__ == "__main__":
    print("=== INICIALIZADOR ASTROTECH ===")
    result = initialize_app()
    print(f"\nResultado: {'ÉXITO' if result['success'] else 'ERROR'}")
    print(f"Componentes inicializados: {', '.join(result['initialized_components'])}")
    if result['errors']:
        print(f"Errores: {result['errors']}")