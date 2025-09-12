"""
Componente FAQ - Preguntas frecuentes con acordeón animado
========================================================

Acordeón interactivo con animaciones suaves y rotación de iconos.
"""

import reflex as rx

class FAQState(rx.State):
    """Estado para manejar las FAQ expandidas"""
    expanded_items: list[int] = []
    
    def toggle_faq(self, item_id: int):
        if item_id in self.expanded_items:
            self.expanded_items.remove(item_id)
        else:
            self.expanded_items.append(item_id)

def faq_item(question: str, answer: str, item_id: int) -> rx.Component:
    """Item individual de FAQ"""
    is_expanded = FAQState.expanded_items.contains(item_id)
    
    return rx.box(
        # Pregunta clickeable
        rx.button(
            rx.hstack(
                rx.heading(
                    question,
                    size="4",
                    color="white",
                    text_align="left"
                ),
                rx.text(
                    "+",
                    font_size="1.5rem",
                    font_weight="bold",
                    color="#FF6B35",
                    transform=rx.cond(is_expanded, "rotate(45deg)", "rotate(0deg)"),
                    transition="transform 0.3s ease"
                ),
                justify="between",
                align="center",
                width="100%"
            ),
            bg="transparent",
            border="none",
            p="6",
            width="100%",
            text_align="left",
            _hover={"bg": "#2D2D2D"},
            transition="all 0.3s ease",
            on_click=FAQState.toggle_faq(item_id)
        ),
        
        # Respuesta expandible
        rx.box(
            rx.text(
                answer,
                color="#666666",
                line_height="1.6",
                p="6",
                pt="0"
            ),
            max_height=rx.cond(is_expanded, "200px", "0px"),
            overflow="hidden",
            transition="max-height 0.3s ease"
        ),
        
        bg="#1A1A1A",
        border_radius="10px",
        mb="4",
        border="1px solid #666666",
        box_shadow="0 4px 6px rgba(0, 0, 0, 0.1)",
        overflow="hidden"
    )

def faq() -> rx.Component:
    """Sección de preguntas frecuentes"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading(
                    "Preguntas Frecuentes",
                    size="8",
                    color="white",
                    text_align="center",
                    mb="12"
                ),
                rx.vstack(
                    faq_item(
                        "¿Es seguro reprogramar mi vehículo?",
                        "Sí, es completamente seguro. Utilizamos equipos profesionales y seguimos protocolos estrictos. Además, guardamos una copia de seguridad de la configuración original.",
                        1
                    ),
                    faq_item(
                        "¿Cuánto tiempo tarda el proceso?",
                        "El proceso completo suele durar entre 2-4 horas, dependiendo del modelo del vehículo. Incluye diagnóstico, backup, reprogramación y pruebas.",
                        2
                    ),
                    faq_item(
                        "¿Afecta la garantía del fabricante?",
                        "La reprogramación puede afectar la garantía del fabricante. Sin embargo, ofrecemos nuestra propia garantía y el proceso es completamente reversible.",
                        3
                    ),
                    faq_item(
                        "¿Qué vehículos pueden ser reprogramados?",
                        "Trabajamos con la mayoría de marcas europeas y asiáticas desde el año 2000. Consulta nuestro selector de vehículos para verificar compatibilidad.",
                        4
                    ),
                    spacing="0",
                    width="100%",
                    max_width="800px"
                ),
                spacing="8",
                align="center"
            ),
            max_width="1200px",
            px="6",
            py="20"
        ),
        bg="#2D2D2D"
    )
