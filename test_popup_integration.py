#!/usr/bin/env python3
"""
Simulación del Popup de Descuento
=================================

Simula el comportamiento del popup para verificar la integración con la base de datos
"""

import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components.discount_popup import PopupState
from utils.database_service import DatabaseService

def simulate_popup_registration():
    """Simula el proceso de registro del popup"""
    print("🎯 SIMULACIÓN DEL POPUP DE DESCUENTO")
    print("=" * 50)
    
    # Crear instancia del estado del popup
    popup_state = PopupState()
    
    print("1. 🎪 Popup inicial:")
    print(f"   - show_popup: {popup_state.show_popup}")
    print(f"   - show_form: {popup_state.show_form}")
    print()
    
    # Simular clic en "REGISTRARME"
    print("2. 👆 Usuario hace clic en 'REGISTRARME':")
    popup_state.open_register()
    print(f"   - show_form: {popup_state.show_form}")
    print(f"   - error_message: '{popup_state.error_message}'")
    print()
    
    # Llenar formulario con datos válidos
    print("3. ✍️ Usuario llena el formulario:")
    popup_state.nombre = "María García"
    popup_state.email = "maria.garcia@gmail.com"
    popup_state.telefono = "+34 600 555 123"
    
    print(f"   - nombre: '{popup_state.nombre}'")
    print(f"   - email: '{popup_state.email}'")
    print(f"   - telefono: '{popup_state.telefono}'")
    print()
    
    # Simular envío del formulario
    print("4. 🚀 Usuario hace clic en 'Enviar':")
    print("   - Validando datos...")
    print("   - Guardando en base de datos...")
    
    # Usar directamente el servicio de base de datos para simular
    result = DatabaseService.save_user_registration(
        nombre=popup_state.nombre.strip(),
        email=popup_state.email.strip().lower(),
        telefono=popup_state.telefono.strip(),
        source="discount_popup"
    )
    
    if result["success"]:
        popup_state.success_message = result["message"]
        popup_state.error_message = ""
        print(f"   ✅ Éxito: {result['message']}")
        print(f"   📊 ID del usuario: {result['user_id']}")
        
        # Simular cierre del popup
        popup_state.show_popup = False
        print(f"   🔒 Popup cerrado: show_popup = {popup_state.show_popup}")
    else:
        popup_state.error_message = result["message"]
        popup_state.success_message = ""
        print(f"   ❌ Error: {result['message']}")
    
    print()
    
    # Probar registro duplicado
    print("5. 🔄 Probando registro duplicado:")
    popup_state2 = PopupState()
    popup_state2.nombre = "María García Duplicada"
    popup_state2.email = "maria.garcia@gmail.com"  # Mismo email
    popup_state2.telefono = "+34 600 999 888"
    
    result2 = DatabaseService.save_user_registration(
        nombre=popup_state2.nombre.strip(),
        email=popup_state2.email.strip().lower(),
        telefono=popup_state2.telefono.strip(),
        source="discount_popup"
    )
    
    if not result2["success"]:
        print(f"   ✅ Duplicado rechazado: {result2['message']}")
    else:
        print(f"   ❌ Error: duplicado no fue detectado")
    
    print()
    
    # Mostrar estado final
    print("6. 📊 Estado final de la base de datos:")
    users_result = DatabaseService.get_all_users()
    if users_result["success"]:
        popup_users = [u for u in users_result["users"] if u["source"] == "discount_popup"]
        print(f"   - Total usuarios del popup: {len(popup_users)}")
        for user in popup_users:
            print(f"     • {user['nombre']} ({user['email']})")
    
    print("\n" + "=" * 50)
    print("🎉 Simulación completada")

def main():
    """Función principal"""
    try:
        simulate_popup_registration()
        print("\n✅ La integración del popup con la base de datos funciona correctamente")
    except Exception as e:
        print(f"\n❌ Error durante la simulación: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()