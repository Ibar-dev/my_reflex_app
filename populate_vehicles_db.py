from utils.database_service import SessionLocal, init_db
from models.vehicle import Vehicle

# Inicializar la base de datos y sesión
init_db()
session = SessionLocal()

# Datos reales de ejemplo
vehiculos = [
    Vehicle(fuel_type="gasolina", brand="BMW", model="Serie 3", year="2021", version="M340i"),
    Vehicle(fuel_type="gasolina", brand="BMW", model="Serie 3", year="2023", version="M340i"),
    Vehicle(fuel_type="diesel", brand="BMW", model="Serie 3", year="2021", version="320d"),
    Vehicle(fuel_type="gasolina", brand="Volkswagen", model="Golf", year="2023", version="GTI"),
    Vehicle(fuel_type="gasolina", brand="Volkswagen", model="Golf", year="2021", version="GTI"),
    Vehicle(fuel_type="diesel", brand="Volkswagen", model="Golf", year="2021", version="TDI"),
    Vehicle(fuel_type="gasolina", brand="Toyota", model="Corolla", year="2023", version="Hybrid"),
    Vehicle(fuel_type="gasolina", brand="Toyota", model="Corolla", year="2021", version="Hybrid"),
    Vehicle(fuel_type="diesel", brand="Toyota", model="Corolla", year="2021", version="D-4D"),
]

# Insertar datos si la tabla está vacía
if session.query(Vehicle).count() == 0:
    session.add_all(vehiculos)
    session.commit()

session.close()
print("Base de datos de vehículos poblada con datos reales.")
