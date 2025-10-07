"""
Página de inicio - Hero section y selector de vehículos
======================================================
"""

import reflex as rx
from components.vehicle_selector import vehicle_selector


def home_page() -> rx.Component:
    """Página principal con selector de vehículos"""
    return vehicle_selector()