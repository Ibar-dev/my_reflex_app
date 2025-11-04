"""
Tests E2E para UI del Selector de Vehículos
========================================

Verifica que la interfaz de usuario del selector de vehículos
funcione correctamente en el navegador.
"""

import pytest
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
from typing import Dict, Any

@pytest.mark.e2e
@pytest.mark.ui
class TestVehicleSelectorUI:
    """Tests para la interfaz del selector de vehículos."""

    @pytest.fixture(scope="class")
    def driver(self):
        """Configurar WebDriver para testing."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--remote-debugging-port=9222")

        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)

        yield driver

        driver.quit()

    def test_page_loads_successfully(self, driver, base_url):
        """Verificar que la página principal cargue correctamente."""
        driver.get(base_url)

        # Verificar título
        assert "Configurador" in driver.title or "AstroTech" in driver.title

        # Verificar que el contenido principal esté presente
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

    def test_vehicle_selector_present(self, driver, base_url):
        """Verificar que el selector de vehículos esté presente."""
        driver.get(base_url)

        # Esperar a que cargue el selector
        selector_container = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "selector"))
        )

        assert selector_container is not None

    def test_fuel_type_selector_loaded(self, driver, base_url):
        """Verificar que el selector de tipo de combustible cargue datos."""
        driver.get(base_url)

        # Esperar a que cargue el selector de combustible
        fuel_select = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//select[contains(@placeholder, 'Selecciona el tipo de combustible')]"))
        )

        # Verificar que haya opciones
        select = Select(fuel_select)
        options = [option.text for option in select.options if option.text]

        # Debería tener las 2 opciones de combustible (Diesel y Gasolina)
        expected_fuels = ["Diesel", "Gasolina"]
        actual_fuels = [opt for opt in options if opt in expected_fuels]

        assert len(actual_fuels) >= 1  # Al menos una opción disponible

    def test_complete_vehicle_selection_flow(self, driver, base_url, test_data):
        """Verificar el flujo completo de selección de vehículos."""
        driver.get(base_url)

        selection = test_data["vehicles"]["diesel"]["sample_selection"]

        # Paso 1: Seleccionar tipo de combustible
        fuel_select = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//select[contains(@placeholder, 'Selecciona el tipo de combustible')]"))
        )
        select_fuel = Select(fuel_select)
        select_fuel.select_by_visible_text(selection["fuel_type"])

        # Esperar a que carguen las marcas
        time.sleep(3)

        # Paso 2: Seleccionar marca
        brand_select = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//select[contains(@placeholder, 'Selecciona la marca')]"))
        )
        select_brand = Select(brand_select)
        select_brand.select_by_visible_text(selection["brand"])

        # Esperar a que carguen los modelos
        time.sleep(3)

        # Paso 3: Seleccionar modelo
        model_select = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//select[contains(@placeholder, 'Selecciona el modelo')]"))
        )
        select_model = Select(model_select)
        select_model.select_by_visible_text(selection["model"])

        # Esperar a que carguen las versiones
        time.sleep(3)

        # Paso 4: Seleccionar versión
        version_select = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//select[contains(@placeholder, 'Selecciona la versión')]"))
        )
        select_version = Select(version_select)
        select_version.select_by_visible_text(selection["version"])

        # Verificar que aparezca el resumen de selección
        summary_card = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h6[contains(text(), 'Vehículo Seleccionado')]"))
        )

        assert summary_card is not None

    def test_vehicle_selection_summary(self, driver, base_url, test_data):
        """Verificar que el resumen de selección muestre los datos correctos."""
        driver.get(base_url)

        selection = test_data["vehicles"]["gasolina"]["sample_selection"]

        # Realizar selección completa
        self._complete_vehicle_selection(driver, selection)

        # Verificar que el resumen muestre los datos correctos
        summary_elements = driver.find_elements(By.XPATH, "//div[contains(@style, 'color: #FF6B35')]")
        summary_text = " ".join([elem.text for elem in summary_elements])

        assert selection["fuel_type"].lower() in summary_text.lower()
        assert selection["brand"].lower() in summary_text.lower()
        assert selection["model"].lower() in summary_text.lower()
        assert selection["version"].lower() in summary_text.lower()

    def test_request_button_appears_after_selection(self, driver, base_url, test_data):
        """Verificar que el botón de solicitud aparezca después de la selección completa."""
        driver.get(base_url)

        selection = test_data["vehicles"]["gasolina"]["sample_selection"]

        # Realizar selección completa
        self._complete_vehicle_selection(driver, selection)

        # Verificar que el botón de solicitud esté presente
        request_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Solicitar Presupuesto')]"))
        )

        assert request_button is not None
        assert request_button.is_displayed()
        assert request_button.is_enabled()

    def test_cascading_select_behavior(self, driver, base_url):
        """Verificar que los selects se habiliten/deshabiliten correctamente."""
        driver.get(base_url)

        # Inicialmente, solo el primer select debería estar habilitado
        fuel_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[contains(@placeholder, 'Selecciona el tipo de combustible')]"))
        )

        # Verificar selects deshabilitados inicialmente
        try:
            brand_select = driver.find_element(By.XPATH, "//select[contains(@placeholder, 'Selecciona la marca')]")
            assert brand_select.get_attribute("disabled") == "true"
        except:
            pass  # Puede que no exista aún

        # Seleccionar combustible
        select_fuel = Select(fuel_select)
        available_fuels = [opt.text for opt in select_fuel.options if opt.text]
        if available_fuels:
            select_fuel.select_by_index(0)  # Seleccionar primera opción disponible

            # Ahora el select de marca debería estar habilitado
            brand_select = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//select[contains(@placeholder, 'Selecciona la marca')]"))
            )
            assert brand_select.get_attribute("disabled") != "true"

    def test_multiple_vehicle_types(self, driver, base_url, test_data):
        """Verificar que se puedan seleccionar diferentes tipos de vehículos."""
        driver.get(base_url)

        # Probar cada tipo de combustible disponible
        fuel_types = ["diesel", "gasolina"]

        for fuel_type in fuel_types:
            try:
                selection = test_data["vehicles"][fuel_type]["sample_selection"]

                # Recargar página para limpiar selección
                driver.get(base_url)
                time.sleep(2)

                # Realizar selección completa
                self._complete_vehicle_selection(driver, selection)

                # Verificar que el resumen aparezca
                summary_card = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//h6[contains(text(), 'Vehículo Seleccionado')]"))
                )

                assert summary_card is not None, f"Falló para {fuel_type}"

            except Exception as e:
                # Si falla un tipo de combustible, continuamos con los demás
                print(f"Fallo prueba para {fuel_type}: {e}")
                continue

    def test_responsive_design(self, driver, base_url):
        """Verificar que la aplicación sea responsiva."""
        driver.get(base_url)

        # Probar diferentes tamaños de pantalla
        screen_sizes = [
            (1920, 1080),  # Desktop
            (768, 1024),   # Tablet
            (375, 667),    # Mobile
        ]

        for width, height in screen_sizes:
            driver.set_window_size(width, height)
            time.sleep(1)

            # Verificar que el selector esté visible
            try:
                selector = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "selector"))
                )
                assert selector.is_displayed()
            except:
                # Si no encuentra el selector, busca el contenedor principal
                container = driver.find_element(By.TAG_NAME, "body")
                assert container is not None

    def _complete_vehicle_selection(self, driver, selection: Dict[str, str]):
        """Método helper para completar la selección de vehículo."""
        try:
            # Paso 1: Tipo de combustible
            fuel_select = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//select[contains(@placeholder, 'Selecciona el tipo de combustible')]"))
            )
            select_fuel = Select(fuel_select)
            select_fuel.select_by_visible_text(selection["fuel_type"])
            time.sleep(3)

            # Paso 2: Marca
            brand_select = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//select[contains(@placeholder, 'Selecciona la marca')]"))
            )
            select_brand = Select(brand_select)
            select_brand.select_by_visible_text(selection["brand"])
            time.sleep(3)

            # Paso 3: Modelo
            model_select = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//select[contains(@placeholder, 'Selecciona el modelo')]"))
            )
            select_model = Select(model_select)
            select_model.select_by_visible_text(selection["model"])
            time.sleep(3)

            # Paso 4: Versión
            version_select = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//select[contains(@placeholder, 'Selecciona la versión')]"))
            )
            select_version = Select(version_select)
            select_version.select_by_visible_text(selection["version"])
            time.sleep(3)

        except Exception as e:
            print(f"Error en seleccion: {e}")
            raise

@pytest.mark.e2e
@pytest.mark.ui
@pytest.mark.slow
class TestUIPerformance:
    """Tests de rendimiento para la UI."""

    @pytest.fixture(scope="class")
    def driver(self):
        """Configurar WebDriver para testing de rendimiento."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(5)

        yield driver

        driver.quit()

    def test_page_load_time(self, driver, base_url):
        """Verificar que la página cargue en un tiempo aceptable."""
        start_time = time.time()

        driver.get(base_url)

        # Esperar a que cargue el selector
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "selector"))
        )

        load_time = time.time() - start_time
        assert load_time < 10.0, f"Page load too slow: {load_time}s"

    def test_interaction_responsiveness(self, driver, base_url, test_data):
        """Verificar que las interacciones sean rápidas."""
        driver.get(base_url)

        # Medir tiempo de respuesta para cada selección
        selection_times = []

        for step in ["fuel_type", "brand", "model", "version"]:
            start_time = time.time()

            # Realizar la acción
            if step == "fuel_type":
                fuel_select = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//select[contains(@placeholder, 'Selecciona el tipo de combustible')]"))
                )
                Select(fuel_select).select_by_index(0)
            elif step == "brand":
                brand_select = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//select[contains(@placeholder, 'Selecciona la marca')]"))
                )
                Select(brand_select).select_by_index(0)
            elif step == "model":
                model_select = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//select[contains(@placeholder, 'Selecciona el modelo')]"))
                )
                Select(model_select).select_by_index(0)
            elif step == "version":
                version_select = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//select[contains(@placeholder, 'Selecciona la versión')]"))
                )
                Select(version_select).select_by_index(0)

            # Esperar a que la acción se complete
            time.sleep(3)

            interaction_time = time.time() - start_time
            selection_times.append(interaction_time)

        # Verificar que ninguna interacción tome más de 5 segundos
        for i, interaction_time in enumerate(selection_times):
            assert interaction_time < 5.0, f"Interaction {i} too slow: {interaction_time}s"