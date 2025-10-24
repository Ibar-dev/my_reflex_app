from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fuel_type = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(String, nullable=False)
    version = Column(String, nullable=False)

class VehicleExpanded(Base):
    """Modelo expandido con datos adicionales de vehículos"""
    __tablename__ = "vehicles_expanded"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fuel_type = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(String, nullable=False)
    version = Column(String, nullable=False)
    transmission = Column(String, nullable=True)
    engine_displacement = Column(String, nullable=True)
    cylinders = Column(String, nullable=True)
    source = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now())
