"""
Script de verificación del proyecto AstroTech
Verifica que todos los archivos necesarios existen
"""

import os
import sys
import json

def check_file(path, description):
    """Verificar si un archivo existe"""
    exists = os.path.exists(path)
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {path}")
    return exists

def check_json_valid(path):
    """Verificar si un JSON es válido"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"  ✓ JSON válido - {len(data)} vehículos encontrados")
        return True
    except Exception as e:
        print(f"  ✗ Error en JSON: {e}")
        return False

def main():
    print("=" * 60)
    print("Verificación del Proyecto AstroTech")
    print("=" * 60)
    print()
    
    all_ok = True
    
    # Archivos críticos
    print("📁 Archivos Críticos:")
    all_ok &= check_file("frontend/app/app.py", "Aplicación principal")
    all_ok &= check_file("frontend/rxconfig.py", "Configuración Reflex")
    all_ok &= check_file("frontend/requirements.txt", "Dependencias")
    print()
    
    # Componentes
    print("🧩 Componentes:")
    all_ok &= check_file("frontend/components/header.py", "Header")
    all_ok &= check_file("frontend/components/hero.py", "Hero")
    all_ok &= check_file("frontend/components/vehicle_selector.py", "Selector")
    all_ok &= check_file("frontend/components/benefits.py", "Beneficios")
    all_ok &= check_file("frontend/components/services.py", "Servicios")
    all_ok &= check_file("frontend/components/faq.py", "FAQ")
    all_ok &= check_file("frontend/components/contact.py", "Contacto")
    all_ok &= check_file("frontend/components/footer.py", "Footer")
    print()
    
    # Datos
    print("📊 Datos:")
    json_path = "frontend/data/vehiculos_turismo.json"
    if check_file(json_path, "Base de datos de vehículos"):
        check_json_valid(json_path)
    else:
        all_ok = False
    print()
    
    # Assets
    print("🎨 Assets:")
    all_ok &= check_file("frontend/assets/styles.css", "CSS principal")
    all_ok &= check_file("frontend/assets/selector-fix.css", "CSS selector")
    
    # Verificar imágenes
    images_ok = True
    images_ok &= check_file("frontend/assets/images/bigstock-Technician-Is-Tuning-Engine-Ca-469398073.jpg", "Imagen hero")
    images_ok &= check_file("frontend/assets/images/centralita-coche.jpg", "Imagen ECU")
    
    if not images_ok:
        print("  ⚠️  Algunas imágenes faltan pero la app funcionará")
    print()
    
    # Utilidades
    print("🔧 Utilidades:")
    all_ok &= check_file("frontend/utils/vehicle_data.py", "Utilidad de datos")
    print()
    
    # Estados
    print("📊 Estados:")
    all_ok &= check_file("frontend/state/vehicle_state.py", "Estado vehículos")
    all_ok &= check_file("frontend/state/contact_state.py", "Estado contacto")
    all_ok &= check_file("frontend/state/global_state.py", "Estado global")
    print()
    
    print("=" * 60)
    if all_ok:
        print("✅ Todos los archivos necesarios están presentes")
        print("\n🚀 Listo para ejecutar:")
        print("   cd frontend")
        print("   reflex init")
        print("   reflex run")
        return 0
    else:
        print("⚠️  Algunos archivos faltan")
        print("\n📝 Revisa los archivos marcados con ✗")
        print("   La aplicación puede funcionar con warnings")
        return 1

if __name__ == "__main__":
    sys.exit(main())