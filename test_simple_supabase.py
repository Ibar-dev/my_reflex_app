#!/usr/bin/env python3
"""
Test Simple de Integración con Supabase - AstroTech
===============================================

Verificación básica de la conexión y funcionamiento con Supabase.
"""

import sys
import os

def test_connection():
    """Verificar la conexión a Supabase"""
    try:
        sys.path.insert(0, '.')
        from utils.supabase_connection import db

        if db.connect():
            print("[OK] Conexión a Supabase establecida")
            db.disconnect()
            return True
        else:
            print("[FAIL] No se pudo conectar a Supabase")
            return False

    except Exception as e:
        print(f"[ERROR] Error en conexión: {e}")
        return False

def test_basic_functions():
    """Verificar funciones básicas de vehículos"""
    try:
        sys.path.insert(0, '.')
        from utils.vehicle_data_supabase import get_vehicle_count, get_vehicle_fuel_types

        # Test básico
        count = get_vehicle_count()
        print(f"[INFO] Total vehículos: {count}")

        fuel_types = get_vehicle_fuel_types()
        print(f"[INFO] Tipos de combustible: {fuel_types}")

        return count > 0 and len(fuel_types) > 0

    except Exception as e:
        print(f"[ERROR] Error en funciones básicas: {e}")
        return False

def main():
    """Ejecutar tests"""
    print("TEST DE INTEGRACION CON SUPABASE")
    print("=" * 40)

    tests = [
        ("Conexion", test_connection),
        ("Funciones Basicas", test_basic_functions),
    ]

    passed = 0
    for name, test_func in tests:
        print(f"\n{name}:")
        if test_func():
            passed += 1
            print(f"[OK] {name} PASSED")
        else:
            print(f"[FAIL] {name} FAILED")

    print(f"\nRESULT: {passed}/{len(tests)} tests passed")
    return passed == len(tests)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)