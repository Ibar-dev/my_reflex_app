"""
Componente Header - Barra de navegación principal
===============================================

Este componente contiene la barra de navegación superior de la aplicación.
Incluye el logo, menú de navegación, botón CTA y menú hamburguesa para móviles.

FUNCIONALIDADES:
- Logo de AstroTech
- Navegación entre páginas (Inicio, Servicios, Acerca de, Contacto)
- Botón "Selecciona tu vehículo" que lleva al selector
- Menú hamburguesa responsivo para dispositivos móviles
- Navegación fija en la parte superior

ESTADO:
- Utiliza el estado global para manejar la navegación
- Cambia de apariencia al hacer scroll

DEPENDENCIAS:
- state.global_state para navegación
- rx.link para enlaces internos
- rx.button para botones interactivos
"""

import reflex as rx

# TODO: Importar estado global cuando esté implementado
# from state.global_state import GlobalState

def header() -> rx.Component:
    """
    Header con navegación principal
    
    Returns:
        rx.Component: Componente de header con navegación
    """
    # TODO: Implementar header completo
    pass

# TODO: Implementar funciones auxiliares del header
# - Logo de la empresa
# - Menú de navegación
# - Botón CTA
# - Menú hamburguesa para móviles
# - Efectos de scroll