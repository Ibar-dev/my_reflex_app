"""
Componente Hero - Sección principal con título, texto, CTA e imagen
===================================================================

Se inspira en la maqueta HTML/CSS y utiliza componentes y estilos de Reflex
para un look moderno, limpio y responsivo con efecto parallax.
"""

import reflex as rx

def hero() -> rx.Component:
    """Hero section with modern design and parallax effect."""
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
            background_image="url('/images/bigstock-Technician-Is-Tuning-Engine-Ca-469398073.jpg')",
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
            rx.flex(
                # Left column: Text content with animations
                rx.vstack(
                    # Título con gradiente
                    rx.box(
                        rx.hstack(
                            # Título principal - Primera línea con gradiente
                            rx.text(
                                "Potencia el coche ",
                                as_="span",
                                font_size={"base": "4rem", "md": "7.5rem"},  
                                font_weight="700",
                                line_height="1.2",
                                background="linear-gradient(45deg, #FF6B35, #FF8C42)",
                                background_clip="text",
                                color="transparent",
                                class_name="fade-in-left hero-title",
                                letter_spacing="-1px",
                            ),
                            # Título principal - Segunda línea en blanco
                            rx.text(
                                "de tus sueños",
                                as_="span",
                                font_size={"base": "4rem", "md": "7.5rem"},  
                                font_weight="700",
                                line_height="1.2",
                                color="white",
                                class_name="fade-in-left hero-title",
                                animation_delay="0.2s",
                                letter_spacing="-1px",
                            ),
                            spacing="0",
                            align_items="flex-start",
                            flex_wrap="wrap",
                        ),
                        mb="4",
                    ),
                    # Descripción con sombra suave - Texto aumentado
                    rx.text(
                        "Reprogramación ECU profesional para maximizar el rendimiento "
                        "de tu vehículo sin comprometer su fiabilidad.",
                        color="rgba(255, 255, 255, 0.9)",
                        font_size={"base": "1.4rem", "md": "1.7rem"},  
                        mb="8",
                        max_width="500px",
                        line_height="1.6",
                        text_shadow="0 2px 4px rgba(0,0,0,0.3)",
                        class_name="fade-in-left hero-text",
                        animation_delay="0.4s",
                        text_align={"base": "center", "md": "left"},
                    ),
                    # Testimonial or trust indicators
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "✓ Técnicos certificados  ✓ Equipos de última generación  ✓ Resultados garantizados",
                                color="rgba(255, 255, 255, 0.95)",
                                font_size={"base": "1.1rem", "md": "1.3rem"},
                                font_weight="500",
                                text_align="center",
                                text_shadow="0 2px 4px rgba(0,0,0,0.3)",
                            ),
                            spacing="2",
                            align="center",
                            width="100%",
                        ),
                        mb="8",
                        border_radius="28px",
                        overflow="hidden",
                        p={"base": "4", "md": "6"},
                        style={
                            "background": "rgba(255, 255, 255, 0.05)",
                            "backdropFilter": "blur(10px)",
                            "border": "1px solid rgba(255, 255, 255, 0.1)",
                            "boxShadow": "0 8px 32px 0 rgba(0, 0, 0, 0.2)",
                            "WebkitBackdropFilter": "blur(10px)",
                            "MozBackdropFilter": "blur(10px)",
                        },
                        class_name="fade-in-left",
                        animation_delay="0.6s",
                        max_width="1000px",
                        mx="auto",
                    ),
                    # CTA button with animation
                    rx.button(
                        "SELECCIONA TU VEHÍCULO",
                        size="3",
                        px="8",
                        py="6",
                        bg="linear-gradient(45deg, #FF6B35, #FF8C42)",
                        color="white",
                        font_weight="600",
                        border_radius="full",
                        _hover={
                            "bg": "linear-gradient(45deg, #FF5A1F, #FF7B30)",
                            "transform": "translateY(-3px) scale(1.05)",
                            "box_shadow": "0 15px 30px rgba(255, 107, 53, 0.5)"
                        },
                        box_shadow="0 8px 20px rgba(255, 107, 53, 0.3)",
                        transition="all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275)",
                        on_click=rx.redirect("/#selector"),
                        class_name="fade-in-left",
                        animation_delay="0.8s",
                    ),
                    spacing="6",
                    align="start",
                    justify="center",
                    height="100%",
                    padding_y="0.5rem",
                    width="100%",  # Ajustado para que ocupe todo el ancho disponible
                ),
                
                # Se eliminó la columna de la imagen
                
                direction={"base": "column", "md": "row"},
                spacing="8",
                width="100%",
                height="100%",
                align_items="center",
                justify_content="center",
                position="relative",
                z_index="2",
            ),
            max_width="1000px",
            pt={"base": "16", "md": "20"},
            pb={"base": "16", "md": "20"},
            px={"base": "4", "md": "6"},
            position="relative",
            z_index="2",
            mx="auto"
        ),
        # Additional animated dots pattern for visual interest
        rx.box(
            position="absolute",
            top="0",
            right="0",
            bottom="0",
            left="0",
            background="radial-gradient(circle, rgba(255, 255, 255, 0.03) 1px, transparent 1px)",
            background_size="20px 20px",
            z_index="1",
            opacity="0.4"
        ),
        width="100%",
        min_height="85vh",
        position="relative",
        overflow="hidden",
        class_name="hero-section",
        id="inicio",
    )
