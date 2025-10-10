"""
Componente Popup de Descuento - Modal promocional
=================================================

Popup modal que ofrece 10% de descuento para nuevos registros.
"""

import reflex as rx


class PopupState(rx.State):
    """Estado para controlar la visibilidad del popup y el formulario de registro"""
    show_popup: bool = True
    show_form: bool = False  # Controla si se muestra el formulario de registro
    
    # Campos del formulario
    nombre: str = ""
    email: str = ""
    telefono: str = ""
    
    def reset_popup(self):
        """Reinicia el popup cuando se recarga la página (F5)"""
        self.show_popup = True
        self.show_form = False
        self.nombre = ""
        self.email = ""
        self.telefono = ""
    
    def close_popup(self):
        """Cierra el popup completamente"""
        self.show_popup = False
        self.show_form = False
    
    def open_register(self):
        """Muestra el formulario de registro dentro del popup"""
        self.show_form = True
    
    def back_to_offer(self):
        """Vuelve a la vista de oferta desde el formulario"""
        self.show_form = False
    
    def submit_registration(self):
        """Envía los datos del formulario al backend (tu compañero lo implementa)"""
        # TODO: Tu compañero debe implementar la llamada al backend aquí
        # Ejemplo: enviar self.nombre, self.email, self.telefono al servidor
        print(f"Registro: {self.nombre}, {self.email}, {self.telefono}")
        
        # Después de enviar, cerrar el popup
        self.show_popup = False
        self.show_form = False
        
        # Limpiar campos
        self.nombre = ""
        self.email = ""
        self.telefono = ""


def offer_content() -> rx.Component:
    """Contenido de la oferta inicial del popup"""
    return rx.vstack(
        # Icono de regalo/promoción (más pequeño)
        rx.box(
            rx.icon(
                "gift",
                size=35,
                color="#FF6B35",
            ),
            bg="linear-gradient(145deg, rgba(255, 107, 53, 0.2), rgba(255, 107, 53, 0.1))",
            p="3",
            border_radius="full",
            mb="2",
        ),
        
        # Título principal (más pequeño)
        rx.heading(
            "¡OFERTA ESPECIAL!",
            size="5",
            color="white",
            text_align="center",
            font_weight="700",
            mb="1",
        ),
        
        # Texto del descuento (más pequeño)
        rx.heading(
            "10% DESCUENTO",
            size="4",
            bg_image="linear-gradient(45deg, #FF6B35, #FF8C42)",
            bg_clip="text",
            text_fill_color="transparent",
            text_align="center",
            font_weight="700",
            mb="2",
        ),
        
        # Descripción (más corta)
        rx.text(
            "Regístrate y obtén 10% OFF en tu primera reprogramación",
            color="rgba(255, 255, 255, 0.85)",
            text_align="center",
            font_size="0.85rem",
            line_height="1.4",
            mb="3",
        ),
        
        # Botón de registro (más compacto)
        rx.button(
            rx.hstack(
                rx.icon("user-plus", size=16),
                rx.text("REGISTRARME", font_weight="700", font_size="0.85rem"),
                spacing="2",
                align="center",
            ),
            on_click=PopupState.open_register,
            bg="linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%)",
            color="white",
            padding="0.75rem 1.5rem",
            border_radius="25px",
            cursor="pointer",
            border="none",
            box_shadow="0 5px 15px rgba(255, 107, 53, 0.4)",
            _hover={
                "transform": "translateY(-2px)",
                "box_shadow": "0 8px 20px rgba(255, 107, 53, 0.6)",
            },
            transition="all 0.3s ease",
            width="100%",
        ),
        
        # Texto pequeño
        rx.text(
            "* Solo nuevos clientes",
            color="rgba(255, 255, 255, 0.5)",
            font_size="0.7rem",
            text_align="center",
            mt="2",
        ),
        
        spacing="2",
        align="center",
        justify="center",
    )


