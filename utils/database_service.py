"""
Servicio de Base de Datos - Gestión de Usuarios
===============================================

Servicios para manejar operaciones de base de datos relacionadas con usuarios
"""


import os
from models.user import UserRegistration, SessionLocal, init_database
from models.vehicle import Base, Vehicle
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
import re
import json
import logging

# Configuración de bases de datos
LEGACY_DATABASE_URL = "sqlite:///vehicles.db"
EXPANDED_DATABASE_URL = "sqlite:///vehicles_expanded.db"

# Motores de base de datos
legacy_engine = create_engine(LEGACY_DATABASE_URL, connect_args={"check_same_thread": False})
expanded_engine = create_engine(EXPANDED_DATABASE_URL, connect_args={"check_same_thread": False})

# Sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=legacy_engine)
ExpandedSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=expanded_engine)

def init_db():
    """Inicializar ambas bases de datos"""
    Base.metadata.create_all(bind=legacy_engine)
    Base.metadata.create_all(bind=expanded_engine)

# Logger centralizado
logger = logging.getLogger("database_service")

# Comprobación exhaustiva de la tabla vehicles
def check_vehicles_table(verbose: bool = True) -> dict:
    """
    Comprueba si la tabla vehicles existe y tiene datos válidos.
    Devuelve un resumen y loguea los resultados.
    """
    db = SessionLocal()
    result = {
        "exists": False,
        "count": 0,
        "fuels": [],
        "brands": [],
        "sample": [],
        "error": None
    }
    try:
        # ¿Existen vehículos?
        count = db.query(Vehicle).count()
        result["count"] = count
        result["exists"] = count > 0
        if count > 0:
            fuels = db.query(Vehicle.fuel_type).distinct().all()
            brands = db.query(Vehicle.brand).distinct().all()
            result["fuels"] = sorted(list(set([f[0] for f in fuels if f[0]])))
            result["brands"] = sorted(list(set([b[0] for b in brands if b[0]])))
            # Muestra 3 ejemplos
            sample = db.query(Vehicle).limit(3).all()
            result["sample"] = [
                {
                    "fuel_type": v.fuel_type,
                    "brand": v.brand,
                    "model": v.model,
                    "year": v.year,
                    "version": v.version
                } for v in sample
            ]
            logger.info(f"La tabla vehicles contiene {count} registros. Ejemplo: {result['sample']}")
        else:
            logger.warning("La tabla vehicles está vacía.")
        if verbose:
            print("\n[CHECK] Tabla vehicles:")
            print(f"  Registros: {result['count']}")
            print(f"  Tipos de combustible: {result['fuels']}")
            print(f"  Marcas: {result['brands']}")
            print(f"  Ejemplo: {result['sample']}")
    except Exception as e:
        logger.error(f"Error comprobando tabla vehicles: {e}")
        result["error"] = str(e)
    finally:
        db.close()
    return result

