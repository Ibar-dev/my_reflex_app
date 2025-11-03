"""
Script de instalación automática de dependencias de Supabase
"""
import subprocess
import sys
import os

def install_dependencies():
    """Instala las dependencias necesarias para Supabase"""
    print("\n" + "=" * 60)
    print("📦 INSTALANDO DEPENDENCIAS DE SUPABASE")
    print("=" * 60 + "\n")
    
    packages = [
        "python-dotenv",
        "psycopg2-binary",
    ]
    
    for package in packages:
        print(f"📥 Instalando {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} instalado correctamente\n")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al instalar {package}: {e}\n")
            return False
    
    print("=" * 60)
    print("✅ TODAS LAS DEPENDENCIAS INSTALADAS")
    print("=" * 60 + "\n")
    return True


def check_env_file():
    """Verifica que el archivo .env existe y tiene las credenciales"""
    print("🔍 Verificando archivo .env...")
    
    if not os.path.exists(".env"):
        print("❌ Archivo .env no encontrado")
        return False
    
    with open(".env", "r", encoding="utf-8") as f:
        content = f.read()
    
    required_vars = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]
    missing = []
    
    for var in required_vars:
        if var not in content:
            missing.append(var)
        elif "TU_PASSWORD_AQUI" in content:
            print(f"⚠️  Debes actualizar DB_PASSWORD en .env")
            return False
    
    if missing:
        print(f"❌ Faltan variables en .env: {missing}")
        return False
    
    print("✅ Archivo .env configurado correctamente\n")
    return True


def main():
    """Función principal"""
    print("\n🚀 CONFIGURACIÓN AUTOMÁTICA DE SUPABASE PARA ASTROTECH")
    
    # Instalar dependencias
    if not install_dependencies():
        print("\n❌ Error al instalar dependencias")
        return
    
    # Verificar .env
    if not check_env_file():
        print("\n⚠️  Por favor, actualiza el archivo .env con tus credenciales de Supabase")
        print("    Encuentra tu contraseña en: Supabase Dashboard > Settings > Database")
        return
    
    print("\n" + "=" * 60)
    print("🎉 CONFIGURACIÓN COMPLETADA")
    print("=" * 60)
    print("\n📋 PRÓXIMOS PASOS:")
    print("\n1. Verifica tu contraseña de Supabase en .env")
    print("2. Ejecuta: python utils/supabase_connection.py")
    print("   (para probar la conexión)")
    print("\n3. Ejecuta: python utils/create_vehicles_table.py")
    print("   (para crear la tabla y datos de ejemplo)")
    print("\n4. Ejecuta: python test_supabase_integration.py")
    print("   (para verificar que todo funciona)")
    print("\n5. Actualiza tu aplicación para usar Supabase")
    print("   (modifica state/vehicle_state_simple.py)")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
