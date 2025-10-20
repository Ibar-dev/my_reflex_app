"""
Servicio de API de Vehículos para AstroTech
==========================================

Integración con APIs externas para obtener datos completos de vehículos.
Incluye cache local para optimizar rendimiento.
"""

import httpx
import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path
import reflex as rx

class VehicleAPIService:
    """Servicio para obtener datos de vehículos desde APIs externas"""
    
    def __init__(self):
        self.nhtsa_base = "https://vpic.nhtsa.dot.gov/api"
        self.carquery_base = "https://www.carqueryapi.com/api/0.3"
        self.cache_file = "data/vehicles_api_cache.json"
        self.cache_duration = timedelta(days=7)  # Cache válido por 1 semana
        
    def _ensure_cache_dir(self):
        """Asegurar que existe el directorio de cache"""
        Path(self.cache_file).parent.mkdir(exist_ok=True)
    
    def _load_cache(self) -> Optional[Dict]:
        """Cargar cache desde archivo"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                    
                # Verificar si el cache es válido
                cache_date = datetime.fromisoformat(cache_data.get('cached_at', '2000-01-01'))
                if datetime.now() - cache_date < self.cache_duration:
                    return cache_data
                    
        except Exception as e:
            print(f"Error cargando cache: {e}")
        
        return None
    
    def _save_cache(self, data: Dict):
        """Guardar datos en cache"""
        try:
            self._ensure_cache_dir()
            cache_data = {
                'cached_at': datetime.now().isoformat(),
                'data': data
            }
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando cache: {e}")
    
    async def get_makes_from_nhtsa(self) -> List[Dict]:
        """Obtener todas las marcas desde NHTSA API (US Department of Transportation)"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.nhtsa_base}/vehicles/getallmakes?format=json"
                )
                response.raise_for_status()
                data = response.json()
                return data.get("Results", [])
        except Exception as e:
            print(f"Error obteniendo marcas NHTSA: {e}")
            return []
    
    async def get_models_from_nhtsa(self, make: str) -> List[Dict]:
        """Obtener modelos por marca desde NHTSA API"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.nhtsa_base}/vehicles/getmodelsformake/{make}?format=json"
                )
                response.raise_for_status()
                data = response.json()
                return data.get("Results", [])
        except Exception as e:
            print(f"Error obteniendo modelos NHTSA para {make}: {e}")
            return []
    
    async def sync_vehicle_data(self) -> Dict:
        """Sincronizar datos de vehículos desde APIs externas"""
        print("[API] Iniciando sincronización de vehículos desde APIs...")
        
        # Intentar cargar desde cache primero
        cached_data = self._load_cache()
        if cached_data:
            print("[API] Datos cargados desde cache (válido)")
            return cached_data['data']
        
        print("[API] Cache expirado o no existe, obteniendo datos frescos...")
        
        vehicle_data = {}
        total_vehicles = 0
        
        try:
            # Obtener marcas principales desde NHTSA
            print("📋 Obteniendo marcas desde NHTSA (US DOT)...")
            makes = await self.get_makes_from_nhtsa()
            
            # Filtrar las marcas más populares para ECU tuning
            popular_makes = [
                "AUDI", "BMW", "MERCEDES-BENZ", "VOLKSWAGEN", "PORSCHE",
                "FORD", "CHEVROLET", "DODGE", "TOYOTA", "HONDA", 
                "NISSAN", "MAZDA", "SUBARU", "MITSUBISHI", "HYUNDAI",
                "KIA", "VOLVO", "JAGUAR", "LAND ROVER", "MINI",
                "SEAT", "SKODA", "OPEL", "PEUGEOT", "CITROEN",
                "RENAULT", "FIAT", "ALFA ROMEO", "JEEP"
            ]
            
            # Procesar solo marcas populares para ECU tuning
            for make_data in makes:
                make_name = make_data.get("Make_Name", "").upper()
                
                if any(popular in make_name for popular in popular_makes):
                    print(f"  🚗 Procesando marca: {make_name}")
                    
                    # Obtener modelos para esta marca
                    models = await self.get_models_from_nhtsa(make_name)
                    
                    if models:
                        vehicle_data[make_name] = []
                        
                        for model_data in models:
                            model_name = model_data.get("Model_Name", "")
                            if model_name:
                                # Generar años típicos para ECU tuning (2010-2024)
                                years = list(range(2010, 2025))
                                
                                vehicle_info = {
                                    "model": model_name,
                                    "years": years,
                                    "fuel_types": ["diesel", "gasolina"],  # Por defecto ambos
                                    "ecu_compatible": True,
                                    "source": "nhtsa_api"
                                }
                                
                                vehicle_data[make_name].append(vehicle_info)
                                total_vehicles += 1
                        
                        print(f"    [OK] {len(models)} modelos procesados")
                    
                    # Limitar requests para evitar rate limiting
                    await asyncio.sleep(0.5)
            
            # Guardar en cache
            self._save_cache(vehicle_data)
            
            print(f"[API] Sincronización completada: {len(vehicle_data)} marcas, {total_vehicles} vehículos")
            
        except Exception as e:
            print(f"[API] Error durante sincronización: {e}")
            # Intentar devolver datos de cache aunque esté expirado
            cached_data = self._load_cache()
            if cached_data:
                print("[API] Usando datos de cache expirados como respaldo")
                return cached_data['data']
        
        return vehicle_data
    
    def get_cached_stats(self) -> Dict:
        """Obtener estadísticas del cache actual"""
        cached_data = self._load_cache()
        if not cached_data:
            return {"cached": False, "total_makes": 0, "total_vehicles": 0}
        
        data = cached_data['data']
        total_makes = len(data)
        total_vehicles = sum(len(models) for models in data.values())
        cache_date = cached_data.get('cached_at', 'Desconocido')
        
        return {
            "cached": True,
            "total_makes": total_makes,
            "total_vehicles": total_vehicles,
            "cache_date": cache_date,
            "cache_valid": datetime.now() - datetime.fromisoformat(cache_date) < self.cache_duration
        }

# Función de utilidad para uso en el estado
async def sync_vehicles_from_api() -> Dict:
    """Función de utilidad para sincronizar vehículos"""
    service = VehicleAPIService()
    return await service.sync_vehicle_data()

def get_api_cache_stats() -> Dict:
    """Obtener estadísticas del cache de API"""
    service = VehicleAPIService()
    return service.get_cached_stats()