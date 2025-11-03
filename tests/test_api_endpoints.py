"""
Tests E2E para API Endpoints
============================

Verifica que todos los endpoints de la API funcionen correctamente
en el entorno Dockerizado.
"""

import pytest
import aiohttp
import asyncio
import json
from typing import Dict, Any, List

@pytest.mark.e2e
@pytest.mark.api
class TestAPIHealth:
    """Tests de salud y conectividad de la API."""

    @pytest.mark.asyncio
    async def test_api_health_check(self, test_client, api_url):
        """Verificar que el endpoint de health funciona."""
        async with test_client.get(f"{api_url}/ping") as response:
            assert response.status == 200
            data = await response.json()
            assert data["status"] == "ok"

    @pytest.mark.asyncio
    async def test_api_root_accessible(self, test_client, api_url):
        """Verificar que el root de la API es accesible."""
        async with test_client.get(api_url) as response:
            assert response.status in [200, 404]  # 404 es aceptable si no hay root endpoint

@pytest.mark.e2e
@pytest.mark.api
class TestVehicleDataAPI:
    """Tests para los datos de vehículos en la API."""

    @pytest.mark.asyncio
    async def test_get_fuel_types(self, test_client, api_url, test_data):
        """Verificar obtención de tipos de combustible."""
        async with test_client.get(f"{api_url}/api/fuel_types") as response:
            assert response.status == 200
            data = await response.json()
            assert isinstance(data, list)
            expected_fuels = ["diesel", "gasolina", "hibrido", "electrico"]
            for fuel in expected_fuels:
                assert fuel in data

    @pytest.mark.asyncio
    async def test_get_brands_by_fuel_type(self, test_client, api_url, test_data):
        """Verificar obtención de marcas por tipo de combustible."""
        fuel_type = "diesel"
        async with test_client.get(f"{api_url}/api/brands?fuel_type={fuel_type}") as response:
            assert response.status == 200
            data = await response.json()
            assert isinstance(data, list)
            assert len(data) > 0
            expected_brands = test_data["vehicles"]["diesel"]["brands"]
            for brand in expected_brands:
                assert brand in data

    @pytest.mark.asyncio
    async def test_get_models_by_brand_and_fuel(self, test_client, api_url, test_data):
        """Verificar obtención de modelos por marca y combustible."""
        fuel_type = "diesel"
        brand = "Audi"
        async with test_client.get(
            f"{api_url}/api/models?fuel_type={fuel_type}&brand={brand}"
        ) as response:
            assert response.status == 200
            data = await response.json()
            assert isinstance(data, list)
            assert len(data) > 0
            assert "A3" in data

    @pytest.mark.asyncio
    async def test_get_versions_complete_flow(self, test_client, api_url, test_data):
        """Verificar obtención de versiones con flujo completo."""
        selection = test_data["vehicles"]["diesel"]["sample_selection"]

        async with test_client.get(
            f"{api_url}/api/versions"
            f"?fuel_type={selection['fuel_type']}"
            f"&brand={selection['brand']}"
            f"&model={selection['model']}"
        ) as response:
            assert response.status == 200
            data = await response.json()
            assert isinstance(data, list)
            assert len(data) > 0
            assert selection["version"] in data

    @pytest.mark.asyncio
    async def test_invalid_fuel_type_400(self, test_client, api_url):
        """Verificar manejo de tipo de combustible inválido."""
        async with test_client.get(f"{api_url}/api/brands?fuel_type=invalid") as response:
            assert response.status == 400

    @pytest.mark.asyncio
    async def test_invalid_brand_400(self, test_client, api_url):
        """Verificar manejo de marca inválida."""
        async with test_client.get(
            f"{api_url}/api/models?fuel_type=diesel&brand=InvalidBrand"
        ) as response:
            assert response.status == 400

