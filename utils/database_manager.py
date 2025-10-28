"""
Gestor Unificado de Base de Datos - AstroTech
=============================================

Centraliza todas las operaciones de base de datos para asegurar sinergia perfecta
entre todos los componentes del sistema.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager
from typing import Generator
import logging

# Importar todos los modelos
from models.user import Base as UserBase, UserRegistration
from models.vehicle import Base as VehicleBase, Vehicle

# Configuración centralizada
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN_DATABASE_PATH = os.path.join(PROJECT_ROOT, "astrotech.db")
MAIN_DATABASE_URL = f"sqlite:///{MAIN_DATABASE_PATH}"

# Logging centralizado
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    Gestor centralizado de base de datos para AstroTech
    Asegura consistencia y sinergia entre todos los componentes
    """

    _instance = None
    _engine = None
    _SessionLocal = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Inicializar el gestor de base de datos"""
        try:
            # Crear engine con configuración optimizada para SQLite
            self._engine = create_engine(
                MAIN_DATABASE_URL,
                connect_args={
                    "check_same_thread": False,
                    "timeout": 20
                },
                poolclass=StaticPool,
                echo=False  # Cambiar a True para debugging SQL
            )

            # Crear sesión
            self._SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine
            )

            # Inicializar todas las tablas
            self._initialize_all_tables()

            logger.info(f"✅ DatabaseManager inicializado - DB: {MAIN_DATABASE_PATH}")

        except Exception as e:
            logger.error(f"❌ Error inicializando DatabaseManager: {e}")
            raise

    def _initialize_all_tables(self):
        """Inicializar todas las tablas de todos los modelos"""
        try:
            # Importar y crear todas las tablas
            UserBase.metadata.create_all(bind=self._engine)
            VehicleBase.metadata.create_all(bind=self._engine)

            logger.info("✅ Todas las tablas inicializadas correctamente")

        except Exception as e:
            logger.error(f"❌ Error creando tablas: {e}")
            raise

    @property
    def engine(self):
        """Obtener el engine de base de datos"""
        return self._engine

    @property
    def SessionLocal(self):
        """Obener la fábrica de sesiones"""
        return self._SessionLocal

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        Context manager para sesiones de base de datos
        Asegura manejo correcto de transacciones
        """
        session = self._SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"❌ Error en transacción de BD: {e}")
            raise
        finally:
            session.close()

    def get_database_info(self) -> dict:
        """Obtener información completa de la base de datos"""
        try:
            with self.get_session() as session:
                # Contar registros en cada tabla
                user_count = session.query(UserRegistration).count()
                vehicle_count = session.query(Vehicle).count()

                return {
                    "database_path": MAIN_DATABASE_PATH,
                    "database_url": MAIN_DATABASE_URL,
                    "tables": {
                        "user_registrations": user_count,
                        "vehicles": vehicle_count
                    },
                    "total_records": user_count + vehicle_count,
                    "engine": "SQLite",
                    "status": "healthy"
                }
        except Exception as e:
            logger.error(f"❌ Error obteniendo información de BD: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

    def health_check(self) -> dict:
        """Verificación de salud de la base de datos"""
        try:
            with self.get_session() as session:
                # Importar text para consultas SQL seguras
                from sqlalchemy import text

                # Probar consulta simple
                session.execute(text("SELECT 1"))

                info = self.get_database_info()

                return {
                    "status": "healthy",
                    "message": "Base de datos funcionando correctamente",
                    "database_info": info,
                    "timestamp": str(session.execute(text("SELECT datetime('now')")).scalar())
                }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Error en base de datos: {e}",
                "timestamp": None
            }

# Instancia global del gestor (lazy initialization)
db_manager = None

def get_database_manager():
    """Obtener instancia del gestor (lazy initialization)"""
    global db_manager
    if db_manager is None:
        db_manager = DatabaseManager()
    return db_manager

def get_database_session():
    """Obtener sesión de base de datos (compatibilidad)"""
    return get_database_manager().SessionLocal()

# Inicialización automática al importar
def initialize_database():
    """Inicializar base de datos (función de compatibilidad)"""
    return db_manager.health_check()["status"] == "healthy"

# Verificación al importar
if __name__ == "__main__":
    manager = get_database_manager()
    health = manager.health_check()
    print(f"Estado BD: {health['status']}")
    if health['status'] == 'healthy':
        print(f"Base de datos unificada lista para usar")
        print(f"Ubicación: {health['database_info']['database_path']}")
        print(f"Tablas: {health['database_info']['tables']}")
    else:
        print(f"Error: {health['message']}")