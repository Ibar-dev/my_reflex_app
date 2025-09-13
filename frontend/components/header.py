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

# Estado local simple para el menú móvil
class _HeaderState(rx.State):
    pass


def _nav_link(text: str, href: str, active: bool = False) -> rx.Component:
    return rx.link(
        text,
        href=href,
        class_name=f"nav-link{' active' if active else ''}",
        on_click=rx.call_script(f"document.getElementById('{href[1:]}').scrollIntoView({{ behavior: 'smooth' }});"),
    )


def _nav_menu(active_key: str, display: str = "flex") -> rx.Component:
    return rx.hstack(
        _nav_link("Inicio", "#inicio", active=active_key == "home"),
        _nav_link("Servicios", "#servicios", active=active_key == "services"),
        _nav_link("Acerca de", "#acerca", active=active_key == "about"),
        _nav_link("Contacto", "#contacto", active=active_key == "contact"),
        spacing="7",
        display=display,
        align="center",
    )


def header(active: str = "home") -> rx.Component:
    """
    Header con navegación principal
    
    Returns:
        rx.Component: Componente de header con navegación
    """
    return rx.box(
        # Barra fija superior
        rx.container(
            rx.hstack(
                # Logo / Marca
                rx.link(
                    rx.text(
                        "AstroTech",
                        color="#FF6B35",
                        font_weight="800",
                        font_size="1.4rem",
                        letter_spacing="0.6px",
                        class_name="brand",
                    ),
                    href="/#inicio",
                    _hover={"text_decoration": "none"},
                ),

                # Menú principal (desktop)
                _nav_menu(active_key=active, display={"base": "none", "md": "flex"}),
                align="center",
                justify="between",
            ),
            max_width="1140px",
            px="24px",
            height="70px",
        ),
        position="sticky",
        top="0",
        z_index="1000",
        bg="linear-gradient(180deg, #202020 0%, #1A1A1A 100%)",
        border_bottom="1px solid",
        border_color="#262626",
        box_shadow="0 1px 0 rgba(255,255,255,0.06)",
    )

# TODO: Implementar funciones auxiliares del header
# - Logo de la empresa
# - Menú de navegación
# - Botón CTA
# - Menú hamburguesa para móviles
# - Efectos de scroll