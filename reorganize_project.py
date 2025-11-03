#!/usr/bin/env python3
"""
Script automatizado para reorganizar la estructura del proyecto AstroTech
"""

import os
import shutil
import glob
from pathlib import Path
import sys

class ProjectReorganizer:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.backup_dir = self.project_root / "backup_before_reorganization"

    def create_directory_structure(self):
        """Crear la nueva estructura de carpetas"""
        print("🏗️ Creando estructura de directorios...")

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
            "data/backup",
            "data/backup/requirements"
        ]

        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"   ✅ Creado: {directory}")

    def create_init_files(self):
        """Crear archivos __init__.py en las nuevas carpetas"""
        print("\n📄 Creando archivos __init__.py...")

        init_directories = [
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

        for directory in init_directories:
            init_file = self.project_root / directory / "__init__.py"
            if not init_file.exists():
                init_file.write_text('"""Paquete de {}"""\n'.format(directory.replace("/", ".")))
                print(f"   ✅ Creado: {directory}/__init__.py")

    def backup_project(self):
        """Crear backup antes de reorganizar"""
        print("💾 Creando backup del proyecto actual...")

        if self.backup_dir.exists():
            shutil.rmtree(self.backup_dir)

        # Crear backup solo de archivos importantes
        important_files = []
        for pattern in ["*.py", "*.md", "*.txt", "*.yml", "*.yaml", "*.json", "*.css", "*.jpg", "*.png", "*.db"]:
            important_files.extend(glob.glob(str(self.project_root / pattern)))

        self.backup_dir.mkdir(exist_ok=True)

        for file_path in important_files:
            rel_path = Path(file_path).relative_to(self.project_root)
            backup_path = self.backup_dir / rel_path
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file_path, backup_path)

        print(f"   ✅ Backup creado en: {self.backup_dir}")

    def move_files(self):
        """Mover archivos a sus nuevas ubicaciones"""
        print("\n📁 Moviendo archivos a nueva estructura...")

        # Movimientos definidos
        moves = [
            # Configuración
            ("settings.py", "config/settings.py"),

            # Scripts de base de datos
            ("create_local_db.py", "scripts/database/create_local_db.py"),
            ("diagnose_database.py", "scripts/database/diagnose_database.py"),
            ("utils/create_vehicles_table.py", "scripts/database/create_vehicles_table.py"),
            ("dev/migrate_vehicle_data.py", "scripts/database/migrate_vehicle_data.py"),
            ("dev/populate_vehicles_db.py", "scripts/database/populate_vehicles_db.py"),
            ("dev/download_vehicle_data.py", "scripts/database/download_vehicle_data.py"),

            # Scripts de deployment
            ("check_supabase_config.py", "scripts/deployment/check_supabase_config.py"),
            ("install_supabase.py", "scripts/deployment/install_supabase.py"),
            ("verify_production.py", "scripts/deployment/verify_production.py"),
            ("deploy_commands.txt", "deployment/deploy_commands.txt"),

            # Scripts de monitoreo
            ("monitor_logs.py", "scripts/monitoring/monitor_logs.py"),
            ("simple_monitor.py", "scripts/monitoring/simple_monitor.py"),

            # Tests E2E
            ("test_e2e_simple.py", "tests/e2e/test_e2e_simple.py"),
            ("test_e2e_supabase.py", "tests/e2e/test_e2e_supabase.py"),
            ("test_e2e_vehicle_selector.py", "tests/e2e/test_e2e_vehicle_selector.py"),
            ("test_production_setup.py", "tests/e2e/test_production_setup.py"),
            ("quick_e2e_test.py", "tests/e2e/quick_e2e_test.py"),
            ("run_e2e_tests.py", "tests/e2e/run_e2e_tests.py"),

            # Tests de integración
            ("integration_test.py", "tests/integration/integration_test.py"),
            ("test_supabase_integration.py", "tests/integration/test_supabase_integration.py"),
            ("test_simple_supabase.py", "tests/integration/test_simple_supabase.py"),

            # Tests de debugging
            ("debug_browser.py", "tests/debug/debug_browser.py"),
            ("debug_production.py", "tests/debug/debug_production.py"),
            ("simple_diagnosis.py", "tests/debug/simple_diagnosis.py"),
            ("simple_test.py", "tests/debug/simple_test.py"),
            ("test_vehicle_fix.py", "tests/debug/test_vehicle_fix.py"),
            ("test_browser_interaction.py", "tests/debug/test_browser_interaction.py"),
            ("test_selector_clicks.py", "tests/debug/test_selector_clicks.py"),
            ("verify_tests.py", "tests/debug/verify_tests.py"),
            ("test_vehicle_selector.html", "tests/debug/test_vehicle_selector.html"),

            # Documentación
            ("deploy-guide.md", "docs/deploy-guide.md"),
            ("docker-instructions.md", "docs/docker-instructions.md"),
            ("INSTRUCCIONES_LOGS.md", "docs/INSTRUCCIONES_LOGS.md"),
            ("MANUAL_CHANGES_REQUIRED.md", "docs/MANUAL_CHANGES_REQUIRED.md"),
            ("SUPABASE_INTEGRATION.md", "docs/SUPABASE_INTEGRATION.md"),
            ("TEST_E2E_REPORT.md", "docs/TEST_E2E_REPORT.md"),
            ("test_summary.md", "docs/test_summary.md"),
            ("CLAUDE.md", "docs/CLAUDE.md"),

            # Docker
            ("Dockerfile", "deployment/docker/Dockerfile"),
            ("docker-compose.yml", "deployment/docker/docker-compose.yml"),
            ("docker-compose.prod.yml", "deployment/docker/docker-compose.prod.yml"),
            ("docker-compose.test.yml", "deployment/docker/docker-compose.test.yml"),
            ("nginx.conf", "deployment/docker/nginx.conf"),
            ("nginx.prod.conf", "deployment/docker/nginx.prod.conf"),

            # Datos
            ("backup/vehicles_api_cache.json", "data/backup/vehicles_api_cache.json"),
            ("backup/vehiculos_turismo.json", "data/backup/vehiculos_turismo.json"),
            ("vehicles_local.db", "data/vehicles_local.db"),
            ("astrotech.db", "data/astrotech.db"),
            ("requirements_backup.txt", "data/backup/requirements/requirements_backup.txt"),
            ("requirements_new.txt", "data/backup/requirements/requirements_new.txt")
        ]

        moved_count = 0
        for src, dst in moves:
            src_path = self.project_root / src
            dst_path = self.project_root / dst

            if src_path.exists():
                # Crear directorio destino si no existe
                dst_path.parent.mkdir(parents=True, exist_ok=True)

                # Mover archivo
                shutil.move(str(src_path), str(dst_path))
                print(f"   ✅ Movido: {src} → {dst}")
                moved_count += 1
            else:
                print(f"   ⚠️ No encontrado: {src}")

        # Eliminar carpetas vacías
        self._remove_empty_directories()

        print(f"\n📊 Total de archivos movidos: {moved_count}")

    def _remove_empty_directories(self):
        """Eliminar directorios vacíos después de mover archivos"""
        empty_dirs = [
            "dev",
            "backup"
        ]

        for dir_name in empty_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists() and dir_path.is_dir():
                try:
                    # Verificar si está vacío
                    if not any(dir_path.iterdir()):
                        dir_path.rmdir()
                        print(f"   🗑️ Eliminado directorio vacío: {dir_name}")
                except OSError:
                    print(f"   ⚠️ No se pudo eliminar directorio: {dir_name}")

    def update_imports(self):
        """Actualizar imports en archivos Python"""
        print("\n🔧 Actualizando imports en archivos Python...")

        # Archivos que necesitan actualización de imports
        files_to_check = []
        for pattern in ["**/*.py"]:
            files_to_check.extend(glob.glob(str(self.project_root / pattern), recursive=True))

        updated_files = 0

        for file_path in files_to_check:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                original_content = content

                # Actualizar imports de settings
                content = content.replace('import settings', 'from config import settings')
                content = content.replace('from settings import', 'from config.settings import')

                # Actualizar referencias a bases de datos
                content = content.replace('sqlite:///astrotech.db', 'sqlite:///data/astrotech.db')
                content = content.replace('sqlite:///vehicles_local.db', 'sqlite:///data/vehicles_local.db')

                # Actualizar imports relativos si es necesario
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    updated_files += 1

            except Exception as e:
                print(f"   ⚠️ Error procesando {file_path}: {e}")

        print(f"   ✅ Archivos actualizados: {updated_files}")

    def create_gitignore(self):
        """Crear/actualizar .gitignore"""
        print("\n📝 Creando .gitignore actualizado...")

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

