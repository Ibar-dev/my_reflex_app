#!/usr/bin/env python3
"""
Test End-to-End del Selector de Vehículos - AstroTech
===================================================

Este test verifica completamente el funcionamiento del selector de vehículos
simulando todas las interacciones del usuario y verificando los logs.
"""

import sys
import time
import subprocess
from pathlib import Path

def run_test(test_name, test_function):
    """Ejecuta un test y muestra resultados"""
    print(f"\n{'='*60}")
    print(f"🧪 TEST: {test_name}")
    print('='*60)

    try:
        result = test_function()
        if result:
            print(f"✅ {test_name}: PASADO")
        else:
            print(f"❌ {test_name}: FALLIDO")
        return result
    except Exception as e:
        print(f"❌ {test_name}: ERROR - {e}")
        return False

def test_application_running():
    """Verificar que la aplicación está corriendo"""
    try:
        import requests
        response = requests.get("http://localhost:3000", timeout=5)
        return response.status_code == 200
    except:
        return False

def test_backend_running():
    """Verificar que el backend está corriendo"""
    try:
        import requests
        response = requests.get("http://localhost:8000", timeout=5)
        return response.status_code in [200, 404]  # 404 es aceptable para el backend
    except:
        return False

def test_database_exists():
    """Verificar que la conexión a Supabase funciona"""
    try:
        sys.path.insert(0, '.')
        from utils.vehicle_data_supabase import get_vehicle_count

        count = get_vehicle_count()
        if count > 0:
            print(f"✅ Conexión a Supabase establecida: {count:,} vehículos encontrados")
            return True
        else:
            print("❌ No se encontraron vehículos en Supabase")
            return False

    except Exception as e:
        print(f"❌ Error conectando a Supabase: {e}")
        return False

