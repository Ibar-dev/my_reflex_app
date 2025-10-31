#!/usr/bin/env python3
"""
Script para crear base de datos local de vehículos con datos de prueba
adaptados al flujo: combustible → marca → modelo → versión
"""

import sqlite3
import os
from pathlib import Path

def create_local_vehicle_db():
    """Crear base de datos local con datos de vehículos de prueba"""

    # Ruta de la base de datos local
    db_path = Path(__file__).parent / "vehicles_local.db"

    # Eliminar base de datos anterior si existe
    if db_path.exists():
        os.remove(db_path)
        print(f"Eliminada base de datos anterior: {db_path}")

    # Crear conexión
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Crear tabla de vehículos
    cursor.execute('''
        CREATE TABLE vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fuel_type TEXT NOT NULL,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            year TEXT NOT NULL,
            version TEXT NOT NULL
        )
    ''')

    # Datos de ejemplo - estructura jerárquica
    vehicles_data = [
        # Diesel
        ("diesel", "Audi", "A3", "2020", "1.6 TDI 115 CV"),
        ("diesel", "Audi", "A3", "2020", "2.0 TDI 150 CV"),
        ("diesel", "Audi", "A3", "2021", "1.6 TDI 115 CV"),
        ("diesel", "Audi", "A4", "2020", "2.0 TDI 150 CV"),
        ("diesel", "Audi", "A4", "2020", "2.0 TDI 190 CV"),
        ("diesel", "Audi", "A6", "2021", "2.0 TDI 204 CV"),
        ("diesel", "Audi", "Q3", "2020", "2.0 TDI 150 CV"),
        ("diesel", "Audi", "Q5", "2021", "2.0 TDI 204 CV"),

        ("diesel", "BMW", "Serie 1", "2020", "118d 116 CV"),
        ("diesel", "BMW", "Serie 1", "2021", "118d 116 CV"),
        ("diesel", "BMW", "Serie 3", "2020", "320d 190 CV"),
        ("diesel", "BMW", "Serie 3", "2020", "330d 265 CV"),
        ("diesel", "BMW", "Serie 5", "2021", "520d 190 CV"),
        ("diesel", "BMW", "Serie 5", "2021", "530d 286 CV"),
        ("diesel", "BMW", "X1", "2020", "sDrive18d 116 CV"),
        ("diesel", "BMW", "X3", "2021", "xDrive20d 190 CV"),

        ("diesel", "Mercedes-Benz", "Clase A", "2020", "A 180 d 116 CV"),
        ("diesel", "Mercedes-Benz", "Clase A", "2021", "A 180 d 116 CV"),
        ("diesel", "Mercedes-Benz", "Clase C", "2020", "C 200 d 160 CV"),
        ("diesel", "Mercedes-Benz", "Clase C", "2020", "C 220 d 194 CV"),
        ("diesel", "Mercedes-Benz", "Clase E", "2021", "E 200 d 160 CV"),
        ("diesel", "Mercedes-Benz", "Clase E", "2021", "E 220 d 194 CV"),
        ("diesel", "Mercedes-Benz", "GLA", "2020", "180 d 116 CV"),
        ("diesel", "Mercedes-Benz", "GLC", "2021", "220 d 194 CV"),

        ("diesel", "Volkswagen", "Golf", "2020", "1.6 TDI 115 CV"),
        ("diesel", "Volkswagen", "Golf", "2021", "2.0 TDI 150 CV"),
        ("diesel", "Volkswagen", "Polo", "2020", "1.6 TDI 80 CV"),
        ("diesel", "Volkswagen", "Polo", "2021", "1.6 TDI 95 CV"),
        ("diesel", "Volkswagen", "Passat", "2020", "2.0 TDI 150 CV"),
        ("diesel", "Volkswagen", "Passat", "2021", "2.0 TDI 190 CV"),
        ("diesel", "Volkswagen", "Tiguan", "2020", "2.0 TDI 150 CV"),
        ("diesel", "Volkswagen", "Tiguan", "2021", "2.0 TDI 190 CV"),

        ("diesel", "Seat", "León", "2020", "1.6 TDI 115 CV"),
        ("diesel", "Seat", "León", "2021", "2.0 TDI 150 CV"),
        ("diesel", "Seat", "Ibiza", "2020", "1.6 TDI 80 CV"),
        ("diesel", "Seat", "Ibiza", "2021", "1.6 TDI 95 CV"),
        ("diesel", "Seat", "Ateca", "2020", "2.0 TDI 150 CV"),
        ("diesel", "Seat", "Ateca", "2021", "2.0 TDI 190 CV"),

        ("diesel", "Skoda", "Octavia", "2020", "2.0 TDI 150 CV"),
        ("diesel", "Skoda", "Octavia", "2021", "2.0 TDI 190 CV"),
        ("diesel", "Skoda", "Fabia", "2020", "1.6 TDI 80 CV"),
        ("diesel", "Skoda", "Fabia", "2021", "1.6 TDI 95 CV"),
        ("diesel", "Skoda", "Kodiaq", "2020", "2.0 TDI 150 CV"),
        ("diesel", "Skoda", "Kodiaq", "2021", "2.0 TDI 190 CV"),

        ("diesel", "Renault", "Clio", "2020", "1.5 dCi 85 CV"),
        ("diesel", "Renault", "Clio", "2021", "1.5 dCi 115 CV"),
        ("diesel", "Renault", "Megane", "2020", "1.5 dCi 115 CV"),
        ("diesel", "Renault", "Megane", "2021", "1.5 dCi 140 CV"),
        ("diesel", "Renault", "Captur", "2020", "1.5 dCi 90 CV"),
        ("diesel", "Renault", "Captur", "2021", "1.5 dCi 115 CV"),

        # Gasolina
        ("gasolina", "Audi", "A3", "2020", "1.0 TFSI 110 CV"),
        ("gasolina", "Audi", "A3", "2021", "1.5 TFSI 150 CV"),
        ("gasolina", "Audi", "A4", "2020", "1.4 TFSI 150 CV"),
        ("gasolina", "Audi", "A4", "2021", "2.0 TFSI 190 CV"),
        ("gasolina", "Audi", "A6", "2021", "2.0 TFSI 204 CV"),
        ("gasolina", "Audi", "Q3", "2020", "1.5 TFSI 150 CV"),
        ("gasolina", "Audi", "Q5", "2021", "2.0 TFSI 204 CV"),

        ("gasolina", "BMW", "Serie 1", "2020", "118i 140 CV"),
        ("gasolina", "BMW", "Serie 1", "2021", "118i 140 CV"),
        ("gasolina", "BMW", "Serie 3", "2020", "320i 184 CV"),
        ("gasolina", "BMW", "Serie 3", "2021", "330i 258 CV"),
        ("gasolina", "BMW", "Serie 5", "2021", "520i 184 CV"),
        ("gasolina", "BMW", "Serie 5", "2021", "530i 252 CV"),
        ("gasolina", "BMW", "X1", "2020", "sDrive18i 140 CV"),
        ("gasolina", "BMW", "X3", "2021", "xDrive20i 184 CV"),

        ("gasolina", "Mercedes-Benz", "Clase A", "2020", "A 180 136 CV"),
        ("gasolina", "Mercedes-Benz", "Clase A", "2021", "A 200 163 CV"),
        ("gasolina", "Mercedes-Benz", "Clase C", "2020", "C 180 156 CV"),
        ("gasolina", "Mercedes-Benz", "Clase C", "2021", "C 200 184 CV"),
        ("gasolina", "Mercedes-Benz", "Clase E", "2021", "E 200 184 CV"),
        ("gasolina", "Mercedes-Benz", "Clase E", "2021", "E 300 245 CV"),
        ("gasolina", "Mercedes-Benz", "GLA", "2020", "180 136 CV"),
        ("gasolina", "Mercedes-Benz", "GLC", "2021", "200 184 CV"),

        ("gasolina", "Volkswagen", "Golf", "2020", "1.0 TSI 110 CV"),
        ("gasolina", "Volkswagen", "Golf", "2021", "1.5 TSI 150 CV"),
        ("gasolina", "Volkswagen", "Polo", "2020", "1.0 TSI 80 CV"),
        ("gasolina", "Volkswagen", "Polo", "2021", "1.0 TSI 95 CV"),
        ("gasolina", "Volkswagen", "Passat", "2020", "1.5 TSI 150 CV"),
        ("gasolina", "Volkswagen", "Passat", "2021", "2.0 TSI 190 CV"),
        ("gasolina", "Volkswagen", "Tiguan", "2020", "1.5 TSI 150 CV"),
        ("gasolina", "Volkswagen", "Tiguan", "2021", "2.0 TSI 190 CV"),

        # Híbrido
        ("hibrido", "Toyota", "Prius", "2020", "1.8 Hybrid 122 CV"),
        ("hibrido", "Toyota", "Prius", "2021", "1.8 Hybrid 122 CV"),
        ("hibrido", "Toyota", "Corolla", "2020", "1.8 Hybrid 122 CV"),
        ("hibrido", "Toyota", "Corolla", "2021", "1.8 Hybrid 122 CV"),
        ("hibrido", "Toyota", "RAV4", "2020", "2.5 Hybrid 222 CV"),
        ("hibrido", "Toyota", "RAV4", "2021", "2.5 Hybrid 222 CV"),
        ("hibrido", "Toyota", "Yaris", "2020", "1.5 Hybrid 116 CV"),
        ("hibrido", "Toyota", "Yaris", "2021", "1.5 Hybrid 116 CV"),

        ("hibrido", "Hyundai", "Ioniq", "2020", "1.6 GDI Hybrid 141 CV"),
        ("hibrido", "Hyundai", "Ioniq", "2021", "1.6 GDI Hybrid 141 CV"),
        ("hibrido", "Hyundai", "Kona", "2020", "1.6 GDI Hybrid 141 CV"),
        ("hibrido", "Hyundai", "Kona", "2021", "1.6 GDI Hybrid 141 CV"),
        ("hibrido", "Hyundai", "Tucson", "2020", "1.6 GDI Hybrid 230 CV"),
        ("hibrido", "Hyundai", "Tucson", "2021", "1.6 GDI Hybrid 230 CV"),

        # Eléctrico
        ("electrico", "Tesla", "Model 3", "2020", "Standard Range Plus"),
        ("electrico", "Tesla", "Model 3", "2021", "Long Range AWD"),
        ("electrico", "Tesla", "Model Y", "2020", "Long Range AWD"),
        ("electrico", "Tesla", "Model Y", "2021", "Performance"),
        ("electrico", "Nissan", "Leaf", "2020", "40 kWh 150 CV"),
        ("electrico", "Nissan", "Leaf", "2021", "62 kWh 160 CV"),
        ("electrico", "Renault", "Zoe", "2020", "R110 110 CV"),
        ("electrico", "Renault", "Zoe", "2021", "R135 135 CV"),
        ("electrico", "Hyundai", "Kona Electric", "2020", "39 kWh 136 CV"),
        ("electrico", "Hyundai", "Kona Electric", "2021", "64 kWh 204 CV"),
    ]

    # Insertar datos
    cursor.executemany('''
        INSERT INTO vehicles (fuel_type, brand, model, year, version)
        VALUES (?, ?, ?, ?, ?)
    ''', vehicles_data)

    # Confirmar cambios
    conn.commit()

    # Verificar datos insertados
    cursor.execute("SELECT COUNT(*) FROM vehicles")
    total_vehicles = cursor.fetchone()[0]

    cursor.execute("SELECT DISTINCT fuel_type FROM vehicles")
    fuel_types = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT brand FROM vehicles")
    brands = [row[0] for row in cursor.fetchall()]

    print(f"Base de datos local creada exitosamente: {db_path}")
    print(f"Total vehículos: {total_vehicles}")
    print(f"Tipos combustible: {fuel_types}")
    print(f"Total marcas: {len(brands)}")

    # Mostrar estructura por tipo de combustible
    for fuel_type in fuel_types:
        cursor.execute("SELECT DISTINCT brand FROM vehicles WHERE fuel_type = ? ORDER BY brand", (fuel_type,))
        brands_fuel = [row[0] for row in cursor.fetchall()]
        print(f"\n{fuel_type.upper()}: {len(brands_fuel)} marcas")
        for brand in brands_fuel:
            cursor.execute("SELECT DISTINCT model FROM vehicles WHERE fuel_type = ? AND brand = ? ORDER BY model", (fuel_type, brand))
            models = [row[0] for row in cursor.fetchall()]
            print(f"   {brand}: {len(models)} modelos")
            cursor.execute("SELECT COUNT(*) FROM vehicles WHERE fuel_type = ? AND brand = ?", (fuel_type, brand))
            count = cursor.fetchone()[0]
            print(f"      ({count} versiones totales)")

    conn.close()
    print(f"\nBase de datos lista para usar: {db_path}")

    return str(db_path)

if __name__ == "__main__":
    create_local_vehicle_db()