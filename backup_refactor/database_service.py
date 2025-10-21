"""
Servicio de Base de Datos - Gestión de Usuarios
===============================================

Servicios para manejar operaciones de base de datos relacionadas con usuarios
"""

from models.user import UserRegistration, SessionLocal, init_database
from sqlalchemy.exc import IntegrityError
import logging
from datetime import datetime
import re

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Inicializar la base de datos al importar
try:
    init_database()
except Exception as e:
    logger.error(f"Error al inicializar la base de datos: {str(e)}")
