#!/usr/bin/env python3
"""
Visor de Usuarios Registrados
============================

Script simple para ver todos los usuarios registrados en la base de datos
"""

import sys
import os
from datetime import datetime

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.database_service import DatabaseService

def format_date(date_str):
    """Formatea una fecha ISO para mostrarla de forma legible"""
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime("%d/%m/%Y %H:%M")
    except:
        return date_str

def show_users():
    """Muestra todos los usuarios registrados"""
    print("👥 USUARIOS REGISTRADOS")
    print("=" * 80)
    
    # Obtener estadísticas
    stats_result = DatabaseService.get_stats()
    if stats_result["success"]:
        stats = stats_result["stats"]
        print(f"📊 ESTADÍSTICAS:")
        print(f"   • Total usuarios: {stats['total_users']}")
        print(f"   • Contactados: {stats['contacted_users']}")
        print(f"   • Pendientes de contactar: {stats['pending_contact']}")
        print(f"   • Registros del popup: {stats['popup_registrations']}")
        print(f"   • Tasa de conversión: {stats['conversion_rate']}%")
        print()
    
    # Obtener usuarios
    users_result = DatabaseService.get_all_users()
    
    if not users_result["success"]:
        print("❌ Error al obtener usuarios")
        return
    
    users = users_result["users"]
    
    if not users:
        print("📭 No hay usuarios registrados aún")
        return
    
    print(f"📋 LISTADO DE USUARIOS ({len(users)} registros):")
    print("-" * 80)
    
    for i, user in enumerate(users, 1):
        status_icon = "✅" if user["is_contacted"] else "⏳"
        status_text = "Contactado" if user["is_contacted"] else "Pendiente"
        
        print(f"{i:2d}. {status_icon} {user['nombre']}")
        print(f"     📧 {user['email']}")
        print(f"     📱 {user['telefono']}")
        print(f"     📅 {format_date(user['created_at'])} | 🏷️ {user['source']} | 🔄 {status_text}")
        print()

def main():
    """Función principal"""
    try:
        show_users()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()