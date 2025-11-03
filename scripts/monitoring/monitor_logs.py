#!/usr/bin/env python3
"""
Monitor de logs en tiempo real para AstroTech
===========================================

Uso:
    python monitor_logs.py                    # Muestra logs de la terminal
    python monitor_logs.py --tail            # Solo logs recientes
    python monitor_logs.py --file            # Muestra logs del archivo
    python monitor_logs.py --help           # Muestra ayuda
"""

import argparse
import sys
import time
import subprocess
from pathlib import Path

def monitor_terminal_logs():
    """Monitorea los logs de la terminal donde corre reflex run"""
    print("🔍 Monitoreando logs de terminal de Reflex...")
    print("📝 Abre http://localhost:3000/ y usa el selector de vehículos")
    print("⏹️  Presiona Ctrl+C para detener el monitoreo")
    print("-" * 60)

    try:
        # En Windows, no podemos monitorear fácilmente otra terminal
        # Así que mostramos instrucciones
        print("\n📋 INSTRUCCIONES:")
        print("1. Abre la terminal donde corre 'reflex run'")
        print("2. Busca mensajes que empiecen con [VEHICLE]")
        print("3. Ejemplos de mensajes a buscar:")
        print("   - [VEHICLE] Iniciando carga de tipos de combustible")
        print("   - [VEHICLE] Tipos de combustible cargados: 1")
        print("   - [VEHICLE] Combustible seleccionado: diesel")
        print("\n💡 También puedes revisar el archivo astrotech.log")

        # Opcional: intentar monitorear el archivo de log
        log_file = Path("astrotech.log")
        if log_file.exists():
            print(f"\n📁 Monitoreando archivo de logs: {log_file}")
            try:
                # Para Windows usar type
                if sys.platform == "win32":
                    process = subprocess.Popen(['powershell', '-Command', f'Get-Content "{log_file}" -Wait -Tail 10'],
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                else:
                    process = subprocess.Popen(['tail', '-f', str(log_file)],
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                for line in iter(process.stdout.readline, ''):
                    if '[VEHICLE]' in line:
                        print(f"🚗 {line.strip()}")

            except Exception as e:
                print(f"No se pudo monitorear el archivo: {e}")

        print("\n⏳ Esperando interacciones del usuario...")

        # Mantener el script corriendo
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n⏹️  Monitoreo detenido")

def monitor_file_logs():
    """Muestra los logs almacenados en el archivo"""
    log_file = Path("astrotech.log")

    if not log_file.exists():
        print(f"❌ Archivo de logs no encontrado: {log_file}")
        return

    print(f"📁 Mostrando logs del archivo: {log_file}")
    print("-" * 60)

    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Filtrar y mostrar solo logs relevantes
        vehicle_logs = [line for line in lines if '[VEHICLE]' in line]
        error_logs = [line for line in lines if 'ERROR' in line or 'Error' in line]

        if vehicle_logs:
            print("🚗 Logs del Selector de Vehículos:")
            for log in vehicle_logs[-20:]:  # Últimos 20 logs
                print(f"  {log.strip()}")

        if error_logs:
            print("\n❌ Logs de Error:")
            for log in error_logs[-10:]:  # Últimos 10 errores
                print(f"  {log.strip()}")

        if not vehicle_logs and not error_logs:
            print("ℹ️  No se encontraron logs relevantes")

    except Exception as e:
        print(f"❌ Error leyendo el archivo de logs: {e}")

def show_status():
    """Muestra el estado actual del sistema"""
    print("📊 Estado del Sistema AstroTech")
    print("-" * 40)

    # Verificar aplicación
    try:
        import requests
        response = requests.get("http://localhost:3000", timeout=2)
        print("✅ Frontend: http://localhost:3000 (Activo)")
    except:
        print("❌ Frontend: http://localhost:3000 (Inactivo)")

    # Verificar backend
    try:
        import requests
        response = requests.get("http://localhost:8000", timeout=2)
        print("✅ Backend: http://localhost:8000 (Activo)")
    except:
        print("❌ Backend: http://localhost:8000 (Inactivo)")

    # Verificar base de datos
    db_files = list(Path(".").glob("*.db"))
    if db_files:
        print(f"✅ Base de datos: {len(db_files)} archivo(s) encontrado(s)")
        for db_file in db_files:
            size = db_file.stat().st_size
            print(f"   - {db_file.name}: {size:,} bytes")
    else:
        print("❌ Base de datos: No se encontraron archivos .db")

    # Verificar archivo de logs
    log_file = Path("astrotech.log")
    if log_file.exists():
        size = log_file.stat().st_size
        print(f"✅ Logs: astrotech.log ({size:,} bytes)")
    else:
        print("❌ Logs: astrotech.log (No existe)")

def main():
    parser = argparse.ArgumentParser(description="Monitor de logs para AstroTech")
    parser.add_argument("--tail", action="store_true", help="Mostrar solo logs recientes")
    parser.add_argument("--file", action="store_true", help="Mostrar logs del archivo")
    parser.add_argument("--status", action="store_true", help="Mostrar estado del sistema")

    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.file:
        monitor_file_logs()
    else:
        show_status()
        print()
        monitor_terminal_logs()

if __name__ == "__main__":
    main()