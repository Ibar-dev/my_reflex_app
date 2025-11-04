#!/usr/bin/env python3
"""
Verificación de Configuración de Supabase - AstroTech
==================================================

Este script ayuda a verificar la configuración de Supabase
y genera instrucciones para configurar CORS correctamente.
"""

import os
import sys

def print_cors_instructions():
    """Imprimir instrucciones para configurar CORS en Supabase"""
    print("\n" + "="*60)
    print("CONFIGURACIÓN DE CORS EN SUPABASE")
    print("="*60)

    print("\n1. Ve a tu dashboard de Supabase:")
    print("   https://supabase.com/dashboard")

    print("\n2. Selecciona tu proyecto:")
    print("   piexexjrjdgkunlezwcv")

    print("\n3. Ve a Settings > API:")
    print("   - En el menú lateral izquierdo, haz clic en 'Settings'")
    print("   - Luego haz clic en 'API'")

    print("\n4. Configura CORS:")
    print("   - Busca la sección 'Additional CORS Settings'")
    print("   - Añade estas URLs:")

    # URLs típicas de Reflex Deploy
    urls = [
        "http://localhost:3000",
        "https://*.reflex.run",
        "https://*.reflex.dev",
        "https://app-{project-name}.reflex.run",
        "https://{project-name}.reflex.run"
    ]

    for url in urls:
        print(f"     • {url}")

    print("\n5. Métodos permitidos:")
    print("   - GET, POST, PUT, DELETE, OPTIONS")

    print("\n6. Headers permitidos:")
    print("   - authorization, content-type, x-client-info")

    print("\n7. Haz clic en 'Save' para guardar los cambios")

def check_current_env():
    """Verificar configuración actual"""
    print("VERIFICACIÓN DE CONFIGURACIÓN ACTUAL")
    print("="*40)

    # Verificar archivo .env
    env_file = Path(".env")
    if env_file.exists():
        print("✅ Archivo .env encontrado")

        with open(env_file, 'r') as f:
            content = f.read()

        if "SUPABASE_URL=" in content:
            print("✅ SUPABASE_URL configurada")
        else:
            print("❌ SUPABASE_URL no encontrada")

        if "SUPABASE_KEY=" in content:
            print("✅ SUPABASE_KEY configurada")
        else:
            print("❌ SUPABASE_KEY no encontrada")
    else:
        print("❌ Archivo .env no encontrado")

    # Verificar variables de entorno actuales
    print("\nVariables de entorno en proceso actual:")
    supabase_url = os.getenv("SUPABASE_URL")
    if supabase_url:
        print(f"✅ SUPABASE_URL: {supabase_url[:30]}...")
    else:
        print("❌ SUPABASE_URL no configurada en proceso")

    supabase_key = os.getenv("SUPABASE_KEY")
    if supabase_key:
        print(f"✅ SUPABASE_KEY: {supabase_key[:20]}...")
    else:
        print("❌ SUPABASE_KEY no configurada en proceso")

def create_env_export():
    """Crear comandos para exportar variables de entorno"""
    print("\n" + "="*60)
    print("COMANDOS PARA CONFIGURAR VARIABLES DE ENTORNO")
    print("="*60)

    print("\nPara Reflex Deploy (Dashboard):")
    print("Añade estas variables en el dashboard de Reflex:")

    env_vars = [
        "SUPABASE_URL=https://piexexjrjdgkunlezwcv.supabase.co",
        "SUPABASE_KEY=sbp_cbb2e381d1c44fcb8975f1272390433684c46451",
        "DB_USER=postgres.piexexjrjdgkunlezwcv",
        "DB_PASSWORD=CN2t6dlUk8zwTlx7",
        "DB_HOST=aws-1-eu-north-1.pooler.supabase.com",
        "DB_PORT=6543",
        "DB_NAME=postgres"
    ]

    for var in env_vars:
        print(f"  • {var}")

    print("\nPara entorno local (terminal):")
    print("Copia y pega estos comandos:")
    for var in env_vars:
        print(f"  export {var}")

def test_connection_details():
    """Probar conexión con detalles"""
    try:
        sys.path.insert(0, '.')
        from utils.supabase_connection import db
        import psycopg2

        print("\n" + "="*60)
        print("DETALLES DE CONEXIÓN A SUPABASE")
        print("="*60)

        # Obtener parámetros de conexión
        params = {
            'host': os.getenv('DB_HOST', 'aws-1-eu-north-1.pooler.supabase.com'),
            'port': os.getenv('DB_PORT', '6543'),
            'database': os.getenv('DB_NAME', 'postgres'),
            'user': os.getenv('DB_USER', 'postgres.piexexjrjdgkunlezwcv'),
            'password': os.getenv('DB_PASSWORD', 'CN2t6dlUk8zwTlx7')
        }

        print("Parámetros de conexión:")
        print(f"  Host: {params['host']}")
        print(f"  Port: {params['port']}")
        print(f"  Database: {params['database']}")
        print(f"  User: {params['user']}")
        print(f"  Password: {'*' * len(params['password'])}")

        # Probar conexión
        conn = psycopg2.connect(**params)
        cursor = conn.cursor()

        # Verificar tabla vehicles
        cursor.execute("SELECT COUNT(*) FROM vehicles;")
        count = cursor.fetchone()[0]
        print(f"\n✅ Conexión exitosa")
        print(f"✅ Tabla vehicles encontrada con {count} registros")

        # Verificar tipos de combustible
        cursor.execute("SELECT DISTINCT fuel_type FROM vehicles ORDER BY fuel_type;")
        fuel_types = [row[0] for row in cursor.fetchall()]
        print(f"✅ Tipos de combustible: {fuel_types}")

        cursor.close()
        conn.close()

        return True

    except Exception as e:
        print(f"❌ Error en conexión: {e}")
        return False

def main():
    """Función principal"""
    print("VERIFICACIÓN COMPLETA DE SUPABASE - ASTROTECH")
    print("=" * 50)

    check_current_env()
    test_connection_details()
    print_cors_instructions()
    create_env_export()

    print(f"\n{'='*60}")
    print("PRÓXIMOS PASOS:")
    print("="*60)
    print("1. Configura CORS en Supabase (sigue las instrucciones arriba)")
    print("2. Añade variables de entorno en Reflex Deploy")
    print("3. Haz deploy nuevamente: reflex deploy")
    print("4. Verifica que el selector funcione en producción")
    print("="*60)

if __name__ == "__main__":
    from pathlib import Path
    main()