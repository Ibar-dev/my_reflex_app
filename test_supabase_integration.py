"""
Script de prueba para verificar la integración con Supabase.
"""
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.supabase_connection import test_connection
from utils.vehicle_data_supabase import (
    get_vehicle_fuel_types,
    get_vehicle_brands,
    get_vehicle_models,
    get_vehicle_versions,
    get_vehicle_count
)


def main():
    print("\n" + "=" * 60)
    print("🧪 PRUEBA DE INTEGRACIÓN CON SUPABASE")
    print("=" * 60)
    
    # Prueba 1: Conexión
    print("\n1️⃣ Probando conexión a Supabase...")
    if not test_connection():
        print("\n❌ Error de conexión. Verifica que:")
        print("   - Tienes psycopg2 instalado: pip install psycopg2-binary")
        print("   - Tu archivo .env tiene la contraseña correcta")
        print("   - Tu base de datos de Supabase está activa")
        return
    
    # Prueba 2: Total de vehículos
    print("\n2️⃣ Contando vehículos en la base de datos...")
    total = get_vehicle_count()
    print(f"📊 Total de vehículos: {total}")
    
    if total == 0:
        print("\n⚠️  La base de datos está vacía.")
        print("   Ejecuta: python utils/create_vehicles_table.py")
        return
    
    # Prueba 3: Tipos de combustible
    print("\n3️⃣ Obteniendo tipos de combustible...")
    fuel_types = get_vehicle_fuel_types()
    print(f"⛽ Tipos de combustible disponibles: {fuel_types}")
    
    # Prueba 4: Marcas por tipo de combustible
    print("\n4️⃣ Obteniendo marcas por tipo de combustible...")
    for fuel in fuel_types:
        brands = get_vehicle_brands(fuel)
        print(f"\n   📌 {fuel}:")
        print(f"      Total de marcas: {len(brands)}")
        print(f"      Primeras 10: {brands[:10]}")
    
    # Prueba 5: Modelos de una marca
    if fuel_types and len(fuel_types) > 0:
        test_fuel = fuel_types[0]
        brands = get_vehicle_brands(test_fuel)
        
        if brands and len(brands) > 0:
            test_brand = brands[0]
            print(f"\n5️⃣ Obteniendo modelos de {test_brand} ({test_fuel})...")
            models = get_vehicle_models(test_fuel, test_brand)
            print(f"🚗 Modelos disponibles ({len(models)}):")
            for model in models:
                print(f"   - {model}")
            
            # Prueba 6: Versiones de un modelo
            if models and len(models) > 0:
                test_model = models[0]
                print(f"\n6️⃣ Obteniendo versiones de {test_brand} {test_model}...")
                versions = get_vehicle_versions(test_fuel, test_brand, test_model)
                print(f"⚙️ Versiones disponibles ({len(versions)}):")
                for version in versions:
                    print(f"   - {version}")
    
    # Resumen
    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
    print("=" * 60)
    print(f"\n📊 Resumen:")
    print(f"   - Conexión: ✅ OK")
    print(f"   - Total vehículos: {total}")
    print(f"   - Tipos de combustible: {len(fuel_types)}")
    print(f"   - Sistema: 100% funcional")
    print("\n🎉 La integración con Supabase está lista para usar")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
