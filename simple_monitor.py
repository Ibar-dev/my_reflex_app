#!/usr/bin/env python3
"""
Monitor simple de logs para AstroTech (sin emojis)
"""

import sys
import time
from pathlib import Path

def show_status():
    """Muestra el estado actual del sistema"""
    print("ESTADO DEL SISTEMA ASTROTECH")
    print("=" * 40)

    # Verificar aplicación
    try:
        import requests
        response = requests.get("http://localhost:3000", timeout=2)
        print("Frontend: http://localhost:3000 (Activo)")
    except:
        print("Frontend: http://localhost:3000 (Inactivo)")

    # Verificar backend
    try:
        import requests
        response = requests.get("http://localhost:8000", timeout=2)
        print("Backend: http://localhost:8000 (Activo)")
    except:
        print("Backend: http://localhost:8000 (Inactivo)")

    # Verificar base de datos
    db_files = list(Path(".").glob("*.db"))
    if db_files:
        print(f"Base de datos: {len(db_files)} archivo(s) encontrado(s)")
        for db_file in db_files:
            size = db_file.stat().st_size
            print(f"   - {db_file.name}: {size:,} bytes")
    else:
        print("Base de datos: No se encontraron archivos .db")

    # Verificar archivo de logs
    log_file = Path("astrotech.log")
    if log_file.exists():
        size = log_file.stat().st_size
        print(f"Logs: astrotech.log ({size:,} bytes)")
    else:
        print("Logs: astrotech.log (No existe)")

def show_recent_logs():
    """Muestra logs recientes del archivo"""
    log_file = Path("astrotech.log")

    if not log_file.exists():
        print("Archivo de logs no encontrado: astrotech.log")
        return

    print("ULTIMOS LOGS REGISTRADOS:")
    print("-" * 40)

    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Mostrar últimas líneas
        recent_lines = lines[-20:]  # Últimas 20 líneas
        for line in recent_lines:
            if '[VEHICLE]' in line or 'ERROR' in line:
                print(line.strip())

    except Exception as e:
        print(f"Error leyendo archivo de logs: {e}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--logs":
        show_recent_logs()
    else:
        show_status()
        print()
        print("USO:")
        print("  python simple_monitor.py         - Muestra estado")
        print("  python simple_monitor.py --logs  - Muestra logs recientes")
        print()
        print("INSTRUCCIONES PARA VER LOGS EN TIEMPO REAL:")
        print("1. La aplicación debe estar corriendo (reflex run)")
        print("2. Abre http://localhost:3000/ en el navegador")
        print("3. Abre DevTools (F12) y ve a la pestaña Console")
        print("4. Busca mensajes que empiecen con [VEHICLE]")
        print("5. También puedes revisar la terminal donde corre 'reflex run'")

if __name__ == "__main__":
    main()