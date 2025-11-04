#!/usr/bin/env python3
"""
Script para verificar el estado de producción y guiar la configuración
"""

import webbrowser
import time

def open_dashboard():
    """Abrir el dashboard de Reflex en el navegador"""
    print("Abriendo dashboard de Reflex...")
    webbrowser.open("https://console.reflex.run")

    print("\nInstrucciones:")
    print("=" * 50)
    print("1. Busca tu proyecto con ID: fdb58d37-e45b-4e5f-8197-213cff0219be")
    print("2. Haz clic en 'Settings'")
    print("3. Ve a 'Environment Variables'")
    print("4. Añade estas 7 variables exactamente:")

    env_vars = [
        "SUPABASE_URL=https://piexexjrjdgkunlezwcv.supabase.co",
        "SUPABASE_KEY=sbp_cbb2e381d1c44fcb8975f1272390433684c46451",
        "DB_USER=postgres.piexexjrjdgkunlezwcv",
        "DB_PASSWORD=CN2t6dlUk8zwTlx7",
        "DB_HOST=aws-1-eu-north-1.pooler.supabase.com",
        "DB_PORT=6543",
        "DB_NAME=postgres"
    ]

    for i, var in enumerate(env_vars, 1):
        print(f"   {i}. {var}")

    print("\n5. Haz clic en 'Save'")
    print("6. Espera 2-3 minutos para que se apliquen los cambios")
    print("7. Recarga tu aplicación: https://app-silver-grass.reflex.run")

def check_app_url():
    """Abrir la aplicación para probar"""
    print("\nAbriendo tu aplicación...")
    webbrowser.open("https://app-silver-grass.reflex.run")

    print("\nPara verificar que funciona:")
    print("=" * 30)
    print("1. Abre la consola del navegador (F12)")
    print("2. Busca estos mensajes:")
    print("   - [VEHICLE] Entorno actual: PROD")
    print("   - [VEHICLE] SUPABASE_URL configurada: https://piexex...")
    print("   - [VEHICLE] Tipos obtenidos de Supabase: ['Diesel', 'Gasolina']")
    print("3. Intenta usar el selector de vehículos")

def main():
    print("VERIFICACIÓN Y CONFIGURACIÓN DE PRODUCCIÓN")
    print("=" * 50)

    print("\nTu aplicación está desplegada en:")
    print("https://app-silver-grass.reflex.run")

    print("\nProblema: El selector no funciona porque faltan variables de entorno.")

    choice = input("\n¿Qué quieres hacer?\n1. Abrir dashboard para configurar variables\n2. Abrir aplicación para probar\n3. Ambos\nEscribe 1, 2, o 3: ")

    if choice == "1":
        open_dashboard()
    elif choice == "2":
        check_app_url()
    elif choice == "3":
        open_dashboard()
        input("\nPresiona Enter después de configurar las variables...")
        check_app_url()
    else:
        print("Opción no válida")

if __name__ == "__main__":
    main()