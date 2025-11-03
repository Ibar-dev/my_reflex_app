"""
Servicio para obtener datos de vehículos desde Supabase.
Reemplaza a vehicle_data_simple.py con conexión a PostgreSQL.
"""
from typing import List, Dict, Optional
import logging
from .supabase_connection import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_vehicle_fuel_types() -> List[str]:
    """
    Obtiene los tipos de combustible disponibles (Diesel, Gasolina).
    
    Returns:
        Lista de tipos de combustible únicos
    """
    if not db.connect():
        logger.error("No se pudo conectar a Supabase")
        return []
    
    try:
        query = """
        SELECT DISTINCT fuel_type 
        FROM vehicles 
        ORDER BY fuel_type;
        """
        results = db.execute_query(query)
        fuel_types = [row['fuel_type'] for row in results]
        logger.info(f"✅ Tipos de combustible obtenidos: {fuel_types}")
        return fuel_types
    
    except Exception as e:
        logger.error(f"❌ Error al obtener tipos de combustible: {e}")
        return []
    
    finally:
        db.disconnect()


def get_vehicle_brands(fuel_type: Optional[str] = None) -> List[str]:
    """
    Obtiene las marcas disponibles, opcionalmente filtradas por tipo de combustible.
    
    Args:
        fuel_type: Tipo de combustible para filtrar (opcional)
    
    Returns:
        Lista de marcas únicas
    """
    if not db.connect():
        logger.error("No se pudo conectar a Supabase")
        return []
    
    try:
        if fuel_type:
            query = """
            SELECT DISTINCT brand 
            FROM vehicles 
            WHERE fuel_type = %s
            ORDER BY brand;
            """
            results = db.execute_query(query, (fuel_type,))
        else:
            query = """
            SELECT DISTINCT brand 
            FROM vehicles 
            ORDER BY brand;
            """
            results = db.execute_query(query)
        
        brands = [row['brand'] for row in results]
        logger.info(f"✅ Marcas obtenidas: {len(brands)}")
        return brands
    
    except Exception as e:
        logger.error(f"❌ Error al obtener marcas: {e}")
        return []
    
    finally:
        db.disconnect()


def get_vehicle_models(fuel_type: str, brand: str) -> List[str]:
    """
    Obtiene los modelos disponibles para una marca y tipo de combustible.
    
    Args:
        fuel_type: Tipo de combustible
        brand: Marca del vehículo
    
    Returns:
        Lista de modelos únicos
    """
    if not db.connect():
        logger.error("No se pudo conectar a Supabase")
        return []
    
    try:
        query = """
        SELECT DISTINCT model 
        FROM vehicles 
        WHERE fuel_type = %s AND brand = %s
        ORDER BY model;
        """
        results = db.execute_query(query, (fuel_type, brand))
        models = [row['model'] for row in results]
        logger.info(f"✅ Modelos obtenidos: {len(models)}")
        return models
    
    except Exception as e:
        logger.error(f"❌ Error al obtener modelos: {e}")
        return []
    
    finally:
        db.disconnect()


def get_vehicle_versions(fuel_type: str, brand: str, model: str) -> List[str]:
    """
    Obtiene las versiones disponibles para un modelo específico.
    
    Args:
        fuel_type: Tipo de combustible
        brand: Marca del vehículo
        model: Modelo del vehículo
    
    Returns:
        Lista de versiones únicas
    """
    if not db.connect():
        logger.error("No se pudo conectar a Supabase")
        return []
    
    try:
        query = """
        SELECT DISTINCT version 
        FROM vehicles 
        WHERE fuel_type = %s AND brand = %s AND model = %s
        ORDER BY version;
        """
        results = db.execute_query(query, (fuel_type, brand, model))
        versions = [row['version'] for row in results if row['version']]
        logger.info(f"✅ Versiones obtenidas: {len(versions)}")
        return versions
    
    except Exception as e:
        logger.error(f"❌ Error al obtener versiones: {e}")
        return []
    
    finally:
        db.disconnect()


def get_vehicle_count() -> int:
    """Obtiene el total de vehículos en la base de datos"""
    if not db.connect():
        return 0
    
    try:
        query = "SELECT COUNT(*) as total FROM vehicles;"
        results = db.execute_query(query)
        total = results[0]['total'] if results else 0
        return total
    
    except Exception as e:
        logger.error(f"❌ Error al contar vehículos: {e}")
        return 0
    
    finally:
        db.disconnect()


def search_vehicles(search_term: str) -> List[Dict]:
    """
    Busca vehículos por término de búsqueda (marca, modelo o versión).
    
    Args:
        search_term: Término de búsqueda
    
    Returns:
        Lista de vehículos que coinciden
    """
    if not db.connect():
        return []
    
    try:
        query = """
        SELECT * FROM vehicles 
        WHERE 
            brand ILIKE %s OR 
            model ILIKE %s OR 
            version ILIKE %s
        ORDER BY brand, model, version
        LIMIT 50;
        """
        search_pattern = f"%{search_term}%"
        results = db.execute_query(query, (search_pattern, search_pattern, search_pattern))
        return results
    
    except Exception as e:
        logger.error(f"❌ Error en búsqueda: {e}")
        return []
    
    finally:
        db.disconnect()


def add_vehicle(fuel_type: str, brand: str, model: str, version: str) -> bool:
    """
    Añade un nuevo vehículo a la base de datos.
    
    Args:
        fuel_type: Tipo de combustible (Diesel o Gasolina)
        brand: Marca del vehículo
        model: Modelo del vehículo
        version: Versión del vehículo
    
    Returns:
        True si se insertó correctamente, False en caso contrario
    """
    if not db.connect():
        return False
    
    try:
        query = """
        INSERT INTO vehicles (fuel_type, brand, model, version)
        VALUES (%s, %s, %s, %s);
        """
        return db.execute_update(query, (fuel_type, brand, model, version))
    
    except Exception as e:
        logger.error(f"❌ Error al añadir vehículo: {e}")
        return False
    
    finally:
        db.disconnect()


if __name__ == "__main__":
    # Pruebas rápidas
    print("🧪 Probando servicio de vehículos...\n")
    
    print("1. Tipos de combustible:")
    print(get_vehicle_fuel_types())
    
    print("\n2. Marcas (Diesel):")
    print(get_vehicle_brands("Diesel")[:5])
    
    print("\n3. Total de vehículos:")
    print(get_vehicle_count())
