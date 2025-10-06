# test_vehicle_data.py
from vehicle_data import debug_json_structure, get_brands_by_fuel

# Ver estructura completa del JSON
debug_json_structure()

# Probar carga de marcas
print("\n🔥 PROBANDO CARGA DE MARCAS:")
print("Diesel:", get_brands_by_fuel("diesel"))
print("Gasolina:", get_brands_by_fuel("gasolina"))