"""
Script de diagnóstico para verificar el JSON
"""

from pathlib import Path
import json

print("=" * 60)
print("🔍 DIAGNÓSTICO DEL JSON")
print("=" * 60)

# 1. Buscar el archivo
possible_paths = [
    Path("data/vehiculos_turismo.json"),
    Path("frontend/data/vehiculos_turismo.json"),
    Path("app/data/vehiculos_turismo.json"),
]

json_path = None
for p in possible_paths:
    print(f"\n📁 Buscando en: {p.absolute()}")
    if p.exists():
        json_path = p
        print(f"   ✅ ENCONTRADO")
        break
    else:
        print(f"   ❌ No existe")

if not json_path:
    print("\n❌ NO SE ENCONTRÓ EL ARCHIVO JSON")
    print("\n💡 Solución:")
    print("   1. Verifica que 'vehiculos_turismo.json' existe")
    print("   2. Colócalo en 'data/vehiculos_turismo.json'")
    exit(1)

# 2. Verificar contenido
print(f"\n✅ Archivo encontrado en: {json_path}")

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ JSON válido")
    print(f"📊 Total vehículos: {len(data)}")
    
    if not data:
        print("❌ El JSON está vacío")
        exit(1)
    
    # 3. Verificar estructura
    print("\n🔍 Verificando estructura...")
    first = data[0]
    
    required = ['make', 'model', 'fuel_type', 'year', 'power_stock']
    missing = [f for f in required if f not in first]
    
    if missing:
        print(f"❌ Faltan campos obligatorios: {missing}")
        print(f"   Campos presentes: {list(first.keys())}")
    else:
        print(f"✅ Estructura correcta")
    
    # 4. Análisis de datos
    print("\n📊 Análisis:")
    fuels = {}
    brands = set()
    
    for v in data:
        fuel = v.get('fuel_type', 'unknown')
        fuels[fuel] = fuels.get(fuel, 0) + 1
        brands.add(v.get('make', 'Unknown'))
    
    print(f"   Combustibles: {fuels}")
    print(f"   Marcas: {len(brands)} ({', '.join(sorted(list(brands))[:5])}...)")
    
    # 5. Mostrar ejemplos
    print("\n📋 Primeros 3 vehículos:")
    for i, v in enumerate(data[:3], 1):
        print(f"   {i}. {v.get('make')} {v.get('model')} ({v.get('year')}) - {v.get('fuel_type')}")
    
    print("\n" + "=" * 60)
    print("✅ TODO CORRECTO")
    print("=" * 60)
    
except json.JSONDecodeError as e:
    print(f"\n❌ ERROR DE SINTAXIS EN EL JSON:")
    print(f"   {e}")
    print("\n💡 Usa un validador JSON online para corregirlo")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()