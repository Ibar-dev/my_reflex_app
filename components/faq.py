"""
Componente FAQ - Preguntas frecuentes con acordeón animado
========================================================

Acordeón interactivo con animaciones suaves y rotación de iconos.
"""

import reflex as rx

class FAQAccordionState(rx.State):
    """Estado para manejar las FAQ expandidas"""
    expanded_items: list[int] = []
    
    def toggle_faq(self, item_id: int):
        if item_id in self.expanded_items:
            self.expanded_items.remove(item_id)
        else:
            self.expanded_items.append(item_id)

def faq_item(question: str, answer: str, item_id: int) -> rx.Component:
    """Item individual de FAQ con animaciones mejoradas"""
    is_expanded = FAQAccordionState.expanded_items.contains(item_id)
    
    return rx.box(
        # Pregunta clickeable
        rx.button(
            rx.hstack(
                rx.heading(
                    question,
                    size="4",
                    color="white",
                    text_align="left",
                    font_weight="600"
                ),
                rx.icon(
                    "chevron-down",
                    size=24,
                    color="#FF6B35",
                    transform=rx.cond(is_expanded, "rotate(180deg)", "rotate(0deg)"),
                    transition="transform 0.4s cubic-bezier(0.4, 0, 0.2, 1)"
                ),
                justify="between",
                align="center",
                width="100%"
            ),
            bg="transparent",
            border="none",
            p="8",
            width="100%",
            text_align="left",
            _hover={"bg": "rgba(255, 107, 53, 0.05)"},
            transition="all 0.3s ease",
            on_click=FAQAccordionState.toggle_faq(item_id),
            cursor="pointer"
        ),
        
        # Respuesta expandible con animación mejorada
        rx.box(
            rx.box(
                rx.text(
                    answer,
                    color="#CCCCCC",
                    line_height="1.7",
                    font_size="0.95rem"
                ),
                p="8",
                pt="0",
                opacity=rx.cond(is_expanded, "1", "0"),
                transition="opacity 0.3s ease 0.1s"
            ),
            max_height=rx.cond(is_expanded, "300px", "0px"),
            overflow="hidden",
            transition="max-height 0.4s cubic-bezier(0.4, 0, 0.2, 1)"
        ),
        
        bg="#2D2D2D",
        border_radius="15px",
        mb="6",
        border="1px solid #404040",
        box_shadow="0 4px 15px rgba(0, 0, 0, 0.15)",
        _hover={
            "box_shadow": "0 8px 25px rgba(255, 107, 53, 0.1)",
            "border_color": "#FF6B35"
        },
        transition="all 0.3s ease",
        overflow="hidden"
    )

def faq() -> rx.Component:
    """Sección de preguntas frecuentes mejorada y centrada"""
    return rx.center(
        rx.container(
            rx.vstack(
                rx.heading(
                    "Preguntas Frecuentes",
                    size="8",
                    color="white",
                    text_align="center",
                    mb="16",
                    font_weight="700",
                    bg_image="linear-gradient(45deg, #FF6B35, #FF8C42)",
                    bg_clip="text",
                    text_fill_color="transparent",
                ),
                rx.center(
                    rx.vstack(
                        faq_item(
                            "¿Es seguro reprogramar mi vehículo?",
                            "Sí, es completamente seguro. Utilizamos equipos profesionales y seguimos protocolos estrictos. Además, guardamos una copia de seguridad de la configuración original para poder revertir los cambios si es necesario.",
                            1
                        ),
                        faq_item(
                            "¿Cuánto tiempo tarda el proceso?",
                            "El proceso completo suele durar entre 2-4 horas, dependiendo del modelo del vehículo y la complejidad de la reprogramación. Incluye diagnóstico previo, backup de seguridad, reprogramación y pruebas finales.",
                            2
                        ),
                        faq_item(
                            "¿Afecta la garantía del fabricante?",
                            "La reprogramación puede afectar la garantía del fabricante en ciertos aspectos relacionados con el motor. Sin embargo, ofrecemos nuestra propia garantía completa y el proceso es completamente reversible.",
                            3
                        ),
                        faq_item(
                            "¿Qué vehículos pueden ser reprogramados?",
                            "Trabajamos con la mayoría de marcas europeas y asiáticas desde el año 2000 en adelante. Utiliza nuestro selector de vehículos para verificar la compatibilidad de tu modelo específico.",
                            4
                        ),
                        faq_item(
                            "¿Qué beneficios obtendré inmediatamente?",
                            "Notarás una mejora inmediata en la respuesta del acelerador, mayor potencia en adelantamientos y una conducción más suave. Los beneficios de consumo se aprecian tras los primeros 500km.",
                            5
                        ),
                        spacing="4",
                        width="100%",
                        max_width="800px"
                    ),
                    width="100%",
                    mx="auto"
                ),
                spacing="6",
                align="center",
                width="100%",
                max_width="900px"
            ),
            max_width="1200px",
            px={"base": "6", "md": "8"},
            py={"base": "16", "md": "24"},
            mx="auto"
        ),
        width="100%",
        bg="#1A1A1A"
    )
