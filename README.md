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

---

## 🚗 Componente: Selector de Vehículos con Botón de Envío

### 📍 Ubicación del Botón para Backend
**⚠️ IMPORTANTE PARA EQUIPO DE BACKEND ⚠️**

El botón de envío de datos del selector de vehículos se encuentra en:

```
📂 Archivo: components/vehicle_selector.py
📍 Línea: ~153-176 (aproximadamente)
🔍 Buscar: "⚠️ BOTÓN PARA BACKEND"
```

### 🎯 Método que Debes Implementar

**Archivo:** `state/vehicle_state.py`  
**Método:** `submit_vehicle_selection()`  
**Línea:** ~132

```python
def submit_vehicle_selection(self):
    """
    ⚠️ MÉTODO PARA BACKEND ⚠️
    
    Datos disponibles para enviar:
    - self.selected_fuel: Tipo de combustible (diesel/gasolina)
    - self.selected_brand: Marca del vehículo
    - self.selected_model: Modelo del vehículo
    - self.selected_year: Año del vehículo
    
    TODO BACKEND: Implementar aquí la llamada a tu API
    """
```

### 📊 Datos que Recibe el Backend

Cuando el usuario hace clic en **"Solicitar Presupuesto"**, se dispara el método `submit_vehicle_selection()` que tiene acceso a:

| Variable | Descripción | Tipo | Ejemplo |
|----------|-------------|------|---------|
| `self.selected_fuel` | Tipo de combustible | string | "diesel" o "gasolina" |
| `self.selected_brand` | Marca del vehículo | string | "Volkswagen" |
| `self.selected_model` | Modelo del vehículo | string | "Golf" |
| `self.selected_year` | Año del vehículo | string | "2023" |

### 💡 Ejemplo de Implementación

```python
def submit_vehicle_selection(self):
    """Envía la selección del vehículo al backend"""
    import requests
    
    try:
        response = requests.post(
            "https://tu-api.com/vehicle/quote",
            json={
                "fuel": self.selected_fuel,
                "brand": self.selected_brand,
                "model": self.selected_model,
                "year": self.selected_year
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Presupuesto solicitado correctamente")
            # Aquí puedes mostrar un mensaje de éxito al usuario
            # Ejemplo: self.show_success_message = True
        else:
            print(f"❌ Error: {response.status_code}")
            # Mostrar mensaje de error al usuario
            
    except Exception as e:
        print(f"❌ Error al enviar datos: {str(e)}")
        # Manejar el error apropiadamente
```

### 🎨 Características del Botón

**Diseño:**
- Fondo: Gradiente naranja (#FF6B35 → #FF8C42)
- Icono: "send" (sobre/enviar)
- Texto: "Solicitar Presupuesto"
- Tamaño: Completo (width: 100%)
- Padding: 1.5rem
- Efecto hover: Elevación y cambio de gradiente

**Comportamiento:**
- Solo visible cuando se completan los 4 pasos del selector
- Al hacer clic ejecuta `VehicleState.submit_vehicle_selection()`
- Efecto visual de elevación al pasar el mouse

### 📝 Validación de Datos

El botón solo aparece cuando:
1. ✅ Se ha seleccionado el combustible
2. ✅ Se ha seleccionado la marca
3. ✅ Se ha seleccionado el modelo  
4. ✅ Se ha seleccionado el año

**Código de validación:**
```python
rx.cond(
    VehicleState.selected_year != "",  # Solo muestra si hay año seleccionado
    # ... botón y resumen ...
)
```

### 🔗 Archivos Relacionados

| Archivo | Descripción | Línea Aprox |
|---------|-------------|-------------|
| `components/vehicle_selector.py` | Componente del botón visual | ~153-176 |
| `state/vehicle_state.py` | Lógica de envío (método a implementar) | ~132-191 |
| `app/app.py` | Integración del selector en la app | ~270 |

### 🎯 Checklist para Backend

- [ ] Revisar el método `submit_vehicle_selection()` en `state/vehicle_state.py`
- [ ] Implementar la llamada a tu API REST/GraphQL
- [ ] Manejar respuestas exitosas (200)
- [ ] Manejar errores (4xx, 5xx)
- [ ] Implementar timeout y reintentos si es necesario
- [ ] Agregar logging para debugging
- [ ] Mostrar feedback visual al usuario (éxito/error)
- [ ] (Opcional) Limpiar el selector después del envío exitoso

---

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
