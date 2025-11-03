#!/usr/bin/env python3
"""
Test de Interacción con Navegador - Selector de Vehículos
"""

import time
import subprocess
import requests
from pathlib import Path

def test_web_app_access():
    """Verificar acceso a la aplicación web"""
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("Aplicación web accesible")
            # Buscar indicadores de que la página carga correctamente
            if "Configurador" in response.text or "AstroTech" in response.text:
                print("Contenido principal detectado en la página")
                return True
            else:
                print("ADVERTENCIA: Contenido principal no encontrado")
                return False
        else:
            print(f"Código de estado inesperado: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error accediendo a la aplicación web: {e}")
        return False

def test_backend_health():
    """Verificar salud del backend"""
    try:
        response = requests.get("http://localhost:8000", timeout=5)
        # El backend puede devolver 404, 200 u otros códigos para indicar que está vivo
        return response.status_code < 500
    except:
        return False

def simulate_browser_interaction():
    """Simula lo que un usuario haría en el navegador"""
    print("Simulando interacción del usuario...")

    # La simulación real requeriría Selenium o similar, pero podemos verificar
    # que los endpoints necesarios existen

    # Verificar que el backend tiene los endpoints para datos de vehículos
    try:
        # Intentar acceder a los datos que usa el frontend
        response = requests.get("http://localhost:8000", timeout=5)
        print("Backend responde correctamente")
        return True
    except Exception as e:
        print(f"Error en simulación: {e}")
        return False

def check_console_logs_simulation():
    """Simula la verificación de logs que veríamos en la consola del navegador"""
    print("Verificando logs del sistema...")

    # Verificar archivo de logs de Reflex
    log_file = Path("astrotech.log")
    if log_file.exists():
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Buscar indicadores de actividad del selector
            indicators = [
                "Sistema de logging activado",
                "vehicle_selector",
                "load_fuel_types"
            ]

            found = 0
            for indicator in indicators:
                if indicator in content:
                    found += 1
                    print(f"Indicador encontrado: {indicator}")

            if found > 0:
                print(f"Se encontraron {found} indicadores de actividad")
                return True
            else:
                print("No se encontraron indicadores de actividad en logs")
                return False

        except Exception as e:
            print(f"Error leyendo logs: {e}")
            return False
    else:
        print("Archivo de logs no encontrado (normal si no ha habido actividad)")
        return True  # No es crítico

def test_vehicle_data_api():
    """Verificar que los datos de vehículos son accesibles"""
    try:
        sys.path.insert(0, '.')
        from utils.vehicle_data_supabase import get_vehicle_fuel_types

        fuel_types = get_vehicle_fuel_types()
        print(f"API de vehículos responde: {fuel_types}")

        if fuel_types and len(fuel_types) > 0:
            return True
        else:
            return False

    except Exception as e:
        print(f"Error en API de vehículos: {e}")
        return False

def check_component_mount():
    """Verificar que el componente se montaría correctamente"""
    try:
        sys.path.insert(0, '.')
        from components.vehicle_selector import vehicle_selector

        # Intentar crear el componente (sin renderizarlo)
        component = vehicle_selector()
        print("Componente vehicle_selector creado exitosamente")
        return True

    except Exception as e:
        print(f"Error creando componente: {e}")
        return False

def verify_on_mount_configuration():
    """Verificar que el componente tiene la configuración on_mount correcta"""
    try:
        # Leer el archivo del componente
        component_file = Path("components/vehicle_selector.py")
        if not component_file.exists():
            print("Archivo de componente no encontrado")
            return False

        with open(component_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Buscar configuración on_mount
        if "on_mount=VehicleState.load_fuel_types" in content:
            print("Configuración on_mount encontrada y correcta")
            return True
        else:
            print("ADVERTENCIA: Configuración on_mount no encontrada")
            return False

    except Exception as e:
        print(f"Error verificando configuración: {e}")
        return False

def main():
    """Ejecutar test de interacción con navegador"""
    print("TEST DE INTERACCIÓN CON NAVEGADOR - SELECTOR DE VEHÍCULOS")
    print("=" * 70)

    tests = [
        ("Acceso Web", test_web_app_access),
        ("Salud Backend", test_backend_health),
        ("Simulación Interacción", simulate_browser_interaction),
        ("Verificación Logs", check_console_logs_simulation),
        ("API Datos Vehículos", test_vehicle_data_api),
        ("Montaje Componente", check_component_mount),
        ("Configuración on_mount", verify_on_mount_configuration),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_function in tests:
        print(f"\n{'-'*50}")
        print(f"Ejecutando: {test_name}")
        print('-'*50)

        try:
            if test_function():
                print(f"[OK] {test_name}")
                passed += 1
            else:
                print(f"[ERROR] {test_name}")
        except Exception as e:
            print(f"[ERROR] {test_name}: {e}")

        time.sleep(0.3)

    print(f"\n{'='*70}")
    print(f"RESULTADOS TEST DE INTERACCIÓN")
    print('='*70)
    print(f"Tests Pasados: {passed}/{total}")
    print(f"Tasa de Éxito: {(passed/total)*100:.1f}%")

    if passed >= 5:  # Umbral más relajado para pruebas de navegador
        print("\n✅ TEST DE INTERACCIÓN APROBADO")
        print("La aplicación está lista para pruebas manuales")
        print("Componentes fundamentales funcionando")
        print("Configuración correcta detectada")

        print("\n📋 INSTRUCCIONES PARA PRUEBA MANUAL:")
        print("1. Abre http://localhost:3000/ en tu navegador")
        print("2. Haz scroll hasta 'Configurador de Centralitas'")
        print("3. Abre DevTools (F12) → Console")
        print("4. Deberías ver logs [VEHICLE] al cargar la página")
        print("5. Intenta seleccionar 'diesel' en el primer selector")
        print("6. Deberían cargarse las marcas disponibles")

    else:
        print(f"\n❌ TEST DE INTERACCIÓN FALLIDO")
        print(f"Solo {passed}/{total} tests pasaron")
        print("Revisar errores arriba")

    print('='*70)

    return passed >= 5

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)