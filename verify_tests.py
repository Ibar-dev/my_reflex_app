#!/usr/bin/env python3
"""
Verificación simple de los tests del selector de vehículos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verify_imports():
    """Verificar que todos los imports en los tests funcionen"""
    print("Verificando imports en los tests...")

    try:
        # Verificar import del conftest
        import tests.conftest
        print("conftest.py - Imports correctos")

        # Verificar fixtures
        from tests.conftest import base_url, test_data
        print("Fixtures base_url y test_data - OK")

        # Verificar datos de prueba
        data = test_data()
        print(f"Tipos de combustible en test_data: {list(data['vehicles'].keys())}")

        # Verificar que no haya caracteres problemáticos
        for fuel_type, vehicle_data in data['vehicles'].items():
            selection = vehicle_data['sample_selection']
            print(f"{fuel_type}: {selection['brand']} {selection['model']} {selection['version']}")

        return True

    except Exception as e:
        print(f"Error en imports: {e}")
        return False

def verify_test_syntax():
    """Verificar sintaxis del archivo de tests"""
    print("\nVerificando sintaxis de test_vehicle_selector_ui.py...")

    try:
        # Compilar el archivo para verificar sintaxis
        with open('tests/test_vehicle_selector_ui.py', 'r', encoding='utf-8') as f:
            content = f.read()

        # Reemplazar caracteres problemáticos si existen
        content = content.replace('🚀', '')
        content = content.replace('✅', '')
        content = content.replace('⚠️', '')
        content = content.replace('❌', '')
        content = content.replace('⏳', '')
        content = content.replace('🧹', '')

        # Intentar compilar
        compile(content, 'tests/test_vehicle_selector_ui.py', 'exec')
        print("Sintaxis de test_vehicle_selector_ui.py - OK")
        return True

    except SyntaxError as e:
        print(f"Error de sintaxis: {e}")
        return False
    except Exception as e:
        print(f"Error verificando sintaxis: {e}")
        return False

def verify_xpath_selectors():
    """Verificar que los selectores XPath sean consistentes"""
    print("\nVerificando selectores XPath...")

    try:
        with open('tests/test_vehicle_selector_ui.py', 'r', encoding='utf-8') as f:
            content = f.read()

        # Buscar selectores XPath
        import re

        # Selectores esperados
        expected_selectors = [
            "Selecciona el tipo de combustible",
            "Selecciona la marca",
            "Selecciona el modelo",
            "Selecciona la versión"
        ]

        issues = []
        for selector in expected_selectors:
            xpath_pattern = f'contains(@placeholder, \'{selector}\')'
            if xpath_pattern not in content:
                issues.append(f"Falta selector: {selector}")

        # Verificar que no queden selectores viejos
        old_selectors = ["combustible", "marca", "modelo", "versión"]
        for old in old_selectors:
            if f'contains(@placeholder, \'{old}\')' in content:
                issues.append(f"Selector viejo encontrado: '{old}'")

        if issues:
            for issue in issues:
                print(f"ERROR: {issue}")
            return False
        else:
            print("Selectores XPath - OK")
            return True

    except Exception as e:
        print(f"Error verificando selectores: {e}")
        return False

def main():
    """Función principal"""
    print("VERIFICACION DE TESTS DEL SELECTOR DE VEHICULOS")
    print("=" * 60)

    all_good = True

    # Verificar imports
    if not verify_imports():
        all_good = False

    # Verificar sintaxis
    if not verify_test_syntax():
        all_good = False

    # Verificar selectores
    if not verify_xpath_selectors():
        all_good = False

    print("\n" + "=" * 60)
    if all_good:
        print("TODAS LAS VERIFICACIONES PASARON")
        print("\nLos tests estan listos para ejecutarse con:")
        print("  pytest tests/test_vehicle_selector_ui.py -v")
        print("\nPara ejecutar un test especifico:")
        print("  pytest tests/test_vehicle_selector_ui.py::TestVehicleSelectorUI::test_fuel_type_selector_loaded -v")
    else:
        print("HAY PROBLEMAS QUE NECESITAN SER REPARADOS")

    return all_good

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)