#!/usr/bin/env python3
"""
Script de diagnóstico para ejecutar en la consola del navegador
en producción. Copia y pega este código en la consola de desarrollo
de tu aplicación desplegada.
"""

# Pega este código en la consola del navegador (F12) en producción
browser_debug_code = """
// Diagnóstico en producción - Pega en la consola del navegador
console.log('=== DIAGNÓSTICO PRODUCCIÓN ASTROTECH ===');

// 1. Verificar entorno
console.log('1. Entorno:', window.location.href);
console.log('2. User Agent:', navigator.userAgent);

// 2. Verificar si Reflex está cargado
if (window.reflex) {
    console.log('3. Reflex: ✅ Cargado');
} else {
    console.log('3. Reflex: ❌ No encontrado');
}

// 3. Verificar eventos del selector de vehículos
setTimeout(() => {
    const selector = document.getElementById('selector');
    if (selector) {
        console.log('4. Selector encontrado: ✅');

        // Buscar selects
        const selects = selector.querySelectorAll('select');
        console.log('5. Selects encontrados:', selects.length);

        // Verificar opciones del primer select (combustible)
        if (selects[0]) {
            const options = selects[0].querySelectorAll('option');
            console.log('6. Opciones de combustible:', options.length);

            if (options.length > 1) {
                console.log('✅ Selector tiene datos');
            } else {
                console.log('❌ Selector vacío - problema de carga');
            }
        }
    } else {
        console.log('4. Selector: ❌ No encontrado');
    }

    // 7. Verificar errores de red
    fetch('/api_fuel_types')
        .then(response => response.json())
        .then(data => console.log('8. API Response:', data))
        .catch(error => console.log('8. API Error:', error));

}, 2000);

console.log('=== FIN DIAGNÓSTICO ===');
"""

print("COPIA Y PEGA ESTE CÓDIGO EN LA CONSOLA DEL NAVEGADOR:")
print("=" * 60)
print(browser_debug_code)
print("=" * 60)
print("\nPasos:")
print("1. Abre tu aplicación en producción")
print("2. Presiona F12 para abrir herramientas de desarrollador")
print("3. Ve a la pestaña 'Console'")
print("4. Copia y pega el código de arriba")
print("5. Presiona Enter y revisa los resultados")