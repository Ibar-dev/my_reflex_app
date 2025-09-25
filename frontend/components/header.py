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

# Estado para navegación activa y menú móvil
class HeaderState(rx.State):
    active_section: str = "inicio"
    is_mobile_open: bool = False
    
    def toggle_mobile_menu(self):
        self.is_mobile_open = not self.is_mobile_open
    
    def set_active_section(self, section: str):
        self.active_section = section


def _nav_link(text: str, href: str, section_id: str) -> rx.Component:
    return rx.link(
        text,
        href=href,
        class_name=rx.cond(
            HeaderState.active_section == section_id,
            "nav-link active",
            "nav-link"
        ),
        on_click=[
            HeaderState.set_active_section(section_id),
            rx.call_script(f"document.getElementById('{href[1:]}').scrollIntoView({{ behavior: 'smooth' }});")
        ],
    )


def _nav_menu(display: str = "flex") -> rx.Component:
    return rx.hstack(
        _nav_link("Inicio", "#inicio", "inicio"),
        _nav_link("Servicios", "#beneficios", "servicios"),
        _nav_link("Acerca de", "#acerca", "acerca"),
        _nav_link("Contacto", "#contacto", "contacto"),
        spacing="4",
        display=display,
        align="center",
        margin_left="auto",  # Esto mueve el menú hacia la derecha
    )


def header(active: str = "inicio") -> rx.Component:
    """
    Header con navegación principal
    
    Returns:
        rx.Component: Componente de header con navegación
    """
    return rx.box(
        rx.hstack(
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
            rx.spacer(),
            _nav_menu(display={"base": "none", "md": "flex"}),
            align="center",
            width="100%",
            padding_x="1.5rem",
            height="70px",  # Aumentado para mejor proporción y visibilidad
        ),
        position="sticky",
        top="0",
        z_index="1000",
        bg="linear-gradient(180deg, #202020 0%, #1A1A1A 100%)",
        border_bottom="1px solid #262626",
        box_shadow="0 1px 0 rgba(255,255,255,0.06)",
        width="100%",
        min_height="70px",  # Altura mínima fija
        max_height="70px",  # Altura máxima fija para evitar cambios de tamaño
    )

# TODO: Implementar funciones auxiliares del header
# - Logo de la empresa
# - Menú de navegación
# - Botón CTA
# - Menú hamburguesa para móviles
# - Efectos de scroll