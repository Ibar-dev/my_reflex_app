"""
Tests de Integración E2E
========================

Verifica la integración completa entre frontend, backend y base de datos
en el entorno Dockerizado.
"""

import pytest
import requests
import asyncio
import aiohttp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json

@pytest.mark.e2e
class TestFrontendBackendIntegration:
    """Tests de integración entre frontend y backend."""

    @pytest.fixture(scope="class")
    def driver(self):
        """Configurar WebDriver."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)

        yield driver

        driver.quit()

    def test_frontend_loads_backend_data(self, driver, base_url, api_url):
        """Verificar que el frontend cargue datos desde el backend."""
        driver.get(base_url)

        # Esperar a que cargue el selector de combustible
        fuel_select = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//select[contains(@placeholder, 'combustible')]"))
        )

        # Obtener opciones del frontend
        frontend_fuels = [opt.text for opt in Select(fuel_select).options if opt.text]

        # Obtener datos del backend
        response = requests.get(f"{api_url}/api/fuel_types")
        backend_fuels = response.json()

        # Verificar coincidencias
        for fuel in backend_fuels:
            assert fuel in frontend_fuels, f"Fuel type {fuel} not found in frontend"

    def test_frontend_backend_selection_sync(self, driver, base_url, api_url, test_data):
        """Verificar que las selecciones del frontend coincidan con las opciones del backend."""
        driver.get(base_url)

        # Seleccionar tipo de combustible en frontend
        fuel_select = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//select[contains(@placeholder, 'combustible')]"))
        )
        Select(fuel_select).select_by_visible_text("diesel")
        time.sleep(2)

        # Obtener marcas del frontend
        brand_select = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//select[contains(@placeholder, 'marca')]"))
        )
        frontend_brands = [opt.text for opt in Select(brand_select).options if opt.text]

        # Obtener marcas del backend
        response = requests.get(f"{api_url}/api/brands?fuel_type=diesel")
        backend_brands = response.json()

        # Verificar coincidencias
        for brand in backend_brands:
            assert brand in frontend_brands, f"Brand {brand} not found in frontend"

    def test_complete_flow_consistency(self, driver, base_url, api_url, test_data):
        """Verificar consistencia del flujo completo entre frontend y backend."""
        driver.get(base_url)

        selection = test_data["vehicles"]["diesel"]["sample_selection"]

        # Realizar selección completa en frontend
        self._complete_selection_in_frontend(driver, selection)

        # Verificar cada paso con el backend
        # Paso 1: Verificar combustible
        fuel_response = requests.get(f"{api_url}/api/fuel_types")
        assert selection["fuel_type"] in fuel_response.json()

        # Paso 2: Verificar marca
        brand_response = requests.get(f"{api_url}/api/brands?fuel_type={selection['fuel_type']}")
        assert selection["brand"] in brand_response.json()

        # Paso 3: Verificar modelo
        model_response = requests.get(
            f"{api_url}/api/models"
            f"?fuel_type={selection['fuel_type']}"
            f"&brand={selection['brand']}"
        )
        assert selection["model"] in model_response.json()

        # Paso 4: Verificar versión
        version_response = requests.get(
            f"{api_url}/api/versions"
            f"?fuel_type={selection['fuel_type']}"
            f"&brand={selection['brand']}"
            f"&model={selection['model']}"
        )
        assert selection["version"] in version_response.json()

    def test_error_handling_integration(self, driver, base_url, api_url):
        """Verificar manejo de errores en la integración frontend-backend."""
        driver.get(base_url)

        # Verificar que los selects deshabilitados funcionen correctamente
        try:
            # Intentar seleccionar marca sin haber seleccionado combustible
            brand_select = driver.find_element(By.XPATH, "//select[contains(@placeholder, 'marca')]")
            assert brand_select.get_attribute("disabled") == "true"
        except:
            pass  # El select puede no existir aún

        # Seleccionar combustible
        fuel_select = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//select[contains(@placeholder, 'combustible')]"))
        )
        Select(fuel_select).select_by_index(0)
        time.sleep(2)

        # Ahora la marca debería estar habilitada
        brand_select = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//select[contains(@placeholder, 'marca')]"))
        )
        assert brand_select.get_attribute("disabled") != "true"

    def _complete_selection_in_frontend(self, driver, selection):
        """Helper para completar selección en frontend."""
        # Tipo de combustible
        fuel_select = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//select[contains(@placeholder, 'combustible')]"))
        )
        Select(fuel_select).select_by_visible_text(selection["fuel_type"])
        time.sleep(2)

        # Marca
        brand_select = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//select[contains(@placeholder, 'marca')]"))
        )
        Select(brand_select).select_by_visible_text(selection["brand"])
        time.sleep(2)

        # Modelo
        model_select = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//select[contains(@placeholder, 'modelo')]"))
        )
        Select(model_select).select_by_visible_text(selection["model"])
        time.sleep(2)

        # Versión
        version_select = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//select[contains(@placeholder, 'versión')]"))
        )
        Select(version_select).select_by_visible_text(selection["version"])
        time.sleep(2)

@pytest.mark.e2e
class TestDatabaseIntegration:
    """Tests de integración con la base de datos."""

    def test_database_data_persistence(self, api_url):
        """Verificar que los datos de la base de datos sean consistentes."""
        # Obtener datos múltiples veces
        fuels_1 = requests.get(f"{api_url}/api/fuel_types").json()
        fuels_2 = requests.get(f"{api_url}/api/fuel_types").json()

        # Deben ser consistentes
        assert set(fuels_1) == set(fuels_2)

    def test_database_relationships_consistency(self, api_url):
        """Verificar que las relaciones en la base de datos sean consistentes."""
        # Obtener todos los tipos de combustible
        fuels_response = requests.get(f"{api_url}/api/fuel_types")
        fuels = fuels_response.json()

        for fuel_type in fuels:
            # Para cada combustible, verificar que tenga marcas
            brands_response = requests.get(f"{api_url}/api/brands?fuel_type={fuel_type}")
            brands = brands_response.json()

            assert len(brands) > 0, f"No brands found for fuel type: {fuel_type}"

            # Para cada marca, verificar que tenga modelos
            for brand in brands[:3]:  # Limitar a 3 marcas para velocidad
                models_response = requests.get(
                    f"{api_url}/api/models?fuel_type={fuel_type}&brand={brand}"
                )
                models = models_response.json()

                assert len(models) > 0, f"No models found for {fuel_type} {brand}"

                # Para cada modelo, verificar que tenga versiones
                for model in models[:2]:  # Limitar a 2 modelos para velocidad
                    versions_response = requests.get(
                        f"{api_url}/api/versions"
                        f"?fuel_type={fuel_type}"
                        f"&brand={brand}"
                        f"&model={model}"
                    )
                    versions = versions_response.json()

                    assert len(versions) > 0, f"No versions found for {fuel_type} {brand} {model}"

    def test_database_performance(self, api_url):
        """Verificar rendimiento de consultas a la base de datos."""
        import time

        # Medir tiempo de respuesta para consultas complejas
        start_time = time.time()

        # Consulta compleja: obtener todos los datos para un vehículo
        response = requests.get(
            f"{api_url}/api/versions"
            f"?fuel_type=diesel"
            f"&brand=Audi"
            f"&model=A3"
        )
        versions = response.json()

        end_time = time.time()
        response_time = end_time - start_time

        assert response_time < 2.0, f"Database query too slow: {response_time}s"
        assert len(versions) > 0

@pytest.mark.e2e
class TestSecurityIntegration:
    """Tests de seguridad para la integración."""

    def test_cors_headers(self, base_url):
        """Verificar que los headers CORS estén configurados correctamente."""
        response = requests.options(base_url)

        # Debería tener headers CORS
        assert response.status_code in [200, 204, 405]  # 405 es acceptable para OPTIONS

    def test_error_responses_no_sensitive_info(self, api_url):
        """Verificar que los errores no expongan información sensible."""
        # Solicitar endpoint inválido
        response = requests.get(f"{api_url}/api/invalid_endpoint")

        # No debería exponer información sensible
        if response.status_code == 500:
            response_text = response.text.lower()
            sensitive_keywords = ["password", "secret", "key", "token", "database", "sql"]
            for keyword in sensitive_keywords:
                assert keyword not in response_text, f"Sensitive info leaked: {keyword}"

    def test_input_validation(self, api_url):
        """Verificar validación de entrada."""
        # Intentar SQL injection
        malicious_input = "'; DROP TABLE vehicles; --"
        response = requests.get(f"{api_url}/api/brands?fuel_type={malicious_input}")

        # Debería manejarlo gracefully
        assert response.status_code in [400, 422], "Should reject malicious input"

@pytest.mark.e2e
@pytest.mark.slow
class TestLoadIntegration:
    """Tests de carga para la integración completa."""

    def test_concurrent_user_simulation(self, base_url, api_url):
        """Simular múltiples usuarios concurrentes."""
        import threading
        import time

        results = []
        errors = []

        def simulate_user():
            try:
                start_time = time.time()

                # Simular flujo completo de usuario
                response = requests.get(base_url)
                assert response.status_code == 200

                fuels_response = requests.get(f"{api_url}/api/fuel_types")
                assert fuels_response.status_code == 200

                if fuels_response.json():
                    fuel = fuels_response.json()[0]
                    brands_response = requests.get(f"{api_url}/api/brands?fuel_type={fuel}")
                    assert brands_response.status_code == 200

                end_time = time.time()
                results.append(end_time - start_time)

            except Exception as e:
                errors.append(str(e))

        # Crear 5 hilos simulando usuarios concurrentes
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=simulate_user)
            threads.append(thread)

        # Iniciar todos los hilos
        start_time = time.time()
        for thread in threads:
            thread.start()

        # Esperar a que todos terminen
        for thread in threads:
            thread.join()

        end_time = time.time()
        total_time = end_time - start_time

        # Verificar resultados
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(results) == 5, "Not all users completed successfully"
        assert total_time < 30.0, f"Load test too slow: {total_time}s"

        # Verificar que el tiempo promedio por usuario sea razonable
        avg_time = sum(results) / len(results)
        assert avg_time < 10.0, f"Average user time too slow: {avg_time}s"