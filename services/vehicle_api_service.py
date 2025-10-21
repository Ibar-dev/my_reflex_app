
from utils.database_service import SessionLocal
from models.vehicle import Vehicle

def get_fuel_types():
    session = SessionLocal()
    types = session.query(Vehicle.fuel_type).distinct().all()
    session.close()
    return [t[0] for t in types]

def get_brands(fuel_type):
    session = SessionLocal()
    brands = session.query(Vehicle.brand).filter(Vehicle.fuel_type == fuel_type).distinct().all()
    session.close()
    return [b[0] for b in brands]

def get_models(fuel_type, brand):
    session = SessionLocal()
    models = session.query(Vehicle.model).filter(Vehicle.fuel_type == fuel_type, Vehicle.brand == brand).distinct().all()
    session.close()
    return [m[0] for m in models]

def get_years(fuel_type, brand, model):
    session = SessionLocal()
    years = session.query(Vehicle.year).filter(Vehicle.fuel_type == fuel_type, Vehicle.brand == brand, Vehicle.model == model).distinct().all()
    session.close()
    return [y[0] for y in years]

def get_versions(fuel_type, brand, model, year):
    session = SessionLocal()
    versions = session.query(Vehicle.version).filter(Vehicle.fuel_type == fuel_type, Vehicle.brand == brand, Vehicle.model == model, Vehicle.year == year).distinct().all()
    session.close()
    return [v[0] for v in versions]