# Node modules (si hay)
node_modules/

# Archivos temporales
*.tmp
*.temp
.cache/
"""

        gitignore_path = self.project_root / ".gitignore"
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(gitignore_content)

        print("   ✅ .gitignore actualizado")

    def update_rxconfig(self):
        """Actualizar rxconfig.py para nuevas rutas"""
        print("\n⚙️ Actualizando rxconfig.py...")

        rxconfig_path = self.project_root / "rxconfig.py"
        if rxconfig_path.exists():
            with open(rxconfig_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Actualizar rutas de bases de datos
            content = content.replace('sqlite:///astrotech.db', 'sqlite:///data/astrotech.db')
            content = content.replace('sqlite:///vehicles_local.db', 'sqlite:///data/vehicles_local.db')

            with open(rxconfig_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print("   ✅ rxconfig.py actualizado")
        else:
            print("   ⚠️ rxconfig.py no encontrado")

    def clean_python_cache(self):
        """Limpiar caché de Python"""
        print("\n🧹 Limpiando caché de Python...")

        removed_count = 0
        for pattern in ["**/__pycache__", "**/*.pyc", "**/*.pyo"]:
            for item_path in glob.glob(str(self.project_root / pattern), recursive=True):
                try:
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)
                    removed_count += 1
                except Exception as e:
                    print(f"   ⚠️ No se pudo eliminar {item_path}: {e}")

        print(f"   ✅ Eliminados {removed_count} archivos de caché")

    def create_project_summary(self):
        """Crear resumen de la nueva estructura"""
        print("\n📊 Creando resumen del proyecto...")

        summary_content = """# 🗂️ Estructura del Proyecto AstroTech

