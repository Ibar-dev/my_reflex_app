"""
Modelos de Base de Datos - Usuarios
===================================

Definición de las tablas y modelos para almacenar información de usuarios
"""

import sqlalchemy as sa
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

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

# Configuración de la base de datos
# Usar la ruta del proyecto para la base de datos
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(PROJECT_ROOT, "users.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Crear engine y sesión
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Necesario para SQLite
    echo=False  # Cambiar a True para ver las consultas SQL en desarrollo
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_database():
    """Inicializa la base de datos creando todas las tablas"""
    try:
        Base.metadata.create_all(bind=engine)
        print(f"✅ Base de datos inicializada en: {DATABASE_PATH}")
        return True
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {str(e)}")
        return False

def get_database_info():
    """Información sobre la base de datos"""
    return {
        "database_path": DATABASE_PATH,
        "database_url": DATABASE_URL,
        "tables": ["user_registrations"]
    }

# Inicializar la base de datos al importar el módulo
if __name__ == "__main__":
    init_database()
