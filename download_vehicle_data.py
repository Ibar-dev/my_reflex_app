#!/usr/bin/env python3
"""
Script para descargar y procesar datos de vehículos desde múltiples fuentes
========================================================================

Fuentes de datos:
1. NHTSA API (https://vpic.nhtsa.dot.gov/api/) - Fabricantes y modelos
2. FuelEconomy.gov CSV - Datos técnicos y consumo
3. Datos generales combinados

Uso: python download_vehicle_data.py
"""

import requests
import pandas as pd
import json
import time
import os
import sqlite3
from typing import List, Dict, Optional
from urllib.parse import urljoin
import zipfile
import io
from datetime import datetime

# Configuración
NHTSA_API_BASE = "https://vpic.nhtsa.dot.gov/api/"
FUEL_ECONOMY_URL = "https://www.fueleconomy.gov/feg/epadata/vehicles.csv.zip"
DATA_DIR = "data"
VEHICLE_DB = "vehicles_expanded.db"
CACHE_DURATION = 30  # días

class VehicleDataDownloader:
    """Descargador y procesador de datos de vehículos"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; VehicleDataBot/1.0)'
        })

        # Crear directorio de datos
        os.makedirs(DATA_DIR, exist_ok=True)

        # Tipos de combustible estándar
        self.fuel_types = {
            'Gasoline': 'gasolina',
            'Diesel': 'diesel',
            'Electric': 'electrico',
            'Hybrid': 'hibrido',
            'E85': 'etanol',
            'Natural Gas': 'gas_natural',
            'Propane': 'propano'
        }

    def log(self, message: str):
        """Función de logging"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    def download_nhtsa_manufacturers(self) -> List[Dict]:
        """Descargar lista de fabricantes desde NHTSA API"""
        self.log("Descargando fabricantes desde NHTSA API...")

        try:
            url = urljoin(NHTSA_API_BASE, "GetAllMakes?format=json")
            response = self.session.get(url)
            response.raise_for_status()

            data = response.json()
            manufacturers = data.get('Results', [])

            # Filtrar fabricantes relevantes (excluir motos, camiones pesados, etc.)
            relevant_manufacturers = []
            exclude_keywords = ['motorcycle', 'truck', 'bus', 'trailer', 'engine']

            for mfg in manufacturers:
                make_name = mfg.get('Make_Name', '').upper()

                # Incluir solo fabricantes de coches relevantes
                if not any(keyword.lower() in make_name.lower() for keyword in exclude_keywords):
                    if len(make_name) > 1:  # Excluir entradas de una sola letra
                        relevant_manufacturers.append({
                            'make_id': mfg.get('Make_ID'),
                            'make_name': mfg.get('Make_Name'),
                            'make_name_clean': self.clean_manufacturer_name(mfg.get('Make_Name', ''))
                        })

            self.log(f"Descargados {len(relevant_manufacturers)} fabricantes relevantes")
            return relevant_manufacturers

        except Exception as e:
            self.log(f"Error descargando fabricantes: {str(e)}")
            return []

    def download_nhtsa_models_for_make(self, make_name: str) -> List[Dict]:
        """Descargar modelos para un fabricante específico"""
        try:
            url = urljoin(NHTSA_API_BASE, f"GetModelsForMake/{make_name}?format=json")
            response = self.session.get(url)
            response.raise_for_status()

            data = response.json()
            models = data.get('Results', [])

            cleaned_models = []
            for model in models:
                model_name = model.get('Model_Name', '').strip()
                if model_name and len(model_name) > 1:
                    cleaned_models.append({
                        'make_name': make_name,
                        'model_name': model_name,
                        'model_name_clean': self.clean_model_name(model_name)
                    })

            return cleaned_models

        except Exception as e:
            self.log(f"Error descargando modelos para {make_name}: {str(e)}")
            return []

    def download_fuel_economy_data(self) -> pd.DataFrame:
        """Descargar datos de consumo de combustible"""
        self.log("Descargando datos de Fuel Economy...")

        try:
            response = self.session.get(FUEL_ECONOMY_URL)
            response.raise_for_status()

            # Extraer ZIP del contenido
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
                csv_file = zip_file.namelist()[0]  # Generalmente 'vehicles.csv'
                with zip_file.open(csv_file) as csv_data:
                    df = pd.read_csv(csv_data, low_memory=False)

            self.log(f"Descargados {len(df)} registros de Fuel Economy")
            return df

        except Exception as e:
            self.log(f"Error descargando datos de Fuel Economy: {str(e)}")
            return pd.DataFrame()

    def clean_manufacturer_name(self, name: str) -> str:
        """Limpiar y estandarizar nombre de fabricante"""
        if not name:
            return ""

        # Eliminar caracteres especiales y estandarizar
        clean_name = name.strip().title()

        # Reemplazos comunes
        replacements = {
            'Aston Martin': 'Aston-Martin',
            'Mercedes-Benz': 'Mercedes-Benz',
            'Alfa Romeo': 'Alfa-Romeo',
            'Land Rover': 'Land-Rover',
        }

        return replacements.get(clean_name, clean_name)

    def clean_model_name(self, name: str) -> str:
        """Limpiar y estandarizar nombre de modelo"""
        if not name:
            return ""

        clean_name = name.strip().title()

        # Eliminar sufijos comunes que no son parte del modelo base
        suffixes_to_remove = [
            ' (Electric)', ' (Hybrid)', ' (Plug-in Hybrid)',
            ' EV', ' Hybrid', ' PHEV', ' Electric'
        ]

        for suffix in suffixes_to_remove:
            if clean_name.endswith(suffix):
                clean_name = clean_name[:-len(suffix)].strip()

        return clean_name

    def extract_fuel_type(self, fuel_type_raw: str) -> str:
        """Extraer y estandarizar tipo de combustible"""
        if pd.isna(fuel_type_raw) or not fuel_type_raw:
            return "gasolina"  # Por defecto

        fuel_type_str = str(fuel_type_raw).lower()

        # Mapeo de tipos de combustible
        for eng_type, spa_type in self.fuel_types.items():
            if eng_type.lower() in fuel_type_str:
                return spa_type

        # Heurísticas adicionales
        if any(x in fuel_type_str for x in ['gas', 'regular', 'premium']):
            return 'gasolina'
        elif any(x in fuel_type_str for x in ['diesel']):
            return 'diesel'
        elif any(x in fuel_type_str for x in ['electric', 'ev']):
            return 'electrico'
        elif any(x in fuel_type_str for x in ['hybrid', 'hev']):
            return 'hibrido'
        elif any(x in fuel_type_str for x in ['plug-in', 'phev']):
            return 'hibrido'

        return 'gasolina'  # Por defecto

    def process_fuel_economy_data(self, df: pd.DataFrame) -> List[Dict]:
        """Procesar datos de Fuel Economy al formato estándar"""
        if df.empty:
            return []

        processed_vehicles = []

        # Columnas relevantes en el dataset de Fuel Economy
        required_columns = ['make', 'model', 'year', 'fuelType', 'trany', 'displ', 'cylinders']
        available_columns = [col for col in required_columns if col in df.columns]

        self.log(f"Procesando datos de {len(df)} vehículos...")

        for _, row in df.iterrows():
            try:
                make = str(row.get('make', '')).strip()
                model = str(row.get('model', '')).strip()
                year = str(row.get('year', '')).strip()
                fuel_type_raw = str(row.get('fuelType', '')).strip()

                if not all([make, model, year]):
                    continue

                # Procesar datos
                fuel_type = self.extract_fuel_type(fuel_type_raw)
                transmission = str(row.get('trany', '')).strip()
                displacement = str(row.get('displ', '')).strip()
                cylinders = str(row.get('cylinders', '')).strip()

                # Crear versión/descripción
                version_parts = []
                if transmission and transmission != 'Auto' and transmission != 'Manual':
                    version_parts.append(transmission)
                if displacement and displacement != 'nan':
                    version_parts.append(f"{displacement}L")
                if cylinders and cylinders != 'nan':
                    version_parts.append(f"{cylinders} Cyl")

                version = ' '.join(version_parts) if version_parts else 'Base'

                vehicle_data = {
                    'fuel_type': fuel_type,
                    'brand': make.title(),
                    'model': model.title(),
                    'year': year,
                    'version': version,
                    'transmission': transmission,
                    'engine_displacement': displacement,
                    'cylinders': cylinders,
                    'source': 'fuel_economy'
                }

                processed_vehicles.append(vehicle_data)

            except Exception as e:
                continue  # Saltar registros problemáticos

        self.log(f"Procesados {len(processed_vehicles)} vehículos válidos")
        return processed_vehicles

    def create_expanded_database(self, vehicles_data: List[Dict]):
        """Crear base de datos expandida"""
        self.log(f"Creando base de datos expandida con {len(vehicles_data)} vehículos...")

        # Conectar a la base de datos
        conn = sqlite3.connect(VEHICLE_DB)
        cursor = conn.cursor()

        # Crear tabla con estructura expandida
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicles_expanded (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fuel_type TEXT NOT NULL,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                year TEXT NOT NULL,
                version TEXT NOT NULL,
                transmission TEXT,
                engine_displacement TEXT,
                cylinders TEXT,
                source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(fuel_type, brand, model, year, version)
            )
        ''')

        # Insertar datos
        inserted_count = 0
        for vehicle in vehicles_data:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO vehicles_expanded
                    (fuel_type, brand, model, year, version, transmission,
                     engine_displacement, cylinders, source)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    vehicle['fuel_type'],
                    vehicle['brand'],
                    vehicle['model'],
                    vehicle['year'],
                    vehicle['version'],
                    vehicle.get('transmission', ''),
                    vehicle.get('engine_displacement', ''),
                    vehicle.get('cylinders', ''),
                    vehicle.get('source', 'unknown')
                ))

                if cursor.rowcount > 0:
                    inserted_count += 1

            except Exception as e:
                continue

        conn.commit()
        conn.close()

        self.log(f"Insertados {inserted_count} vehículos nuevos en la base de datos")

        # Crear índices para mejor rendimiento
        conn = sqlite3.connect(VEHICLE_DB)
        cursor = conn.cursor()

        cursor.execute('CREATE INDEX IF NOT EXISTS idx_fuel_type ON vehicles_expanded(fuel_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_brand ON vehicles_expanded(brand)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_brand_fuel ON vehicles_expanded(brand, fuel_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_model ON vehicles_expanded(model)')

        conn.commit()
        conn.close()

        self.log("Índices creados correctamente")

    def generate_sample_data(self):
        """Generar datos de muestra combinando información"""
        self.log("Generando datos de muestra combinados...")

        # Fabricantes populares para reprogramación ECU
        popular_brands = [
            'Audi', 'BMW', 'Mercedes-Benz', 'Porsche', 'Volkswagen',
            'Ford', 'Chevrolet', 'Toyota', 'Honda', 'Nissan',
            'Hyundai', 'Kia', 'Subaru', 'Mazda', 'Volvo'
        ]

        sample_vehicles = []

        for brand in popular_brands:
            # Modelos populares por marca
            brand_models = self.get_popular_models_for_brand(brand)

            for model in brand_models:
                # Generar datos para diferentes años
                for year in range(2018, 2025):
                    # Combustibles comunes por marca/modelo
                    fuel_types = self.get_fuel_types_for_brand_model(brand, model)

                    for fuel_type in fuel_types:
                        # Versiones comunes
                        versions = self.get_common_versions(fuel_type, brand, model)

                        for version in versions:
                            sample_vehicles.append({
                                'fuel_type': fuel_type,
                                'brand': brand,
                                'model': model,
                                'year': str(year),
                                'version': version,
                                'source': 'generated'
                            })

        self.log(f"Generados {len(sample_vehicles)} vehículos de muestra")
        return sample_vehicles

    def get_popular_models_for_brand(self, brand: str) -> List[str]:
        """Obtener modelos populares para una marca"""
        models_map = {
            'Audi': ['A3', 'A4', 'A5', 'A6', 'Q3', 'Q5', 'Q7', 'TT'],
            'BMW': ['Serie 1', 'Serie 2', 'Serie 3', 'Serie 4', 'Serie 5', 'X1', 'X3', 'X5'],
            'Mercedes-Benz': ['Clase A', 'Clase C', 'Clase E', 'Clase S', 'GLA', 'GLC', 'GLE'],
            'Porsche': ['911', 'Cayenne', 'Macan', 'Panamera', 'Taycan'],
            'Volkswagen': ['Golf', 'Polo', 'Passat', 'Tiguan', 'T-Roc', 'Arteon'],
            'Ford': ['Fiesta', 'Focus', 'Mondeo', 'Kuga', 'Puma', 'Mustang'],
            'Chevrolet': ['Camaro', 'Corvette', 'Spark', 'Aveo', 'Trax'],
            'Toyota': ['Corolla', 'Yaris', 'RAV4', 'Hilux', 'Prius'],
            'Honda': ['Civic', 'Accord', 'CR-V', 'HR-V', 'Fit'],
            'Nissan': ['Qashqai', 'Juke', 'Leaf', 'X-Trail', 'Micra'],
            'Hyundai': ['Tucson', 'Santa Fe', 'i30', 'i10', 'Kona'],
            'Kia': ['Sportage', 'Sorento', 'Rio', 'Picanto', 'Stinger'],
            'Subaru': ['Impreza', 'Forester', 'Outback', 'XV', 'WRX'],
            'Mazda': ['Mazda 2', 'Mazda 3', 'Mazda 6', 'CX-3', 'CX-5'],
            'Volvo': ['XC40', 'XC60', 'XC90', 'S60', 'V60']
        }

        return models_map.get(brand, ['Model Base'])

    def get_fuel_types_for_brand_model(self, brand: str, model: str) -> List[str]:
        """Obtener tipos de combustible comunes para marca/modelo"""
        fuel_types = ['gasolina']

        # Marcas con diesel común
        if brand in ['Volkswagen', 'Audi', 'BMW', 'Mercedes-Benz', 'Ford', 'Renault']:
            fuel_types.append('diesel')

        # Modelos híbridos populares
        hybrid_models = ['Prius', 'C-HR', 'Niro', 'Ioniq', 'Insight']
        if model in hybrid_models:
            fuel_types.append('hibrido')

        # Eléctricos
        electric_models = ['Leaf', 'Taycan', 'Model 3', 'ID.3', 'e-Golf']
        if model in electric_models:
            fuel_types.append('electrico')

        return fuel_types

    def get_common_versions(self, fuel_type: str, brand: str, model: str) -> List[str]:
        """Obtener versiones comunes"""
        base_versions = ['Base', 'Sport', 'Premium', 'Limited']

        if fuel_type == 'diesel':
            return ['TDI', 'BlueTDI', 'd', 'D']
        elif fuel_type == 'hibrido':
            return ['Hybrid', 'PHEV', 'HEV']
        elif fuel_type == 'electrico':
            return ['EV', 'Electric', 'Pure']
        else:
            return base_versions

    def run_full_download(self):
        """Ejecutar proceso completo de descarga"""
        self.log("=== Iniciando descarga de datos de vehículos ===")
        start_time = time.time()

        all_vehicles = []

        # 1. Descargar datos de Fuel Economy (prioridad - datos reales)
        self.log("Paso 1: Descargando datos de Fuel Economy...")
        fuel_df = self.download_fuel_economy_data()
        if not fuel_df.empty:
            fuel_vehicles = self.process_fuel_economy_data(fuel_df)
            all_vehicles.extend(fuel_vehicles)

        # 2. Generar datos de muestra para complementar
        self.log("Paso 2: Generando datos complementarios...")
        sample_vehicles = self.generate_sample_data()
        all_vehicles.extend(sample_vehicles)

        # 3. Eliminar duplicados basados en clave única
        unique_vehicles = []
        seen_keys = set()

        for vehicle in all_vehicles:
            key = (vehicle['fuel_type'], vehicle['brand'],
                   vehicle['model'], vehicle['year'], vehicle['version'])

            if key not in seen_keys:
                seen_keys.add(key)
                unique_vehicles.append(vehicle)

        # 4. Crear base de datos
        self.log("Paso 3: Creando base de datos expandida...")
        self.create_expanded_database(unique_vehicles)

        # 5. Generar estadísticas
        self.generate_database_stats()

        end_time = time.time()
        total_time = end_time - start_time

        self.log(f"=== Proceso completado en {total_time:.2f} segundos ===")
        self.log(f"Total de vehículos únicos: {len(unique_vehicles)}")
        self.log(f"Base de datos creada: {VEHICLE_DB}")

    def generate_database_stats(self):
        """Generar estadísticas de la base de datos"""
        self.log("Generando estadísticas de la base de datos...")

        conn = sqlite3.connect(VEHICLE_DB)
        cursor = conn.cursor()

        # Estadísticas generales
        cursor.execute("SELECT COUNT(*) FROM vehicles_expanded")
        total_vehicles = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT fuel_type) FROM vehicles_expanded")
        fuel_types_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT brand) FROM vehicles_expanded")
        brands_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT model) FROM vehicles_expanded")
        models_count = cursor.fetchone()[0]

        # Estadísticas por tipo de combustible
        cursor.execute("""
            SELECT fuel_type, COUNT(*) as count
            FROM vehicles_expanded
            GROUP BY fuel_type
            ORDER BY count DESC
        """)
        fuel_stats = cursor.fetchall()

        # Estadísticas por marca
        cursor.execute("""
            SELECT brand, COUNT(*) as count
            FROM vehicles_expanded
            GROUP BY brand
            ORDER BY count DESC
            LIMIT 10
        """)
        brand_stats = cursor.fetchall()

        conn.close()

        # Imprimir estadísticas
        self.log("\n" + "="*50)
        self.log("ESTADÍSTICAS DE LA BASE DE DATOS")
        self.log("="*50)
        self.log(f"Total de vehículos: {total_vehicles:,}")
        self.log(f"Tipos de combustible: {fuel_types_count}")
        self.log(f"Marcas: {brands_count}")
        self.log(f"Modelos: {models_count}")

        self.log("\nVehículos por tipo de combustible:")
        for fuel_type, count in fuel_stats:
            percentage = (count / total_vehicles) * 100
            self.log(f"  {fuel_type}: {count:,} ({percentage:.1f}%)")

        self.log("\nTop 10 marcas:")
        for brand, count in brand_stats:
            percentage = (count / total_vehicles) * 100
            self.log(f"  {brand}: {count:,} ({percentage:.1f}%)")

        self.log("="*50)

def main():
    """Función principal"""
    downloader = VehicleDataDownloader()

    try:
        downloader.run_full_download()

        print("\n" + "="*60)
        print("✅ DESCARGA DE DATOS DE VEHÍCULOS COMPLETADA")
        print("="*60)
        print(f"Base de datos creada: {VEHICLE_DB}")
        print("Ahora puedes usar la nueva base de datos en tu aplicación Reflex.")
        print("="*60)

    except Exception as e:
        print(f"\n❌ Error durante el proceso: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()