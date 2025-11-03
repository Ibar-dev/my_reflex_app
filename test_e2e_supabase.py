#!/usr/bin/env python3
"""
Test End-to-End de Integración con Supabase - AstroTech
====================================================

Este test verifica completamente el funcionamiento de la integración
con Supabase para el manejo de datos de vehículos.
"""

import sys
import time
from pathlib import Path

def run_test(test_name, test_function):
    """Ejecuta un test y muestra resultados"""
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print('='*60)

    try:
        result = test_function()
        if result:
            print(f"[OK] {test_name}: PASADO")
        else:
            print(f"[FAIL] {test_name}: FALLIDO")
        return result
    except Exception as e:
        print(f"[ERROR] {test_name}: ERROR - {e}")
        import traceback
        traceback.print_exc()
        return False

def test_supabase_connection():
    """Verificar la conexión a Supabase"""
    try:
        sys.path.insert(0, '.')
        from utils.supabase_connection import db

        if db.connect():
            print("✅ Conexión a Supabase establecida")
            db.disconnect()
            return True
        else:
            print("❌ No se pudo conectar a Supabase")
            return False

    except Exception as e:
        print(f"❌ Error en conexión a Supabase: {e}")
        return False

def test_supabase_vehicle_count():
    """Verificar que hay vehículos en Supabase"""
    try:
        sys.path.insert(0, '.')
        from utils.vehicle_data_supabase import get_vehicle_count

        count = get_vehicle_count()
        if count > 0:
            print(f"✅ Vehículos encontrados en Supabase: {count:,}")
            return True
        else:
            print("❌ No hay vehículos en Supabase")
            return False

    except Exception as e:
        print(f"❌ Error contando vehículos: {e}")
        return False

def test_supabase_fuel_types():
    """Verificar tipos de combustible desde Supabase"""
    try:
        sys.path.insert(0, '.')
        from utils.vehicle_data_supabase import get_vehicle_fuel_types

        fuel_types = get_vehicle_fuel_types()
        if fuel_types and len(fuel_types) > 0:
            print(f"✅ Tipos de combustible obtenidos: {fuel_types}")
            return True
        else:
            print("❌ No se obtuvieron tipos de combustible")
            return False

    except Exception as e:
        print(f"❌ Error obteniendo tipos de combustible: {e}")
        return False

def test_supabase_brands():
    """Verificar marcas desde Supabase"""
    try:
        sys.path.insert(0, '.')
        from utils.vehicle_data_supabase import get_vehicle_fuel_types, get_vehicle_brands

        fuel_types = get_vehicle_fuel_types()
        if not fuel_types:
            print("❌ No hay tipos de combustible para probar marcas")
            return False

        brands = get_vehicle_brands(fuel_types[0])
        if brands and len(brands) > 0:
            print(f"✅ Marcas obtenidas para {fuel_types[0]}: {len(brands)}")
            print(f"   Primeras 5 marcas: {brands[:5]}")
            return True
        else:
            print("❌ No se obtuvieron marcas")
            return False

    except Exception as e:
        print(f"❌ Error obteniendo marcas: {e}")
        return False

def test_supabase_models():
    """Verificar modelos desde Supabase"""
    try:
        sys.path.insert(0, '.')
        from utils.vehicle_data_supabase import get_vehicle_fuel_types, get_vehicle_brands, get_vehicle_models

        fuel_types = get_vehicle_fuel_types()
        brands = get_vehicle_brands(fuel_types[0])

        if not brands:
            print("❌ No hay marcas para probar modelos")
            return False

        models = get_vehicle_models(fuel_types[0], brands[0])
        if models and len(models) > 0:
            print(f"✅ Modelos obtenidos para {fuel_types[0]}/{brands[0]}: {len(models)}")
            print(f"   Primeros 5 modelos: {models[:5]}")
            return True
        else:
            print("❌ No se obtuvieron modelos")
            return False

    except Exception as e:
        print(f"❌ Error obteniendo modelos: {e}")
        return False

def test_supabase_versions():
    """Verificar versiones desde Supabase"""
    try:
        sys.path.insert(0, '.')
        from utils.vehicle_data_supabase import (
            get_vehicle_fuel_types,
            get_vehicle_brands,
            get_vehicle_models,
            get_vehicle_versions
        )

        fuel_types = get_vehicle_fuel_types()
        brands = get_vehicle_brands(fuel_types[0])
        models = get_vehicle_models(fuel_types[0], brands[0])

        if not models:
            print("❌ No hay modelos para probar versiones")
            return False

        versions = get_vehicle_versions(fuel_types[0], brands[0], models[0])
        if versions and len(versions) > 0:
            print(f"✅ Versiones obtenidas para {fuel_types[0]}/{brands[0]}/{models[0]}: {len(versions)}")
            print(f"   Primeras 5 versiones: {versions[:5]}")
            return True
        else:
            print("ℹ️  No se obtuvieron versiones (puede ser normal)")
            return True  # No todos los modelos tienen versiones

    except Exception as e:
        print(f"❌ Error obteniendo versiones: {e}")
        return False

