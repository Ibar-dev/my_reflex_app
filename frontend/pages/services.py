"""
Página de servicios - Información detallada sobre los servicios de reprogramación ECU
===================================================================================

Esta página proporciona información detallada sobre todos los servicios
que ofrece AstroTech, incluyendo procesos, garantías y tecnología utilizada.

ESTRUCTURA:
- Hero section con título de servicios
- Servicios principales con descripciones detalladas
- Proceso de trabajo paso a paso
- Sección de garantías y soporte

SERVICIOS PRINCIPALES:
- Reprogramación ECU completa
- Diagnóstico avanzado del sistema
- Backup de configuración original
- Soporte técnico especializado

PROCESO DE TRABAJO:
1. Diagnóstico del sistema
2. Backup de configuración original
3. Reprogramación optimizada
4. Pruebas y verificación

GARANTÍAS:
- Garantía completa en servicios
- Reversibilidad del proceso
- Soporte técnico 24/7

DEPENDENCIAS:
- rx.grid para layout de servicios
- rx.container para contenedores
- rx.heading, rx.text para contenido
"""

import reflex as rx

def ecu_explanation() -> rx.Component:
    """Sección de explicación de la centralita ECU con imagen de fondo."""
    return rx.box(
        # Parallax background with overlay
        rx.box(
            # Dark overlay with gradient
            rx.box(
                position="absolute",
                top="0",
                left="0",
                right="0",
                bottom="0",
                bg="linear-gradient(135deg, rgba(18, 18, 18, 0.92) 0%, rgba(30, 30, 30, 0.85) 100%)",
                z_index="1",
            ),
            # Animated glow effect
            rx.box(
                position="absolute",
                top="20%",
                right="-20%",
                width="50%",
                height="50%",
                border_radius="full",
                bg="radial-gradient(circle, rgba(255,107,53,0.15) 0%, rgba(255,107,53,0) 70%)",
                z_index="1",
                animation="pulse 8s infinite ease-in-out",
            ),
            rx.box(
                position="absolute",
                bottom="-10%",
                left="-5%",
                width="40%",
                height="40%",
                border_radius="full",
                bg="radial-gradient(circle, rgba(255,140,66,0.1) 0%, rgba(255,140,66,0) 60%)",
                z_index="1",
                animation="pulse 10s infinite ease-in-out",
                animation_delay="2s",
            ),
            # Background image
            position="absolute",
            top="0",
            left="0",
            right="0",
            bottom="0",
            background_image="url('/images/centralita-coche.jpg')",
            background_size="cover",
            background_position="center",
            background_repeat="no-repeat",
            background_attachment="fixed",
            filter="blur(1px)",
            z_index="0",
            class_name="parallax-bg",
        ),
        
        # Main content container
        rx.container(
            rx.vstack(
                rx.heading(
                    "¿Qué es la reprogramación ECU?",
                    size="4xl",
                    mb=6,
                    color="white",
                    class_name="fade-in-left",
                    text_align="left",
                    width="100%",
                    max_width="800px",
                    position="relative",
                    z_index="2",
                ),
                rx.text(
                    "La Unidad de Control del Motor (ECU) es el cerebro de tu vehículo. "
                    "La reprogramación ECU permite optimizar el rendimiento del motor "
                    "ajustando parámetros como la inyección de combustible, encendido y presión del turbo.",
                    color="rgba(255, 255, 255, 0.9)",
                    mb=8,
                    class_name="fade-in-left",
                    animation_delay="0.2s",
                    text_align="left",
                    width="100%",
                    max_width="800px",
                    position="relative",
                    z_index="2",
                    line_height="1.8",
                    fontSize="1.1rem",
                ),
                rx.unordered_list(
                    rx.list_item("Mayor potencia y par motor"),
                    rx.list_item("Mejor respuesta del acelerador"),
                    rx.list_item("Reducción del consumo de combustible"),
                    rx.list_item("Eliminación de limitadores electrónicos"),
                    spacing=4,
                    color="rgba(255, 255, 255, 0.9)",
                    mb=8,
                    class_name="fade-in-left",
                    animation_delay="0.3s",
                    padding_left=6,
                    fontSize="1.1rem",
                    position="relative",
                    z_index="2",
                    width="100%",
                    max_width="800px",
                ),
                align_items="start",
                py=24,
                position="relative",
                z_index="2",
            ),
            max_width="1200px",
            position="relative",
            z_index="2",
            padding_top="80px",
            padding_bottom="80px",
            min_height="100vh",
            display="flex",
            alignItems="center",
        ),
        position="relative",
        overflow="hidden",
        min_height="100vh",
        id="que-es-ecu"
    )

def services_page() -> rx.Component:
    """
    Página de servicios detallada
    
    Returns:
        rx.Component: Página completa de servicios
    """
    return rx.box(
        ecu_explanation(),
        # Otras secciones irán aquí
        min_height="100vh",
        bg="black",
    )

# TODO: Implementar funciones auxiliares de la página de servicios
# - main_services_section(): Servicios principales
# - process_section(): Proceso de trabajo
# - warranty_section(): Garantías y soporte