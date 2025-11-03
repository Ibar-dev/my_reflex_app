"""
Script de diagnóstico para verificar la funcionalidad de clics en el selector de vehículos
"""
import sys
import os

def check_files():
    """Verificar que los archivos necesarios existen"""
    print("=" * 60)
    print("DIAGNÓSTICO: Verificación de archivos CSS")
    print("=" * 60)
    
    files_to_check = [
        "assets/styles.css",
        "assets/selector-fix.css",
        "components/vehicle_selector.py",
        "state/vehicle_state_simple.py"
    ]
    
    for file in files_to_check:
        exists = os.path.exists(file)
        status = "✅ Existe" if exists else "❌ NO EXISTE"
        print(f"{status}: {file}")
    
    print()

def check_css_content():
    """Verificar el contenido del CSS fix"""
    print("=" * 60)
    print("DIAGNÓSTICO: Contenido de selector-fix.css")
    print("=" * 60)
    
    css_file = "assets/selector-fix.css"
    if os.path.exists(css_file):
        with open(css_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Verificar reglas críticas
        critical_rules = [
            "pointer-events: auto !important",
            ".rt-SelectTrigger",
            "[role=\"combobox\"]",
            "#selector"
        ]
        
        for rule in critical_rules:
            if rule in content:
                print(f"✅ Encontrado: {rule}")
            else:
                print(f"❌ NO encontrado: {rule}")
    else:
        print("❌ Archivo selector-fix.css no encontrado")
    
    print()

def check_app_stylesheets():
    """Verificar la configuración de stylesheets en app.py"""
    print("=" * 60)
    print("DIAGNÓSTICO: Configuración de stylesheets en app.py")
    print("=" * 60)
    
    app_file = "app/app.py"
    if os.path.exists(app_file):
        with open(app_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar la línea de stylesheets
        if 'stylesheets=' in content:
            print("✅ Configuración de stylesheets encontrada")
            
            # Extraer la línea completa
            for line in content.split('\n'):
                if 'stylesheets=' in line:
                    print(f"   Línea: {line.strip()}")
                    
                    # Verificar orden correcto
                    if 'styles.css' in line and 'selector-fix.css' in line:
                        print("✅ Ambos archivos CSS están incluidos")
                        if line.index('styles.css') < line.index('selector-fix.css'):
                            print("✅ Orden correcto: styles.css primero, selector-fix.css después")
                        else:
                            print("⚠️ ADVERTENCIA: El orden puede ser incorrecto")
                    break
        else:
            print("❌ No se encontró configuración de stylesheets")
    else:
        print("❌ Archivo app/app.py no encontrado")
    
    print()

def check_select_component():
    """Verificar el componente de selector"""
    print("=" * 60)
    print("DIAGNÓSTICO: Componente de selector de vehículos")
    print("=" * 60)
    
    selector_file = "components/vehicle_selector.py"
    if os.path.exists(selector_file):
        with open(selector_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar uso de rx.select.root (nueva sintaxis)
        if 'rx.select.root' in content:
            print("✅ Usando nueva sintaxis rx.select.root")
            count = content.count('rx.select.root')
            print(f"   Encontradas {count} instancias de rx.select.root")
        else:
            print("⚠️ No se encontró rx.select.root (puede usar sintaxis antigua)")
        
        # Verificar eventos on_change
        if 'on_change=' in content:
            print("✅ Eventos on_change configurados")
            count = content.count('on_change=')
            print(f"   Encontrados {count} eventos on_change")
        else:
            print("❌ No se encontraron eventos on_change")
        
        # Verificar cursor pointer
        if 'cursor="pointer"' in content or "cursor='pointer'" in content:
            print("✅ Cursor pointer configurado en componentes")
        else:
            print("⚠️ No se encontró configuración de cursor pointer")
    else:
        print("❌ Archivo vehicle_selector.py no encontrado")
    
    print()

def show_recommendations():
    """Mostrar recomendaciones para solucionar el problema"""
    print("=" * 60)
    print("RECOMENDACIONES")
    print("=" * 60)
    print()
    print("1. REINICIAR EL SERVIDOR:")
    print("   - Detén el servidor de Reflex (Ctrl+C)")
    print("   - Ejecuta: reflex run --loglevel debug")
    print()
    print("2. LIMPIAR CACHÉ:")
    print("   - Elimina la carpeta .web/")
    print("   - Ejecuta: reflex init")
    print("   - Ejecuta: reflex run")
    print()
    print("3. VERIFICAR EN EL NAVEGADOR:")
    print("   - Abre las DevTools (F12)")
    print("   - Ve a la pestaña 'Elements' o 'Inspector'")
    print("   - Busca los elementos <select> o [role='combobox']")
    print("   - Verifica en 'Computed' que pointer-events sea 'auto'")
    print()
    print("4. VERIFICAR CONSOLA DEL NAVEGADOR:")
    print("   - Busca errores JavaScript en la consola")
    print("   - Busca advertencias sobre eventos bloqueados")
    print()
    print("5. FORZAR RECARGA:")
    print("   - Ctrl+Shift+R (Windows/Linux)")
    print("   - Cmd+Shift+R (Mac)")
    print("   - O limpia caché del navegador")
    print()

def main():
    """Ejecutar todos los diagnósticos"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║  DIAGNÓSTICO DE SELECTOR DE VEHÍCULOS - PROBLEMAS DE CLIC  ║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    check_files()
    check_css_content()
    check_app_stylesheets()
    check_select_component()
    show_recommendations()
    
    print("=" * 60)
    print("DIAGNÓSTICO COMPLETADO")
    print("=" * 60)
    print()

if __name__ == "__main__":
    main()
