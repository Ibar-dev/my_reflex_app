#!/usr/bin/env python3
"""
Script para migrar datos de la base de datos antigua a la nueva estructura expandida
============================================================================

Este script:
1. Mantiene los datos existentes
2. Añade nueva funcionalidad de búsqueda
3. Compatibilidad con sistema actual

Uso: python migrate_vehicle_data.py
"""

import os
import sqlite3
import pandas as pd
from datetime import datetime
from typing import List, Dict

# Configuración
OLD_DB = "vehicles.db"
NEW_DB = "vehicles_expanded.db"
BACKUP_DB = "vehicles_backup.db"

class VehicleDataMigrator:
    """Migrador de datos de vehículos"""

    def __init__(self):
        self.log("Iniciando migración de datos de vehículos...")

    def log(self, message: str):
        """Función de logging"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    def backup_existing_database(self):
        """Crear copia de seguridad de la base de datos existente"""
        if os.path.exists(OLD_DB):
            self.log("Creando copia de seguridad de la base de datos existente...")
            import shutil
            shutil.copy2(OLD_DB, BACKUP_DB)
            self.log(f"Copia de seguridad creada: {BACKUP_DB}")
            return True
        else:
            self.log("No existe base de datos anterior, continuando...")
            return False

    def check_existing_data(self) -> Dict:
        """Verificar datos existentes en la base de datos antigua"""
        self.log("Verificando base de datos existente...")

        if not os.path.exists(OLD_DB):
            self.log("No existe base de datos vehicles.db")
            return {'exists': False, 'count': 0}

        conn = sqlite3.connect(OLD_DB)
        cursor = conn.cursor()

        try:
            # Verificar si existe la tabla vehicles
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vehicles'")
            table_exists = cursor.fetchone() is not None

            if not table_exists:
                self.log("La tabla 'vehicles' no existe en la base de datos")
                return {'exists': False, 'count': 0}

            # Contar registros
            cursor.execute("SELECT COUNT(*) FROM vehicles")
            count = cursor.fetchone()[0]

            # Obtener muestra de datos
            cursor.execute("SELECT * FROM vehicles LIMIT 5")
            sample = cursor.fetchall()

            # Obtener tipos de combustible únicos
            cursor.execute("SELECT DISTINCT fuel_type FROM vehicles")
            fuel_types = [row[0] for row in cursor.fetchall()]

            # Obtener marcas únicas
            cursor.execute("SELECT DISTINCT brand FROM vehicles")
            brands = [row[0] for row in cursor.fetchall()]

            conn.close()

            stats = {
                'exists': True,
                'count': count,
                'fuel_types': fuel_types,
                'brands': brands,
                'sample': sample
            }

            self.log(f"Base de datos existente encontrada:")
            self.log(f"  - Registros: {count}")
            self.log(f"  - Tipos de combustible: {fuel_types}")
            self.log(f"  - Marcas: {brands}")

            return stats

        except Exception as e:
            self.log(f"Error verificando base de datos: {str(e)}")
            conn.close()
            return {'exists': False, 'count': 0}

    def create_expanded_database_structure(self):
        """Crear estructura de la base de datos expandida"""
        self.log("Creando estructura de base de datos expandida...")

        conn = sqlite3.connect(NEW_DB)
        cursor = conn.cursor()

        # Crear tabla principal
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
                source TEXT DEFAULT 'migrated',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(fuel_type, brand, model, year, version)
            )
        ''')

        # Crear índices
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_fuel_type_expanded ON vehicles_expanded(fuel_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_brand_expanded ON vehicles_expanded(brand)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_brand_fuel_expanded ON vehicles_expanded(brand, fuel_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_model_expanded ON vehicles_expanded(model)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_year_expanded ON vehicles_expanded(year)')

        # Crear tabla de metadatos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS migration_metadata (
                id INTEGER PRIMARY KEY,
                migration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                old_db_records INTEGER DEFAULT 0,
                new_db_records INTEGER DEFAULT 0,
                migration_status TEXT DEFAULT 'in_progress'
            )
        ''')

        conn.commit()
        conn.close()

        self.log("Estructura de base de datos expandida creada")

    def migrate_legacy_data(self) -> int:
        """Migrar datos de la base de datos antigua a la nueva"""
        self.log("Iniciando migración de datos existentes...")

        if not os.path.exists(OLD_DB):
            self.log("No existe base de datos vehicles.db para migrar")
            return 0

        # Conectar a ambas bases de datos
        old_conn = sqlite3.connect(OLD_DB)
        new_conn = sqlite3.connect(NEW_DB)

        old_cursor = old_conn.cursor()
        new_cursor = new_conn.cursor()

        try:
            # Leer datos de la tabla antigua
            old_cursor.execute("SELECT fuel_type, brand, model, year, version FROM vehicles")
            old_data = old_cursor.fetchall()

            if not old_data:
                self.log("No hay datos para migrar en la base de datos antigua")
                return 0

            self.log(f"Encontrados {len(old_data)} registros para migrar")

            # Insertar en la nueva tabla
            migrated_count = 0
            duplicates_count = 0

            for row in old_data:
                fuel_type, brand, model, year, version = row

                try:
                    new_cursor.execute('''
                        INSERT OR IGNORE INTO vehicles_expanded
                        (fuel_type, brand, model, year, version, source)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (fuel_type, brand, model, year, version, 'legacy_migrated'))

                    if new_cursor.rowcount > 0:
                        migrated_count += 1
                    else:
                        duplicates_count += 1

                except Exception as e:
                    self.log(f"Error migrando registro {row}: {str(e)}")
                    continue

            new_conn.commit()

            self.log(f"Migración completada:")
            self.log(f"  - Registros migrados: {migrated_count}")
            self.log(f"  - Duplicados omitidos: {duplicates_count}")

            # Actualizar metadatos de migración
            new_cursor.execute('''
                INSERT OR REPLACE INTO migration_metadata
                (id, old_db_records, new_db_records, migration_status)
                VALUES (1, ?, ?, 'completed')
            ''', (len(old_data), migrated_count))

            new_conn.commit()

            return migrated_count

        except Exception as e:
            self.log(f"Error durante la migración: {str(e)}")
            new_conn.rollback()
            return 0

        finally:
            old_conn.close()
            new_conn.close()

    def enhance_migrated_data(self):
        """Mejorar datos migrados con información adicional"""
        self.log("Mejorando datos migrados con información adicional...")

        conn = sqlite3.connect(NEW_DB)
        cursor = conn.cursor()

        try:
            # Añadir información de transmisiones comunes por marca/modelo
            transmission_map = {
                'BMW': ['Automatic', 'Manual', 'Steptronic'],
                'Mercedes-Benz': ['Automatic', '7G-TRONIC', '9G-TRONIC'],
                'Audi': ['Automatic', 'S-Tronic', 'Tiptronic'],
                'Volkswagen': ['Manual', 'Automatic', 'DSG'],
                'Ford': ['Manual', 'Automatic', 'PowerShift'],
                'Toyota': ['Manual', 'Automatic', 'CVT'],
                'Honda': ['Manual', 'Automatic', 'CVT'],
                'Nissan': ['Manual', 'Automatic', 'CVT'],
                'Hyundai': ['Manual', 'Automatic', 'DCT'],
                'Kia': ['Manual', 'Automatic', 'DCT']
            }

            # Actualizar transmisiones para registros que no tienen
            for brand, transmissions in transmission_map.items():
                if transmissions:
                    # Asignar la transmisión más común como predeterminada
                    default_transmission = transmissions[0]
                    cursor.execute('''
                        UPDATE vehicles_expanded
                        SET transmission = ?
                        WHERE brand = ? AND (transmission IS NULL OR transmission = '')
                    ''', (default_transmission, brand))

                    # Añadir otras variantes de transmisión
                    for transmission in transmissions[1:]:
                        cursor.execute('''
                            INSERT OR IGNORE INTO vehicles_expanded
                            (fuel_type, brand, model, year, version, transmission, source)
                            SELECT fuel_type, brand, model, year, version, ?, 'enhanced'
                            FROM vehicles_expanded
                            WHERE brand = ? AND transmission = ?
                        ''', (transmission, brand, default_transmission))

            # Añadir información de cilindros común por tipo de combustible
            cylinder_map = {
                'gasolina': ['4', '6', '8', '12'],
                'diesel': ['4', '6', '8'],
                'hibrido': ['4'],
                'electrico': ['Electric']
            }

            for fuel_type, cylinders in cylinder_map.items():
                # Asignar 4 cilindros como predeterminado para la mayoría
                default_cylinders = cylinders[0]
                cursor.execute('''
                    UPDATE vehicles_expanded
                    SET cylinders = ?
                    WHERE fuel_type = ? AND (cylinders IS NULL OR cylinders = '')
                ''', (default_cylinders, fuel_type))

            conn.commit()

            # Contar registros mejorados
            cursor.execute("SELECT COUNT(*) FROM vehicles_expanded WHERE transmission IS NOT NULL")
            with_transmission = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM vehicles_expanded WHERE cylinders IS NOT NULL")
            with_cylinders = cursor.fetchone()[0]

            self.log(f"Mejora de datos completada:")
            self.log(f"  - Registros con transmisión: {with_transmission}")
            self.log(f"  - Registros con cilindros: {with_cylinders}")

        except Exception as e:
            self.log(f"Error mejorando datos: {str(e)}")
            conn.rollback()

        finally:
            conn.close()

    def validate_migration(self):
        """Validar que la migración se completó correctamente"""
        self.log("Validando migración...")

        if not os.path.exists(NEW_DB):
            self.log("ERROR: No se creó la base de datos expandida")
            return False

        conn = sqlite3.connect(NEW_DB)
        cursor = conn.cursor()

        try:
            # Verificar estructura
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vehicles_expanded'")
            table_exists = cursor.fetchone() is not None

            if not table_exists:
                self.log("ERROR: No existe la tabla vehicles_expanded")
                return False

            # Verificar datos
            cursor.execute("SELECT COUNT(*) FROM vehicles_expanded")
            total_records = cursor.fetchone()[0]

            if total_records == 0:
                self.log("ADVERTENCIA: No hay registros en la base de datos expandida")
                return True  # No es un error, podría ser una instalación nueva

            # Verificar integridad de datos
            cursor.execute("SELECT COUNT(*) FROM vehicles_expanded WHERE fuel_type IS NULL OR fuel_type = ''")
            missing_fuel = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM vehicles_expanded WHERE brand IS NULL OR brand = ''")
            missing_brand = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM vehicles_expanded WHERE model IS NULL OR model = ''")
            missing_model = cursor.fetchone()[0]

            # Estadísticas
            cursor.execute("SELECT COUNT(DISTINCT fuel_type) FROM vehicles_expanded")
            fuel_types = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(DISTINCT brand) FROM vehicles_expanded")
            brands = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(DISTINCT model) FROM vehicles_expanded")
            models = cursor.fetchone()[0]

            conn.close()

            self.log(f"Validación completada:")
            self.log(f"  - Total de registros: {total_records:,}")
            self.log(f"  - Tipos de combustible: {fuel_types}")
            self.log(f"  - Marcas: {brands}")
            self.log(f"  - Modelos: {models}")

            if missing_fuel > 0:
                self.log(f"  - ADVERTENCIA: {missing_fuel} registros sin tipo de combustible")

            if missing_brand > 0:
                self.log(f"  - ADVERTENCIA: {missing_brand} registros sin marca")

            if missing_model > 0:
                self.log(f"  - ADVERTENCIA: {missing_model} registros sin modelo")

            return True

        except Exception as e:
            self.log(f"Error en validación: {str(e)}")
            conn.close()
            return False

    def generate_migration_report(self):
        """Generar reporte de la migración"""
        self.log("Generando reporte de migración...")

        conn = sqlite3.connect(NEW_DB)
        cursor = conn.cursor()

        try:
            # Estadísticas generales
            cursor.execute("SELECT COUNT(*) FROM vehicles_expanded")
            total = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(DISTINCT brand) FROM vehicles_expanded")
            brands = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(DISTINCT model) FROM vehicles_expanded")
            models = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(DISTINCT fuel_type) FROM vehicles_expanded")
            fuel_types = cursor.fetchone()[0]

            # Por fuente de datos
            cursor.execute("""
                SELECT source, COUNT(*) as count
                FROM vehicles_expanded
                GROUP BY source
                ORDER BY count DESC
            """)
            source_stats = cursor.fetchall()

            # Top 10 marcas
            cursor.execute("""
                SELECT brand, COUNT(*) as count
                FROM vehicles_expanded
                GROUP BY brand
                ORDER BY count DESC
                LIMIT 10
            """)
            top_brands = cursor.fetchall()

            # Por tipo de combustible
            cursor.execute("""
                SELECT fuel_type, COUNT(*) as count
                FROM vehicles_expanded
                GROUP BY fuel_type
                ORDER BY count DESC
            """)
            fuel_stats = cursor.fetchall()

            # Por año
            cursor.execute("""
                SELECT year, COUNT(*) as count
                FROM vehicles_expanded
                WHERE year != ''
                GROUP BY year
                ORDER BY year DESC
                LIMIT 10
            """)
            year_stats = cursor.fetchall()

            conn.close()

            # Imprimir reporte
            print("\n" + "="*60)
            print("REPORTE DE MIGRACIÓN DE BASE DE DATOS DE VEHÍCULOS")
            print("="*60)
            print(f"Base de datos destino: {NEW_DB}")
            print(f"Fecha de migración: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("")
            print("ESTADÍSTICAS GENERALES:")
            print(f"  • Total de vehículos: {total:,}")
            print(f"  • Marcas únicas: {brands}")
            print(f"  • Modelos únicos: {models}")
            print(f"  • Tipos de combustible: {fuel_types}")

            print("\nVEHÍCULOS POR FUENTE DE DATOS:")
            for source, count in source_stats:
                percentage = (count / total) * 100
                print(f"  • {source}: {count:,} ({percentage:.1f}%)")

            print("\nTOP 10 MARCAS:")
            for i, (brand, count) in enumerate(top_brands, 1):
                percentage = (count / total) * 100
                print(f"  {i:2d}. {brand}: {count:,} ({percentage:.1f}%)")

            print("\nVEHÍCULOS POR TIPO DE COMBUSTIBLE:")
            for fuel_type, count in fuel_stats:
                percentage = (count / total) * 100
                print(f"  • {fuel_type}: {count:,} ({percentage:.1f}%)")

            if year_stats:
                print("\nVEHÍCULOS POR AÑO (últimos 10):")
                for year, count in year_stats:
                    percentage = (count / total) * 100
                    print(f"  • {year}: {count:,} ({percentage:.1f}%)")

            print("\n" + "="*60)
            print("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
            print(f"La nueva base de datos está lista para usarse: {NEW_DB}")
            print("="*60)

        except Exception as e:
            self.log(f"Error generando reporte: {str(e)}")
            conn.close()

    def run_migration(self):
        """Ejecutar proceso completo de migración"""
        start_time = datetime.now()
        self.log("=== INICIANDO PROCESO DE MIGRACIÓN ===")

        try:
            # 1. Verificar datos existentes
            old_stats = self.check_existing_data()

            # 2. Crear copia de seguridad
            self.backup_existing_database()

            # 3. Crear nueva estructura
            self.create_expanded_database_structure()

            # 4. Migrar datos existentes
            migrated_count = self.migrate_legacy_data()

            # 5. Mejorar datos
            if migrated_count > 0:
                self.enhance_migrated_data()

            # 6. Validar migración
            if self.validate_migration():
                # 7. Generar reporte
                self.generate_migration_report()

                end_time = datetime.now()
                duration = end_time - start_time

                self.log(f"=== MIGRACIÓN COMPLETADA EN {duration.total_seconds():.2f} SEGUNDOS ===")
                return True
            else:
                self.log("ERROR: La validación de la migración falló")
                return False

        except Exception as e:
            self.log(f"ERROR CRÍTICO en la migración: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Función principal"""
    migrator = VehicleDataMigrator()

    try:
        success = migrator.run_migration()

        if success:
            print("\n✅ La base de datos de vehículos ha sido actualizada exitosamente.")
            print("Ahora puedes ejecutar el script de descarga para añadir más datos:")
            print("python download_vehicle_data.py")
        else:
            print("\n❌ La migración falló. Revisa los logs para más detalles.")

    except KeyboardInterrupt:
        print("\n⚠️ Migración interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")

if __name__ == "__main__":
    main()