## 📁 Directorios Principales

### `/app/`
- `app.py` - Aplicación principal Reflex

### `/components/`
- Componentes UI de la aplicación
- `vehicle_selector.py` - Selector de vehículos
- `contact.py` - Formulario de contacto
- etc.

### `/state/`
- Estados de la aplicación Reflex
- `vehicle_state_simple.py` - Estado del selector
- `contact_state.py` - Estado del formulario

### `/utils/`
- Utilidades y servicios
- `vehicle_data_supabase.py` - Conexión a Supabase
- `email_service.py` - Servicio de email

### `/config/`
- `settings.py` - Configuración de la aplicación

### `/scripts/`
- Scripts de utilidad organizados por categoría
- `database/` - Scripts de base de datos
- `deployment/` - Scripts de deployment
- `monitoring/` - Scripts de monitoreo

### `/tests/`
- Tests organizados por tipo
- `unit/` - Tests unitarios
- `integration/` - Tests de integración
- `e2e/` - Tests end-to-end
- `debug/` - Scripts de debugging

### `/docs/`
- Documentación del proyecto

### `/deployment/`
- Archivos de deployment y Docker

### `/data/`
- Bases de datos y backups

## 🚀 Comandos Útiles

### Desarrollo Local
```bash
reflex run
```

### Tests
```bash
# Tests E2E
pytest tests/e2e/ -v

# Tests de integración
pytest tests/integration/ -v

# Tests específicos
pytest tests/e2e/test_vehicle_selector_ui.py -v
```

### Deployment
```bash
# Deploy a producción
reflex deploy --project fdb58d37-e45b-4e5f-8197-213cff0219be
```

## 📝 Notas
- Las bases de datos ahora están en `/data/`
- La configuración está en `/config/`
- Los tests están organizados por tipo
- Los scripts están categorizados por función
"""

        summary_path = self.project_root / "docs" / "PROJECT_STRUCTURE.md"
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)

        print("   ✅ Resumen creado en docs/PROJECT_STRUCTURE.md")

    def run_reorganization(self):
        """Ejecutar reorganización completa"""
        print("🚀 INICIANDO REORGANIZACIÓN DEL PROYECTO ASTROTECH")
        print("=" * 60)

        try:
            # 1. Backup
            self.backup_project()

            # 2. Crear estructura
            self.create_directory_structure()
            self.create_init_files()

            # 3. Mover archivos
            self.move_files()

            # 4. Actualizar código
            self.update_imports()
            self.update_rxconfig()

            # 5. Crear archivos de configuración
            self.create_gitignore()

            # 6. Limpiar
            self.clean_python_cache()

            # 7. Documentación
            self.create_project_summary()

            print("\n" + "=" * 60)
            print("✅ REORGANIZACIÓN COMPLETADA EXITOSAMENTE")
            print(f"📁 Backup guardado en: {self.backup_dir}")
            print("\n📋 Próximos pasos:")
            print("1. Revisa los archivos movidos")
            print("2. Ejecuta 'reflex run' para verificar que todo funciona")
            print("3. Si funciona correctamente, haz commit de los cambios")
            print("4. Deploy a producción")

        except Exception as e:
            print(f"\n❌ ERROR durante la reorganización: {e}")
            print(f"💾 Puedes restaurar desde: {self.backup_dir}")
            sys.exit(1)

def main():
    """Función principal"""
    project_root = Path(__file__).parent

    print("Verificando ubicacion del proyecto...")
    print(f"Raiz del proyecto: {project_root}")

    # Verificar que estamos en el lugar correcto
    if not (project_root / "rxconfig.py").exists():
        print("ERROR: No se encontro rxconfig.py. ¿Estas en el directorio correcto del proyecto?")
        sys.exit(1)

    # Confirmar reorganización
    response = input("\nADVERTENCIA: Esta reorganizacion movera muchos archivos. ¿Deseas continuar? (s/N): ")
    if response.lower() not in ['s', 'si', 'yes', 'y']:
        print("Reorganizacion cancelada")
        sys.exit(0)

    # Ejecutar reorganización
    reorganizer = ProjectReorganizer(project_root)
    reorganizer.run_reorganization()

if __name__ == "__main__":
    main()