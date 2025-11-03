#!/usr/bin/env python3
"""
Diagnóstico simple sin emojis para verificar el estado de la base de datos
"""

import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 60)
    print("DIAGNOSTICO SIMPLE DE BASE DE DATOS - ASTROTECH")
    print("=" * 60)

    try:
        # Verificar archivos de BD
        print("\nVerificando archivos de base de datos...")
        db_files = ["astrotech.db", "vehicles_expanded.db", "vehicles.db"]

        for db_file in db_files:
            if os.path.exists(db_file):
                size = os.path.getsize(db_file) / 1024
                print(f"   {db_file}: {size:.2f} KB (EXISTE)")
            else:
                print(f"   {db_file}: NO EXISTE")

        # Verificar datos
        print("\nVerificando contenido de la base de datos...")
        from utils.vehicle_data_supabase import get_vehicle_count

        total_vehicles = get_vehicle_count()
        print(f"Total de vehiculos en BD: {total_vehicles:,}")

        if total_vehicles == 0:
            print("ERROR: La tabla de vehiculos esta VACIA")
            return False

        # Verificar tipos de combustible
        from utils.vehicle_data_supabase import get_vehicle_fuel_types
        fuel_types = get_vehicle_fuel_types()
        print(f"Tipos de combustible: {fuel_types}")

        # Verificar marcas
        if fuel_types:
            from utils.vehicle_data_supabase import get_vehicle_brands
            brands = get_vehicle_brands(fuel_types[0])
            print(f"Marcas ({fuel_types[0]}): {len(brands)} encontradas")
            if brands:
                print(f"Ejemplos: {', '.join(brands[:3])}")

        # Verificar modelos
        if fuel_types and brands:
            from utils.vehicle_data_supabase import get_vehicle_models
            models = get_vehicle_models(fuel_types[0], brands[0])
            print(f"Modelos ({brands[0]}): {len(models)} encontrados")
            if models:
                print(f"Ejemplos: {', '.join(models[:3])}")

        print("\n" + "=" * 60)
        print("RESUMEN: Sistema funciona correctamente")
        print(f"- Vehiculos: {total_vehicles:,}")
        print(f"- Combustibles: {len(fuel_types)}")
        print(f"- Marcas: {len(brands) if 'brands' in locals() else 0}")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\nSISTEMA FUNCIONAL")
    else:
        print("\nHAY PROBLEMAS QUE REQUIEREN ATENCION")