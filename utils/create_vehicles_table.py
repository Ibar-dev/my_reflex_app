"""
Script para crear la tabla de vehículos en Supabase con datos de marcas españolas.
"""
import sys
import os

# Añadir el directorio raíz al path para importar utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.supabase_connection import db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SQL para crear la tabla de vehículos
CREATE_VEHICLES_TABLE = """
CREATE TABLE IF NOT EXISTS vehicles (
    id SERIAL PRIMARY KEY,
    fuel_type VARCHAR(50) NOT NULL CHECK (fuel_type IN ('Diesel', 'Gasolina')),
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(150) NOT NULL,
    version VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_fuel_type ON vehicles(fuel_type);
CREATE INDEX IF NOT EXISTS idx_brand ON vehicles(brand);
CREATE INDEX IF NOT EXISTS idx_model ON vehicles(model);

-- Índice compuesto para búsquedas combinadas
CREATE INDEX IF NOT EXISTS idx_fuel_brand_model ON vehicles(fuel_type, brand, model);
"""

# SQL para crear función de actualización automática de timestamp
CREATE_UPDATE_TRIGGER = """
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_vehicles_updated_at ON vehicles;

CREATE TRIGGER update_vehicles_updated_at
BEFORE UPDATE ON vehicles
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
"""


def create_vehicles_table():
    """Crea la tabla de vehículos en Supabase"""
    if not db.connect():
        logger.error("No se pudo conectar a la base de datos")
        return False
    
    try:
        # Crear tabla
        logger.info("📦 Creando tabla 'vehicles'...")
        db.execute_update(CREATE_VEHICLES_TABLE)
        
        # Crear trigger para updated_at
        logger.info("⚡ Creando trigger de actualización automática...")
        db.execute_update(CREATE_UPDATE_TRIGGER)
        
        logger.info("✅ Tabla 'vehicles' creada exitosamente")
        return True
    
    except Exception as e:
        logger.error(f"❌ Error al crear tabla: {e}")
        return False
    
    finally:
        db.disconnect()


