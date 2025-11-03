#!/usr/bin/env python3
"""
Script de diagnóstico para producción - AstroTech
===============================================

Verifica la configuración y conectividad en el entorno actual.
"""

import os
import sys

def check_environment():
    """Verificar el entorno actual"""
    print(f"Entorno actual: {os.getenv('RX_ENV', 'DEV (default)')}")
    print(f"Python path: {sys.executable}")
    print(f"Directorio actual: {os.getcwd()}")

def check_supabase_env():
    """Verificar variables de entorno de Supabase"""
    required_vars = [
        'SUPABASE_URL',
        'SUPABASE_KEY',
        'DB_USER',
        'DB_PASSWORD',
        'DB_HOST',
        'DB_PORT',
        'DB_NAME'
    ]

    print("\nVariables de entorno de Supabase:")
    missing_vars = []

    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Ocultar información sensible
            if 'PASSWORD' in var or 'KEY' in var:
                display_value = f"{value[:8]}...{value[-4:]}" if len(value) > 12 else "***"
            else:
                display_value = value
            print(f"  {var}: {display_value}")
        else:
            print(f"  {var}: [FALTANTE]")
            missing_vars.append(var)

    return len(missing_vars) == 0

def test_supabase_connection():
    """Probar conexión a Supabase"""
    try:
        sys.path.insert(0, '.')
        from utils.supabase_connection import db

        print("\nProbando conexión a Supabase...")
        if db.connect():
            print("[OK] Conexión exitosa")

            # Probar consulta simple
            from utils.vehicle_data_supabase import get_vehicle_count
            count = get_vehicle_count()
            print(f"[OK] Vehículos encontrados: {count}")

            db.disconnect()
            return True
        else:
            print("[FAIL] No se pudo conectar")
            return False

    except Exception as e:
        print(f"[ERROR] Error en conexión: {e}")
        return False

def main():
    """Ejecutar diagnóstico completo"""
    print("DIAGNÓSTICO DE PRODUCCIÓN - ASTROTECH")
    print("=" * 50)

    check_environment()
    env_ok = check_supabase_env()
    conn_ok = test_supabase_connection()

    print(f"\n{'='*50}")
    print("RESUMEN:")
    print(f"Variables de entorno: {'OK' if env_ok else 'FAIL'}")
    print(f"Conexión Supabase: {'OK' if conn_ok else 'FAIL'}")

    if env_ok and conn_ok:
        print("\n[SUCCESS] Todo configurado correctamente")
        return True
    else:
        print("\n[WARNING] Hay problemas que necesitan solucionarse")
        if not env_ok:
            print("- Configura las variables de entorno en Reflex Deploy")
        if not conn_ok:
            print("- Verifica las credenciales y conectividad a Supabase")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)