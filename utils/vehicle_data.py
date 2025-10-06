"""
Utilidades para datos de vehículos - AstroTech CORREGIDO
=========================================================
"""

import json
import os
from typing import Dict, List, Any
from pathlib import Path

def get_data_path() -> Path:
    """
    Obtener ruta absoluta al archivo JSON de forma confiable.
    """
    # Opción 1: Usar Path del archivo actual
    current_file = Path(__file__)  # utils/vehicle_data.py
    project_root = current_file.parent.parent  # Sube 2 niveles
    json_path = project_root / "data" / "vehiculos_turismo.json"
    
    # Opción 2: Si la anterior falla, buscar desde el directorio de trabajo
    if not json_path.exists():
        json_path = Path("data/vehiculos_turismo.json")
    
    # Opción 3: Buscar en frontend/data
    if not json_path.exists():
        json_path = Path("frontend/data/vehiculos_turismo.json")
    
    return json_path

def load_vehicle_data() -> List[Dict[str, Any]]:
    """
    Cargar datos de vehículos desde el JSON enriquecido.
    
    Returns:
        List[Dict]: Lista de todos los vehículos con datos técnicos
    """
    try:
        json_path = get_data_path()
        
        print(f"🔍 Intentando cargar desde: {json_path.absolute()}")
        
        if not json_path.exists():
            print(f"❌ Archivo NO encontrado: {json_path.absolute()}")
            print(f"📁 Directorio actual: {Path.cwd()}")
            return []
        
        print(f"✅ Archivo encontrado, cargando...")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            vehicles = json.load(f)
        
        if not isinstance(vehicles, list):
            print(f"❌ El JSON no es una lista, es: {type(vehicles)}")
            return []
        
        print(f"✅ Cargados {len(vehicles)} vehículos")
        
        # Verificar estructura del primer vehículo
        if vehicles:
            first = vehicles[0]
            required_fields = ['make', 'model', 'fuel_type', 'year']
            missing = [f for f in required_fields if f not in first]
            if missing:
                print(f"⚠️  Faltan campos en el JSON: {missing}")
            else:
                print(f"✅ Estructura del JSON correcta")
                print(f"   Ejemplo: {first.get('make')} {first.get('model')} ({first.get('year')})")
        
        return vehicles
        
    except json.JSONDecodeError as e:
        print(f"❌ Error de sintaxis en JSON: {e}")
        return []
    except Exception as e:
        print(f"❌ Error inesperado cargando datos: {e}")
        import traceback
        traceback.print_exc()
        return []

def get_brands_by_fuel(fuel_type: str) -> List[str]:
    """
    Obtener marcas disponibles por tipo de combustible.
    """
    print(f"\n🔧 get_brands_by_fuel('{fuel_type}')")
    
    try:
        vehicles = load_vehicle_data()
        
        if not vehicles:
            print(f"⚠️  No hay vehículos, usando fallback")
            return ["Audi", "BMW", "Ford", "Mercedes-Benz", "Volkswagen", "Peugeot", "Renault", "SEAT"]
        
        brands = set()
        fuel_matches = 0
        
        for vehicle in vehicles:
            v_fuel = vehicle.get('fuel_type', '').strip().lower()
            v_make = vehicle.get('make', '').strip()
            
            # Debug: Mostrar primeros 3 vehículos
            if fuel_matches < 3:
                print(f"   Vehículo {fuel_matches + 1}: fuel='{v_fuel}', make='{v_make}'")
            
            if v_fuel == fuel_type.lower() and v_make:
                brands.add(v_make)
                fuel_matches += 1
        
        result = sorted(list(brands))
        print(f"✅ Encontradas {len(result)} marcas para '{fuel_type}'")
        print(f"   Marcas: {result[:5]}{'...' if len(result) > 5 else ''}")
        
        if not result:
            print(f"⚠️  No hay marcas para '{fuel_type}', verificar JSON")
            return ["Audi", "BMW", "Ford"]
        
        return result
        
    except Exception as e:
        print(f"❌ Error en get_brands_by_fuel: {e}")
        return ["Audi", "BMW", "Ford"]

def get_models_by_brand(brand: str, fuel_type: str) -> List[str]:
    """
    Obtener modelos disponibles por marca y combustible.
    """
    print(f"\n🔧 get_models_by_brand('{brand}', '{fuel_type}')")
    
    try:
        vehicles = load_vehicle_data()
        
        if not vehicles:
            fallback = {
                "Ford": ["Focus", "Fiesta", "Mustang"],
                "Audi": ["A3", "A4", "A6"],
                "BMW": ["Serie 3", "Serie 5", "X3"],
            }
            return fallback.get(brand, [f"{brand} Modelo 1"])
        
        models = set()
        
        for vehicle in vehicles:
            v_make = vehicle.get('make', '').strip()
            v_fuel = vehicle.get('fuel_type', '').strip().lower()
            v_model = vehicle.get('model', '').strip()
            
            if v_make == brand and v_fuel == fuel_type.lower() and v_model:
                models.add(v_model)
        
        result = sorted(list(models))
        print(f"✅ Encontrados {len(result)} modelos")
        print(f"   Modelos: {result[:5]}{'...' if len(result) > 5 else ''}")
        
        return result if result else [f"{brand} Genérico"]
        
    except Exception as e:
        print(f"❌ Error en get_models_by_brand: {e}")
        return [f"{brand} Genérico"]

def get_vehicles_by_brand_model(brand: str, model: str, fuel_type: str) -> List[Dict[str, Any]]:
    """
    Obtener vehículos específicos.
    """
    print(f"\n🔧 get_vehicles_by_brand_model('{brand}', '{model}', '{fuel_type}')")
    
    try:
        vehicles = load_vehicle_data()
        
        if not vehicles:
            return [{
                "make": brand,
                "model": model,
                "year": 2023,
                "fuel_type": fuel_type,
                "power_stock": 150,
                "tuning_potential": {
                    "power_tuned": 190,
                    "power_gain": 40
                }
            }]
        
        filtered = [
            v for v in vehicles
            if (v.get('make', '').strip() == brand and
                v.get('model', '').strip() == model and
                v.get('fuel_type', '').strip().lower() == fuel_type.lower())
        ]
        
        result = sorted(filtered, key=lambda x: x.get('year', 0), reverse=True)
        print(f"✅ Encontrados {len(result)} vehículos")
        
        return result if result else [{
            "make": brand,
            "model": model,
            "year": 2023,
            "fuel_type": fuel_type,
            "power_stock": 150,
            "tuning_potential": {"power_tuned": 190, "power_gain": 40}
        }]
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

# Resto de funciones sin cambios...
def calculate_base_price(power_gain: int, fuel_type: str) -> int:
    """Calcular precio base."""
    base_price = 250
    price_per_cv = 8 if fuel_type == 'diesel' else 6
    return round((base_price + (power_gain * price_per_cv)) / 10) * 10

def get_vehicle_stats() -> Dict[str, Any]:
    """Estadísticas de la base de datos."""
    vehicles = load_vehicle_data()
    return {
        'total_vehicles': len(vehicles),
        'brands': len(set(v.get('make', '') for v in vehicles)),
    }