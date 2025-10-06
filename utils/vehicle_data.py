"""
Utilidades para datos de vehículos - AstroTech
=============================================

Carga y procesa datos de vehículos desde el JSON enriquecido para reprogramación ECU.
"""

import json
import os
from typing import Dict, List, Any

def load_vehicle_data() -> List[Dict[str, Any]]:
    """
    Cargar datos de vehículos desde el JSON enriquecido.
    
    Returns:
        List[Dict]: Lista de todos los vehículos con datos técnicos
    """
    try:
        # Obtener la ruta del archivo JSON
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, "..", "data", "vehiculos_turismo.json")
        json_path = os.path.normpath(json_path)  # Normalizar la ruta
        
        print(f"Intentando cargar archivo: {json_path}")
        
        if not os.path.exists(json_path):
            print(f"Archivo no encontrado: {json_path}")
            return []
            
        with open(json_path, 'r', encoding='utf-8') as f:
            vehicles = json.load(f)
        
        print(f"Cargados {len(vehicles)} vehículos")
        return vehicles
    except Exception as e:
        print(f"Error cargando datos de vehículos: {e}")
        return []

def get_brands_by_fuel(fuel_type: str) -> List[str]:
    """
    Obtener marcas disponibles por tipo de combustible.
    
    Args:
        fuel_type: Tipo de combustible ('gasolina', 'diesel')
    
    Returns:
        List[str]: Lista de marcas disponibles
    """
    try:
        vehicles = load_vehicle_data()
        if not vehicles:
            # Fallback con datos básicos si no se puede cargar el JSON
            return ["Ford", "Audi", "BMW", "Mercedes-Benz", "Volkswagen"]
            
        brands = set()
        
        for vehicle in vehicles:
            if vehicle.get('fuel_type') == fuel_type:
                make = vehicle.get('make', '').strip()
                if make:
                    brands.add(make)
        
        result = sorted(list(brands))
        print(f"Marcas encontradas para {fuel_type}: {len(result)}")
        return result
    except Exception as e:
        print(f"Error obteniendo marcas: {e}")
        return ["Ford", "Audi", "BMW", "Mercedes-Benz", "Volkswagen"]

def get_models_by_brand(brand: str, fuel_type: str) -> List[str]:
    """
    Obtener modelos disponibles por marca y tipo de combustible.
    
    Args:
        brand: Marca del vehículo
        fuel_type: Tipo de combustible ('gasolina', 'diesel')
    
    Returns:
        List[str]: Lista de modelos disponibles
    """
    try:
        vehicles = load_vehicle_data()
        if not vehicles:
            # Fallback con datos básicos
            fallback_models = {
                "Ford": ["Focus", "Fiesta", "Mustang"],
                "Audi": ["A3", "A4", "A6"],
                "BMW": ["Serie 3", "Serie 5", "X3"],
                "Mercedes-Benz": ["C-Class", "E-Class"],
                "Volkswagen": ["Golf", "Passat"]
            }
            return fallback_models.get(brand, [])
            
        models = set()
        
        for vehicle in vehicles:
            if (vehicle.get('make') == brand and 
                vehicle.get('fuel_type') == fuel_type):
                model = vehicle.get('model', '').strip()
                if model:
                    models.add(model)
        
        result = sorted(list(models))
        print(f"Modelos encontrados para {brand} ({fuel_type}): {len(result)}")
        return result
    except Exception as e:
        print(f"Error obteniendo modelos: {e}")
        return []

def get_vehicles_by_brand_model(brand: str, model: str, fuel_type: str) -> List[Dict[str, Any]]:
    """
    Obtener vehículos específicos por marca, modelo y combustible.
    
    Args:
        brand: Marca del vehículo
        model: Modelo del vehículo
        fuel_type: Tipo de combustible ('gasolina', 'diesel')
    
    Returns:
        List[Dict]: Lista de vehículos con esas especificaciones
    """
    try:
        vehicles = load_vehicle_data()
        if not vehicles:
            # Fallback con un vehículo básico de ejemplo
            return [{
                "id": 1,
                "make": brand,
                "model": model,
                "year": 2022,
                "fuel_type": fuel_type,
                "engine_name": "Motor Genérico",
                "displacement": "2.0L",
                "power_stock": 150,
                "torque_stock": 300,
                "ecu_brand": "Bosch",
                "ecu_model": "Generic ECU",
                "tuning_potential": {
                    "power_tuned": 180,
                    "torque_tuned": 360,
                    "power_gain": 30,
                    "torque_gain": 60,
                    "fuel_reduction": 10
                }
            }]
            
        filtered_vehicles = []
        
        for vehicle in vehicles:
            if (vehicle.get('make') == brand and 
                vehicle.get('model') == model and
                vehicle.get('fuel_type') == fuel_type):
                filtered_vehicles.append(vehicle)
        
        # Ordenar por año descendente
        result = sorted(filtered_vehicles, key=lambda x: x.get('year', 0), reverse=True)
        print(f"Vehículos encontrados para {brand} {model} ({fuel_type}): {len(result)}")
        return result
    except Exception as e:
        print(f"Error obteniendo vehículos: {e}")
        return []

def calculate_base_price(power_gain: int, fuel_type: str) -> int:
    """
    Calcular precio base de reprogramación según ganancia de potencia.
    
    Args:
        power_gain: Ganancia de potencia en CV
        fuel_type: Tipo de combustible
    
    Returns:
        int: Precio en euros
    """
    base_price = 250  # Precio base
    
    # Precio por CV adicional
    price_per_cv = 8 if fuel_type == 'diesel' else 6
    
    total_price = base_price + (power_gain * price_per_cv)
    
    # Redondear a múltiplos de 10
    return round(total_price / 10) * 10

def get_vehicle_stats() -> Dict[str, Any]:
    """
    Obtener estadísticas generales de los vehículos disponibles.
    
    Returns:
        Dict: Estadísticas de la base de datos
    """
    vehicles = load_vehicle_data()
    
    stats = {
        'total_vehicles': len(vehicles),
        'brands': len(set(v.get('make', '') for v in vehicles)),
        'models': len(set(f"{v.get('make', '')} {v.get('model', '')}" for v in vehicles)),
        'fuel_types': {
            'gasolina': len([v for v in vehicles if v.get('fuel_type') == 'gasolina']),
            'diesel': len([v for v in vehicles if v.get('fuel_type') == 'diesel'])
        },
        'top_brands': {}
    }
    
    # Top marcas
    brand_count = {}
    for vehicle in vehicles:
        brand = vehicle.get('make', 'Unknown')
        brand_count[brand] = brand_count.get(brand, 0) + 1
    
    stats['top_brands'] = dict(sorted(brand_count.items(), key=lambda x: x[1], reverse=True)[:10])
    
    return stats
