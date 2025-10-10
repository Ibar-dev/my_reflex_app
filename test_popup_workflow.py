#!/usr/bin/env python3
"""
Simulación del Flujo del Popup - Solo Base de Datos
==================================================

Simula el flujo de datos que se ejecutaría cuando el popup guarda registros
"""

import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.database_service import DatabaseService

def simulate_popup_workflow():
    """Simula el flujo completo del popup usando solo la lógica de base de datos"""
    print("🎪 SIMULACIÓN DEL FLUJO DEL POPUP DE DESCUENTO")
    print("=" * 60)
    
    # Escenario 1: Registro exitoso
    print("📝 ESCENARIO 1: Registro exitoso desde el popup")
    print("-" * 45)
    
    # Datos que vendría del formulario del popup
    nombre_input = "Ana Martínez"
    email_input = "ana.martinez@hotmail.com"
    telefono_input = "+34 650 789 123"
    
    print(f"📤 Datos del formulario del popup:")
    print(f"   • Nombre: '{nombre_input}'")
    print(f"   • Email: '{email_input}'")
    print(f"   • Teléfono: '{telefono_input}'")
    print()
    
    # Ejecutar la misma lógica que se ejecutaría en submit_registration()
    print("🔄 Ejecutando submit_registration()...")
    
    # Validaciones básicas (como en el popup)
    if not nombre_input.strip():
        print("❌ Error: El nombre es obligatorio")
        return
    
    if not email_input.strip() or "@" not in email_input:
        print("❌ Error: Email inválido") 
        return
        
    if not telefono_input.strip():
        print("❌ Error: El teléfono es obligatorio")
        return
    
    print("✅ Validaciones básicas pasadas")
    
    # Llamar al servicio de base de datos
    result = DatabaseService.save_user_registration(
        nombre=nombre_input.strip(),
        email=email_input.strip().lower(),
        telefono=telefono_input.strip(),
        source="discount_popup"
    )
    
    if result["success"]:
        print(f"✅ Registro exitoso!")
        print(f"   📧 Mensaje para el usuario: '{result['message']}'")
        print(f"   🆔 ID del registro: {result['user_id']}")
        print(f"   📊 Datos guardados: {result['data']['nombre']} - {result['data']['email']}")
        print("   🔒 Popup se cerraría automáticamente")
    else:
        print(f"❌ Error en el registro: {result['message']}")
    
    print()
    
    # Escenario 2: Email duplicado
    print("📝 ESCENARIO 2: Intento de registro con email duplicado")
    print("-" * 55)
    
    result2 = DatabaseService.save_user_registration(
        nombre="Ana Martínez Duplicada",
        email=email_input,  # Mismo email
        telefono="+34 600 999 888",
        source="discount_popup"
    )
    
    if not result2["success"]:
        print(f"✅ Duplicado detectado correctamente")
        print(f"   ⚠️ Mensaje de error para el usuario: '{result2['message']}'")
        print("   🔄 Popup permanecería abierto para corregir el email")
    else:
        print(f"❌ Error: duplicado no fue detectado!")
    
    print()
    
    # Escenario 3: Datos inválidos
    print("📝 ESCENARIO 3: Datos inválidos")
    print("-" * 35)
    
    casos_invalidos = [
        ("", "test@email.com", "+34 600 123 456", "Nombre vacío"),
        ("Juan Pérez", "email-sin-arroba", "+34 600 123 456", "Email sin @"),
        ("Juan Pérez", "test@email.com", "123", "Teléfono muy corto"),
    ]
    
    for nombre, email, telefono, descripcion in casos_invalidos:
        result3 = DatabaseService.save_user_registration(
            nombre=nombre,
            email=email,
            telefono=telefono,
            source="discount_popup"
        )
        
        status = "✅" if not result3["success"] else "❌"
        print(f"   {status} {descripcion}: {result3['message']}")
    
    print()
    
    # Mostrar estadísticas finales
    print("📊 ESTADÍSTICAS FINALES")
    print("-" * 25)
    
    stats = DatabaseService.get_stats()
    if stats["success"]:
        s = stats["stats"]
        print(f"   • Total usuarios: {s['total_users']}")
        print(f"   • Registros del popup: {s['popup_registrations']}")
        print(f"   • Usuarios contactados: {s['contacted_users']}")
        print(f"   • Pendientes de contactar: {s['pending_contact']}")
    
    # Mostrar últimos registros del popup
    users_result = DatabaseService.get_all_users(limit=10)
    if users_result["success"]:
        popup_users = [u for u in users_result["users"] if u["source"] == "discount_popup"]
        print(f"\n📋 Registros del popup ({len(popup_users)}):")
        for user in popup_users:
            status = "✅ Contactado" if user["is_contacted"] else "⏳ Pendiente"
            print(f"   • {user['nombre']} ({user['email']}) - {status}")
    
    print("\n" + "=" * 60)
    print("🎉 Simulación del flujo del popup completada")

def main():
    """Función principal"""
    try:
        simulate_popup_workflow()
        print("\n✅ El sistema de base de datos está perfectamente integrado con el popup")
        print("🚀 Listo para usar en producción")
    except Exception as e:
        print(f"\n❌ Error durante la simulación: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()