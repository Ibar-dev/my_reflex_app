#!/usr/bin/env python3
"""
Analisis Simple de Base de Datos - AstroTech
============================================
"""

import sqlite3
import os

def analyze_db():
    print("ANALISIS DE BASE DE DATOS ASTROTECH")
    print("=" * 50)

    # Verificar bases de datos
    dbs = []
    for db in ['astrotech.db', 'vehicles.db', 'vehicles_expanded.db']:
        if os.path.exists(db):
            size = os.path.getsize(db)
            print(f"[OK] {db}: {size:,} bytes")
            dbs.append(db)
        else:
            print(f"[X] {db}: No existe")

    print("\nCONTENIDO DE BASES DE DATOS:")
    print("-" * 50)

    for db in dbs:
        try:
            conn = sqlite3.connect(db)
            cursor = conn.cursor()

            # Verificar tablas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            print(f"\n{db}:")
            for table_name, in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"  {table_name}: {count:,} registros")

                # Si es tabla de vehicles con datos, verificar contenido
                if 'vehicle' in table_name.lower() and count > 0:
                    cursor.execute(f"SELECT DISTINCT fuel_type FROM {table_name} LIMIT 3")
                    fuels = cursor.fetchall()
                    print(f"    Combustibles: {[f[0] for f in fuels if f[0]]}")

                    cursor.execute(f"SELECT DISTINCT brand FROM {table_name} LIMIT 5")
                    brands = cursor.fetchall()
                    print(f"    Marcas: {[b[0] for b in brands if b[0]]}")

            conn.close()

        except Exception as e:
            print(f"  Error: {e}")

    print("\nVERIFICACION DE CONFIGURACION:")
    print("-" * 50)

    # Verificar settings
    try:
        import settings
        print(f"DATABASE_URL: {settings.DATABASE_URL}")
        print(f"DB Path: {settings.DATABASE_PATH}")
        print(f"DB exists: {settings.DATABASE_PATH.exists()}")
    except Exception as e:
        print(f"Error settings: {e}")

    # Verificar que datos devuelve la app
    try:
        from utils.vehicle_data_simple import get_vehicle_fuel_types, get_vehicle_count
        fuels = get_vehicle_fuel_types()
        total = get_vehicle_count()
        print(f"\nDATOS EN APP:")
        print(f"Total vehiculos: {total:,}")
        print(f"Tipos combustible: {fuels}")
    except Exception as e:
        print(f"Error vehicle_data: {e}")

    print("\nARCHIVOS CSS:")
    print("-" * 50)
    css_files = ['assets/styles.css', 'assets/selector-fix.css']
    for css in css_files:
        if os.path.exists(css):
            size = os.path.getsize(css)
            print(f"[OK] {css}: {size:,} bytes")
        else:
            print(f"[X] {css}: No existe")

if __name__ == "__main__":
    analyze_db()