@pytest.mark.e2e
@pytest.mark.api
class TestVehicleFlowAPI:
    """Tests para el flujo completo de selección de vehículos."""

    @pytest.mark.asyncio
    async def test_complete_diesel_flow(self, test_client, api_url, test_data):
        """Verificar flujo completo para vehículos diesel."""
        selection = test_data["vehicles"]["diesel"]["sample_selection"]

        # Paso 1: Obtener tipos de combustible
        async with test_client.get(f"{api_url}/api/fuel_types") as response:
            assert response.status == 200
            fuels = await response.json()
            assert selection["fuel_type"] in fuels

        # Paso 2: Obtener marcas para diesel
        async with test_client.get(
            f"{api_url}/api/brands?fuel_type={selection['fuel_type']}"
        ) as response:
            assert response.status == 200
            brands = await response.json()
            assert selection["brand"] in brands

        # Paso 3: Obtener modelos para Audi diesel
        async with test_client.get(
            f"{api_url}/api/models"
            f"?fuel_type={selection['fuel_type']}"
            f"&brand={selection['brand']}"
        ) as response:
            assert response.status == 200
            models = await response.json()
            assert selection["model"] in models

        # Paso 4: Obtener versiones para Audi A3 diesel
        async with test_client.get(
            f"{api_url}/api/versions"
            f"?fuel_type={selection['fuel_type']}"
            f"&brand={selection['brand']}"
            f"&model={selection['model']}"
        ) as response:
            assert response.status == 200
            versions = await response.json()
            assert selection["version"] in versions

    @pytest.mark.asyncio
    async def test_complete_electric_flow(self, test_client, api_url, test_data):
        """Verificar flujo completo para vehículos eléctricos."""
        selection = test_data["vehicles"]["electrico"]["sample_selection"]

        # Flujo completo para eléctricos
        async with test_client.get(f"{api_url}/api/fuel_types") as response:
            assert response.status == 200
            fuels = await response.json()
            assert selection["fuel_type"] in fuels

        async with test_client.get(
            f"{api_url}/api/brands?fuel_type={selection['fuel_type']}"
        ) as response:
            assert response.status == 200
            brands = await response.json()
            assert selection["brand"] in brands

        async with test_client.get(
            f"{api_url}/api/models"
            f"?fuel_type={selection['fuel_type']}"
            f"&brand={selection['brand']}"
        ) as response:
            assert response.status == 200
            models = await response.json()
            assert selection["model"] in models

        async with test_client.get(
            f"{api_url}/api/versions"
            f"?fuel_type={selection['fuel_type']}"
            f"&brand={selection['brand']}"
            f"&model={selection['model']}"
        ) as response:
            assert response.status == 200
            versions = await response.json()
            assert selection["version"] in versions

    @pytest.mark.asyncio
    async def test_multiple_fuel_types_availability(self, test_client, api_url, test_data):
        """Verificar que todos los tipos de combustible tengan datos."""
        async with test_client.get(f"{api_url}/api/fuel_types") as response:
            assert response.status == 200
            fuel_types = await response.json()

            for fuel_type in fuel_types:
                async with test_client.get(
                    f"{api_url}/api/brands?fuel_type={fuel_type}"
                ) as response:
                    assert response.status == 200
                    brands = await response.json()
                    assert len(brands) > 0, f"No hay marcas para {fuel_type}"

@pytest.mark.e2e
@pytest.mark.api
class TestAPIPerformance:
    """Tests de rendimiento para la API."""

    @pytest.mark.asyncio
    async def test_api_response_time(self, test_client, api_url):
        """Verificar que los tiempos de respuesta sean aceptables."""
        import time

        start_time = time.time()
        async with test_client.get(f"{api_url}/api/fuel_types") as response:
            await response.text()
            end_time = time.time()

        response_time = end_time - start_time
        assert response_time < 2.0, f"Response time too slow: {response_time}s"

    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_concurrent_requests(self, test_client, api_url):
        """Verificar que la API maneje múltiples solicitudes concurrentes."""
        import asyncio

        async def make_request():
            async with test_client.get(f"{api_url}/api/fuel_types") as response:
                return response.status

        # Hacer 10 solicitudes concurrentes
        tasks = [make_request() for _ in range(10)]
        results = await asyncio.gather(*tasks)

        # Todas deberían ser exitosas
        assert all(status == 200 for status in results)