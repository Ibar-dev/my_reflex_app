#!/usr/bin/env python3
"""
Verificación Rápida del Sistema
==============================

Script para verificar que todo el sistema esté funcionando correctamente
"""

import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verify_system():
    """Verificación completa del sistema"""
    print("🔍 VERIFICACIÓN DEL SISTEMA DE BASE DE DATOS")
    print("=" * 50)
    
    errors = []
    
    # 1. Verificar imports
    print("1. 📦 Verificando imports...")
    try:
        import reflex as rx
        print("   ✅ Reflex importado correctamente")
    except ImportError:
        errors.append("❌ Error al importar Reflex")
    
    try:
        from utils.database_service import DatabaseService
        print("   ✅ DatabaseService importado correctamente")
    except ImportError as e:
        errors.append(f"❌ Error al importar DatabaseService: {e}")
    
    try:
        from components.discount_popup import PopupState, discount_popup
        print("   ✅ Componentes del popup importados correctamente")
    except ImportError as e:
        errors.append(f"❌ Error al importar popup: {e}")
    
    try:
        from models.user import UserRegistration, get_database_info
        print("   ✅ Modelos importados correctamente")
    except ImportError as e:
        errors.append(f"❌ Error al importar modelos: {e}")
    
    print()
    
    # 2. Verificar base de datos
    print("2. 🗄️ Verificando base de datos...")
    try:
        from models.user import init_database
        if init_database():
            print("   ✅ Base de datos inicializada correctamente")
        else:
            errors.append("❌ Error al inicializar base de datos")
    except Exception as e:
        errors.append(f"❌ Error en base de datos: {e}")
    
    # 3. Verificar archivos de base de datos
    db_path = os.path.join(os.path.dirname(__file__), "users.db")
    if os.path.exists(db_path):
        print(f"   ✅ Archivo de base de datos existe: {db_path}")
    else:
        errors.append("❌ Archivo de base de datos no encontrado")
    
    print()
    
    # 4. Verificar funcionalidad básica
    print("3. ⚙️ Verificando funcionalidad básica...")
    try:
        # Obtener estadísticas
        stats = DatabaseService.get_stats()
        if stats["success"]:
            print(f"   ✅ Estadísticas obtenidas: {stats['stats']['total_users']} usuarios")
        else:
            errors.append("❌ Error al obtener estadísticas")
    except Exception as e:
        errors.append(f"❌ Error en funcionalidad: {e}")
    
    # 5. Verificar validaciones
    print("   🛡️ Verificando validaciones...")
    try:
        # Test de validación de email
        valid_email = DatabaseService.validate_email("test@example.com")
        invalid_email = DatabaseService.validate_email("invalid-email")
        
        if valid_email and not invalid_email:
            print("   ✅ Validaciones de email funcionando")
        else:
            errors.append("❌ Error en validaciones de email")
        
        # Test de validación de teléfono
        valid_phone = DatabaseService.validate_phone("+34 600 123 456")
        invalid_phone = DatabaseService.validate_phone("123")
        
        if valid_phone and not invalid_phone:
            print("   ✅ Validaciones de teléfono funcionando")
        else:
            errors.append("❌ Error en validaciones de teléfono")
            
    except Exception as e:
        errors.append(f"❌ Error en validaciones: {e}")
    
    print()
    
    # 6. Verificar archivos del proyecto
    print("4. 📁 Verificando archivos del proyecto...")
    required_files = [
        "models/user.py",
        "utils/database_service.py", 
        "components/discount_popup.py",
        "requirements.txt"
    ]
    
    for file_path in required_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if os.path.exists(full_path):
            print(f"   ✅ {file_path}")
        else:
            errors.append(f"❌ Archivo faltante: {file_path}")
    
    print()
    
    # 7. Resultado final
    if errors:
        print("❌ ERRORES ENCONTRADOS:")
        for error in errors:
            print(f"   {error}")
        print(f"\n💥 {len(errors)} errores encontrados")
        return False
    else:
        print("🎉 VERIFICACIÓN COMPLETA")
        print("✅ Todos los componentes funcionando correctamente")
        print("🚀 Sistema listo para usar")
        return True

def main():
    """Función principal"""
    try:
        success = verify_system()
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error durante la verificación: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()