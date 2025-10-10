# Proyecto: Potenciación de Coches con Reflex

## 🎯 Objetivo del Proyecto

El objetivo de esta página web es ofrecer una plataforma moderna y profesional para la personalización y mejora de vehículos mediante la reprogramación ECU. Los usuarios podrán seleccionar el tipo de motor, marca y modelo de su coche, recibir recomendaciones personalizadas y contactar fácilmente con profesionales especializados. El sitio busca ser una referencia en el sector, transmitiendo confianza, tecnología y resultados medibles.

## 🚦 Estado Actual del Proyecto

- Estructura de carpetas y archivos creada.
- Archivos principales con comentarios explicativos y documentación interna.
- Imports y dependencias preparados para desarrollo futuro.
- **Falta implementar:** lógica de componentes, páginas funcionales, estados reactivos, integración con backend, datos reales y estilos finales.

## Estructura del proyecto
- `app.py`: Punto de entrada principal.
- `components/`: Componentes reutilizables de la interfaz.
- `pages/`: Páginas principales de la aplicación.
- `state/`: Lógica de estado y gestión de datos.
- `utils/`: Funciones auxiliares.
- `assets/`: Archivos estáticos (imágenes, CSS, JS).
- `tests/`: Pruebas unitarias y de integración.

## Instalación
1. Clona el repositorio.
2. Crea y activa el entorno virtual:
    ```bash
    python -m venv .myvenv
    source .myvenv/Scripts/activate
    ```
3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
4. Ejecuta la aplicación:
    ```bash
    reflex run
    ```

## Funcionalidad principal
- Selección de tipo de motor, marca, modelo y opciones avanzadas.
- Recomendación de productos de mejora personalizados.
- Formulario de contacto (email y/o teléfono obligatorio).
- Envío de datos al profesional correspondiente.
- **Popup de descuento promocional:** Modal compacto en esquina inferior derecha con formulario de registro integrado.

## 🎁 Componente: Popup de Descuento (discount_popup.py)

### Descripción
Popup promocional compacto que aparece en la **esquina inferior derecha** de la página ofreciendo un **10% de descuento** a nuevos clientes que se registren.

### Características
- **Posición:** Fixed en esquina inferior derecha (bottom: 20px, right: 20px)
- **Tamaño:** Compacto (320px de ancho)
- **Animación:** Desliza desde abajo con fade-in
- **Responsive:** Se adapta en móviles con max-width
- **Dos vistas:**
  1. **Vista de oferta:** Muestra la promoción del 10% de descuento
  2. **Vista de formulario:** Formulario de registro con nombre, email y teléfono

### Estado (PopupState)
```python
show_popup: bool = True      # Controla visibilidad del popup
show_form: bool = False      # Alterna entre oferta y formulario
nombre: str = ""             # Campo nombre del usuario
email: str = ""              # Campo email del usuario
telefono: str = ""           # Campo teléfono del usuario
```

### Métodos
- `close_popup()`: Cierra el popup completamente
- `open_register()`: Muestra el formulario de registro
- `back_to_offer()`: Vuelve a la vista de oferta
- `submit_registration()`: Envía datos al backend (**TODO: Implementar por backend**)

### Integración con Backend
El método `submit_registration()` está preparado para enviar los datos:
```python
def submit_registration(self):
    # TODO: Backend debe implementar aquí la llamada al servidor
    # Datos disponibles: self.nombre, self.email, self.telefono
    print(f"Registro: {self.nombre}, {self.email}, {self.telefono}")
```

### Estilos y Diseño
- **Colores:** Naranja (#FF6B35) y fondo oscuro degradado
- **Border:** 2px solid con borde naranja
- **Shadow:** Efecto de profundidad con glow naranja
- **Inputs:** Fondo oscuro con borde que se ilumina en naranja al focus
- **Botones:** Gradiente naranja con efectos hover

### Comportamiento
1. Al cargar la página → Muestra la vista de oferta
2. Click en "REGISTRARME" → Despliega formulario
3. Click en "Volver" → Regresa a la oferta
4. Click en "Enviar" → Envía datos y cierra popup
5. Click en "X" → Cierra todo

### Archivos Relacionados
- **Componente:** `components/discount_popup.py`
- **Estilos CSS:** `assets/styles.css` (animación `popupSlideInBottomRight`)
- **Integración:** `app/app.py` (línea donde se importa y usa)

## 🛠️ Pasos Lógicos para Completar el Proyecto

1. **Implementar Componentes Base**
    - Desarrollar los componentes reutilizables en la carpeta `components/` (header, footer, selector de vehículos, formularios, etc.).
2. **Crear Estados Reactivos**
    - Implementar la lógica de estado en la carpeta `state/` para navegación, formularios y selector de vehículos.
3. **Desarrollar Páginas Principales**
    - Completar las páginas en `pages/` (inicio, servicios, acerca de, contacto) integrando los componentes y estados.
4. **Integrar Datos y Backend**
    - Conectar con el backend para obtener datos reales de vehículos y gestionar el envío de formularios.
5. **Diseñar y Pulir Estilos**
    - Desarrollar los estilos CSS en `assets/` para lograr una experiencia visual atractiva y profesional.
6. **Añadir Pruebas**
    - Implementar pruebas unitarias y de integración en la carpeta `tests/`.
7. **Revisar Accesibilidad y SEO**
    - Asegurar que la web sea accesible y optimizada para buscadores.

## 🚀 Estado Ideal para Lanzamiento a Producción

- Todas las páginas y componentes implementados y funcionales.
- Estados reactivos y navegación fluida.
- Integración completa con backend y datos reales.
- Estilos finales pulidos y responsivos.
- Pruebas superadas y sin errores críticos.
- Documentación actualizada y clara.
- Imágenes y recursos optimizados.
- Cumplimiento de buenas prácticas de seguridad, accesibilidad y SEO.

## Contacto y soporte
Para dudas o sugerencias, contacta al equipo de desarrollo.

---
Equipo Reflex Potenciación de Coches
