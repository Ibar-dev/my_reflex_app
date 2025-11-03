"""
Configuración pytest para tests E2E
=================================
"""

import pytest
import asyncio
import aiohttp
import requests
from pathlib import Path
from typing import Dict, Any
import time

# URLs base para testing
BASE_URL = "http://localhost:3001"
API_URL = "http://localhost:8001"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def base_url():
    """URL base para frontend testing."""
    return BASE_URL

@pytest.fixture(scope="session")
def api_url():
    """URL base para API testing."""
    return API_URL

@pytest.fixture(scope="session")
async def test_client():
    """Cliente HTTP asíncrono para testing."""
    async with aiohttp.ClientSession() as session:
        yield session

@pytest.fixture(scope="session")
def sync_test_client():
    """Cliente HTTP síncrono para testing."""
    return requests.Session()

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Configurar entorno de testing."""
    # Crear directorios necesarios
    test_dirs = ["test-results", "test-results/screenshots", "test-results/logs"]
    for dir_path in test_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

    print("\n🚀 Iniciando entorno de testing...")

    # Esperar que la aplicación esté lista
    max_wait = 60  # 60 segundos máximo
    wait_interval = 2

    for i in range(0, max_wait, wait_interval):
        try:
            response = requests.get(f"{BASE_URL}", timeout=5)
            if response.status_code == 200:
                print(f"✅ Aplicación lista después de {i} segundos")
                break
        except requests.exceptions.RequestException:
            if i % 10 == 0:
                print(f"⏳ Esperando aplicación... {i}/{max_wait}s")
            time.sleep(wait_interval)
    else:
        pytest.fail("❌ La aplicación no estuvo lista después de 60 segundos")

    yield

    print("🧹 Limpiando entorno de testing...")

@pytest.fixture(scope="session")
def test_data():
    """Datos de prueba para los tests."""
    return {
        "vehicles": {
            "diesel": {
                "brands": ["Audi", "BMW", "Mercedes-Benz", "Volkswagen", "Seat", "Skoda", "Renault"],
                "sample_selection": {
                    "fuel_type": "diesel",
                    "brand": "Audi",
                    "model": "A3",
                    "version": "1.6 TDI 115 CV"
                }
            },
            "gasolina": {
                "brands": ["Audi", "BMW", "Mercedes-Benz", "Volkswagen"],
                "sample_selection": {
                    "fuel_type": "gasolina",
                    "brand": "Audi",
                    "model": "A3",
                    "version": "1.0 TFSI 110 CV"
                }
            },
            "hibrido": {
                "brands": ["Toyota", "Hyundai"],
                "sample_selection": {
                    "fuel_type": "hibrido",
                    "brand": "Toyota",
                    "model": "Prius",
                    "version": "1.8 Hybrid 122 CV"
                }
            },
            "electrico": {
                "brands": ["Tesla", "Nissan", "Renault", "Hyundai"],
                "sample_selection": {
                    "fuel_type": "electrico",
                    "brand": "Tesla",
                    "model": "Model 3",
                    "version": "Standard Range Plus"
                }
            }
        },
        "url_paths": {
            "home": "/",
            "selector": "/",
            "api_health": "/ping",
            "api_vehicles": "/api/vehicles"
        }
    }

def pytest_configure(config):
    """Configuración adicional de pytest."""
    config.addinivalue_line(
        "markers", "e2e: mark test as end-to-end test"
    )
    config.addinivalue_line(
        "markers", "api: mark test as API test"
    )
    config.addinivalue_line(
        "markers", "ui: mark test as UI test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )

def pytest_html_report_title(report):
    """Título personalizado para el reporte HTML."""
    report.title = "AstroTech App - E2E Test Report"

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capturar screenshots para tests fallidos."""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            # Tomar screenshot del estado actual
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options

            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")

            driver = webdriver.Chrome(options=chrome_options)
            driver.get(BASE_URL)

            screenshot_path = f"test-results/screenshots/failed_{item.name}_{int(time.time())}.png"
            driver.save_screenshot(screenshot_path)
            driver.quit()

            # Adjuntar screenshot al reporte
            rep.extra_html = f'<img src="{screenshot_path}" width="800">'

        except Exception as e:
            print(f"⚠️ No se pudo capturar screenshot: {e}")