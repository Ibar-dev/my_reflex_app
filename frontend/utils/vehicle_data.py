"""
Utilidades para datos de vehículos - AstroTech
=============================================

Carga y procesa datos de vehículos desde vehiculos_turismo.json
Con logging detallado para debugging.
"""

import json
import os
from typing import Dict, List, Any
from pathlib import Path

# Cache para evitar múltiples lecturas del JSON
_VEHICLE_CACHE = None

def load_vehicle_data() -> List[Dict[str, Any]]:
    """
    Cargar datos de vehículos desde vehiculos_turismo.json.
    Usa caché para mejorar rendimiento.
    
    Returns:
        List[Dict]: Lista de todos los vehículos con datos técnicos
    """
    global _VEHICLE_CACHE
    
    # Retornar caché si existe
    if _VEHICLE_CACHE is not None:
        return _VEHICLE_CACHE
    
    try:
        # Buscar el archivo JSON en múltiples ubicaciones posibles
        possible_paths = [
            # Desde app/
            Path(__file__).parent.parent / "data" / "vehiculos_turismo.json",
            # Desde frontend/
            Path(__file__).parent.parent / "data" / "vehiculos_turismo.json",
            # Ruta absoluta relativa al proyecto
            Path.cwd() / "data" / "vehiculos_turismo.json",
            Path.cwd() / "frontend" / "data" / "vehiculos_turismo.json",
        ]
        
        json_path = None
        for path in possible_paths:
            if path.exists():
                json_path = path
                break
        
        if not json_path:
            print(f"❌ ERROR: No se encontró vehiculos_turismo.json en:")
            for path in possible_paths:
                print(f"   - {path}")
            print("\n💡 SOLUCIÓN: Asegúrate de que vehiculos_turismo.json esté en:")
            print(f"   {possible_paths[0]}")
            return []
        
        print(f"📂 Cargando vehículos desde: {json_path}")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            vehicles = json.load(f)
        
        # Validar estructura básica
        if not isinstance(vehicles, list):
            print(f"❌ ERROR: El JSON debe ser una lista, encontrado: {type(vehicles)}")
            return []
        
        # Validar que tiene datos
        if len(vehicles) == 0:
            print(f"⚠️  WARNING: El JSON está vacío")
            return []
        
        # Verificar estructura del primer vehículo
        first_vehicle = vehicles[0]
        required_fields = ['make', 'model', 'fuel_type', 'year']
        missing_fields = [f for f in required_fields if f not in first_vehicle]
        
        if missing_fields:
            print(f"⚠️  WARNING: Faltan campos en el JSON: {missing_fields}")
            print(f"   Campos presentes: {list(first_vehicle.keys())}")
        
        _VEHICLE_CACHE = vehicles
        print(f"✅ Cargados {len(vehicles)} vehículos correctamente")
        print(f"📊 Ejemplo: {first_vehicle.get('make')} {first_vehicle.get('model')} ({first_vehicle.get('year')})")
        
        return vehicles
        
    except json.JSONDecodeError as e:
        print(f"❌ ERROR: JSON inválido en línea {e.lineno}: {e.msg}")
        return []
    except Exception as e:
        print(f"❌ ERROR cargando vehiculos_turismo.json: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return []

def get_brands_by_fuel(fuel_type: str) -> List[str]:
    """
    Obtener marcas únicas por tipo de combustible.
    
    Args:
        fuel_type: 'gasolina' o 'diesel' (exactamente como aparece en JSON)
    
    Returns:
        List[str]: Lista ordenada de marcas disponibles
    """
    try:
        vehicles = load_vehicle_data()
        
        if not vehicles:
            print(f"⚠️  No hay vehículos, usando fallback")
            return _get_fallback_brands()
        
        # Extraer marcas únicas para el combustible especificado
        brands = set()
        fuel_type_lower = fuel_type.lower()  # Normalizar a minúsculas
        
        for vehicle in vehicles:
            vehicle_fuel = vehicle.get('fuel_type', '').lower()
            
            # Buscar coincidencias flexibles
            if vehicle_fuel == fuel_type_lower:
                make = vehicle.get('make', '').strip()
                if make:
                    brands.add(make)
        
        if not brands:
            print(f"⚠️  No se encontraron marcas para '{fuel_type}'")
            print(f"   Tipos de combustible en JSON: {set(v.get('fuel_type', '') for v in vehicles[:10])}")
            return _get_fallback_brands()
        
        result = sorted(list(brands))
        print(f"✅ Marcas para {fuel_type}: {len(result)} marcas")
        print(f"   Ejemplos: {result[:5]}")
        return result
        
    except Exception as e:
        print(f"❌ ERROR en get_brands_by_fuel: {e}")
        return _get_fallback_brands()

def get_models_by_brand(brand: str, fuel_type: str) -> List[str]:
    """
    Obtener modelos únicos por marca y combustible.
    
    Args:
        brand: Marca del vehículo (debe coincidir exactamente)
        fuel_type: 'gasolina' o 'diesel'
    
    Returns:
        List[str]: Lista ordenada de modelos disponibles
    """
    try:
        vehicles = load_vehicle_data()
        
        if not vehicles:
            print(f"⚠️  No hay vehículos, usando fallback")
            return ["Modelo Genérico"]
        
        # Extraer modelos únicos
        models = set()
        fuel_type_lower = fuel_type.lower()
        
        for vehicle in vehicles:
            vehicle_fuel = vehicle.get('fuel_type', '').lower()
            vehicle_brand = vehicle.get('make', '').strip()
            
            if vehicle_brand == brand and vehicle_fuel == fuel_type_lower:
                model = vehicle.get('model', '').strip()
                if model:
                    models.add(model)
        
        if not models:
            print(f"⚠️  No se encontraron modelos para {brand} ({fuel_type})")
            return ["Modelo Genérico"]
        
        result = sorted(list(models))
        print(f"✅ Modelos para {brand} ({fuel_type}): {len(result)} modelos")
        print(f"   Ejemplos: {result[:5]}")
        return result
        
    except Exception as e:
        print(f"❌ ERROR en get_models_by_brand: {e}")
        return ["Modelo Genérico"]

def get_vehicles_by_brand_model(brand: str, model: str, fuel_type: str) -> List[Dict[str, Any]]:
    """
    Obtener vehículos específicos filtrados por marca, modelo y combustible.
    
    Args:
        brand: Marca del vehículo
        model: Modelo del vehículo
        fuel_type: 'gasolina' o 'diesel'
    
    Returns:
        List[Dict]: Lista de vehículos que coinciden (ordenados por año desc)
    """
    try:
        vehicles = load_vehicle_data()
        
        if not vehicles:
            print(f"⚠️  No hay vehículos, creando demo")
            return [_create_demo_vehicle(brand, model, fuel_type)]
        
        # Filtrar vehículos
        filtered = []
        fuel_type_lower = fuel_type.lower()
        
        for vehicle in vehicles:
            if (vehicle.get('make', '').strip() == brand and 
                vehicle.get('model', '').strip() == model and
                vehicle.get('fuel_type', '').lower() == fuel_type_lower):
                filtered.append(vehicle)
        
        if not filtered:
            print(f"⚠️  No se encontraron vehículos para {brand} {model} ({fuel_type})")
            return [_create_demo_vehicle(brand, model, fuel_type)]
        
        # Ordenar por año descendente
        result = sorted(filtered, key=lambda x: x.get('year', 0), reverse=True)
        print(f"✅ Vehículos encontrados: {len(result)}")
        print(f"   Años disponibles: {[v.get('year') for v in result[:5]]}")
        return result
        
    except Exception as e:
        print(f"❌ ERROR en get_vehicles_by_brand_model: {e}")
        return [_create_demo_vehicle(brand, model, fuel_type)]

def _get_fallback_brands() -> List[str]:
    """Marcas de fallback si no se puede leer el JSON"""
    return [
        "Audi", "BMW", "Mercedes-Benz", "Volkswagen", "Ford",
        "Peugeot", "Renault", "SEAT", "Opel", "Citroën",
        "Toyota", "Honda", "Nissan", "Mazda", "Hyundai",
        "Kia", "Chevrolet", "Fiat", "Alfa Romeo", "Volvo"
    ]

def _create_demo_vehicle(brand: str, model: str, fuel_type: str) -> Dict[str, Any]:
    """Crear vehículo de demostración"""
    
    # Especificaciones por marca para demos más realistas
    brand_specs = {
        "Audi": {"power": 150, "tuned": 190, "gain": 40, "torque": 320, "torque_tuned": 380},
        "BMW": {"power": 150, "tuned": 190, "gain": 40, "torque": 320, "torque_tuned": 380},
        "Mercedes-Benz": {"power": 170, "tuned": 220, "gain": 50, "torque": 360, "torque_tuned": 440},
        "Volkswagen": {"power": 150, "tuned": 190, "gain": 40, "torque": 320, "torque_tuned": 380},
        "Ford": {"power": 150, "tuned": 190, "gain": 40, "torque": 370, "torque_tuned": 420},
        "Peugeot": {"power": 130, "tuned": 165, "gain": 35, "torque": 300, "torque_tuned": 360},
        "Renault": {"power": 130, "tuned": 165, "gain": 35, "torque": 300, "torque_tuned": 360},
        "SEAT": {"power": 150, "tuned": 190, "gain": 40, "torque": 320, "torque_tuned": 380},
    }
    
    specs = brand_specs.get(brand, {
        "power": 150, "tuned": 190, "gain": 40, "torque": 300, "torque_tuned": 380
    })
    
    return {
        "make": brand,
        "model": model,
        "year": 2023,
        "fuel_type": fuel_type,
        "engine_name": f"Motor {fuel_type.title()} 2.0",
        "displacement": "2.0L",
        "power_stock": specs["power"],
        "torque_stock": specs["torque"],
        "ecu_brand": "Bosch",
        "ecu_model": "EDC17",
        "tuning_potential": {
            "power_tuned": specs["tuned"],
            "torque_tuned": specs["torque_tuned"],
            "power_gain": specs["gain"],
            "torque_gain": specs["torque_tuned"] - specs["torque"],
            "fuel_reduction": 12
        }
    }

def get_vehicle_stats() -> Dict[str, Any]:
    """
    Obtener estadísticas de la base de datos de vehículos.
    Útil para debugging y verificación.
    
    Returns:
        Dict con estadísticas generales
    """
    vehicles = load_vehicle_data()
    
    if not vehicles:
        return {
            'total_vehicles': 0,
            'error': 'No se pudo cargar vehiculos_turismo.json'
        }
    
    # Calcular estadísticas
    brands = set(v.get('make', '') for v in vehicles if v.get('make'))
    models = set(f"{v.get('make', '')} {v.get('model', '')}" for v in vehicles if v.get('make') and v.get('model'))
    
    fuel_types = {}
    for vehicle in vehicles:
        fuel = vehicle.get('fuel_type', 'unknown').lower()
        fuel_types[fuel] = fuel_types.get(fuel, 0) + 1
    
    # Top 10 marcas
    brand_count = {}
    for vehicle in vehicles:
        brand = vehicle.get('make', 'Unknown')
        brand_count[brand] = brand_count.get(brand, 0) + 1
    
    top_brands = dict(sorted(brand_count.items(), key=lambda x: x[1], reverse=True)[:10])
    
    stats = {
        'total_vehicles': len(vehicles),
        'unique_brands': len(brands),
        'unique_models': len(models),
        'fuel_types': fuel_types,
        'top_brands': top_brands,
        'sample_vehicle': vehicles[0] if vehicles else None
    }
    
    return stats

def debug_json_structure():
    """
    Función de debugging para verificar la estructura del JSON.
    Llama a esta función si tienes problemas.
    """
    print("\n" + "="*60)
    print("🔍 DEBUGGING: Estructura del JSON")
    print("="*60 + "\n")
    
    vehicles = load_vehicle_data()
    
    if not vehicles:
        print("❌ No se pudieron cargar vehículos")
        return
    
    # Mostrar primer vehículo completo
    print("📋 Estructura del primer vehículo:")
    print(json.dumps(vehicles[0], indent=2, ensure_ascii=False))
    
    # Estadísticas
    stats = get_vehicle_stats()
    print("\n📊 Estadísticas:")
    for key, value in stats.items():
        if key != 'sample_vehicle':
            print(f"   {key}: {value}")
    
    print("\n" + "="*60 + "\n")

# Para testing: ejecutar este archivo directamente
if __name__ == "__main__":
    debug_json_structure()