"""
Datos de vehículos para reprogramación ECU - AstroTech
======================================================

Este archivo contiene todos los datos de vehículos disponibles para
reprogramación ECU, organizados por marca, modelo y año.

ESTRUCTURA DE DATOS:
- Marcas principales: Audi, BMW, Mercedes-Benz, Volkswagen, Seat, Skoda
- Modelos por marca con diferentes versiones
- Años de fabricación disponibles
- Información técnica de cada vehículo

DATOS POR VEHÍCULO:
- year: Año de fabricación
- fuel_type: Tipo de combustible ('diesel' o 'gasolina')
- original_power: Potencia original en CV
- tuned_power: Potencia después de reprogramación en CV
- consumption_reduction: Reducción de consumo en porcentaje
- price: Precio de la reprogramación en euros
- description: Descripción técnica del vehículo

MARCAS INCLUIDAS:
- Audi: A3, A4, Q5
- BMW: Serie 3, Serie 5, X3
- Mercedes-Benz: Clase C, Clase E, GLC
- Volkswagen: Golf, Passat, Tiguan
- Seat: Ibiza, Leon, Ateca
- Skoda: Octavia, Superb, Kodiaq

FILTRADO:
- Los datos se filtran dinámicamente según:
  - Tipo de combustible seleccionado
  - Marca seleccionada
  - Modelo seleccionado
  - Año seleccionado

USO:
- Importado por VehicleState para filtrado
- Utilizado por el selector de vehículos
- Base de datos local para la aplicación

ACTUALIZACIONES FUTURAS:
- Integración con base de datos real
- API para datos dinámicos
- Más marcas y modelos
- Precios actualizados automáticamente
"""

def get_vehicle_data() -> dict:
    """
    Obtener datos de vehículos disponibles para reprogramación
    
    Returns:
        dict: Diccionario con datos de vehículos organizados por marca/modelo/año
    """
    # TODO: Implementar datos completos de vehículos
    return {}

# TODO: Implementar estructura completa de datos
# Estructura esperada:
# {
#     'Marca': {
#         'Modelo': [
#             {
#                 'year': int,
#                 'fuel_type': str,
#                 'original_power': int,
#                 'tuned_power': int,
#                 'consumption_reduction': int,
#                 'price': int,
#                 'description': str
#             }
#         ]
#     }
# }

# TODO: Agregar funciones auxiliares
# - get_brands_by_fuel(): Obtener marcas por combustible
# - get_models_by_brand(): Obtener modelos por marca
# - get_years_by_model(): Obtener años por modelo
# - validate_vehicle_data(): Validar datos de vehículos
# - calculate_improvements(): Calcular mejoras de potencia/consumo