class DatabaseService:
    """Servicio para operaciones de base de datos de usuarios"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Valida formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(telefono: str) -> bool:
        """Valida formato de teléfono (flexible para diferentes formatos)"""
        # Eliminar espacios y caracteres especiales
        clean_phone = re.sub(r'[^0-9+]', '', telefono)
        # Mínimo 9 dígitos (sin incluir +)
        return len(clean_phone.replace('+', '')) >= 9
    
    @staticmethod
    def save_user_registration(nombre: str, email: str, telefono: str, source: str = "discount_popup") -> dict:
        """
        Guarda un nuevo registro de usuario en la base de datos
        
        Args:
            nombre: Nombre completo del usuario
            email: Email del usuario
            telefono: Teléfono del usuario
            source: Fuente del registro (discount_popup, contact_form, etc.)
        
        Returns:
            dict: {"success": bool, "message": str, "user_id": int, "data": dict}
        """
        
        # Validaciones de entrada
        if not nombre or not nombre.strip():
            return {
                "success": False,
                "message": "El nombre es obligatorio",
                "user_id": None,
                "data": None
            }
        
        if not email or not DatabaseService.validate_email(email.strip()):
            return {
                "success": False,
                "message": "Email inválido",
                "user_id": None,
                "data": None
            }
        
        if not telefono or not DatabaseService.validate_phone(telefono.strip()):
            return {
                "success": False,
                "message": "Teléfono inválido (mínimo 9 dígitos)",
                "user_id": None,
                "data": None
            }
        
        # Limpiar datos
        nombre_clean = nombre.strip().title()
        email_clean = email.strip().lower()
        telefono_clean = telefono.strip()
        
        db = SessionLocal()
        try:
            # Verificar si el email ya existe
            existing_user = db.query(UserRegistration).filter(
                UserRegistration.email == email_clean
            ).first()
            
            if existing_user:
                logger.warning(f"Intento de registro duplicado: {email_clean}")
                return {
                    "success": False,
                    "message": "Este email ya está registrado",
                    "user_id": existing_user.id,
                    "data": existing_user.to_dict()
                }
            
            # Crear nuevo usuario
            new_user = UserRegistration(
                nombre=nombre_clean,
                email=email_clean,
                telefono=telefono_clean,
                source=source
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            logger.info(f"OK Usuario registrado exitosamente: {email_clean} (ID: {new_user.id})")
            
            return {
                "success": True,
                "message": "¡Registro exitoso! Te contactaremos pronto con tu descuento.",
                "user_id": new_user.id,
                "data": new_user.to_dict()
            }
            
        except IntegrityError:
            db.rollback()
            logger.error(f"Error de integridad al registrar: {email_clean}")
            return {
                "success": False,
                "message": "Error: Email duplicado",
                "user_id": None,
                "data": None
            }
        except Exception as e:
            db.rollback()
            logger.error(f"Error inesperado al guardar usuario: {str(e)}")
            return {
                "success": False,
                "message": "Error interno del servidor. Inténtalo más tarde.",
                "user_id": None,
                "data": None
            }
        finally:
            db.close()
    
    @staticmethod
    def get_all_users(limit: int = 100) -> dict:
        """
        Obtiene todos los usuarios registrados
        
        Args:
            limit: Límite de registros a obtener
            
        Returns:
            dict: {"success": bool, "users": list, "count": int}
        """
        db = SessionLocal()
        try:
            users = db.query(UserRegistration).order_by(
                UserRegistration.created_at.desc()
            ).limit(limit).all()
            
            total_count = db.query(UserRegistration).count()
            
            return {
                "success": True,
                "users": [user.to_dict() for user in users],
                "count": len(users),
                "total_count": total_count
            }
        except Exception as e:
            logger.error(f"Error al obtener usuarios: {str(e)}")
            return {
                "success": False,
                "users": [],
                "count": 0,
                "total_count": 0
            }
        finally:
            db.close()
    
    @staticmethod
    def get_user_by_email(email: str) -> dict:
        """
        Busca un usuario por email
        
        Args:
            email: Email del usuario
            
        Returns:
            dict: {"success": bool, "user": dict, "found": bool}
        """
        if not email or not DatabaseService.validate_email(email.strip()):
            return {
                "success": False,
                "user": None,
                "found": False,
                "message": "Email inválido"
            }
        
        db = SessionLocal()
        try:
            user = db.query(UserRegistration).filter(
                UserRegistration.email == email.strip().lower()
            ).first()
            
            if user:
                return {
                    "success": True,
                    "user": user.to_dict(),
                    "found": True,
                    "message": "Usuario encontrado"
                }
            else:
                return {
                    "success": True,
                    "user": None,
                    "found": False,
                    "message": "Usuario no encontrado"
                }
        except Exception as e:
            logger.error(f"Error al buscar usuario: {str(e)}")
            return {
                "success": False,
                "user": None,
                "found": False,
                "message": "Error al buscar usuario"
            }
        finally:
            db.close()
    
    @staticmethod
    def mark_user_contacted(user_id: int) -> dict:
        """
        Marca un usuario como contactado
        
        Args:
            user_id: ID del usuario
            
        Returns:
            dict: {"success": bool, "message": str}
        """
        db = SessionLocal()
        try:
            user = db.query(UserRegistration).filter(
                UserRegistration.id == user_id
            ).first()
            
            if not user:
                return {
                    "success": False,
                    "message": "Usuario no encontrado"
                }
            
            user.is_contacted = True
            user.updated_at = datetime.utcnow()
            db.commit()
            
            logger.info(f"Usuario {user_id} marcado como contactado")
            
            return {
                "success": True,
                "message": "Usuario marcado como contactado"
            }
        except Exception as e:
            db.rollback()
            logger.error(f"Error al marcar usuario como contactado: {str(e)}")
            return {
                "success": False,
                "message": "Error al actualizar usuario"
            }
        finally:
            db.close()
    
    @staticmethod
    def get_stats() -> dict:
        """
        Obtiene estadísticas de registros
        
        Returns:
            dict: Estadísticas de la base de datos
        """
        db = SessionLocal()
        try:
            total_users = db.query(UserRegistration).count()
            contacted_users = db.query(UserRegistration).filter(
                UserRegistration.is_contacted == True
            ).count()
            popup_registrations = db.query(UserRegistration).filter(
                UserRegistration.source == "discount_popup"
            ).count()
            
            return {
                "success": True,
                "stats": {
                    "total_users": total_users,
                    "contacted_users": contacted_users,
                    "pending_contact": total_users - contacted_users,
                    "popup_registrations": popup_registrations,
                    "conversion_rate": round((popup_registrations / total_users * 100), 2) if total_users > 0 else 0
                }
            }
        except Exception as e:
            logger.error(f"Error al obtener estadísticas: {str(e)}")
            return {
                "success": False,
                "stats": {}
            }
        finally:
            db.close()

# ==================== SERVICIOS DE VEHÍCULOS EXPANDIDOS ====================

class VehicleCacheService:
    """Servicio de cache y actualización automática para datos de vehículos"""

    CACHE_DIR = "data"
    CACHE_FILE = os.path.join(CACHE_DIR, "vehicle_data_cache.json")
    METADATA_FILE = os.path.join(CACHE_DIR, "vehicle_metadata.json")
    CACHE_DURATION_DAYS = 30

    def __init__(self):
        os.makedirs(self.CACHE_DIR, exist_ok=True)

    def log(self, message: str):
        """Función de logging específica para el servicio de cache"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[VehicleCache][{timestamp}] {message}")
        logger.info(f"VehicleCache: {message}")

    def get_database_stats(self, use_expanded=True) -> dict:
        """Obtener estadísticas actuales de la base de datos"""
        try:
            if use_expanded and os.path.exists("vehicles_expanded.db"):
                import sqlite3
                conn = sqlite3.connect("vehicles_expanded.db")
                cursor = conn.cursor()

                cursor.execute("SELECT COUNT(*) FROM vehicles_expanded")
                total = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(DISTINCT brand) FROM vehicles_expanded")
                brands = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(DISTINCT model) FROM vehicles_expanded")
                models = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(DISTINCT fuel_type) FROM vehicles_expanded")
                fuel_types = cursor.fetchone()[0]

                conn.close()

                return {
                    'total_vehicles': total,
                    'brands': brands,
                    'models': models,
                    'fuel_types': fuel_types,
                    'database_type': 'expanded'
                }
            else:
                # Usar la base de datos legacy
                db = SessionLocal()
                try:
                    total = db.query(Vehicle).count()
                    brands = db.query(Vehicle.brand).distinct().count()
                    models = db.query(Vehicle.model).distinct().count()
                    fuel_types = db.query(Vehicle.fuel_type).distinct().count()

                    return {
                        'total_vehicles': total,
                        'brands': brands,
                        'models': models,
                        'fuel_types': fuel_types,
                        'database_type': 'legacy'
                    }
                finally:
                    db.close()

        except Exception as e:
            self.log(f"Error obteniendo estadísticas: {str(e)}")
            return {
                'total_vehicles': 0,
                'brands': 0,
                'models': 0,
                'fuel_types': 0,
                'database_type': 'error'
            }

    def load_metadata(self) -> dict:
        """Cargar metadatos del cache"""
        try:
            if os.path.exists(self.METADATA_FILE):
                with open(self.METADATA_FILE, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    return metadata
        except Exception as e:
            self.log(f"Error cargando metadatos: {str(e)}")

        return {
            'last_update': None,
            'total_vehicles': 0,
            'update_status': 'never_updated',
            'source': 'unknown'
        }

    def save_metadata(self, metadata: dict):
        """Guardar metadatos del cache"""
        try:
            metadata['last_check'] = datetime.now().isoformat()
            with open(self.METADATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.log(f"Error guardando metadatos: {str(e)}")

    def is_cache_expired(self) -> bool:
        """Verificar si el cache ha expirado"""
        metadata = self.load_metadata()

        if not metadata.get('last_update'):
            return True

        try:
            last_update = datetime.fromisoformat(metadata['last_update'])
            expiry_date = last_update + timedelta(days=self.CACHE_DURATION_DAYS)
            return datetime.now() > expiry_date
        except:
            return True

    def check_update_needed(self) -> dict:
        """Verificar si se necesita una actualización"""
        current_stats = self.get_database_stats()
        metadata = self.load_metadata()
        cache_expired = self.is_cache_expired()

        update_needed = cache_expired

        # Si los datos actuales son muy diferentes a los del cache
        if not update_needed and metadata.get('total_vehicles', 0) != current_stats.get('total_vehicles', 0):
            update_needed = True

        return {
            'update_needed': update_needed,
            'cache_expired': cache_expired,
            'current_stats': current_stats,
            'last_update': metadata.get('last_update'),
            'cache_vehicles': metadata.get('total_vehicles', 0),
            'current_vehicles': current_stats.get('total_vehicles', 0)
        }

    def trigger_update(self) -> dict:
        """Trigger actualización de datos de vehículos"""
        self.log("Iniciando actualización de datos de vehículos...")

        try:
            # Importar y ejecutar el descargador
            import subprocess
            import sys

            # Ejecutar script de descarga
            result = subprocess.run(
                [sys.executable, "download_vehicle_data.py"],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )

            if result.returncode == 0:
                self.log("Actualización completada exitosamente")

                # Actualizar metadatos
                new_stats = self.get_database_stats()
                metadata = {
                    'last_update': datetime.now().isoformat(),
                    'total_vehicles': new_stats.get('total_vehicles', 0),
                    'update_status': 'success',
                    'source': 'auto_update'
                }
                self.save_metadata(metadata)

                return {
                    'success': True,
                    'message': 'Actualización completada exitosamente',
                    'new_stats': new_stats,
                    'output': result.stdout
                }
            else:
                error_msg = f"Error en actualización: {result.stderr}"
                self.log(error_msg)

                metadata = {
                    'last_update': datetime.now().isoformat(),
                    'update_status': 'failed',
                    'source': 'auto_update',
                    'error': error_msg
                }
                self.save_metadata(metadata)

                return {
                    'success': False,
                    'message': error_msg,
                    'output': result.stderr
                }

        except Exception as e:
            error_msg = f"Error crítico en actualización: {str(e)}"
            self.log(error_msg)

            metadata = {
                'last_update': datetime.now().isoformat(),
                'update_status': 'failed',
                'source': 'auto_update',
                'error': error_msg
            }
            self.save_metadata(metadata)

            return {
                'success': False,
                'message': error_msg
            }

    def get_update_status(self) -> dict:
        """Obtener estado actual de la actualización"""
        metadata = self.load_metadata()
        current_stats = self.get_database_stats()
        cache_info = self.check_update_needed()

        return {
            'metadata': metadata,
            'current_stats': current_stats,
            'cache_info': cache_info,
            'expanded_db_available': os.path.exists("vehicles_expanded.db")
        }

    def schedule_auto_update(self):
        """Programar actualización automática si es necesario"""
        cache_info = self.check_update_needed()

        if cache_info['update_needed']:
            self.log("Se requiere actualización automática de datos de vehículos")
            # En un entorno real, esto se ejecutaría como tarea en background
            # Por ahora, solo registramos la necesidad
            return True
        else:
            self.log("Los datos están actualizados, no se requiere actualización")
            return False

# Instancia global del servicio de cache
vehicle_cache_service = VehicleCacheService()

# ==================== FUNCIONES ACTUALIZADAS ====================

def check_vehicles_table(verbose: bool = True, use_expanded: bool = True) -> dict:
    """
    Comprueba si la tabla vehicles existe y tiene datos válidos.
    Ahora soporta ambas bases de datos (legacy y expanded).
    """
    # Preferir la base de datos expandida si existe
    if use_expanded and os.path.exists("vehicles_expanded.db"):
        return check_expanded_vehicles_table(verbose)

    # Mantener compatibilidad con la base de datos legacy
    return check_legacy_vehicles_table(verbose)

def check_expanded_vehicles_table(verbose: bool = True) -> dict:
    """Comprobar tabla vehicles_expanded"""
    import sqlite3

    result = {
        "exists": False,
        "count": 0,
        "fuels": [],
        "brands": [],
        "sample": [],
        "error": None,
        "database_type": "expanded"
    }

    try:
        conn = sqlite3.connect("vehicles_expanded.db")
        cursor = conn.cursor()

        # Verificar que existe la tabla
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vehicles_expanded'")
        if not cursor.fetchone():
            result["error"] = "Tabla vehicles_expanded no existe"
            conn.close()
            return result

        # Contar vehículos
        cursor.execute("SELECT COUNT(*) FROM vehicles_expanded")
        count = cursor.fetchone()[0]
        result["count"] = count
        result["exists"] = count > 0

        if count > 0:
            # Obtener tipos de combustible
            cursor.execute("SELECT DISTINCT fuel_type FROM vehicles_expanded ORDER BY fuel_type")
            fuels = [row[0] for row in cursor.fetchall() if row[0]]
            result["fuels"] = fuels

            # Obtener marcas
            cursor.execute("SELECT DISTINCT brand FROM vehicles_expanded ORDER BY brand")
            brands = [row[0] for row in cursor.fetchall() if row[0]]
            result["brands"] = brands

            # Obtener muestra
            cursor.execute("SELECT fuel_type, brand, model, version FROM vehicles_expanded LIMIT 3")
            sample = cursor.fetchall()
            result["sample"] = [
                {
                    "fuel_type": row[0],
                    "brand": row[1],
                    "model": row[2],
                    "version": row[3]
                }
                for row in sample
            ]

            logger.info(f"Tabla vehicles_expanded contiene {count} registros")
        else:
            logger.warning("La tabla vehicles_expanded está vacía")

        if verbose:
            print("\n[CHECK] Tabla vehicles_expanded:")
            print(f"  Registros: {result['count']}")
            print(f"  Tipos de combustible: {result['fuels']}")
            print(f"  Marcas: {result['brands']}")
            print(f"  Ejemplo: {result['sample']}")

    except Exception as e:
        logger.error(f"Error comprobando tabla vehicles_expanded: {e}")
        result["error"] = str(e)
    finally:
        if 'conn' in locals():
            conn.close()

    return result

def check_legacy_vehicles_table(verbose: bool = True) -> dict:
    """Comprobar tabla vehicles original (función existente)"""
    db = SessionLocal()
    result = {
        "exists": False,
        "count": 0,
        "fuels": [],
        "brands": [],
        "sample": [],
        "error": None,
        "database_type": "legacy"
    }

    try:
        # ¿Existen vehículos?
        count = db.query(Vehicle).count()
        result["count"] = count
        result["exists"] = count > 0

        if count > 0:
            fuels = db.query(Vehicle.fuel_type).distinct().all()
            brands = db.query(Vehicle.brand).distinct().all()
            result["fuels"] = sorted(list(set([f[0] for f in fuels if f[0]])))
            result["brands"] = sorted(list(set([b[0] for b in brands if b[0]])))

            # Muestra 3 ejemplos
            sample = db.query(Vehicle).limit(3).all()
            result["sample"] = [
                {
                    "fuel_type": v.fuel_type,
                    "brand": v.brand,
                    "model": v.model,
                    "year": v.year,
                    "version": v.version
                }
                for v in sample
            ]

            logger.info(f"La tabla vehicles contiene {count} registros. Ejemplo: {result['sample']}")
        else:
            logger.warning("La tabla vehicles está vacía.")

        if verbose:
            print("\n[CHECK] Tabla vehicles:")
            print(f"  Registros: {result['count']}")
            print(f"  Tipos de combustible: {result['fuels']}")
            print(f"  Marcas: {result['brands']}")
            print(f"  Ejemplo: {result['sample']}")

    except Exception as e:
        logger.error(f"Error comprobando tabla vehicles: {e}")
        result["error"] = str(e)
    finally:
        db.close()

    return result

# Inicializar la base de datos al importar
try:
    init_db()
    # Programar verificación de actualización automática
    vehicle_cache_service.schedule_auto_update()
except Exception as e:
    logger.error(f"Error al inicializar la base de datos: {str(e)}")
