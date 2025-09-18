"""
Componente Benefits - Sección de beneficios con tarjetas animadas
===============================================================

Tarjetas con efectos hover, iconos y animaciones basadas en la maqueta.
"""

import reflex as rx

def benefits() -> rx.Component:
    """Sección de beneficios con tarjetas animadas y diseño moderno"""
    return rx.box(
        # Fondo con patrón de puntos y gradiente para efecto visual
        rx.box(
            position="absolute",
            top="0",
            left="0",
            right="0",
            bottom="0",
            bg="radial-gradient(circle at 30% 20%, rgba(255, 107, 53, 0.03) 0%, rgba(30, 30, 30, 0) 70%)",
            z_index="0",
            # Patrón de puntos
            _after={
                "content": "''",
                "position": "absolute",
                "top": "0",
                "right": "0",
                "bottom": "0",
                "left": "0",
                "background": "radial-gradient(circle, rgba(255, 255, 255, 0.03) 1px, transparent 1px)",
                "background_size": "20px 20px",
                "z_index": "1",
                "opacity": "0.5",
            },
        ),
        rx.center(
            rx.container(
                rx.vstack(
                    # Título con gradiente y animación
                    rx.heading(
                        "Más potencia, menos consumo",
                        size="8",
                        color="white",
                        text_align="center",
                        mb="4",
                        font_weight="800",
                        bg_image="linear-gradient(45deg, #FF6B35, #FF8C42)",
                        bg_clip="text",
                        text_fill_color="transparent",
                        class_name="fade-in",
                    ),
                    # Subtítulo con animación retrasada
                    rx.text(
                        "Optimiza el rendimiento de tu vehículo con nuestra tecnología de reprogramación ECU",
                        color="rgba(255, 255, 255, 0.8)",
                        text_align="center",
                        font_size="1.2rem",
                        mb="16",
                        max_width="800px",
                        class_name="fade-in",
                        animation_delay="0.2s",
                        text_shadow="0 2px 4px rgba(0,0,0,0.2)",
                    ),
                rx.center(
                    rx.grid(
                        # Tarjeta 1: Mayor Potencia - Con efecto de flotación y animación
                        rx.box(
                            rx.vstack(
                                # Ícono más compacto
                                rx.center(
                                    rx.icon("zap", size=50, color="#FF6B35"),
                                    width="100%",
                                    height="60px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                    mb="2",
                                    class_name="fade-in-up",
                                ),
                                # Título con gradiente
                                rx.heading(
                                    "Mayor Potencia",
                                    size="5",
                                    color="white",
                                    mb="3",
                                    text_align="center",
                                    bg_image="linear-gradient(45deg, #FF6B35, #FF8C42)",
                                    bg_clip="text",
                                    text_fill_color="transparent",
                                    font_weight="700",
                                    class_name="fade-in-up",
                                    animation_delay="0.1s",
                                ),
                                # Descripción con texto más legible
                                rx.text(
                                    "Aumenta la potencia de tu motor hasta un 30% manteniendo la fiabilidad del vehículo.",
                                    color="rgba(255, 255, 255, 0.9)",
                                    line_height="1.6",
                                    text_align="center",
                                    font_size="1.05rem",
                                    class_name="fade-in-up",
                                    animation_delay="0.2s",
                                ),
                                spacing="6",
                                align="center",
                                height="100%",
                            ),
                            # Diseño de la tarjeta con efecto neumorfísmico
                            bg="linear-gradient(145deg, #202020, #1a1a1a)",
                            border_radius="30px",
                            p="6",
                            py="8",
                            border="1px solid #2c2c2c",
                            min_height="240px",
                            box_shadow="0 10px 25px rgba(0, 0, 0, 0.2), inset 0 1px 1px rgba(255, 255, 255, 0.06)",
                            _hover={
                                "transform": "translateY(-15px)",
                                "box_shadow": "0 20px 40px rgba(255, 107, 53, 0.2), inset 0 1px 1px rgba(255, 255, 255, 0.06)",
                                "border_color": "#FF6B35",
                                "border_width": "1px",
                            },
                            transition="all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275)",
                            cursor="pointer",
                            class_name="benefit-card fade-in-up",
                            position="relative",
                            overflow="hidden",
                            # Efecto de brillo en esquina
                            _after={
                                "content": "''",
                                "position": "absolute",
                                "top": "-50%",
                                "left": "-50%",
                                "width": "40px",
                                "height": "200px",
                                "background": "linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0) 100%)",
                                "transform": "rotate(35deg)",
                                "filter": "blur(3px)",
                                "opacity": "0",
                                "z_index": "1",
                                "transition": "all 0.8s ease"
                            },
                            _hover_after={
                                "transform": "rotate(35deg) translateX(450px)", 
                                "opacity": "1"
                            },
                            animation_delay="0.1s",
                        ),
                        
                        # Tarjeta 2: Menor Consumo - Con efecto de flotación y animación
                        rx.box(
                            rx.vstack(
                                # Ícono más compacto
                                rx.center(
                                    rx.icon("dollar-sign", size=50, color="#FF6B35"),
                                    width="100%",
                                    height="60px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                    mb="2",
                                    class_name="fade-in-up",
                                    animation_delay="0.3s",
                                ),
                                # Título con gradiente
                                rx.heading(
                                    "Menor Consumo",
                                    size="5",
                                    color="white",
                                    mb="3",
                                    text_align="center",
                                    bg_image="linear-gradient(45deg, #FF6B35, #FF8C42)",
                                    bg_clip="text",
                                    text_fill_color="transparent",
                                    font_weight="700",
                                    class_name="fade-in-up",
                                    animation_delay="0.4s",
                                ),
                                # Descripción con texto más legible
                                rx.text(
                                    "Reduce el consumo de combustible hasta un 15% con una conducción eficiente.",
                                    color="rgba(255, 255, 255, 0.9)",
                                    line_height="1.6",
                                    text_align="center",
                                    font_size="1.05rem",
                                    class_name="fade-in-up",
                                    animation_delay="0.5s",
                                ),
                                spacing="6",
                                align="center",
                                height="100%",
                            ),
                            # Diseño de la tarjeta con efecto neumorfísmico
                            bg="linear-gradient(145deg, #202020, #1a1a1a)",
                            border_radius="30px",
                            p="6",
                            py="8",
                            border="1px solid #2c2c2c",
                            min_height="240px",
                            box_shadow="0 10px 25px rgba(0, 0, 0, 0.2), inset 0 1px 1px rgba(255, 255, 255, 0.06)",
                            _hover={
                                "transform": "translateY(-15px)",
                                "box_shadow": "0 20px 40px rgba(255, 107, 53, 0.2), inset 0 1px 1px rgba(255, 255, 255, 0.06)",
                                "border_color": "#FF6B35",
                                "border_width": "1px",
                            },
                            transition="all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275)",
                            cursor="pointer",
                            class_name="benefit-card fade-in-up",
                            position="relative",
                            overflow="hidden",
                            # Efecto de brillo en esquina
                            _after={
                                "content": "''",
                                "position": "absolute",
                                "top": "-50%",
                                "left": "-50%",
                                "width": "40px",
                                "height": "200px",
                                "background": "linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0) 100%)",
                                "transform": "rotate(35deg)",
                                "filter": "blur(3px)",
                                "opacity": "0",
                                "z_index": "1",
                                "transition": "all 0.8s ease"
                            },
                            _hover_after={
                                "transform": "rotate(35deg) translateX(450px)", 
                                "opacity": "1"
                            },
                            animation_delay="0.2s",
                        ),
                        
                        # Tarjeta 3: Proceso Reversible - Con efecto de flotación y animación
                        rx.box(
                            rx.vstack(
                                # Ícono más compacto
                                rx.center(
                                    rx.icon("wrench", size=50, color="#FF6B35"),
                                    width="100%",
                                    height="60px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                    mb="2",
                                    class_name="fade-in-up",
                                    animation_delay="0.6s",
                                ),
                                # Título con gradiente
                                rx.heading(
                                    "Proceso Reversible",
                                    size="5",
                                    color="white",
                                    mb="3",
                                    text_align="center",
                                    bg_image="linear-gradient(45deg, #FF6B35, #FF8C42)",
                                    bg_clip="text",
                                    text_fill_color="transparent",
                                    font_weight="700",
                                    class_name="fade-in-up",
                                    animation_delay="0.7s",
                                ),
                                # Descripción con texto más legible
                                rx.text(
                                    "La reprogramación es completamente reversible. Puedes volver a la configuración original cuando quieras.",
                                    color="rgba(255, 255, 255, 0.9)",
                                    line_height="1.6",
                                    text_align="center",
                                    font_size="1.05rem",
                                    class_name="fade-in-up",
                                    animation_delay="0.8s",
                                ),
                                spacing="6",
                                align="center",
                                height="100%",
                            ),
                            # Diseño de la tarjeta con efecto neumorfísmico
                            bg="linear-gradient(145deg, #202020, #1a1a1a)",
                            border_radius="30px",
                            p="6",
                            py="8",
                            border="1px solid #2c2c2c",
                            min_height="240px",
                            box_shadow="0 10px 25px rgba(0, 0, 0, 0.2), inset 0 1px 1px rgba(255, 255, 255, 0.06)",
                            _hover={
                                "transform": "translateY(-15px)",
                                "box_shadow": "0 20px 40px rgba(255, 107, 53, 0.2), inset 0 1px 1px rgba(255, 255, 255, 0.06)",
                                "border_color": "#FF6B35",
                                "border_width": "1px",
                            },
                            transition="all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275)",
                            cursor="pointer",
                            class_name="benefit-card fade-in-up",
                            position="relative",
                            overflow="hidden",
                            # Efecto de brillo en esquina
                            _after={
                                "content": "''",
                                "position": "absolute",
                                "top": "-50%",
                                "left": "-50%",
                                "width": "40px",
                                "height": "200px",
                                "background": "linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0) 100%)",
                                "transform": "rotate(35deg)",
                                "filter": "blur(3px)",
                                "opacity": "0",
                                "z_index": "1",
                                "transition": "all 0.8s ease"
                            },
                            _hover_after={
                                "transform": "rotate(35deg) translateX(450px)", 
                                "opacity": "1"
                            },
                            animation_delay="0.3s",
                        ),
                        
                        # Tarjeta 4: Garantía Incluida - Con efecto de flotación y animación
                        rx.box(
                            rx.vstack(
                                # Ícono más compacto
                                rx.center(
                                    rx.icon("shield-check", size=50, color="#FF6B35"),
                                    width="100%",
                                    height="60px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                    mb="2",
                                    class_name="fade-in-up",
                                    animation_delay="0.9s",
                                ),
                                # Título con gradiente
                                rx.heading(
                                    "Garantía Incluida",
                                    size="5",
                                    color="white",
                                    mb="3",
                                    text_align="center",
                                    bg_image="linear-gradient(45deg, #FF6B35, #FF8C42)",
                                    bg_clip="text",
                                    text_fill_color="transparent",
                                    font_weight="700",
                                    class_name="fade-in-up",
                                    animation_delay="1.0s",
                                ),
                                # Descripción con texto más legible
                                rx.text(
                                    "Ofrecemos garantía completa en todos nuestros servicios de reprogramación ECU.",
                                    color="rgba(255, 255, 255, 0.9)",
                                    line_height="1.6",
                                    text_align="center",
                                    font_size="1.05rem",
                                    class_name="fade-in-up",
                                    animation_delay="1.1s",
                                ),
                                spacing="6",
                                align="center",
                                height="100%",
                            ),
                            # Diseño de la tarjeta con efecto neumorfísmico
                            bg="linear-gradient(145deg, #202020, #1a1a1a)",
                            border_radius="30px",
                            p="6",
                            py="8",
                            border="1px solid #2c2c2c",
                            min_height="240px",
                            box_shadow="0 10px 25px rgba(0, 0, 0, 0.2), inset 0 1px 1px rgba(255, 255, 255, 0.06)",
                            _hover={
                                "transform": "translateY(-15px)",
                                "box_shadow": "0 20px 40px rgba(255, 107, 53, 0.2), inset 0 1px 1px rgba(255, 255, 255, 0.06)",
                                "border_color": "#FF6B35",
                                "border_width": "1px",
                            },
                            transition="all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275)",
                            cursor="pointer",
                            class_name="benefit-card fade-in-up",
                            position="relative",
                            overflow="hidden",
                            # Efecto de brillo en esquina
                            _after={
                                "content": "''",
                                "position": "absolute",
                                "top": "-50%",
                                "left": "-50%",
                                "width": "40px",
                                "height": "200px",
                                "background": "linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0) 100%)",
                                "transform": "rotate(35deg)",
                                "filter": "blur(3px)",
                                "opacity": "0",
                                "z_index": "1",
                                "transition": "all 0.8s ease"
                            },
                            _hover_after={
                                "transform": "rotate(35deg) translateX(450px)", 
                                "opacity": "1"
                            },
                            animation_delay="0.4s",
                        ),
                        
                        columns={"base": "1", "md": "2", "lg": "4"},
                        spacing="6",
                        width="100%",
                        class_name="fade-in-up",
                        justify="center",
                        max_width="1200px"
                    ),
                    width="100%"
                ),
                spacing="6",
                align="center",
                width="100%"
            ),
                max_width="1400px",
                px={"base": "6", "md": "8"},
                py={"base": "16", "md": "24"},
                mx="auto"
            ),
            width="100%"
        ),
        bg="#1A1A1A"
    )
