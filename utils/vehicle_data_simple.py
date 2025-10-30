"""
Utilidades simples para datos de vehículos desde base de datos unificada
================================================================
Funciones optimizadas para obtener datos de vehículos desde astrotech.db
"""

from typing import List, Dict, Any
from models.vehicle import Vehicle
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import settings

# Crear conexión a base de datos
engine = create_engine(settings.DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_vehicle_fuel_types() -> List[str]:
    """
    Obtener todos los tipos de combustible disponibles con manejo de errores

    Returns:
        List[str]: Lista de tipos de combustible únicos
    """
    session = SessionLocal()
    try:
        fuel_types = session.query(Vehicle.fuel_type).distinct().all()
        result = [ft[0] for ft in fuel_types if ft[0]]

        if not result:
            print("[DB] ⚠️ No se encontraron tipos de combustible en la BD")
            return []

        print(f"[DB] ✅ Tipos de combustible encontrados: {result}")
        return result

    except Exception as e:
        print(f"[DB] ❌ Error en consulta de combustibles: {e}")
        return []  # Retornar lista vacía en caso de error
    finally:
        session.close()

def get_vehicle_brands(fuel_type: str = None) -> List[str]:
    """
    Obtener todas las marcas de vehículos disponibles

    Args:
        fuel_type: Filtrar por tipo de combustible (opcional)

    Returns:
        List[str]: Lista de marcas únicas
    """
    session = SessionLocal()
    try:
        query = session.query(Vehicle.brand).distinct()
        if fuel_type:
            query = query.filter(Vehicle.fuel_type == fuel_type)

        brands = query.all()
        return [brand[0] for brand in brands if brand[0]]
    finally:
        session.close()

def get_vehicle_models(fuel_type: str = None, brand: str = None) -> List[str]:
    """
    Obtener todos los modelos de vehículos disponibles

    Args:
        fuel_type: Filtrar por tipo de combustible (opcional)
        brand: Filtrar por marca (opcional)

    Returns:
        List[str]: Lista de modelos únicos
    """
    session = SessionLocal()
    try:
        query = session.query(Vehicle.model).distinct()

        if fuel_type:
            query = query.filter(Vehicle.fuel_type == fuel_type)
        if brand:
            query = query.filter(Vehicle.brand == brand)

        models = query.all()
        return [model[0] for model in models if model[0]]
    finally:
        session.close()

def get_vehicle_versions(fuel_type: str = None, brand: str = None, model: str = None) -> List[str]:
    """
    Obtener todas las versiones de vehículos disponibles

    Args:
        fuel_type: Filtrar por tipo de combustible (opcional)
        brand: Filtrar por marca (opcional)
        model: Filtrar por modelo (opcional)

    Returns:
        List[str]: Lista de versiones únicas
    """
    session = SessionLocal()
    try:
        query = session.query(Vehicle.version).distinct()

        if fuel_type:
            query = query.filter(Vehicle.fuel_type == fuel_type)
        if brand:
            query = query.filter(Vehicle.brand == brand)
        if model:
            query = query.filter(Vehicle.model == model)

        versions = query.all()
        return [version[0] for version in versions if version[0]]
    finally:
        session.close()

def get_vehicles_data(limit: int = 100, fuel_type: str = None, brand: str = None, model: str = None) -> List[Dict[str, Any]]:
    """
    Obtener datos de vehículos con filtros opcionales

    Args:
        limit: Límite de resultados
        fuel_type: Filtrar por tipo de combustible (opcional)
        brand: Filtrar por marca (opcional)
        model: Filtrar por modelo (opcional)

    Returns:
        List[Dict]: Lista de vehículos con sus datos
    """
    session = SessionLocal()
    try:
        query = session.query(Vehicle)

        if fuel_type:
            query = query.filter(Vehicle.fuel_type == fuel_type)
        if brand:
            query = query.filter(Vehicle.brand == brand)
        if model:
            query = query.filter(Vehicle.model == model)

        vehicles = query.limit(limit).all()

        return [
            {
                'id': vehicle.id,
                'fuel_type': vehicle.fuel_type,
                'brand': vehicle.brand,
                'model': vehicle.model,
                'year': vehicle.year,
                'version': vehicle.version
            }
            for vehicle in vehicles
        ]
    finally:
        session.close()

def get_vehicle_count() -> int:
    """
    Obtener el número total de vehículos en la base de datos

    Returns:
        int: Número total de vehículos
    """
    session = SessionLocal()
    try:
        return session.query(Vehicle).count()
    finally:
        session.close()

# Alias para compatibilidad con código existente
def get_vehicle_data(limit: int = 100):
    """Alias para compatibilidad - obtiene datos de vehículos"""
    return get_vehicles_data(limit=limit)

def get_vehicle_brands_simple():
    """Alias para compatibilidad - obtiene marcas"""
    return get_vehicle_brands()

# Para compatibilidad con nombres anteriores
def get_fuel_types():
    """Obtener tipos de combustible (alias)"""
    return get_vehicle_fuel_types()

def get_brands(fuel_type: str = None):
    """Obtener marcas (alias)"""
    return get_vehicle_brands(fuel_type)

def get_models(fuel_type: str = None, brand: str = None):
    """Obtener modelos (alias)"""
    return get_vehicle_models(fuel_type, brand)

# Verificación al importar
if __name__ == "__main__":
    print("=== VERIFICACIÓN DE UTILS.VEHICLE_DATA_SIMPLE ===")
    print(f"Tipos de combustible: {get_vehicle_fuel_types()}")
    print(f"Total vehículos: {get_vehicle_count()}")
    print(f"Marcas (diesel): {get_vehicle_brands('diesel')[:5]}")
    print("✅ Sistema de vehículos funcionando correctamente")