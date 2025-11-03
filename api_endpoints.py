"""
API Endpoints para Tests E2E
============================

Endpoints REST para que los tests E2E puedan verificar
el funcionamiento de la aplicación.
"""

import reflex as rx
from utils.vehicle_data_simple import (
    get_vehicle_fuel_types,
    get_vehicle_brands,
    get_vehicle_models,
    get_vehicle_versions
)

@rx.api.get
def ping():
    """Health check endpoint."""
    return {"status": "ok", "timestamp": rx.state.time()}

@rx.api.get
def api_fuel_types():
    """Obtener tipos de combustible disponibles."""
    try:
        fuel_types = get_vehicle_fuel_types()
        return fuel_types
    except Exception as e:
        rx.state.console.error(f"Error getting fuel types: {e}")
        return []

@rx.api.get
def api_brands(fuel_type: str):
    """Obtener marcas por tipo de combustible."""
    try:
        if not fuel_type:
            return []
        brands = get_vehicle_brands(fuel_type)
        return brands
    except Exception as e:
        rx.state.console.error(f"Error getting brands: {e}")
        return []

@rx.api.get
def api_models(fuel_type: str, brand: str):
    """Obtener modelos por tipo de combustible y marca."""
    try:
        if not fuel_type or not brand:
            return []
        models = get_vehicle_models(fuel_type, brand)
        return models
    except Exception as e:
        rx.state.console.error(f"Error getting models: {e}")
        return []

@rx.api.get
def api_versions(fuel_type: str, brand: str, model: str):
    """Obtener versiones por tipo de combustible, marca y modelo."""
    try:
        if not fuel_type or not brand or not model:
            return []
        versions = get_vehicle_versions(fuel_type, brand, model)
        return versions
    except Exception as e:
        rx.state.console.error(f"Error getting versions: {e}")
        return []

@rx.api.get
def api_vehicles(limit: int = 100):
    """Obtener lista de vehículos con filtros opcionales."""
    try:
        from utils.vehicle_data_simple import get_vehicles_data
        vehicles = get_vehicles_data(limit=limit)
        return vehicles
    except Exception as e:
        rx.state.console.error(f"Error getting vehicles: {e}")
        return []