#!/usr/bin/env python3
"""
Simple E2E Test - Quick verification
===================================

Quick test to verify main functionality without complex setup.
"""

import sys
import time
from pathlib import Path

def test_file_structure():
    """Verify required files exist."""
    print("Testing file structure...")

    required_files = [
        "components/vehicle_selector.py",
        "state/vehicle_state_simple.py",
        "utils/vehicle_data_simple.py",
        "models/vehicle.py",
        "vehicles_local.db",
        "settings.py"
    ]

    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"FAIL: Missing file - {file_path}")
            return False

    print("PASS: All required files present")
    return True

def test_database():
    """Test database connectivity and data."""
    print("Testing database...")

    try:
        sys.path.append('.')
        from utils.vehicle_data_supabase import (
            get_vehicle_fuel_types,
            get_vehicle_brands,
            get_vehicle_models,
            get_vehicle_versions,
            get_vehicle_count
        )

        # Test basic connectivity
        count = get_vehicle_count()
        print(f"Database connected. Total vehicles: {count}")
        assert count > 0, "No vehicles found"

        # Test fuel types
        fuel_types = get_vehicle_fuel_types()
        print(f"Fuel types: {fuel_types}")
        assert len(fuel_types) > 0, "No fuel types found"

        # Test complete flow
        if fuel_types:
            fuel = fuel_types[0]
            brands = get_vehicle_brands(fuel)
            print(f"Brands for {fuel}: {len(brands)}")
            assert len(brands) > 0, "No brands found"

            if brands:
                brand = brands[0]
                models = get_vehicle_models(fuel, brand)
                print(f"Models for {brand}: {len(models)}")
                assert len(models) > 0, "No models found"

                if models:
                    model = models[0]
                    versions = get_vehicle_versions(fuel, brand, model)
                    print(f"Versions for {model}: {len(versions)}")
                    assert len(versions) > 0, "No versions found"

        print("PASS: Database tests completed")
        return True

    except Exception as e:
        print(f"FAIL: Database test failed - {e}")
        return False

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")

    try:
        sys.path.append('.')

        # Test main components
        from components.vehicle_selector import vehicle_selector
        print("PASS: Vehicle selector imported")

        from state.vehicle_state_simple import VehicleState
        print("PASS: Vehicle state imported")

        from utils.vehicle_data_supabase import get_vehicle_fuel_types
        print("PASS: Vehicle data utils imported")

        from models.vehicle import Vehicle
        print("PASS: Vehicle model imported")

        print("PASS: All imports successful")
        return True

    except Exception as e:
        print(f"FAIL: Import failed - {e}")
        return False

def main():
    """Run all tests."""
    print("AstroTech App - Simple E2E Test")
    print("=" * 40)

    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("Database", test_database)
    ]

    results = {}
    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            results[test_name] = test_func()
            if results[test_name]:
                passed += 1
        except Exception as e:
            print(f"FAIL: {test_name} - {e}")
            results[test_name] = False

    # Summary
    print("\n" + "=" * 40)
    print("TEST SUMMARY")
    print("=" * 40)
    print(f"Total: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")

    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"{status}: {test_name}")

    if passed == total:
        print("\nSUCCESS: All tests passed!")
        print("Application is ready for deployment!")
    else:
        print(f"\nFAILED: {total - passed} test(s) failed.")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)