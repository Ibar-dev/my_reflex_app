"""
Modelos de Base de Datos - Usuarios
===================================

Definición de las tablas y modelos para almacenar información de usuarios
Versión optimizada para sinergia perfecta con otros componentes.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
import settings

Base = declarative_base()

class UserRegistration(Base):
    """Modelo para almacenar registros de usuarios del popup de descuento"""
    __tablename__ = "user_registrations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    telefono = Column(String(20), nullable=False)
    source = Column(String(50), default="discount_popup")  # De dónde vino el registro
    is_contacted = Column(Boolean, default=False)  # Si ya fue contactado
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<UserRegistration(id={self.id}, nombre='{self.nombre}', email='{self.email}')>"

    def to_dict(self):
        """Convierte el objeto a diccionario para JSON"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono,
            "source": self.source,
            "is_contacted": self.is_contacted,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

# Configuración de la base de datos usando settings centralizado
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # Necesario para SQLite
    echo=False  # Cambiar a True para ver las consultas SQL en desarrollo
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_database():
    """Inicializa la base de datos creando todas las tablas"""
    try:
        Base.metadata.create_all(bind=engine)
        print(f"Base de datos de usuarios inicializada en: {settings.DATABASE_PATH}")
        return True
    except Exception as e:
        print(f"Error al inicializar la base de datos: {str(e)}")
        return False

def get_database_info():
    """Información sobre la base de datos"""
    info = settings.get_database_info()
    info["tables"] = ["user_registrations"]
    return info

class UserService:
    """Servicio para operaciones de usuarios con sinergia perfecta"""

    @staticmethod
    def find_by_email(email: str) -> dict:
        """
        Busca un usuario por email de forma optimizada

        Args:
            email: Email a buscar

        Returns:
            dict: {"success": bool, "user": dict or None, "found": bool, "message": str}
        """
        if not email:
            return {
                "success": False,
                "user": None,
                "found": False,
                "message": "Email no proporcionado"
            }

        # Limpiar email para búsqueda
        email_clean = email.strip().lower()

        session = SessionLocal()
        try:
            user = session.query(UserRegistration).filter(
                UserRegistration.email == email_clean
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
            print(f"Error buscando usuario por email: {str(e)}")
            return {
                "success": False,
                "user": None,
                "found": False,
                "message": f"Error en búsqueda: {str(e)}"
            }
        finally:
            session.close()

    @staticmethod
    def save_user(nombre: str, email: str, telefono: str, source: str = "contact_form") -> dict:
        """
        Guarda un nuevo usuario en la base de datos

        Args:
            nombre: Nombre del usuario
            email: Email del usuario
            telefono: Teléfono del usuario
            source: Fuente del registro

        Returns:
            dict: Resultado de la operación
        """
        session = SessionLocal()
        try:
            # Verificar si ya existe
            existing = session.query(UserRegistration).filter(
                UserRegistration.email == email.strip().lower()
            ).first()

            if existing:
                return {
                    "success": False,
                    "message": "Email ya registrado",
                    "user_id": existing.id
                }

            # Crear nuevo usuario
            new_user = UserRegistration(
                nombre=nombre.strip().title(),
                email=email.strip().lower(),
                telefono=telefono.strip(),
                source=source
            )

            session.add(new_user)
            session.commit()
            session.refresh(new_user)

            return {
                "success": True,
                "message": "Usuario registrado correctamente",
                "user_id": new_user.id,
                "user": new_user.to_dict()
            }

        except Exception as e:
            session.rollback()
            print(f"Error guardando usuario: {str(e)}")
            return {
                "success": False,
                "message": f"Error: {str(e)}",
                "user_id": None
            }
        finally:
            session.close()

# Inicializar la base de datos al importar el módulo
if __name__ == "__main__":
    init_database()