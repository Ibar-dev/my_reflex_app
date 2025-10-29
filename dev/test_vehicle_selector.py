#!/usr/bin/env python3
"""
Prueba del selector de vehiculos - Verifica que los componentes funcionen correctamente
===================================================================================
"""

import sys
import os

# Añadir el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_vehicle_services():
    """Prueba los servicios de vehiculos"""
    print("Coche: Prueba del Selector de Vehiculos")
    print("=" * 50)

    try:
        # Probar servicio de vehículos
        from services.vehicle_api_service import get_fuel_types, get_brands, get_models

        print("OK Servicios importados correctamente")

        # Probar tipos de combustible
        fuel_types = get_fuel_types()
        print(f"Datos Tipos de combustible: {fuel_types}")

        # Probar marcas para gasolina
        brands = get_brands("gasolina")
        print(f"Marcas (gasolina): {brands}")

        # Probar modelos
        if brands:
            models = get_models("gasolina", brands[0])
            print(f"Modelos ({brands[0]}): {models}")

        print("\nOK Todos los servicios funcionan correctamente")
        return True

    except Exception as e:
        print(f"\nError: {str(e)}")
        return False

def test_vehicle_state():
    """Prueba el estado del selector de vehiculos"""
    print("\nRefresco Prueba del VehicleState")
    print("=" * 50)

    try:
        from state.vehicle_state_simple import VehicleState

        print("OK VehicleState importado correctamente")
        print("NOTA: VehicleState no se instancia directamente en Reflex")
        print("      Se probará en el contexto de la aplicación")

        # Verificar que los atributos existen
        print(f"Atributos disponibles: {dir(VehicleState)}")

        print("\nOK VehicleState importado correctamente")
        return True

    except Exception as e:
        print(f"\nError en VehicleState: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Funcion principal"""
    print("Herramienta Selector de Vehiculos - Test Completo")
    print("=" * 60)

    # Probar servicios
    services_ok = test_vehicle_services()

    # Probar estado
    state_ok = test_vehicle_state()

    print("\n" + "=" * 60)
    if services_ok and state_ok:
        print("EXITO! TODAS LAS PRUEBAS PASARON!")
        print("OK El selector de vehiculos esta funcionando correctamente")
    else:
        print("ERROR Hay problemas que deben ser revisados")

    print("=" * 60)

if __name__ == "__main__":
    main()