"""
Utilidades de logging para diagnóstico en frontend y backend
"""

import reflex as rx
import logging

# Configurar logger específico para vehículos
vehicle_logger = logging.getLogger('vehicle_selector')

def log_browser(message: str, level: str = "info"):
    """
    Genera código JavaScript para logging en la consola del navegador
    """
    colors = {
        "info": "#2196F3",
        "warning": "#FF9800",
        "error": "#F44336",
        "success": "#4CAF50"
    }

    color = colors.get(level, "#2196F3")
    emoji = {
        "info": "ℹ️",
        "warning": "⚠️",
        "error": "❌",
        "success": "✅"
    }.get(level, "ℹ️")

    return f"""
    console.log('%c[VEHICLE] {emoji} {message}', 'color: {color}; font-weight: bold; font-size: 12px;');
    """

def create_browser_log_component(message: str, level: str = "info"):
    """
    Crea un componente de Reflex que hace logging en la consola del navegador
    """
    return rx.script(
        log_browser(message, level)
    )

# Funciones de logging específicas para vehículos
def log_vehicle_loading():
    """Log cuando开始加载 vehículos"""
    return create_browser_log_component("Iniciando selector de vehículos", "info")

def log_vehicle_success(data_type: str, count: int):
    """Log cuando se cargan datos exitosamente"""
    return create_browser_log_component(f"Datos cargados: {data_type} ({count} elementos)", "success")

def log_vehicle_error(operation: str, error: str):
    """Log cuando hay un error"""
    return create_browser_log_component(f"Error en {operation}: {error}", "error")

def log_vehicle_selection(selection_type: str, value: str):
    """Log cuando el usuario selecciona algo"""
    return create_browser_log_component(f"Selección: {selection_type} = {value}", "info")