#!/usr/bin/env python3
"""
Diagnóstico Integral de BD y CSS - AstroTech
============================================

Script completo para verificar:
1. ¿Qué base de datos está usando realmente la app?
2. ¿Qué datos contiene?
3. ¿Qué archivos CSS están cargados?
4. ¿Hay conflictos CSS o BD?

Resultado: Análisis completo del problema de selección de vehículos
"""

import os
import sqlite3
import hashlib
from pathlib import Path

def get_file_info(filepath):
    """Obtener información detallada de un archivo"""
    if Path(filepath).exists():
        stat = Path(filepath).stat()
        return {
            "exists": True,
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "readable": os.access(filepath, os.R_OK)
        }
    return {"exists": False, "size": 0, "modified": 0, "readable": False}

def check_database_contents(db_path):
    """Verificar contenido específico de una base de datos"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Lista todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        result = {"path": db_path, "tables": {}, "total_vehicles": 0}

        for table_name, in tables:
            # Contar registros
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            result["tables"][table_name] = count

            # Si es tabla de vehículos, verificar estructura
            if 'vehicle' in table_name.lower():
                result["total_vehicles"] = count
                if count > 0:
                    # Verificar tipos de combustible
                    cursor.execute(f"SELECT DISTINCT fuel_type FROM {table_name} LIMIT 5")
                    fuels = cursor.fetchall()
                    result["sample_fuels"] = [f[0] for f in fuels if f[0]]

                    # Verificar marcas
                    cursor.execute(f"SELECT DISTINCT brand FROM {table_name} LIMIT 10")
                    brands = cursor.fetchall()
                    result["sample_brands"] = [b[0] for b in brands if b[0]]

                    # Verificar estructura de columnas
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = cursor.fetchall()
                    result["columns"] = [col[1] for col in columns]

        conn.close()
        return result

    except Exception as e:
        return {"path": db_path, "error": str(e), "tables": {}}

def analyze_python_imports():
    """Analizar qué archivos Python referencian qué BD"""
    python_files = []
    for root, dirs, files in os.walk('.'):
        # Skip .venv y .git
        if '.venv' in root or '.git' in root:
            continue
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Buscar referencias a bases de datos
                    db_refs = []
                    if 'astrotech.db' in content:
                        db_refs.append('astrotech.db')
                    if 'vehicles.db' in content:
                        db_refs.append('vehicles.db')
                    if 'vehicles_expanded.db' in content:
                        db_refs.append('vehicles_expanded.db')
                    if 'reflex.db' in content:
                        db_refs.append('reflex.db')

                    if db_refs:
                        python_files.append({
                            "file": filepath,
                            "db_references": db_refs,
                            "has_vehicle_import": 'vehicle' in content.lower()
                        })
                except:
                    pass

    return python_files

def check_css_files():
    """Verificar archivos CSS y sus contenidos"""
    css_files = []
    css_locations = [
        'assets/styles.css',
        'assets/selector-fix.css',
        '.web/styles.css',
        '.web/selector-fix.css'
    ]

    for css_path in css_locations:
        info = get_file_info(css_path)
        if info["exists"]:
            try:
                with open(css_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Analizar contenido CSS
                css_files.append({
                    "path": css_path,
                    "size": info["size"],
                    "has_select_styles": 'select' in content.lower(),
                    "has_radix_styles": 'radix' in content.lower(),
                    "has_vehicle_styles": 'vehicle' in content.lower(),
                    "has_pointer_events": 'pointer-events' in content,
                    "line_count": len(content.splitlines())
                })
            except Exception as e:
                css_files.append({
                    "path": css_path,
                    "size": info["size"],
                    "error": str(e),
                    "line_count": 0
                })
        else:
            css_files.append({
                "path": css_path,
                "exists": False
            })

    return css_files

def main():
    print("="*80)
    print("DIAGNOSTICO INTEGRAL DE ASTROTECH - BD y CSS")
    print("="*80)

    # 1. Verificar archivos de BD
    print("\nANALISIS DE ARCHIVOS DE BASE DE DATOS:")
    print("-"*50)

    db_files = ['astrotech.db', 'vehicles.db', 'vehicles_expanded.db', 'reflex.db']
    found_dbs = []

    for db_file in db_files:
        info = get_file_info(db_file)
        if info["exists"]:
            found_dbs.append(db_file)
            print(f"[OK] {db_file}: {info['size']:,} bytes, Legible: {info['readable']}")
        else:
            print(f"[X] {db_file}: No existe")

    # 2. Analizar contenido de cada BD
    print("\nCONTENIDO DE BASES DE DATOS:")
    print("-"*50)

    for db_file in found_dbs:
        result = check_database_contents(db_file)
        if "error" in result:
            print(f"[ERROR] {db_file}: ERROR - {result['error']}")
        else:
            print(f"\n[BD] {db_file}:")
            print(f"   Tablas: {list(result['tables'].keys())}")
            for table, count in result['tables'].items():
                print(f"   - {table}: {count:,} registros")

            if result.get('total_vehicles', 0) > 0:
                print(f"   Combustibles: {result.get('sample_fuels', [])}")
                print(f"   Marcas: {result.get('sample_brands', [])[:5]}...")
                print(f"   Columnas: {result.get('columns', [])}")

    # 3. Analizar imports Python
    print("\n🐍 REFERENCIAS DE BASES DE DATOS EN CÓDIGO PYTHON:")
    print("-"*50)

    python_refs = analyze_python_imports()
    for ref in python_refs:
        print(f"📄 {ref['file']}:")
        print(f"   BD references: {ref['db_references']}")
        print(f"   Vehicle imports: {ref['has_vehicle_import']}")
        print()

    # 4. Verificar configuración
    print("⚙️ CONFIGURACIÓN ACTUAL:")
    print("-"*50)

    try:
        import settings
        print(f"✅ settings.DATABASE_URL: {settings.DATABASE_URL}")
        print(f"✅ DB Path exists: {settings.DATABASE_PATH.exists()}")
        print(f"✅ DB Size: {settings.DATABASE_PATH.stat().st_size:,} bytes")
    except Exception as e:
        print(f"❌ Error al leer settings: {e}")

    try:
        import rxconfig
        print(f"✅ rxconfig.db_url: {rxconfig.config.db_url}")
    except Exception as e:
        print(f"❌ Error al leer rxconfig: {e}")

    # 5. Analizar archivos CSS
    print("\n🎨 ANÁLISIS DE ARCHIVOS CSS:")
    print("-"*50)

    css_analysis = check_css_files()
    for css in css_analysis:
        if css.get("exists", False):
            print(f"🎨 {css['path']}:")
            print(f"   Size: {css['size']:,} bytes")
            print(f"   Lines: {css['line_count']:,}")
            print(f"   Select styles: {'✅' if css['has_select_styles'] else '❌'}")
            print(f"   Radix styles: {'✅' if css['has_radix_styles'] else '❌'}")
            print(f"   Pointer events: {'✅' if css['has_pointer_events'] else '❌'}")
            if "error" in css:
                print(f"   ⚠️ Error: {css['error']}")
        else:
            print(f"❌ {css['path']}: No existe")

    # 6. Verificar estado actual de la app
    print("\n🚀 ESTADO ACTUAL DE LA APLICACIÓN:")
    print("-"*50)

    try:
        from utils.vehicle_data_supabase import get_vehicle_fuel_types, get_vehicle_count
        fuel_types = get_vehicle_fuel_types()
        total_vehicles = get_vehicle_count()

        print(f"✅ VehicleDataSimple conectado")
        print(f"   Total vehículos: {total_vehicles:,}")
        print(f"   Tipos de combustible: {fuel_types}")

        if fuel_types:
            from utils.vehicle_data_supabase import get_vehicle_brands
            brands = get_vehicle_brands(fuel_types[0])
            print(f"   Marcas ({fuel_types[0]}): {len(brands)} encontradas")

    except Exception as e:
        print(f"❌ Error al verificar VehicleDataSimple: {e}")

    # 7. Verificar archivos CSS cargados en la app
    print("\n📦 CSS CARGADOS EN APP.PY:")
    print("-"*50)

    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            app_content = f.read()

        if 'styles.css' in app_content:
            print("✅ styles.css está referenciado en app.py")
        if 'selector-fix.css' in app_content:
            print("✅ selector-fix.css está referenciado en app.py")

        # Buscar imports de assets
        import re
        css_matches = re.findall(r'assets/([^"]+)\.css', app_content)
        for match in css_matches:
            print(f"   📄 {match}.css")

    except Exception as e:
        print(f"❌ Error al analizar app.py: {e}")

    # 8. Resumen y diagnóstico
    print("\n🎯 DIAGNÓSTICO FINAL:")
    print("="*50)

    # BD principal
    if Path('astrotech.db').exists():
        astrotech_info = check_database_contents('astrotech.db')
        if astrotech_info.get('total_vehicles', 0) > 0:
            print("✅ Base de datos principal (astrotech.db) tiene datos")
        else:
            print("⚠️ Base de datos principal (astrotech.db) está vacía")

    # Conflictos de BD
    if len(found_dbs) > 1:
        print(f"⚠️ MÚLTIPLES BASES DE DATOS ENCONTRADAS: {found_dbs}")
        print("   Esto puede causar confusión en la aplicación")

    # CSS
    existing_css = [css for css in css_analysis if css.get("exists", False)]
    if len(existing_css) > 1:
        print(f"⚠️ MÚLTIPLES ARCHIVOS CSS: {len(existing_css)} encontrados")
        for css in existing_css:
            if not css.get('has_radix_styles', False):
                print(f"   ⚠️ {css['path']}: No tiene estilos Radix UI")

    # Configuración
    try:
        import settings
        if not settings.DATABASE_PATH.exists():
            print("❌ settings.DATABASE_PATH no existe")
        else:
            print("✅ Configuración de BD es correcta")
    except:
        print("❌ Error en configuración de settings")

    print("\n🔧 RECOMENDACIONES:")
    print("-"*30)
    print("1. Verificar que la app esté usando 'astrotech.db'")
    print("2. Asegurar que solo exista un archivo CSS principal")
    print("3. Comprobar que los estilos Radix UI estén cargados")
    print("4. Revisar que no haya bloqueos pointer-events en CSS")
    print("5. Verificar imports de estado en vehicle_selector.py")

    print("\n" + "="*80)

if __name__ == "__main__":
    main()