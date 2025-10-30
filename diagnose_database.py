#!/usr/bin/env python3
"""
Script de diagnóstico para verificar el estado de la base de datos de vehículos
================================================================================
"""

import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_database_status():
    """Verificar el estado completo de la base de datos"""
    print("=" * 60)
    print("DIAGNOSTICO DE BASE DE DATOS - ASTROTECH")
    print("=" * 60)

    try:
        # 1. Verificar conexión a la BD
        print("\n1. Verificando conexión a base de datos...")
        from utils.vehicle_data_simple import get_vehicle_count

        total_vehicles = get_vehicle_count()
        print(f"   OK: Conexión exitosa")
        print(f"   Total de vehículos en BD: {total_vehicles:,}")

        if total_vehicles == 0:
            print("   WARNING: La tabla de vehículos está VACÍA")
            print("   Solución: Ejecutar 'python dev/populate_vehicles_db.py'")
            return False

        # 2. Verificar tipos de combustible
        print("\n2. Verificando tipos de combustible...")
        from utils.vehicle_data_simple import get_vehicle_fuel_types

        fuel_types = get_vehicle_fuel_types()
        print(f"   OK: Tipos disponibles: {fuel_types}")

        if not fuel_types:
            print("   ERROR: No hay tipos de combustible en la BD")
            return False

        # 3. Verificar marcas por combustible
        print("\n3. Verificando marcas disponibles...")
        from utils.vehicle_data_simple import get_vehicle_brands

        for fuel in fuel_types:
            brands = get_vehicle_brands(fuel)
            print(f"   - {fuel}: {len(brands)} marcas")
            if len(brands) > 0:
                print(f"     Ejemplos: {', '.join(brands[:5])}")

        # 4. Verificar modelos para una marca
        print("\n4. Verificando modelos disponibles...")
        from utils.vehicle_data_simple import get_vehicle_models

        test_fuel = fuel_types[0] if fuel_types else None
        test_brands = get_vehicle_brands(test_fuel) if test_fuel else []

        if test_brands:
            test_brand = test_brands[0]
            models = get_vehicle_models(test_fuel, test_brand)
            print(f"   - {test_brand} ({test_fuel}): {len(models)} modelos")
            if models:
                print(f"     Ejemplos: {', '.join(models[:5])}")

        # 5. Verificar versiones
        print("\n5. Verificando versiones disponibles...")
        from utils.vehicle_data_simple import get_vehicle_versions

        if test_brands and models:
            test_model = models[0]
            versions = get_vehicle_versions(test_fuel, test_brand, test_model)
            print(f"   - {test_brand} {test_model}: {len(versions)} versiones")
            if versions:
                print(f"     Ejemplos: {', '.join(versions[:3])}")

        # 6. Resumen final
        print("\n" + "=" * 60)
        print("RESUMEN DEL DIAGNOSTICO")
        print("=" * 60)
        print(f"OK: Base de datos OPERATIVA")
        print(f"OK: Vehículos: {total_vehicles:,}")
        print(f"OK: Tipos de combustible: {len(fuel_types)}")
        print(f"OK: Sistema FUNCIONANDO CORRECTAMENTE")
        print("=" * 60)

        return True

    except ImportError as e:
        print(f"\n❌ ERROR DE IMPORTACIÓN: {e}")
        print("💡 Asegúrate de estar en el directorio raíz del proyecto")
        return False

    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_database_file():
    """Verificar si el archivo de base de datos existe"""
    print("\nVerificando archivo de base de datos...")

    db_files = [
        "astrotech.db",
        "vehicles_expanded.db",
        "users.db",
        "vehicles.db"
    ]

    for db_file in db_files:
        if os.path.exists(db_file):
            size = os.path.getsize(db_file)
            size_kb = size / 1024
            print(f"   OK: {db_file}: {size_kb:.2f} KB")
        else:
            print(f"   ERROR: {db_file}: NO EXISTE")

if __name__ == "__main__":
    print("INICIANDO DIAGNOSTICO DEL SISTEMA ASTROTECH...\n")

    # Verificar archivos de BD
    check_database_file()

    # Verificar estado de la BD
    success = check_database_status()

    if not success:
        print("\nSE DETECTARON PROBLEMAS")
        print("=" * 60)
        print("PASOS PARA SOLUCIONAR:")
        print("1. Verificar que astrotech.db existe")
        print("2. Ejecutar: python dev/populate_vehicles_db.py")
        print("3. Volver a ejecutar este diagnóstico")
        print("=" * 60)
        sys.exit(1)
    else:
        print("\nSISTEMA COMPLETAMENTE FUNCIONAL")
        sys.exit(0)