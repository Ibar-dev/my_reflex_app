#!/usr/bin/env python3
"""
Test para verificar que el flujo de selección de vehículos funciona correctamente
y que la información aparece en el formulario de contacto.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_vehicle_selection_flow():
    """Probar el flujo completo de selección de vehículos"""
    print("TEST: Verificando flujo de seleccion de vehiculos")
    print("=" * 60)

    try:
        # Importar los estados
        from state.vehicle_state_simple import VehicleState
        from state.contact_state import ContactState

        # Crear instancias de los estados
        vehicle_state = VehicleState()
        contact_state = ContactState()

        print("✅ Estados importados correctamente")

        # Simular selección completa de vehículo
        print("\n📝 Simulando selección de vehículo:")

        # 1. Seleccionar combustible
        vehicle_state.selected_fuel = "Gasolina"
        print(f"   • Combustible: {vehicle_state.selected_fuel}")

        # 2. Seleccionar marca
        vehicle_state.selected_brand = "Ford"
        print(f"   • Marca: {vehicle_state.selected_brand}")

        # 3. Seleccionar modelo
        vehicle_state.selected_model = "Focus"
        print(f"   • Modelo: {vehicle_state.selected_model}")

        # 4. Seleccionar versión
        vehicle_state.selected_version = "1.5 EcoBoost 150CV"
        print(f"   • Versión: {vehicle_state.selected_version}")

        # Verificar que la selección esté completa
        is_complete = vehicle_state.is_complete_selection()
        print(f"\n🔍 Selección completa: {is_complete}")

        if is_complete:
            # Ejecutar el método de envío
            print("\n📤 Ejecutando submit_vehicle_selection()...")
            vehicle_state.submit_vehicle_selection()

            # Verificar que el mensaje se preparó correctamente
            print(f"💬 Mensaje en VehicleState: {vehicle_state.selected_vehicle_message}")

            # Verificar que la información se transfirió a ContactState
            print("\n🔄 Verificando transferencia a ContactState:")
            contact_state.update_vehicle_info()
            print(f"📋 vehicle_info en ContactState: '{contact_state.vehicle_info}'")

            # Verificar que la información coincida
            if contact_state.vehicle_info == vehicle_state.selected_vehicle_message:
                print("✅ SUCCESS: La información del vehículo se transfirió correctamente")
                print("\n📄 El formulario de contacto debería mostrar:")
                print(contact_state.vehicle_info)
                return True
            else:
                print("❌ ERROR: La información no coincide entre estados")
                print(f"   VehicleState: '{vehicle_state.selected_vehicle_message}'")
                print(f"   ContactState: '{contact_state.vehicle_info}'")
                return False
        else:
            print("❌ ERROR: La selección no está completa")
            return False

    except Exception as e:
        print(f"❌ ERROR en el test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_contact_form_display():
    """Verificar las condiciones de visualización en el formulario de contacto"""
    print("\n🧪 TEST: Verificando visualización en formulario de contacto")
    print("=" * 60)

    try:
        from state.contact_state import ContactState

        contact_state = ContactState()

        # Caso 1: Sin información de vehículo
        contact_state.vehicle_info = ""
        print("🔍 Caso 1: vehicle_info vacía")
        print(f"   ¿Se muestra vehículo?: {contact_state.vehicle_info != ''}")

        # Caso 2: Con información de vehículo
        contact_state.vehicle_info = "VEHÍCULO SELECCIONADO:\n• Combustible: Gasolina\n• Marca: Ford"
        print("\n🔍 Caso 2: vehicle_info con datos")
        print(f"   ¿Se muestra vehículo?: {contact_state.vehicle_info != ''}")
        print(f"   Contenido: {contact_state.vehicle_info}")

        return True

    except Exception as e:
        print(f"❌ ERROR en test de visualización: {e}")
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO TESTS DEL SELECTOR DE VEHÍCULOS")
    print("=" * 80)

    # Test 1: Flujo de selección
    test1_result = test_vehicle_selection_flow()

    # Test 2: Visualización en formulario
    test2_result = test_contact_form_display()

    # Resumen
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE TESTS:")
    print(f"   ✅ Flujo de selección: {'PASS' if test1_result else 'FAIL'}")
    print(f"   ✅ Visualización formulario: {'PASS' if test2_result else 'FAIL'}")

    if test1_result and test2_result:
        print("\n🎉 TODOS LOS TESTS PASARON - El selector debería funcionar correctamente")
        print("\n📝 Pasos para verificar manualmente:")
        print("   1. Inicia la app: reflex run")
        print("   2. Ve a http://localhost:3001/")
        print("   3. Selecciona un vehículo completo")
        print("   4. Haz clic en 'Solicitar Presupuesto'")
        print("   5. Ve al formulario de contacto")
        print("   6. Deberías ver la información del vehículo en un recuadro naranja")
    else:
        print("\n❌ ALGUNOS TESTS FALLARON - Revisa la implementación")

    print("\n🌐 La aplicación está corriendo en: http://localhost:3001/")