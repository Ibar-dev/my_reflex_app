#!/usr/bin/env python3
"""
Integration Test - Complete Flow Verification
=============================================

Comprehensive test that verifies the complete vehicle selection flow
end-to-end.
"""

import sys
import time
from pathlib import Path

def test_complete_vehicle_flow():
    """Test complete vehicle selection flow for all fuel types."""
    print("Testing complete vehicle flow...")

    try:
        sys.path.append('.')
        from utils.vehicle_data_simple import (
            get_vehicle_fuel_types,
            get_vehicle_brands,
            get_vehicle_models,
            get_vehicle_versions
        )

        # Get all available fuel types
        fuel_types = get_vehicle_fuel_types()
        print(f"Available fuel types: {fuel_types}")

        # Test complete flow for each fuel type
        all_flows_successful = True

        for fuel_type in fuel_types:
            print(f"\nTesting {fuel_type} flow:")

            try:
                # Step 1: Get brands for this fuel type
                brands = get_vehicle_brands(fuel_type)
                print(f"  Brands available: {len(brands)}")
                assert len(brands) > 0, f"No brands found for {fuel_type}"

                # Step 2: Test first brand
                first_brand = brands[0]
                models = get_vehicle_models(fuel_type, first_brand)
                print(f"  Models for {first_brand}: {len(models)}")
                assert len(models) > 0, f"No models found for {first_brand}"

                # Step 3: Test first model
                first_model = models[0]
                versions = get_vehicle_versions(fuel_type, first_brand, first_model)
                print(f"  Versions for {first_model}: {len(versions)}")
                assert len(versions) > 0, f"No versions found for {first_model}"

                # Step 4: Verify complete selection
                complete_selection = {
                    "fuel_type": fuel_type,
                    "brand": first_brand,
                    "model": first_model,
                    "version": versions[0]
                }

                print(f"  Complete selection: {complete_selection}")

            except Exception as e:
                print(f"  FAIL: {fuel_type} flow failed - {e}")
                all_flows_successful = False

        if all_flows_successful:
            print("PASS: All fuel type flows completed successfully")
        else:
            print("FAIL: Some fuel type flows failed")

        return all_flows_successful

    except Exception as e:
        print(f"FAIL: Complete flow test failed - {e}")
        return False

def test_data_consistency():
    """Test data consistency across the database."""
    print("Testing data consistency...")

    try:
        sys.path.append('.')
        from utils.vehicle_data_simple import (
            get_vehicle_fuel_types,
            get_vehicle_brands,
            get_vehicle_models,
            get_vehicle_versions
        )

        fuel_types = get_vehicle_fuel_types()
        consistency_errors = []

        for fuel_type in fuel_types:
            brands = get_vehicle_brands(fuel_type)

            for brand in brands[:2]:  # Test first 2 brands for speed
                models = get_vehicle_models(fuel_type, brand)

                for model in models[:2]:  # Test first 2 models for speed
                    versions = get_vehicle_versions(fuel_type, brand, model)

                    if len(versions) == 0:
                        consistency_errors.append(
                            f"No versions for {fuel_type}/{brand}/{model}"
                        )

        if consistency_errors:
            print(f"FAIL: Consistency errors found:")
            for error in consistency_errors:
                print(f"  - {error}")
            return False
        else:
            print("PASS: Data consistency verified")
            return True

    except Exception as e:
        print(f"FAIL: Data consistency test failed - {e}")
        return False

def test_performance_benchmarks():
    """Test performance of database operations."""
    print("Testing performance benchmarks...")

    try:
        sys.path.append('.')
        from utils.vehicle_data_simple import (
            get_vehicle_fuel_types,
            get_vehicle_brands,
            get_vehicle_models,
            get_vehicle_versions
        )

        # Test response times
        benchmarks = []

        # Test fuel types
        start_time = time.time()
        fuel_types = get_vehicle_fuel_types()
        fuel_time = time.time() - start_time
        benchmarks.append(("Fuel types", fuel_time))

        # Test brands
        start_time = time.time()
        brands = get_vehicle_brands("diesel")
        brands_time = time.time() - start_time
        benchmarks.append(("Brands", brands_time))

        # Test models
        start_time = time.time()
        models = get_vehicle_models("diesel", "Audi")
        models_time = time.time() - start_time
        benchmarks.append(("Models", models_time))

        # Test versions
        start_time = time.time()
        versions = get_vehicle_versions("diesel", "Audi", "A3")
        versions_time = time.time() - start_time
        benchmarks.append(("Versions", versions_time))

        # Print benchmarks
        print("Performance benchmarks:")
        slow_operations = []
        for operation, duration in benchmarks:
            print(f"  {operation}: {duration:.3f}s")
            if duration > 1.0:  # Consider slow if > 1 second
                slow_operations.append(operation)

        if slow_operations:
            print(f"WARNING: Slow operations detected: {slow_operations}")
            return False
        else:
            print("PASS: All operations under 1 second")
            return True

    except Exception as e:
        print(f"FAIL: Performance test failed - {e}")
        return False

def test_error_handling():
    """Test error handling in edge cases."""
    print("Testing error handling...")

    try:
        sys.path.append('.')
        from utils.vehicle_data_simple import (
            get_vehicle_brands,
            get_vehicle_models,
            get_vehicle_versions
        )

        error_count = 0

        # Test invalid fuel type
        result = get_vehicle_brands("invalid_fuel_type")
        if result != []:
            print("FAIL: Invalid fuel type should return empty list")
            error_count += 1

        # Test invalid brand
        result = get_vehicle_models("diesel", "InvalidBrand")
        if result != []:
            print("FAIL: Invalid brand should return empty list")
            error_count += 1

        # Test invalid model
        result = get_vehicle_versions("diesel", "Audi", "InvalidModel")
        if result != []:
            print("FAIL: Invalid model should return empty list")
            error_count += 1

        # Test empty parameters
        result = get_vehicle_models("", "Audi")
        if result != []:
            print("FAIL: Empty fuel type should return empty list")
            error_count += 1

        result = get_vehicle_versions("diesel", "", "A3")
        if result != []:
            print("FAIL: Empty brand should return empty list")
            error_count += 1

        if error_count == 0:
            print("PASS: Error handling working correctly")
            return True
        else:
            print(f"FAIL: {error_count} error handling tests failed")
            return False

    except Exception as e:
        print(f"FAIL: Error handling test failed - {e}")
        return False

def main():
    """Run comprehensive integration tests."""
    print("AstroTech App - Integration Test Suite")
    print("=" * 45)

    tests = [
        ("Complete Vehicle Flow", test_complete_vehicle_flow),
        ("Data Consistency", test_data_consistency),
        ("Performance Benchmarks", test_performance_benchmarks),
        ("Error Handling", test_error_handling)
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
    print("\n" + "=" * 45)
    print("INTEGRATION TEST SUMMARY")
    print("=" * 45)
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")

    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"{status}: {test_name}")

    if passed == total:
        print("\nSUCCESS: All integration tests passed!")
        print("Application is fully functional and ready!")
    else:
        print(f"\nFAILED: {total - passed} integration test(s) failed.")
        print("Please review the failing components.")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)