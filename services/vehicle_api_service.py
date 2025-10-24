
import os
import sqlite3
from typing import List
from models.vehicle import Vehicle, VehicleExpanded

# Configuración de bases de datos
EXPANDED_DB_PATH = "vehicles_expanded.db"
DEFAULT_DB_PATH = "vehicles.db"

def get_database_session(expanded=True):
    """Obtener sesión de base de datos (expandida o por defecto)"""
    if expanded and os.path.exists(EXPANDED_DB_PATH):
        # Usar la base de datos expandida
        conn = sqlite3.connect(EXPANDED_DB_PATH)
        return conn, True  # expanded=True
    else:
        # Usar la base de datos por defecto a través de SQLAlchemy
        from utils.database_service import SessionLocal
        return SessionLocal(), False  # expanded=False

def get_fuel_types(expanded=True):
    """Obtener tipos de combustible disponibles"""
    session, is_expanded = get_database_session(expanded)

    try:
        if is_expanded:
            # Usar SQLite directo
            cursor = session.cursor()
            cursor.execute("SELECT DISTINCT fuel_type FROM vehicles_expanded ORDER BY fuel_type")
            types = cursor.fetchall()
            return [t[0] for t in types]
        else:
            # Usar SQLAlchemy
            types = session.query(Vehicle.fuel_type).distinct().all()
            return [t[0] for t in types]
    finally:
        session.close()

def get_brands(fuel_type: str, expanded=True):
    """Obtener marcas para un tipo de combustible específico"""
    session, is_expanded = get_database_session(expanded)

    try:
        if is_expanded:
            cursor = session.cursor()
            cursor.execute(
                "SELECT DISTINCT brand FROM vehicles_expanded WHERE fuel_type = ? ORDER BY brand",
                (fuel_type,)
            )
            brands = cursor.fetchall()
            return [b[0] for b in brands]
        else:
            brands = session.query(Vehicle.brand).filter(Vehicle.fuel_type == fuel_type).distinct().all()
            return [b[0] for b in brands]
    finally:
        session.close()

def get_models(fuel_type: str, brand: str, expanded=True):
    """Obtener modelos para un tipo de combustible y marca específicos"""
    session, is_expanded = get_database_session(expanded)

    try:
        if is_expanded:
            cursor = session.cursor()
            cursor.execute(
                "SELECT DISTINCT model FROM vehicles_expanded WHERE fuel_type = ? AND brand = ? ORDER BY model",
                (fuel_type, brand)
            )
            models = cursor.fetchall()
            return [m[0] for m in models]
        else:
            models = session.query(Vehicle.model).filter(
                Vehicle.fuel_type == fuel_type,
                Vehicle.brand == brand
            ).distinct().all()
            return [m[0] for m in models]
    finally:
        session.close()

def get_years(fuel_type: str, brand: str, model: str, expanded=True):
    """Obtener años para un tipo de combustible, marca y modelo específicos"""
    session, is_expanded = get_database_session(expanded)

    try:
        if is_expanded:
            cursor = session.cursor()
            cursor.execute(
                "SELECT DISTINCT year FROM vehicles_expanded WHERE fuel_type = ? AND brand = ? AND model = ? ORDER BY year DESC",
                (fuel_type, brand, model)
            )
            years = cursor.fetchall()
            return [y[0] for y in years]
        else:
            years = session.query(Vehicle.year).filter(
                Vehicle.fuel_type == fuel_type,
                Vehicle.brand == brand,
                Vehicle.model == model
            ).distinct().all()
            return [y[0] for y in years]
    finally:
        session.close()

def get_versions(fuel_type: str, brand: str, model: str, expanded=True):
    """Obtener versiones para una configuración específica de vehículo (sin año)"""
    session, is_expanded = get_database_session(expanded)

    try:
        if is_expanded:
            cursor = session.cursor()
            cursor.execute(
                """SELECT DISTINCT version FROM vehicles_expanded
                   WHERE fuel_type = ? AND brand = ? AND model = ?
                   ORDER BY version""",
                (fuel_type, brand, model)
            )
            versions = cursor.fetchall()
            return [v[0] for v in versions]
        else:
            versions = session.query(Vehicle.version).filter(
                Vehicle.fuel_type == fuel_type,
                Vehicle.brand == brand,
                Vehicle.model == model
            ).distinct().all()
            return [v[0] for v in versions]
    finally:
        session.close()