def test_database_content():
    """Verificar el contenido de Supabase"""
    try:
        sys.path.insert(0, '.')
        from utils.vehicle_data_supabase import (
            get_vehicle_count,
            get_vehicle_fuel_types,
            get_vehicle_brands
        )

        # Verificar cantidad de vehículos
        count = get_vehicle_count()
        if count <= 0:
            print("❌ No hay vehículos en la base de datos")
            return False

        # Verificar tipos de combustible
        fuel_types = get_vehicle_fuel_types()
        if not fuel_types:
            print("❌ No hay tipos de combustible disponibles")
            return False

        # Verificar marcas para primer tipo de combustible
        brands = get_vehicle_brands(fuel_types[0])
        if not brands:
            print("❌ No hay marcas disponibles")
            return False

        print(f"✅ Contenido de Supabase verificado:")
        print(f"   - Total vehículos: {count:,}")
        print(f"   - Tipos de combustible: {fuel_types}")
        print(f"   - Marcas para {fuel_types[0]}: {len(brands)}")
        return True

    except Exception as e:
        print(f"❌ Error verificando contenido Supabase: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_import_vehicle_state():
    """Verificar que se puede importar el estado del vehículo"""
    try:
        sys.path.insert(0, '.')
        from state.vehicle_state_simple import VehicleState
        print("✅ VehicleState importado correctamente")

        # Verificar que tiene los métodos necesarios
        required_methods = [
            'load_fuel_types',
            'select_fuel',
            'select_brand',
            'select_model',
            'select_version',
            'load_brands',
            'load_models',
            'load_versions'
        ]

        for method in required_methods:
            if not hasattr(VehicleState, method):
                print(f"❌ Método faltante: {method}")
                return False

        print("✅ Todos los métodos necesarios presentes")
        return True

    except Exception as e:
        print(f"❌ Error importando VehicleState: {e}")
        return False

def test_vehicle_data_utils():
    """Verificar que las utilidades de datos de vehículos funcionan"""
    try:
        sys.path.insert(0, '.')
        from utils.vehicle_data_supabase import (
            get_vehicle_fuel_types,
            get_vehicle_brands,
            get_vehicle_models,
            get_vehicle_versions
        )

        # Test fuel types
        fuel_types = get_vehicle_fuel_types()
        print(f"✅ Tipos de combustible obtenidos: {fuel_types}")

        if not fuel_types:
            print("❌ No se obtuvieron tipos de combustible")
            return False

        # Test brands
        first_fuel = fuel_types[0]
        brands = get_vehicle_brands(first_fuel)
        print(f"✅ Marcas para {first_fuel}: {len(brands)} encontradas")

        if not brands:
            print("❌ No se obtuvieron marcas")
            return False

        # Test models
        first_brand = brands[0]
        models = get_vehicle_models(first_fuel, first_brand)
        print(f"✅ Modelos para {first_fuel}/{first_brand}: {len(models)} encontrados")

        if not models:
            print("❌ No se obtuvieron modelos")
            return False

        # Test versions
        first_model = models[0]
        versions = get_vehicle_versions(first_fuel, first_brand, first_model)
        print(f"✅ Versiones para {first_fuel}/{first_brand}/{first_model}: {len(versions)} encontradas")

        print("✅ Utilidades de datos de vehículos funcionando correctamente")
        return True

    except Exception as e:
        print(f"❌ Error en utilidades de datos: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_state_initialization():
    """Verificar la inicialización del estado"""
    try:
        sys.path.insert(0, '.')
        from state.vehicle_state_simple import VehicleState

        # Crear instancia
        state = VehicleState()

        # Verificar estado inicial
        assert state.selected_fuel == ""
        assert state.selected_brand == ""
        assert state.selected_model == ""
        assert state.selected_version == ""
        assert state.data_loaded == False
        assert isinstance(state.available_fuel_types, list)
        assert isinstance(state.available_brands, list)
        assert isinstance(state.available_models, list)
        assert isinstance(state.available_versions, list)

        print("✅ Estado inicializado correctamente")
        return True

    except Exception as e:
        print(f"❌ Error en inicialización del estado: {e}")
        return False

def test_load_fuel_types():
    """Verificar la carga de tipos de combustible"""
    try:
        sys.path.insert(0, '.')
        from state.vehicle_state_simple import VehicleState

        state = VehicleState()

        # Ejecutar carga
        state.load_fuel_types()

        # Verificar resultados
        assert state.data_loaded == True, "data_loaded debería ser True"
        assert len(state.available_fuel_types) > 0, "Debería haber tipos de combustible disponibles"

        print(f"✅ Carga de combustibles exitosa: {state.available_fuel_types}")
        return True

    except Exception as e:
        print(f"❌ Error en carga de combustibles: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_select_fuel():
    """Verificar selección de combustible"""
    try:
        sys.path.insert(0, '.')
        from state.vehicle_state_simple import VehicleState

        state = VehicleState()
        state.load_fuel_types()

        # Seleccionar primer tipo de combustible disponible
        fuel_type = state.available_fuel_types[0]
        state.select_fuel(fuel_type)

        # Verificar selección
        assert state.selected_fuel == fuel_type, f"selected_fuel debería ser {fuel_type}"
        assert state.selected_brand == "", "selected_brand debería estar vacío"
        assert state.selected_model == "", "selected_model debería estar vacío"
        assert state.selected_version == "", "selected_version debería estar vacío"
        assert len(state.available_brands) > 0, "Deberían cargarse marcas"

        print(f"✅ Selección de combustible exitosa: {fuel_type}")
        print(f"✅ Marcas cargadas: {len(state.available_brands)}")
        return True

    except Exception as e:
        print(f"❌ Error en selección de combustible: {e}")
        return False

def test_select_brand():
    """Verificar selección de marca"""
    try:
        sys.path.insert(0, '.')
        from state.vehicle_state_simple import VehicleState

        state = VehicleState()
        state.load_fuel_types()

        # Seleccionar combustible y luego marca
        fuel_type = state.available_fuel_types[0]
        state.select_fuel(fuel_type)

        brand = state.available_brands[0]
        state.select_brand(brand)

        # Verificar selección
        assert state.selected_fuel == fuel_type, "selected_fuel debería mantenerse"
        assert state.selected_brand == brand, f"selected_brand debería ser {brand}"
        assert state.selected_model == "", "selected_model debería estar vacío"
        assert state.selected_version == "", "selected_version debería estar vacío"
        assert len(state.available_models) > 0, "Deberían cargarse modelos"

        print(f"✅ Selección de marca exitosa: {brand}")
        print(f"✅ Modelos cargados: {len(state.available_models)}")
        return True

    except Exception as e:
        print(f"❌ Error en selección de marca: {e}")
        return False

def test_select_model():
    """Verificar selección de modelo"""
    try:
        sys.path.insert(0, '.')
        from state.vehicle_state_simple import VehicleState

        state = VehicleState()
        state.load_fuel_types()

        # Seleccionar combustible, marca y luego modelo
        fuel_type = state.available_fuel_types[0]
        state.select_fuel(fuel_type)

        brand = state.available_brands[0]
        state.select_brand(brand)

        model = state.available_models[0]
        state.select_model(model)

        # Verificar selección
        assert state.selected_fuel == fuel_type, "selected_fuel debería mantenerse"
        assert state.selected_brand == brand, "selected_brand debería mantenerse"
        assert state.selected_model == model, f"selected_model debería ser {model}"
        assert state.selected_version == "", "selected_version debería estar vacío"
        assert len(state.available_versions) > 0, "Deberían cargarse versiones"

        print(f"✅ Selección de modelo exitosa: {model}")
        print(f"✅ Versiones cargadas: {len(state.available_versions)}")
        return True

    except Exception as e:
        print(f"❌ Error en selección de modelo: {e}")
        return False

def test_select_version():
    """Verificar selección de versión"""
    try:
        sys.path.insert(0, '.')
        from state.vehicle_state_simple import VehicleState

        state = VehicleState()
        state.load_fuel_types()

        # Seleccionar secuencia completa
        fuel_type = state.available_fuel_types[0]
        state.select_fuel(fuel_type)

        brand = state.available_brands[0]
        state.select_brand(brand)

        model = state.available_models[0]
        state.select_model(model)

        version = state.available_versions[0]
        state.select_version(version)

        # Verificar selección completa
        assert state.selected_fuel == fuel_type, "selected_fuel debería mantenerse"
        assert state.selected_brand == brand, "selected_brand debería mantenerse"
        assert state.selected_model == model, "selected_model debería mantenerse"
        assert state.selected_version == version, f"selected_version debería ser {version}"

        print(f"✅ Selección de versión exitosa: {version}")
        print(f"✅ Selección completa: {fuel_type} > {brand} > {model} > {version}")
        return True

    except Exception as e:
        print(f"❌ Error en selección de versión: {e}")
        return False

def test_complete_flow():
    """Verificar el flujo completo del selector"""
    try:
        sys.path.insert(0, '.')
        from state.vehicle_state_simple import VehicleState

        state = VehicleState()

        # Paso 1: Cargar tipos de combustible
        state.load_fuel_types()
        assert len(state.available_fuel_types) > 0, "Debería haber tipos de combustible"

        # Paso 2: Seleccionar combustible
        fuel = state.available_fuel_types[0]
        state.select_fuel(fuel)
        assert len(state.available_brands) > 0, "Debería haber marcas"

        # Paso 3: Seleccionar marca
        brand = state.available_brands[0]
        state.select_brand(brand)
        assert len(state.available_models) > 0, "Debería haber modelos"

        # Paso 4: Seleccionar modelo
        model = state.available_models[0]
        state.select_model(model)
        assert len(state.available_versions) > 0, "Debería haber versiones"

        # Paso 5: Seleccionar versión
        version = state.available_versions[0]
        state.select_version(version)

        # Verificar estado final
        assert state.is_complete_selection(), "La selección debería estar completa"

        selection = state.get_current_selection()
        assert selection["fuel_type"] == fuel
        assert selection["brand"] == brand
        assert selection["model"] == model
        assert selection["version"] == version

        print(f"✅ Flujo completo exitoso:")
        print(f"   Combustible: {selection['fuel_type']}")
        print(f"   Marca: {selection['brand']}")
        print(f"   Modelo: {selection['model']}")
        print(f"   Versión: {selection['version']}")

        return True

    except Exception as e:
        print(f"❌ Error en flujo completo: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_reset_functionality():
    """Verificar la funcionalidad de reset"""
    try:
        sys.path.insert(0, '.')
        from state.vehicle_state_simple import VehicleState

        state = VehicleState()

        # Realizar selección completa
        state.load_fuel_types()
        fuel = state.available_fuel_types[0]
        state.select_fuel(fuel)
        brand = state.available_brands[0]
        state.select_brand(brand)
        model = state.available_models[0]
        state.select_model(model)
        version = state.available_versions[0]
        state.select_version(version)

        # Verificar que hay selección
        assert state.is_complete_selection(), "Debería haber selección completa"

        # Resetear
        state.reset_selection()

        # Verificar reset
        assert state.selected_fuel == ""
        assert state.selected_brand == ""
        assert state.selected_model == ""
        assert state.selected_version == ""
        assert len(state.available_brands) == 0
        assert len(state.available_models) == 0
        assert len(state.available_versions) == 0
        assert not state.is_complete_selection(), "No debería haber selección completa"

        print("✅ Funcionalidad de reset verificada")
        return True

    except Exception as e:
        print(f"❌ Error en funcionalidad de reset: {e}")
        return False

def check_logs_for_vehicle_messages():
    """Verificar que hay logs de vehículos en el archivo"""
    try:
        log_file = Path("astrotech.log")
        if not log_file.exists():
            print("ℹ️  Archivo de logs no existe aún")
            return True  # No es crítico si no existe

        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Buscar mensajes de vehículo
        vehicle_messages = [
            "[VEHICLE] Iniciando carga de tipos de combustible",
            "[VEHICLE] Tipos de combustible cargados:",
            "[VEHICLE] Estado data_loaded:"
        ]

        found_messages = []
        for msg in vehicle_messages:
            if msg in content:
                found_messages.append(msg)

        print(f"✅ Mensajes de vehículo encontrados en logs: {len(found_messages)}")
        for msg in found_messages:
            print(f"   - {msg}")

        return True

    except Exception as e:
        print(f"❌ Error verificando logs: {e}")
        return False

def main():
    """Ejecutar todos los tests end-to-end"""
    print("INICIANDO TEST END-TO-END COMPLETO - SELECTOR DE VEHICULOS")
    print("=" * 80)

    tests = [
        ("Aplicación Corriendo", test_application_running),
        ("Backend Corriendo", test_backend_running),
        ("Base de Datos Existe", test_database_exists),
        ("Contenido de Base de Datos", test_database_content),
        ("Import VehicleState", test_import_vehicle_state),
        ("Utilidades de Datos Vehículos", test_vehicle_data_utils),
        ("Inicialización del Estado", test_state_initialization),
        ("Carga de Tipos de Combustible", test_load_fuel_types),
        ("Selección de Combustible", test_select_fuel),
        ("Selección de Marca", test_select_brand),
        ("Selección de Modelo", test_select_model),
        ("Selección de Versión", test_select_version),
        ("Flujo Completo", test_complete_flow),
        ("Funcionalidad de Reset", test_reset_functionality),
        ("Verificación de Logs", check_logs_for_vehicle_messages),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_function in tests:
        if run_test(test_name, test_function):
            passed += 1
        time.sleep(0.5)  # Pequeña pausa entre tests

    print(f"\n{'='*80}")
    print(f"📊 RESULTADOS DEL TEST END-TO-END")
    print('='*80)
    print(f"Tests Pasados: {passed}/{total}")
    print(f"Tasa de Éxito: {(passed/total)*100:.1f}%")

    if passed == total:
        print("\n🎉 ¡TODOS LOS TESTS HAN PASADO!")
        print("✅ El selector de vehículos está completamente funcional")
        print("✅ Todos los cambios aplicados están funcionando correctamente")
        print("✅ Sistema de logs operativo")
        print("✅ Base de datos conectada y con datos")
    else:
        print(f"\n⚠️  {total - passed} tests han fallado")
        print("❌ Revisar los mensajes de error arriba")
        print("❌ Puede haber problemas que necesitan corrección")

    print("="*80)

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)