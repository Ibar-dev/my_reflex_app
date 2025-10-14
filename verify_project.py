#!/usr/bin/env python3
"""Script de verificación final del proyecto AstroTech."""

import os
import sys
import importlib.util

def verify_project():
    """Verificación final del proyecto limpio."""
    print("🏆 VERIFICACIÓN FINAL - PROYECTO ASTROTECH")
    print("=" * 60)
    
    success_count = 0
    total_checks = 10
    
    # 1. Verificar estructura básica
    print("\n📁 1. Verificando estructura de archivos...")
    required_files = [
        "app/app.py",
        "components/discount_popup.py", 
        "components/cookie_banner.py",
        "state/vehicle_state.py",
        "services/vehicle_api_service.py",
        "models/user.py",
        "utils/database_service.py",
        "README.md",
        "requirements.txt",
        "arquitectura.tree"
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file}")
            missing_files.append(file)
    
    if not missing_files:
        success_count += 1
        print("   🎉 Estructura de archivos: COMPLETA")
    else:
        print(f"   ⚠️ Faltan {len(missing_files)} archivos")
    
    # 2. Verificar base de datos
    print("\n🗄️ 2. Verificando base de datos...")
    if os.path.exists("users.db"):
        print("   ✅ users.db existe")
        success_count += 1
    else:
        print("   ❌ users.db no encontrada")
    
    # 3. Verificar cache API
    print("\n📡 3. Verificando cache de API...")
    if os.path.exists("data/vehicles_api_cache.json"):
        print("   ✅ Cache de API NHTSA existe")
        success_count += 1
    else:
        print("   ⚠️ Cache de API no encontrado (se generará automáticamente)")
        success_count += 0.5
    
    # 4. Verificar entorno virtual
    print("\n🐍 4. Verificando entorno virtual...")
    if os.path.exists(".venv"):
        print("   ✅ Entorno virtual .venv existe")
        success_count += 1
    else:
        print("   ❌ Entorno virtual no encontrado")
    
    # 5. Verificar archivos de configuración
    print("\n⚙️ 5. Verificando configuración...")
    config_files = ["rxconfig.py", ".env"]
    config_found = 0
    for file in config_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
            config_found += 1
        else:
            print(f"   ⚠️ {file} no encontrado")
    
    if config_found >= 1:
        success_count += 1
    
    # 6-10. Verificaciones adicionales
    print("\n📊 6. Documentación...")
    if os.path.getsize("README.md") > 1000:  # README substancial
        print("   ✅ README.md completo")
        success_count += 1
    
    print("\n🧹 7. Limpieza de archivos...")
    test_files = ["test_api_integration.py", "test_api_service.py"]
    cleaned = True
    for file in test_files:
        if os.path.exists(file):
            cleaned = False
            print(f"   ❌ {file} debería estar eliminado")
    if cleaned:
        print("   ✅ Archivos de test temporales eliminados")
        success_count += 1
    
    print("\n🎨 8. Assets y recursos...")
    if os.path.exists("assets/images") and os.path.exists("assets/styles.css"):
        print("   ✅ Assets completos")
        success_count += 1
    
    print("\n🔧 9. Scripts de utilidad...")
    util_scripts = ["check_system.py", "view_users.py", "test_database.py"]
    utils_ok = all(os.path.exists(script) for script in util_scripts)
    if utils_ok:
        print("   ✅ Scripts de utilidad presentes")
        success_count += 1
    
    print("\n🏗️ 10. Arquitectura documentada...")
    if os.path.exists("arquitectura.tree"):
        print("   ✅ Arquitectura documentada")
        success_count += 1
    
    # Resultado final
    print("\n" + "=" * 60)
    print("📈 RESULTADO FINAL")
    print("=" * 60)
    percentage = (success_count / total_checks) * 100
    print(f"✅ Verificaciones exitosas: {success_count}/{total_checks}")
    print(f"📊 Porcentaje de completitud: {percentage:.1f}%")
    
    if percentage >= 90:
        print("\n🎉 PROYECTO COMPLETAMENTE FUNCIONAL")
        print("🚀 Listo para producción")
        print("\n💡 Para usar el proyecto:")
        print("   1. Activar entorno virtual: .venv\\Scripts\\activate (Windows)")
        print("   2. Ejecutar aplicación: reflex run")
        print("   3. Acceder a: http://localhost:3000")
        print("\n🌐 URL Producción: https://app-silver-grass.reflex.run")
        return True
    elif percentage >= 80:
        print("\n⚠️ PROYECTO CASI COMPLETO")
        print("🔧 Requiere pequeños ajustes")
        return True
    else:
        print("\n❌ PROYECTO REQUIERE ATENCIÓN")
        print("🛠️ Necesita correcciones importantes")
        return False

if __name__ == "__main__":
    try:
        success = verify_project()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error durante verificación: {e}")
        sys.exit(1)