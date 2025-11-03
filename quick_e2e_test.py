#!/usr/bin/env python3
"""
Quick E2E Test - Verificación rápida de funcionalidad principal
=========================================================

Test simplificado que verifica que los componentes principales funcionen
sin requerir Docker completo.
"""

import sys
import requests
import time
import subprocess
import os
from pathlib import Path

def test_database_connectivity():
    """Verificar conexión y datos en la base de datos."""
    print("Testing database connectivity...")

    try:
        # Importar funciones de la base de datos
        sys.path.append('.')
        from utils.vehicle_data_simple import (
            get_vehicle_fuel_types,
            get_vehicle_brands,
            get_vehicle_models,
            get_vehicle_versions,
            get_vehicle_count
        )

        # Test 1: Conexión básica
        count = get_vehicle_count()
        print(f"✅ Database connected. Total vehicles: {count}")
        assert count > 0, "No vehicles found in database"

        # Test 2: Tipos de combustible
        fuel_types = get_vehicle_fuel_types()
        print(f"✅ Fuel types found: {fuel_types}")
        assert len(fuel_types) > 0, "No fuel types found"
        assert "diesel" in fuel_types, "Diesel not found"

        # Test 3: Marcas para diesel
        brands = get_vehicle_brands("diesel")
        print(f"✅ Brands for diesel: {len(brands)} found")
        assert len(brands) > 0, "No brands found for diesel"

        # Test 4: Modelos para Audi diesel
        models = get_vehicle_models("diesel", "Audi")
        print(f"✅ Models for Audi diesel: {len(models)} found")
        assert len(models) > 0, "No models found for Audi diesel"

        # Test 5: Versiones para Audi A3 diesel
        versions = get_vehicle_versions("diesel", "Audi", "A3")
        print(f"✅ Versions for Audi A3 diesel: {len(versions)} found")
        assert len(versions) > 0, "No versions found for Audi A3 diesel"

        print("✅ All database tests passed!")
        return True

    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_api_endpoints():
    """Verificar endpoints de la API."""
    print("\n🔍 Testing API endpoints...")

    try:
        # Iniciar la aplicación en background
        print("🚀 Starting Reflex app...")
        process = subprocess.Popen([
            sys.executable, "-m", "reflex", "run", "--backend-host", "0.0.0.0"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Esperar a que inicie
        max_wait = 30
        for i in range(max_wait):
            try:
                response = requests.get("http://localhost:3000", timeout=2)
                if response.status_code == 200:
                    print(f"✅ App started after {i} seconds")
                    break
            except requests.exceptions.RequestException:
                if i % 5 == 0:
                    print(f"⏳ Waiting for app... {i}/{max_wait}s")
                time.sleep(1)
        else:
            print("❌ App failed to start")
            process.terminate()
            return False

        # Test endpoints
        try:
            # Test health
            response = requests.get("http://localhost:8000/ping", timeout=5)
            assert response.status_code == 200
            print("✅ Health endpoint working")

            # Test fuel types endpoint (si existe)
            try:
                response = requests.get("http://localhost:8000/api/fuel_types", timeout=5)
                if response.status_code == 200:
                    fuel_types = response.json()
                    print(f"✅ API fuel types endpoint: {fuel_types}")
            except:
                print("⚠️ API fuel types endpoint not available")

            print("✅ All API tests passed!")

        finally:
            # Terminar la aplicación
            process.terminate()
            process.wait(timeout=5)

        return True

    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def test_vehicle_selector_logic():
    """Verificar la lógica del selector de vehículos."""
    print("\n🔍 Testing vehicle selector logic...")

    try:
        sys.path.append('.')
        from state.vehicle_state_simple import VehicleState

        # No podemos instanciar directamente, pero podemos verificar las funciones
        print("✅ VehicleState class found")

        # Verificar que las funciones existan
        from utils.vehicle_data_simple import (
            get_vehicle_fuel_types,
            get_vehicle_brands,
            get_vehicle_models,
            get_vehicle_versions
        )

        # Test flujo completo
        fuel_types = get_vehicle_fuel_types()
        assert len(fuel_types) > 0

        selected_fuel = fuel_types[0]
        brands = get_vehicle_brands(selected_fuel)
        assert len(brands) > 0

        selected_brand = brands[0]
        models = get_vehicle_models(selected_fuel, selected_brand)
        assert len(models) > 0

        selected_model = models[0]
        versions = get_vehicle_versions(selected_fuel, selected_brand, selected_model)
        assert len(versions) > 0

        print(f"✅ Complete flow works: {selected_fuel} -> {selected_brand} -> {selected_model} -> {versions[0]}")
        print("✅ All selector logic tests passed!")

        return True

    except Exception as e:
        print(f"❌ Selector logic test failed: {e}")
        return False

def test_components_import():
    """Verificar que los componentes se puedan importar."""
    print("\n🔍 Testing component imports...")

    try:
        sys.path.append('.')

        # Test imports principales
        from components.vehicle_selector import vehicle_selector
        print("✅ Vehicle selector component imported")

        from state.vehicle_state_simple import VehicleState
        print("✅ Vehicle state imported")

        from utils.vehicle_data_simple import get_vehicle_fuel_types
        print("✅ Vehicle data utils imported")

        from models.vehicle import Vehicle
        print("✅ Vehicle model imported")

        print("✅ All component imports successful!")
        return True

    except Exception as e:
        print(f"❌ Component import failed: {e}")
        return False

def test_file_structure():
    """Verificar estructura de archivos."""
    print("\n🔍 Testing file structure...")

    required_files = [
        "components/vehicle_selector.py",
        "state/vehicle_state_simple.py",
        "utils/vehicle_data_simple.py",
        "models/vehicle.py",
        "vehicles_local.db",
        "settings.py"
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False

    print("✅ All required files present!")
    return True

def generate_test_report(results):
    """Generar reporte de resultados."""
    print("\n" + "="*50)
    print("📊 QUICK E2E TEST REPORT")
    print("="*50)

    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    failed_tests = total_tests - passed_tests

    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")

    print("\n📋 Test Results:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name}")

    if failed_tests == 0:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("The application is ready for deployment!")
    else:
        print(f"\n⚠️ {failed_tests} test(s) failed.")
        print("Please check the failing components before deployment.")

    return failed_tests == 0

def main():
    """Función principal del test rápido."""
    print("AstroTech App - Quick E2E Test Suite")
    print("=" * 50)

    # Ejecutar todos los tests
    results = {}

    results["File Structure"] = test_file_structure()
    results["Component Imports"] = test_components_import()
    results["Database Connectivity"] = test_database_connectivity()
    results["Vehicle Selector Logic"] = test_vehicle_selector_logic()
    results["API Endpoints"] = test_api_endpoints()

    # Generar reporte
    success = generate_test_report(results)

    # Salir con código apropiado
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()