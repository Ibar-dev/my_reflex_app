#!/usr/bin/env python3
"""
Test para verificar configuración de producción
"""

import os
import sys

def test_env_vars():
    """Verificar variables de entorno"""
    required = [
        'SUPABASE_URL',
        'SUPABASE_KEY',
        'DB_USER',
        'DB_PASSWORD',
        'DB_HOST',
        'DB_PORT',
        'DB_NAME'
    ]

    missing = []
    for var in required:
        if not os.getenv(var):
            missing.append(var)

    if missing:
        print(f"FALTAN variables: {missing}")
        return False
    else:
        print("[OK] Todas las variables de entorno configuradas")
        return True

def test_supabase():
    """Probar conexión a Supabase"""
    try:
        from utils.supabase_connection import db
        from utils.vehicle_data_supabase import get_vehicle_fuel_types

        if db.connect():
            fuel_types = get_vehicle_fuel_types()
            print(f"[OK] Conexión OK: {len(fuel_types)} combustibles")
            db.disconnect()
            return True
        else:
            print("[FAIL] No se conectó")
            return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

if __name__ == "__main__":
    print("VERIFICACIÓN DE PRODUCCIÓN")
    print("=" * 30)

    env_ok = test_env_vars()
    conn_ok = test_supabase()

    if env_ok and conn_ok:
        print("\n[SUCCESS] Todo listo para producción")
    else:
        print("\n[WARNING] Configura variables de entorno en Reflex Deploy")