def get_vehicle_stats(expanded=True):
    """Obtener estadísticas de la base de datos de vehículos"""
    session, is_expanded = get_database_session(expanded)

    try:
        if is_expanded:
            cursor = session.cursor()

            # Estadísticas generales
            cursor.execute("SELECT COUNT(*) FROM vehicles_expanded")
            total = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(DISTINCT brand) FROM vehicles_expanded")
            brands = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(DISTINCT model) FROM vehicles_expanded")
            models = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(DISTINCT fuel_type) FROM vehicles_expanded")
            fuel_types = cursor.fetchone()[0]

            # Top marcas
            cursor.execute(
                "SELECT brand, COUNT(*) as count FROM vehicles_expanded GROUP BY brand ORDER BY count DESC LIMIT 10"
            )
            top_brands = cursor.fetchall()

            return {
                'total_vehicles': total,
                'total_brands': brands,
                'total_models': models,
                'total_fuel_types': fuel_types,
                'top_brands': top_brands,
                'database_type': 'expanded'
            }
        else:
            total = session.query(Vehicle).count()
            brands = session.query(Vehicle.brand).distinct().count()
            models = session.query(Vehicle.model).distinct().count()
            fuel_types = session.query(Vehicle.fuel_type).distinct().count()

            return {
                'total_vehicles': total,
                'total_brands': brands,
                'total_models': models,
                'total_fuel_types': fuel_types,
                'top_brands': [],
                'database_type': 'legacy'
            }
    finally:
        session.close()

def search_vehicles(search_term: str, expanded=True):
    """Buscar vehículos por término de búsqueda"""
    session, is_expanded = get_database_session(expanded)

    try:
        if is_expanded:
            cursor = session.cursor()
            cursor.execute(
                """SELECT DISTINCT brand, model, fuel_type FROM vehicles_expanded
                   WHERE brand LIKE ? OR model LIKE ?
                   ORDER BY brand, model
                   LIMIT 20""",
                (f'%{search_term}%', f'%{search_term}%')
            )
            results = cursor.fetchall()
            return [
                {
                    'brand': r[0],
                    'model': r[1],
                    'fuel_type': r[2]
                }
                for r in results
            ]
        else:
            results = session.query(Vehicle.brand, Vehicle.model, Vehicle.fuel_type).filter(
                (Vehicle.brand.like(f'%{search_term}%')) |
                (Vehicle.model.like(f'%{search_term}%'))
            ).distinct().limit(20).all()
            return [
                {
                    'brand': r[0],
                    'model': r[1],
                    'fuel_type': r[2]
                }
                for r in results
            ]
    finally:
        session.close()

def get_popular_vehicles(limit: int = 10, expanded=True):
    """Obtener vehículos populares (basados en cantidad de configuraciones)"""
    session, is_expanded = get_database_session(expanded)

    try:
        if is_expanded:
            cursor = session.cursor()
            cursor.execute(
                """SELECT brand, model, COUNT(*) as count
                   FROM vehicles_expanded
                   GROUP BY brand, model
                   ORDER BY count DESC
                   LIMIT ?""",
                (limit,)
            )
            results = cursor.fetchall()
            return [
                {
                    'brand': r[0],
                    'model': r[1],
                    'configurations': r[2]
                }
                for r in results
            ]
        else:
            # Para la base de datos legacy, agrupar por marca y modelo
            from sqlalchemy import func
            results = session.query(
                Vehicle.brand,
                Vehicle.model,
                func.count().label('count')
            ).group_by(Vehicle.brand, Vehicle.model).order_by(func.count().desc()).limit(limit).all()

            return [
                {
                    'brand': r[0],
                    'model': r[1],
                    'configurations': r[2]
                }
                for r in results
            ]
    finally:
        session.close()