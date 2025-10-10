#!/usr/bin/env python3
"""
Script de Prueba - Sistema de Base de Datos
==========================================

Prueba la funcionalidad del sistema de base de datos para registros de usuarios
"""

import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.database_service import DatabaseService
from models.user import get_database_info, init_database

def test_database_operations():
    """Prueba las operaciones básicas de la base de datos"""
    print("🧪 Iniciando pruebas del sistema de base de datos...")
    print("=" * 60)
    
    # 1. Información de la base de datos
    print("📋 1. Información de la base de datos:")
    db_info = get_database_info()
    for key, value in db_info.items():
        print(f"   {key}: {value}")
    print()
    
    # 2. Inicializar base de datos
    print("🔧 2. Inicializando base de datos...")
    if init_database():
        print("   ✅ Base de datos inicializada correctamente")
    else:
        print("   ❌ Error al inicializar la base de datos")
        return False
    print()
    
    # 3. Probar registro de usuario válido
    print("👤 3. Probando registro de usuario válido...")
    result = DatabaseService.save_user_registration(
        nombre="Juan Pérez Test",
        email="juan.test@example.com",
        telefono="+34 600 123 456",
        source="test_script"
    )
    
    if result["success"]:
        print(f"   ✅ Usuario registrado: ID {result['user_id']}")
        print(f"   📧 Mensaje: {result['message']}")
        test_user_id = result["user_id"]
    else:
        print(f"   ❌ Error al registrar: {result['message']}")
        test_user_id = None
    print()
    
    # 4. Probar registro duplicado
    print("🔄 4. Probando registro duplicado...")
    result2 = DatabaseService.save_user_registration(
        nombre="Juan Pérez Duplicado",
        email="juan.test@example.com",  # Mismo email
        telefono="+34 600 999 999",
        source="test_script"
    )
    
    if not result2["success"]:
        print(f"   ✅ Duplicado rechazado correctamente: {result2['message']}")
    else:
        print(f"   ❌ Error: duplicado no fue rechazado")
    print()
    
    # 5. Probar validaciones
    print("🛡️ 5. Probando validaciones...")
    
    # Email inválido
    result3 = DatabaseService.save_user_registration(
        nombre="Test Validación",
        email="email-invalido",
        telefono="+34 600 123 456"
    )
    print(f"   Email inválido: {'✅' if not result3['success'] else '❌'} {result3['message']}")
    
    # Nombre vacío
    result4 = DatabaseService.save_user_registration(
        nombre="",
        email="test2@example.com",
        telefono="+34 600 123 456"
    )
    print(f"   Nombre vacío: {'✅' if not result4['success'] else '❌'} {result4['message']}")
    
    # Teléfono inválido
    result5 = DatabaseService.save_user_registration(
        nombre="Test Teléfono",
        email="test3@example.com",
        telefono="123"  # Muy corto
    )
    print(f"   Teléfono inválido: {'✅' if not result5['success'] else '❌'} {result5['message']}")
    print()
    
    # 6. Buscar usuario por email
    print("🔍 6. Probando búsqueda por email...")
    search_result = DatabaseService.get_user_by_email("juan.test@example.com")
    if search_result["success"] and search_result["found"]:
        user = search_result["user"]
        print(f"   ✅ Usuario encontrado: {user['nombre']} ({user['email']})")
    else:
        print(f"   ❌ Error en búsqueda: {search_result['message']}")
    print()
    
    # 7. Marcar como contactado
    if test_user_id:
        print("📞 7. Probando marcar como contactado...")
        contact_result = DatabaseService.mark_user_contacted(test_user_id)
        if contact_result["success"]:
            print(f"   ✅ Usuario marcado como contactado: {contact_result['message']}")
        else:
            print(f"   ❌ Error al marcar: {contact_result['message']}")
        print()
    
    # 8. Obtener todos los usuarios
    print("📊 8. Obteniendo todos los usuarios...")
    users_result = DatabaseService.get_all_users()
    if users_result["success"]:
        print(f"   ✅ {users_result['count']} usuarios obtenidos de {users_result['total_count']} totales")
        for user in users_result["users"]:
            status = "🔵 Contactado" if user["is_contacted"] else "🟡 Pendiente"
            print(f"      - {user['nombre']} ({user['email']}) {status}")
    else:
        print(f"   ❌ Error al obtener usuarios")
    print()
    
    # 9. Estadísticas
    print("📈 9. Obteniendo estadísticas...")
    stats_result = DatabaseService.get_stats()
    if stats_result["success"]:
        stats = stats_result["stats"]
        print(f"   ✅ Estadísticas obtenidas:")
        print(f"      - Total usuarios: {stats['total_users']}")
        print(f"      - Contactados: {stats['contacted_users']}")
        print(f"      - Pendientes: {stats['pending_contact']}")
        print(f"      - Del popup: {stats['popup_registrations']}")
        print(f"      - Tasa de conversión: {stats['conversion_rate']}%")
    else:
        print(f"   ❌ Error al obtener estadísticas")
    
    print("\n" + "=" * 60)
    print("🎉 Pruebas completadas")
    return True

def main():
    """Función principal"""
    try:
        success = test_database_operations()
        if success:
            print("\n✅ Todas las pruebas pasaron correctamente")
            print("🚀 El sistema de base de datos está listo para usar")
        else:
            print("\n❌ Algunas pruebas fallaron")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error inesperado durante las pruebas: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()