def form_content() -> rx.Component:
    """Formulario de registro para el popup"""
    return rx.vstack(
        # Título del formulario
        rx.heading(
            "Registro",
            size="5",
            color="white",
            text_align="center",
            font_weight="700",
            mb="2",
        ),
        
        # Campo: Nombre
        rx.vstack(
            rx.text("Nombre completo", color="white", font_size="0.85rem", font_weight="600"),
            rx.input(
                placeholder="Ej: Juan Pérez",
                value=PopupState.nombre,
                on_change=PopupState.set_nombre,
                bg="#1f1f1f",
                border="1px solid #555",
                color="white",
                padding="0.65rem 0.75rem",
                border_radius="10px",
                width="100%",
                height="42px",
                font_size="0.95rem",
                line_height="1.5",
                _placeholder={"color": "#888"},
                _focus={
                    "border_color": "#FF6B35",
                    "box_shadow": "0 0 0 1px #FF6B35",
                    "bg": "#2a2a2a",
                },
            ),
            spacing="1",
            width="100%",
            align="start",
        ),
        
        # Campo: Email
        rx.vstack(
            rx.text("Email", color="white", font_size="0.85rem", font_weight="600"),
            rx.input(
                placeholder="tu@email.com",
                type="email",
                value=PopupState.email,
                on_change=PopupState.set_email,
                bg="#1f1f1f",
                border="1px solid #555",
                color="white",
                padding="0.65rem 0.75rem",
                border_radius="10px",
                width="100%",
                height="42px",
                font_size="0.95rem",
                line_height="1.5",
                _placeholder={"color": "#888"},
                _focus={
                    "border_color": "#FF6B35",
                    "box_shadow": "0 0 0 1px #FF6B35",
                    "bg": "#2a2a2a",
                },
            ),
            spacing="1",
            width="100%",
            align="start",
        ),
        
        # Campo: Teléfono
        rx.vstack(
            rx.text("Teléfono", color="white", font_size="0.85rem", font_weight="600"),
            rx.input(
                placeholder="+34 600 123 456",
                type="tel",
                value=PopupState.telefono,
                on_change=PopupState.set_telefono,
                bg="#1f1f1f",
                border="1px solid #555",
                color="white",
                padding="0.65rem 0.75rem",
                border_radius="10px",
                width="100%",
                height="42px",
                font_size="0.95rem",
                line_height="1.5",
                _placeholder={"color": "#888"},
                _focus={
                    "border_color": "#FF6B35",
                    "box_shadow": "0 0 0 1px #FF6B35",
                    "bg": "#2a2a2a",
                },
            ),
            spacing="1",
            width="100%",
            align="start",
        ),
        
        # Botones: Volver y Enviar
        rx.hstack(
            # Botón Volver
            rx.button(
                rx.hstack(
                    rx.icon("arrow-left", size=14),
                    rx.text("Volver", font_size="0.8rem"),
                    spacing="1",
                ),
                on_click=PopupState.back_to_offer,
                bg="#3a3a3a",
                color="white",
                padding="0.65rem 1rem",
                border_radius="20px",
                cursor="pointer",
                border="none",
                _hover={"bg": "#4a4a4a"},
                transition="all 0.3s ease",
                flex="1",
            ),
            
            # Botón Enviar
            rx.button(
                rx.hstack(
                    rx.icon("send", size=14),
                    rx.text("Enviar", font_size="0.8rem", font_weight="700"),
                    spacing="1",
                ),
                on_click=PopupState.submit_registration,
                bg="linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%)",
                color="white",
                padding="0.65rem 1rem",
                border_radius="20px",
                cursor="pointer",
                border="none",
                box_shadow="0 4px 12px rgba(255, 107, 53, 0.4)",
                _hover={
                    "transform": "translateY(-2px)",
                    "box_shadow": "0 6px 16px rgba(255, 107, 53, 0.6)",
                },
                transition="all 0.3s ease",
                flex="1",
            ),
            
            spacing="2",
            width="100%",
        ),
        
        spacing="2",
        align="center",
        width="100%",
    )


def discount_popup() -> rx.Component:
    """Popup compacto con oferta de 10% de descuento - Esquina inferior derecha"""
    return rx.cond(
        PopupState.show_popup,
        rx.box(
            # Botón de cerrar (X)
            rx.box(
                rx.icon(
                    "x",
                    size=18,
                    color="white",
                    cursor="pointer",
                    _hover={"color": "#FF6B35"},
                ),
                position="absolute",
                top="0.75rem",
                right="0.75rem",
                on_click=PopupState.close_popup,
                cursor="pointer",
                z_index="10001",
            ),
            
            # Contenido dinámico: Oferta o Formulario
            rx.cond(
                PopupState.show_form,
                form_content(),  # Muestra formulario si show_form es True
                offer_content(),  # Muestra oferta si show_form es False
            ),
            
            # Estilos del modal - ABAJO DERECHA
            position="fixed",
            bottom="30px",
            right="20px",
            bg="linear-gradient(145deg, #1e1e1e, #2a2a2a)",
            border="2px solid #FF6B35",
            border_radius="20px",
            padding="1.25rem 1.15rem",
            box_shadow="0 15px 40px rgba(0, 0, 0, 0.6), 0 0 40px rgba(255, 107, 53, 0.3)",
            z_index="10000",
            width="320px",
            max_width="calc(100vw - 40px)",
            max_height="calc(100vh - 60px)",
            overflow_y="auto",
            
            # Animación de entrada desde abajo derecha
            animation="popupSlideInBottomRight 0.5s ease-out",
        )
    )
