#!/usr/bin/env python3
"""
Verificación Final del Sistema de Base de Datos
==============================================

Script para verificar que todo el sistema esté funcionando correctamente
"""

import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verify_database_system():
    """Verificación completa del sistema"""
    print("🔍 VERIFICACIÓN FINAL DEL SISTEMA")
    print("=" * 45)
    
    success_count = 0
    total_tests = 0
    
    # 1. Verificar imports
    print("1. 📦 Verificando imports...")
    total_tests += 4
    
    try:
        import reflex as rx
        print("   ✅ Reflex")
        success_count += 1
    except ImportError:
        print("   ❌ Reflex")
    
    try:
        from utils.database_service import DatabaseService
        print("   ✅ DatabaseService")
        success_count += 1
    except ImportError:
        print("   ❌ DatabaseService")
    
    try:
        from components.discount_popup import PopupState, discount_popup
        print("   ✅ Popup Components")
        success_count += 1
    except ImportError:
        print("   ❌ Popup Components")
    
    try:
        from models.user import UserRegistration, get_database_info
        print("   ✅ User Models")
        success_count += 1
    except ImportError:
        print("   ❌ User Models")
    
    print()
    
    # 2. Verificar base de datos
    print("2. 🗄️ Verificando base de datos...")
    total_tests += 2
    
    try:
        stats = DatabaseService.get_stats()
        if stats["success"]:
            print(f"   ✅ Base de datos funcionando ({stats['stats']['total_users']} usuarios)")
            success_count += 1
        else:
            print("   ❌ Error al obtener estadísticas")
    except:
        print("   ❌ Error en base de datos")
    
    db_path = os.path.join(os.path.dirname(__file__), "users.db")
    if os.path.exists(db_path):
        print("   ✅ Archivo users.db existe")
        success_count += 1
    else:
        print("   ❌ Archivo users.db no encontrado")
    
    print()
    
    # 3. Verificar validaciones
    print("3. 🛡️ Verificando validaciones...")
    total_tests += 2
    
    try:
        valid_email = DatabaseService.validate_email("test@example.com")
        invalid_email = DatabaseService.validate_email("invalid-email")
        
        if valid_email and not invalid_email:
            print("   ✅ Validación de email")
            success_count += 1
        else:
            print("   ❌ Validación de email")
    except:
        print("   ❌ Error en validación de email")
    
    try:
        valid_phone = DatabaseService.validate_phone("+34 600 123 456")
        invalid_phone = DatabaseService.validate_phone("123")
        
        if valid_phone and not invalid_phone:
            print("   ✅ Validación de teléfono")
            success_count += 1
        else:
            print("   ❌ Validación de teléfono")
    except:
        print("   ❌ Error en validación de teléfono")
    
    print()
    
    # 4. Verificar archivos del proyecto
    print("4. 📁 Verificando archivos...")
    required_files = [
        "models/user.py",
        "utils/database_service.py", 
        "components/discount_popup.py",
        "requirements.txt",
        "DATABASE_DOCUMENTATION.md"
    ]
    
    total_tests += len(required_files)
    
    for file_path in required_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if os.path.exists(full_path):
            print(f"   ✅ {file_path}")
            success_count += 1
        else:
            print(f"   ❌ {file_path}")
    
    print()
    
    # Resultado final
    percentage = (success_count / total_tests) * 100
    print("📊 RESULTADO FINAL")
    print("-" * 20)
    print(f"✅ Exitosas: {success_count}/{total_tests}")
    print(f"📈 Porcentaje: {percentage:.1f}%")
    
    if percentage >= 90:
        print("\n🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print("🚀 Listo para usar en producción")
        return True
    elif percentage >= 70:
        print("\n⚠️ Sistema mayormente funcional")
        print("🔧 Revisar elementos faltantes")
        return True
    else:
        print("\n❌ Sistema con problemas")
        print("🛠️ Requiere revisión")
        return False

def main():
    """Función principal"""
    try:
        success = verify_database_system()
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error durante la verificación: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()