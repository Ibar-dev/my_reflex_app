#!/usr/bin/env python3
"""
Script simplificado para reorganizar la estructura del proyecto AstroTech
"""

import os
import shutil
from pathlib import Path

def create_directories():
    """Crear estructura de directorios"""
    print("Creando estructura de directorios...")

    directories = [
        "config",
        "scripts/database",
        "scripts/deployment",
        "scripts/monitoring",
        "tests/unit",
        "tests/integration",
        "tests/e2e",
        "tests/debug",
        "docs",
        "deployment/docker",
        "data/backup"
    ]

    for directory in directories:
        dir_path = Path(directory)
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  Creado: {directory}")

def move_files_safely():
    """Mover archivos principales de forma segura"""
    print("\nMoviendo archivos principales...")

    # Movimientos importantes
    moves = [
        ("settings.py", "config/settings.py"),
        ("vehicles_local.db", "data/vehicles_local.db"),
        ("astrotech.db", "data/astrotech.db"),
    ]

    for src, dst in moves:
        src_path = Path(src)
        dst_path = Path(dst)

        if src_path.exists():
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src_path), str(dst_path))
            print(f"  Movido: {src} -> {dst}")
        else:
            print(f"  No encontrado: {src}")

def move_test_files():
    """Mover archivos de tests"""
    print("\nMoviendo archivos de tests...")

    test_files = [
        ("test_e2e_simple.py", "tests/e2e/"),
        ("test_vehicle_selector_ui.py", "tests/e2e/"),
        ("conftest.py", "tests/"),
        ("debug_browser.py", "tests/debug/"),
        ("verify_tests.py", "tests/debug/"),
        ("test_vehicle_fix.py", "tests/debug/"),
        ("test_vehicle_selector.html", "tests/debug/"),
    ]

    for src, dst_dir in test_files:
        src_path = Path(src)
        dst_path = Path(dst_dir) / src_path.name

        if src_path.exists():
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src_path), str(dst_path))
            print(f"  Movido: {src} -> {dst_dir}")

def move_scripts():
    """Mover scripts"""
    print("\nMoviendo scripts...")

    script_moves = [
        ("create_local_db.py", "scripts/database/"),
        ("diagnose_database.py", "scripts/database/"),
        ("check_supabase_config.py", "scripts/deployment/"),
        ("verify_production.py", "scripts/deployment/"),
        ("monitor_logs.py", "scripts/monitoring/"),
    ]

    for src, dst_dir in script_moves:
        src_path = Path(src)
        dst_path = Path(dst_dir) / src_path.name

        if src_path.exists():
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src_path), str(dst_path))
            print(f"  Movido: {src} -> {dst_dir}")

def move_docs():
    """Mover documentación"""
    print("\nMoviendo documentación...")

    doc_files = [
        "CLAUDE.md",
        "deploy-guide.md",
        "SUPABASE_INTEGRATION.md"
    ]

    for doc in doc_files:
        src_path = Path(doc)
        dst_path = Path("docs") / doc

        if src_path.exists():
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src_path), str(dst_path))
            print(f"  Movido: {doc} -> docs/")

def create_init_files():
    """Crear archivos __init__.py"""
    print("\nCreando archivos __init__.py...")

    init_dirs = [
        "config",
        "scripts",
        "scripts/database",
        "scripts/deployment",
        "scripts/monitoring",
        "tests/unit",
        "tests/integration",
        "tests/e2e",
        "tests/debug"
    ]

    for directory in init_dirs:
        init_file = Path(directory) / "__init__.py"
        if not init_file.exists():
            init_file.write_text('"""\nPaquete de {}\n"""'.format(directory))
            print(f"  Creado: {directory}/__init__.py")

def update_settings_import():
    """Actualizar imports de settings en archivos principales"""
    print("\nActualizando imports de settings...")

    files_to_check = [
        "rxconfig.py",
        "app/app.py",
        "utils/vehicle_data_supabase.py",
        "state/vehicle_state_simple.py"
    ]

    for file_path in files_to_check:
        path = Path(file_path)
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Reemplazar imports de settings
            updated_content = content.replace('import settings', 'from config import settings')

            if content != updated_content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                print(f"  Actualizado: {file_path}")

def update_rxconfig():
    """Actualizar rxconfig.py para nuevas rutas de BD"""
    print("\nActualizando rxconfig.py...")

    rxconfig_path = Path("rxconfig.py")
    if rxconfig_path.exists():
        with open(rxconfig_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Actualizar rutas de bases de datos
        content = content.replace('sqlite:///astrotech.db', 'sqlite:///data/astrotech.db')
        content = content.replace('sqlite:///vehicles_local.db', 'sqlite:///data/vehicles_local.db')

        with open(rxconfig_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print("  Actualizado: rxconfig.py")

def create_gitignore():
    """Crear .gitignore actualizado"""
    print("\nCreando .gitignore...")

    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Virtual Environment
venv/
env/
ENV/

# Reflex
.web/
.reflex/

# Databases
*.db
data/*.db
!data/.gitkeep

# Logs
logs/*.log
*.log

# Environment
.env
.env.local

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Backup files
*.backup
*.bak
data/backup/*
backup_before_reorganization/

# Test results
test-results/
.coverage
htmlcov/
"""

    with open(".gitignore", 'w', encoding='utf-8') as f:
        f.write(gitignore_content)

    print("  Creado: .gitignore")

def clean_cache():
    """Limpiar caché de Python"""
    print("\nLimpiando caché de Python...")

    import glob

    removed = 0
    for cache_dir in glob.glob("**/__pycache__", recursive=True):
        try:
            shutil.rmtree(cache_dir)
            removed += 1
        except:
            pass

    print(f"  Eliminados {removed} directorios __pycache__")

def main():
    """Función principal"""
    print("REORGANIZACION DEL PROYECTO ASTROTECH")
    print("=" * 50)

    # Verificar que estamos en el lugar correcto
    if not Path("rxconfig.py").exists():
        print("ERROR: No se encontro rxconfig.py")
        return

    try:
        # Ejecutar reorganización
        create_directories()
        create_init_files()
        move_files_safely()
        move_test_files()
        move_scripts()
        move_docs()
        update_settings_import()
        update_rxconfig()
        create_gitignore()
        clean_cache()

        print("\n" + "=" * 50)
        print("REORGANIZACION COMPLETADA")
        print("\nNueva estructura:")
        print("- config/       (Configuracion)")
        print("- data/         (Bases de datos)")
        print("- docs/         (Documentacion)")
        print("- scripts/      (Scripts organizados)")
        print("- tests/        (Tests organizados)")
        print("- deployment/   (Archivos de deployment)")

        print("\nPróximos pasos:")
        print("1. Ejecuta: reflex run")
        print("2. Verifica que todo funciona")
        print("3. Haz git add .")
        print("4. Haz git commit -m 'refactor: reorganizar estructura del proyecto'")

    except Exception as e:
        print(f"\nERROR: {e}")
        print("La reorganizacion fallo. Revisa los errores.")

if __name__ == "__main__":
    main()