def insert_sample_vehicles():
    """Inserta vehículos de marcas populares en España"""
    sample_vehicles = [
        # Diesel - Audi
        ('Diesel', 'Audi', 'A3', '2.0 TDI 150CV'),
        ('Diesel', 'Audi', 'A3', '2.0 TDI 184CV S-Tronic'),
        ('Diesel', 'Audi', 'A4', '2.0 TDI 150CV'),
        ('Diesel', 'Audi', 'A4', '2.0 TDI 190CV Quattro'),
        ('Diesel', 'Audi', 'Q3', '2.0 TDI 150CV'),
        ('Diesel', 'Audi', 'Q5', '2.0 TDI 204CV Quattro'),
        ('Diesel', 'Audi', 'Q5', '3.0 TDI 286CV Quattro'),
        
        # Diesel - BMW
        ('Diesel', 'BMW', 'Serie 1', '116d 116CV'),
        ('Diesel', 'BMW', 'Serie 1', '118d 150CV'),
        ('Diesel', 'BMW', 'Serie 3', '318d 150CV'),
        ('Diesel', 'BMW', 'Serie 3', '320d 190CV'),
        ('Diesel', 'BMW', 'Serie 5', '520d 190CV'),
        ('Diesel', 'BMW', 'X3', 'xDrive20d 190CV'),
        ('Diesel', 'BMW', 'X5', 'xDrive30d 265CV'),
        
        # Diesel - Mercedes-Benz
        ('Diesel', 'Mercedes-Benz', 'Clase A', 'A180d 116CV'),
        ('Diesel', 'Mercedes-Benz', 'Clase A', 'A200d 150CV'),
        ('Diesel', 'Mercedes-Benz', 'Clase C', 'C200d 160CV'),
        ('Diesel', 'Mercedes-Benz', 'Clase C', 'C220d 194CV'),
        ('Diesel', 'Mercedes-Benz', 'Clase E', 'E220d 194CV'),
        ('Diesel', 'Mercedes-Benz', 'GLC', '220d 4MATIC 194CV'),
        
        # Diesel - Volkswagen
        ('Diesel', 'Volkswagen', 'Golf', '2.0 TDI 115CV'),
        ('Diesel', 'Volkswagen', 'Golf', '2.0 TDI 150CV'),
        ('Diesel', 'Volkswagen', 'Passat', '2.0 TDI 150CV'),
        ('Diesel', 'Volkswagen', 'Passat', '2.0 TDI 190CV 4Motion'),
        ('Diesel', 'Volkswagen', 'Tiguan', '2.0 TDI 150CV'),
        ('Diesel', 'Volkswagen', 'Tiguan', '2.0 TDI 200CV 4Motion'),
        
        # Diesel - SEAT
        ('Diesel', 'SEAT', 'León', '1.6 TDI 115CV'),
        ('Diesel', 'SEAT', 'León', '2.0 TDI 150CV'),
        ('Diesel', 'SEAT', 'Ateca', '2.0 TDI 150CV'),
        ('Diesel', 'SEAT', 'Tarraco', '2.0 TDI 150CV'),
        
        # Diesel - Renault
        ('Diesel', 'Renault', 'Clio', 'dCi 85CV'),
        ('Diesel', 'Renault', 'Mégane', 'dCi 115CV'),
        ('Diesel', 'Renault', 'Captur', 'dCi 115CV'),
        ('Diesel', 'Renault', 'Kadjar', 'dCi 150CV'),
        
        # Diesel - Peugeot
        ('Diesel', 'Peugeot', '208', 'BlueHDi 100CV'),
        ('Diesel', 'Peugeot', '308', 'BlueHDi 130CV'),
        ('Diesel', 'Peugeot', '3008', 'BlueHDi 130CV'),
        ('Diesel', 'Peugeot', '5008', 'BlueHDi 130CV'),
        
        # Diesel - Ford
        ('Diesel', 'Ford', 'Focus', '1.5 TDCi 120CV'),
        ('Diesel', 'Ford', 'Kuga', '2.0 TDCi 150CV'),
        ('Diesel', 'Ford', 'Mondeo', '2.0 TDCi 180CV'),
        
        # Diesel - Opel
        ('Diesel', 'Opel', 'Astra', '1.5 Diesel 122CV'),
        ('Diesel', 'Opel', 'Insignia', '2.0 CDTI 170CV'),
        ('Diesel', 'Opel', 'Crossland', '1.5 Diesel 120CV'),
        
        # Gasolina - Audi
        ('Gasolina', 'Audi', 'A3', '1.0 TFSI 115CV'),
        ('Gasolina', 'Audi', 'A3', '1.5 TFSI 150CV'),
        ('Gasolina', 'Audi', 'A4', '2.0 TFSI 190CV'),
        ('Gasolina', 'Audi', 'Q3', '1.5 TFSI 150CV'),
        ('Gasolina', 'Audi', 'Q3', '2.0 TFSI 190CV Quattro'),
        ('Gasolina', 'Audi', 'Q5', '2.0 TFSI 252CV Quattro'),
        
        # Gasolina - BMW
        ('Gasolina', 'BMW', 'Serie 1', '118i 140CV'),
        ('Gasolina', 'BMW', 'Serie 1', '120i 178CV'),
        ('Gasolina', 'BMW', 'Serie 3', '318i 156CV'),
        ('Gasolina', 'BMW', 'Serie 3', '320i 184CV'),
        ('Gasolina', 'BMW', 'Serie 5', '520i 184CV'),
        ('Gasolina', 'BMW', 'X3', 'xDrive30i 252CV'),
        ('Gasolina', 'BMW', 'X5', 'xDrive40i 340CV'),
        
        # Gasolina - Mercedes-Benz
        ('Gasolina', 'Mercedes-Benz', 'Clase A', 'A180 136CV'),
        ('Gasolina', 'Mercedes-Benz', 'Clase A', 'A200 163CV'),
        ('Gasolina', 'Mercedes-Benz', 'Clase C', 'C200 184CV'),
        ('Gasolina', 'Mercedes-Benz', 'Clase E', 'E200 184CV'),
        ('Gasolina', 'Mercedes-Benz', 'GLA', 'GLA200 163CV'),
        ('Gasolina', 'Mercedes-Benz', 'GLC', 'GLC200 197CV'),
        
        # Gasolina - Volkswagen
        ('Gasolina', 'Volkswagen', 'Golf', '1.0 TSI 110CV'),
        ('Gasolina', 'Volkswagen', 'Golf', '1.5 TSI 130CV'),
        ('Gasolina', 'Volkswagen', 'Golf', '2.0 TSI 245CV GTI'),
        ('Gasolina', 'Volkswagen', 'Passat', '1.5 TSI 150CV'),
        ('Gasolina', 'Volkswagen', 'Tiguan', '1.5 TSI 150CV'),
        ('Gasolina', 'Volkswagen', 'T-Roc', '1.0 TSI 115CV'),
        
        # Gasolina - SEAT
        ('Gasolina', 'SEAT', 'Ibiza', '1.0 TSI 95CV'),
        ('Gasolina', 'SEAT', 'Ibiza', '1.0 TSI 110CV'),
        ('Gasolina', 'SEAT', 'León', '1.0 TSI 110CV'),
        ('Gasolina', 'SEAT', 'León', '1.5 TSI 130CV'),
        ('Gasolina', 'SEAT', 'León', '2.0 TSI 300CV Cupra'),
        ('Gasolina', 'SEAT', 'Ateca', '1.5 TSI 150CV'),
        ('Gasolina', 'SEAT', 'Arona', '1.0 TSI 110CV'),
        
        # Gasolina - Renault
        ('Gasolina', 'Renault', 'Clio', 'TCe 90CV'),
        ('Gasolina', 'Renault', 'Clio', 'TCe 100CV'),
        ('Gasolina', 'Renault', 'Mégane', 'TCe 140CV'),
        ('Gasolina', 'Renault', 'Captur', 'TCe 130CV'),
        ('Gasolina', 'Renault', 'Kadjar', 'TCe 140CV'),
        
        # Gasolina - Peugeot
        ('Gasolina', 'Peugeot', '208', 'PureTech 100CV'),
        ('Gasolina', 'Peugeot', '208', 'PureTech 130CV'),
        ('Gasolina', 'Peugeot', '308', 'PureTech 130CV'),
        ('Gasolina', 'Peugeot', '3008', 'PureTech 130CV'),
        ('Gasolina', 'Peugeot', '3008', 'PureTech 180CV'),
        ('Gasolina', 'Peugeot', '5008', 'PureTech 130CV'),
        
        # Gasolina - Ford
        ('Gasolina', 'Ford', 'Fiesta', '1.0 EcoBoost 100CV'),
        ('Gasolina', 'Ford', 'Focus', '1.0 EcoBoost 125CV'),
        ('Gasolina', 'Ford', 'Focus', '1.5 EcoBoost 150CV'),
        ('Gasolina', 'Ford', 'Puma', '1.0 EcoBoost 125CV'),
        ('Gasolina', 'Ford', 'Kuga', '1.5 EcoBoost 150CV'),
        
        # Gasolina - Opel
        ('Gasolina', 'Opel', 'Corsa', '1.2 Turbo 100CV'),
        ('Gasolina', 'Opel', 'Astra', '1.2 Turbo 130CV'),
        ('Gasolina', 'Opel', 'Crossland', '1.2 Turbo 110CV'),
        ('Gasolina', 'Opel', 'Mokka', '1.2 Turbo 130CV'),
        
        # Gasolina - Toyota
        ('Gasolina', 'Toyota', 'Yaris', '1.5 VVTi 125CV'),
        ('Gasolina', 'Toyota', 'Corolla', '1.8 VVTi 122CV'),
        ('Gasolina', 'Toyota', 'C-HR', '1.8 VVTi 122CV'),
        ('Gasolina', 'Toyota', 'RAV4', '2.5 VVTi 178CV'),
        
        # Gasolina - Honda
        ('Gasolina', 'Honda', 'Civic', '1.0 VTEC Turbo 129CV'),
        ('Gasolina', 'Honda', 'Civic', '1.5 VTEC Turbo 182CV'),
        ('Gasolina', 'Honda', 'CR-V', '1.5 VTEC Turbo 193CV'),
        
        # Gasolina - Nissan
        ('Gasolina', 'Nissan', 'Micra', '1.0 IG-T 100CV'),
        ('Gasolina', 'Nissan', 'Qashqai', '1.3 DIG-T 140CV'),
        ('Gasolina', 'Nissan', 'X-Trail', '1.3 DIG-T 160CV'),
        
        # Gasolina - Hyundai
        ('Gasolina', 'Hyundai', 'i20', '1.0 T-GDi 100CV'),
        ('Gasolina', 'Hyundai', 'i30', '1.0 T-GDi 120CV'),
        ('Gasolina', 'Hyundai', 'Tucson', '1.6 T-GDi 150CV'),
        ('Gasolina', 'Hyundai', 'Kona', '1.0 T-GDi 120CV'),
        
        # Gasolina - Kia
        ('Gasolina', 'Kia', 'Rio', '1.0 T-GDi 100CV'),
        ('Gasolina', 'Kia', 'Ceed', '1.0 T-GDi 120CV'),
        ('Gasolina', 'Kia', 'Sportage', '1.6 T-GDi 150CV'),
        ('Gasolina', 'Kia', 'Niro', '1.6 GDi 141CV'),
    ]
    
    if not db.connect():
        logger.error("No se pudo conectar a la base de datos")
        return False
    
    try:
        insert_query = """
        INSERT INTO vehicles (fuel_type, brand, model, version)
        VALUES (%s, %s, %s, %s);
        """
        
        logger.info(f"📝 Insertando {len(sample_vehicles)} vehículos...")
        
        count = 0
        for vehicle in sample_vehicles:
            if db.execute_update(insert_query, vehicle):
                count += 1
        
        logger.info(f"✅ {count} vehículos insertados correctamente")
        return True
    
    except Exception as e:
        logger.error(f"❌ Error al insertar vehículos: {e}")
        return False
    
    finally:
        db.disconnect()


def main():
    """Función principal"""
    print("\n" + "=" * 60)
    print("🚀 INICIALIZANDO BASE DE DATOS DE VEHÍCULOS EN SUPABASE")
    print("=" * 60)
    
    # Crear tabla
    print("\n1️⃣ Creando tabla de vehículos...")
    if create_vehicles_table():
        print("✅ Tabla creada exitosamente")
        
        # Insertar datos de ejemplo
        print("\n2️⃣ ¿Deseas insertar vehículos de ejemplo?")
        response = input("   Escribe 's' para continuar o 'n' para saltar: ").lower()
        
        if response == 's':
            print("\n   Insertando vehículos...")
            if insert_sample_vehicles():
                print("✅ Vehículos insertados exitosamente")
            else:
                print("❌ Error al insertar vehículos")
        else:
            print("⏭️  Saltando inserción de vehículos")
    else:
        print("❌ Error al crear la tabla")
    
    print("\n" + "=" * 60)
    print("🎉 PROCESO COMPLETADO")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