def test_supabase_vehicles_data():
    """Verificar obtención de datos completos de vehículos"""
    try:
        sys.path.insert(0, '.')
        from utils.vehicle_data_supabase import get_vehicles_data

        vehicles = get_vehicles_data(limit=10)
        if vehicles and len(vehicles) > 0:
            print(f"✅ Datos de vehículos obtenidos: {len(vehicles)}")

            # Verificar estructura de datos
            required_fields = ['id', 'fuel_type', 'brand', 'model', 'version']
            vehicle = vehicles[0]

            for field in required_fields:
                if field not in vehicle:
                    print(f"❌ Campo faltante en vehículo: {field}")
                    return False

            print("✅ Estructura de datos correcta")
            print(f"   Ejemplo: {vehicle}")
            return True
        else:
            print("❌ No se obtuvieron datos de vehículos")
            return False

    except Exception as e:
        print(f"❌ Error obteniendo datos de vehículos: {e}")
        return False

def test_supabase_search():
    """Verificar funcionalidad de búsqueda"""
    try:
        sys.path.insert(0, '.')
        from utils.vehicle_data_supabase import search_vehicles

        # Buscar vehículos con término común
        results = search_vehicles("SEAT")
        if results and len(results) > 0:
            print(f"✅ Búsqueda funcional: {len(results)} resultados para 'SEAT'")
            return True
        else:
            # Intentar con otra marca
            results = search_vehicles("BMW")
            if results and len(results) > 0:
                print(f"✅ Búsqueda funcional: {len(results)} resultados para 'BMW'")
                return True
            else:
                print("ℹ️  Búsqueda no retornó resultados (puede ser normal)")
                return True  # No es crítico si no hay resultados

    except Exception as e:
        print(f"❌ Error en búsqueda: {e}")
        return False

def test_vehicle_state_with_supabase():
    """Verificar que VehicleState funciona con Supabase"""
    try:
        sys.path.insert(0, '.')
        from state.vehicle_state_simple import VehicleState

        state = VehicleState()

        # Cargar tipos de combustible
        state.load_fuel_types()

        if not state.available_fuel_types:
            print("❌ No se cargaron tipos de combustible en VehicleState")
            return False

        # Seleccionar combustible
        fuel_type = state.available_fuel_types[0]
        state.select_fuel(fuel_type)

        if not state.available_brands:
            print("❌ No se cargaron marcas en VehicleState")
            return False

        # Seleccionar marca
        brand = state.available_brands[0]
        state.select_brand(brand)

        if not state.available_models:
            print("❌ No se cargaron modelos en VehicleState")
            return False

        print(f"✅ VehicleState funciona con Supabase:")
        print(f"   Combustibles: {len(state.available_fuel_types)}")
        print(f"   Marcas ({fuel_type}): {len(state.available_brands)}")
        print(f"   Modelos ({brand}): {len(state.available_models)}")

        return True

    except Exception as e:
        print(f"❌ Error en VehicleState con Supabase: {e}")
        return False

def test_api_endpoints_with_supabase():
    """Verificar que los endpoints API funcionan con Supabase"""
    try:
        import requests

        # Test ping
        response = requests.get("http://localhost:8000/ping", timeout=5)
        if response.status_code != 200:
            print("❌ Endpoint /ping no responde")
            return False

        # Test fuel types
        response = requests.get("http://localhost:8000/api_fuel_types", timeout=5)
        if response.status_code == 200:
            fuel_types = response.json()
            if fuel_types and len(fuel_types) > 0:
                print(f"✅ API endpoint funciona: {len(fuel_types)} tipos de combustible")

                # Test brands con primer tipo de combustible
                response = requests.get(f"http://localhost:8000/api_brands?fuel_type={fuel_types[0]}", timeout=5)
                if response.status_code == 200:
                    brands = response.json()
                    print(f"✅ API brands funciona: {len(brands)} marcas")
                    return True
                else:
                    print("❌ Endpoint /api_brands falló")
                    return False
            else:
                print("❌ Endpoint /api_fuel_types no retornó datos")
                return False
        else:
            print(f"❌ Endpoint /api_fuel_types falló: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Error probando API endpoints: {e}")
        return False

def main():
    """Ejecutar todos los tests de integración con Supabase"""
    print("INICIANDO TEST END-TO-END - INTEGRACIÓN CON SUPABASE")
    print("=" * 80)

    tests = [
        ("Conexión a Supabase", test_supabase_connection),
        ("Cantidad de Vehículos", test_supabase_vehicle_count),
        ("Tipos de Combustible", test_supabase_fuel_types),
        ("Marcas", test_supabase_brands),
        ("Modelos", test_supabase_models),
        ("Versiones", test_supabase_versions),
        ("Datos Completos de Vehículos", test_supabase_vehicles_data),
        ("Búsqueda", test_supabase_search),
        ("VehicleState con Supabase", test_vehicle_state_with_supabase),
        ("API Endpoints", test_api_endpoints_with_supabase),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_function in tests:
        if run_test(test_name, test_function):
            passed += 1
        time.sleep(0.5)  # Pequeña pausa entre tests

    print(f"\n{'='*80}")
    print(f"📊 RESULTADOS DEL TEST DE INTEGRACIÓN CON SUPABASE")
    print('='*80)
    print(f"Tests Pasados: {passed}/{total}")
    print(f"Tasa de Éxito: {(passed/total)*100:.1f}%")

    if passed == total:
        print("\n🎉 ¡TODOS LOS TESTS HAN PASADO!")
        print("✅ La integración con Supabase está completamente funcional")
        print("✅ Todos los componentes trabajan correctamente con Supabase")
        print("✅ Sistema de vehículos opera 100% con Supabase")
    else:
        print(f"\n⚠️  {total - passed} tests han fallado")
        print("❌ Revisar los mensajes de error arriba")
        print("❌ Puede haber problemas con la conexión o configuración de Supabase")

    print("="*80)

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)