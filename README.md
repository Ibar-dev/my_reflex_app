# Proyecto: Potenciación de Coches con Reflex

## 🎯 Objetivo del Proyecto

El objetivo de esta página web es ofrecer una plataforma moderna y profesional para la personalización y mejora de vehículos mediante la reprogramación ECU. Los usuarios podrán seleccionar el tipo de motor, marca y modelo de su coche, recibir recomendaciones personalizadas y contactar fácilmente con profesionales especializados. El sitio busca ser una referencia en el sector, transmitiendo confianza, tecnología y resultados medibles.

## 🚦 Estado Actual del Proyecto

- ✅ **Estructura de carpetas y archivos** creada
- ✅ **Sistema de base de datos** completamente implementado
- ✅ **Popup de descuento** funcional con persistencia de datos
- ✅ **Componentes principales** desarrollados
- ✅ **Validaciones y manejo de errores** implementado
- ✅ **Scripts de prueba y verificación** disponibles
- ✅ **Compatibilidad Reflex 0.8.14+** - Errores de deployment corregidos
- ✅ **Banner de cookies RGPD** - Cumplimiento legal implementado
- ✅ **Despliegue en producción** - App funcionando en Reflex Cloud
- 🔄 **En desarrollo:** integración completa de páginas y estilos finales

## 📁 Estructura del Proyecto y Componentes Principales

### 🏠 **Aplicación Principal**
- **📍 `app/app.py`**: Punto de entrada principal de la aplicación
  - Importa todos los componentes y estados
  - Define estilos globales y configuración
  - Maneja el enrutamiento de páginas
  - **Ejecutar:** `reflex run`

- **📍 `rxconfig.py`**: Configuración de Reflex
  - Puerto frontend: 3000
  - Puerto backend: 8000
  - Base de datos: SQLite

### 🧩 **Componentes de Interfaz** (`components/`)
- **📍 `components/header.py`**: Barra de navegación superior
- **📍 `components/hero.py`**: Sección principal de bienvenida
- **📍 `components/vehicle_selector.py`**: Selector de marca/modelo de vehículo
- **📍 `components/benefits.py`**: Sección de beneficios del servicio
- **📍 `components/services.py`**: Servicios ofrecidos
- **📍 `components/faq.py`**: Preguntas frecuentes
- **📍 `components/contact.py`**: Formulario de contacto
- **📍 `components/footer.py`**: Pie de página
- **📍 `components/discount_popup.py`**: **⭐ POPUP DE DESCUENTO**
  - Modal promocional con 10% descuento
  - Formulario de registro integrado
  - Validaciones en tiempo real
  - Integración completa con base de datos
  - **✅ Compatible con Reflex 0.8.14+**
- **📍 `components/cookie_banner.py`**: **⭐ BANNER DE COOKIES RGPD**
  - Cumplimiento total con RGPD
  - Modal de configuración granular
  - Opciones: Esenciales, Analíticas, Marketing
  - Persistencia de preferencias del usuario
  - **✅ Desplegado en producción**

### 📄 **Páginas** (`pages/`)
- **📍 `pages/home.py`**: Página principal
- **📍 `pages/home_new.py`**: Versión alternativa de inicio
- **📍 `pages/about.py`**: Página "Acerca de nosotros"
- **📍 `pages/services.py`**: Página de servicios detallados
- **📍 `pages/contact.py`**: Página de contacto

### 🔧 **Estados y Lógica** (`state/`)
- **📍 `state/global_state.py`**: Estado global de la aplicación
- **📍 `state/vehicle_state.py`**: Gestión del selector de vehículos
- **📍 `state/contact_state.py`**: Formulario de contacto
- **📍 `state/cookie_state.py`**: **⭐ GESTIÓN DE COOKIES RGPD**
  - Persistencia de preferencias de cookies
  - Estados para diferentes tipos de cookies
  - Métodos de aceptación/rechazo
  - **✅ Funcional en producción**

### 🗄️ **Sistema de Base de Datos**
- **📍 `models/user.py`**: **⭐ MODELO DE DATOS**
  - Tabla `user_registrations`
  - Validaciones de datos
  - Configuración SQLite
  - Inicialización automática de BD

- **📍 `utils/database_service.py`**: **⭐ SERVICIO DE BD**
  - Operaciones CRUD completas
  - Validaciones robustas (email, teléfono)
  - Prevención de duplicados
  - Estadísticas y reportes
  - Manejo de errores

- **📍 `users.db`**: Base de datos SQLite (generada automáticamente)

### 🛠️ **Utilidades** (`utils/`)
- **📍 `utils/email_service.py`**: Servicio de envío de emails
- **📍 `utils/vehicle_data.py`**: Datos de vehículos disponibles
- **📍 `utils/popup_state.py`**: Estado del popup (vacío, lógica en discount_popup.py)

### 🧪 **Scripts de Verificación y Pruebas**
- **📍 `test_database.py`**: **⭐ PRUEBAS COMPLETAS DE BD**
  - Prueba todas las operaciones de base de datos
  - Validaciones y casos límite
  - **Ejecutar:** `python test_database.py`

- **📍 `test_popup_workflow.py`**: **⭐ SIMULACIÓN DEL POPUP**
  - Simula el flujo completo del popup
  - Prueba casos válidos e inválidos
  - **Ejecutar:** `python test_popup_workflow.py`

- **📍 `view_users.py`**: **⭐ VISOR DE REGISTROS**
  - Muestra todos los usuarios registrados
  - Estadísticas del sistema
  - **Ejecutar:** `python view_users.py`

- **📍 `check_system.py`**: **⭐ VERIFICACIÓN COMPLETA**
  - Verifica que todo el sistema funcione
  - Chequea imports, BD, validaciones
  - **Ejecutar:** `python check_system.py`

### 🎨 **Recursos** (`assets/`)
- **📍 `assets/styles.css`**: Estilos CSS personalizados
- **📍 `assets/selector-fix.css`**: Estilos específicos del selector
- **📍 `assets/components/`**: Componentes de estilo
- **📍 `assets/images/`**: Imágenes del proyecto

### 📊 **Datos** (`data/`)
- **📍 `data/vehiculos_turismo.json`**: Base de datos de vehículos

### 📚 **Documentación**
- **📍 `DATABASE_DOCUMENTATION.md`**: **⭐ DOCUMENTACIÓN COMPLETA DE BD**
  - Explicación detallada del sistema
  - Ejemplos de uso
  - Flujo de datos

- **📍 `README.md`**: Este archivo (documentación principal)

## 🚀 Instalación y Ejecución

### 1. **Preparar el Entorno**
```bash
# Clonar el repositorio
git clone <repository-url>
cd my_reflex_app

# Crear entorno virtual
python -m venv .myvenv

# Activar entorno virtual (Windows)
.myvenv\Scripts\activate

# Activar entorno virtual (Linux/Mac)
source .myvenv/bin/activate
```

### 2. **Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### 3. **Verificar el Sistema**
```bash
# Verificación completa del sistema
python check_system.py

# Verificar base de datos específicamente
python test_database.py
```

### 4. **Ejecutar la Aplicación**
```bash
# Iniciar el servidor de desarrollo
reflex run

# La aplicación estará disponible en:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

---
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
## � Sistema de Cookies RGPD

### **Ubicación:** `components/cookie_banner.py` + `state/cookie_state.py`

### **Características Principales:**
- **Cumplimiento RGPD:** Totalmente conforme con la normativa europea
- **Opciones Granulares:** Esenciales, Analíticas, Marketing
- **Persistencia:** Preferencias guardadas en cookies del navegador
- **Modal Configuración:** Interface detallada para gestionar preferencias
- **Responsive:** Optimizado para móviles y desktop

### **Estados del Banner:**
```python
cookies_accepted: bool = False       # Control principal de visibilidad
show_settings: bool = False          # Modal de configuración
essential_cookies: bool = True       # Siempre activadas
analytics_cookies: bool = False      # Opcionales
marketing_cookies: bool = False      # Opcionales
```

### **Métodos Principales:**
- `accept_all()`: Acepta todas las cookies
- `accept_essential_only()`: Solo cookies esenciales
- `open_config()`: Abre modal de configuración
- `save_custom_settings()`: Guarda preferencias personalizadas
- `on_load()`: **⭐ Carga preferencias desde cookies**

### **Integración Legal:**
- Texto explicativo sobre uso de datos
- Enlaces a política de privacidad
- Gestión de datos de contacto (nombre, email, teléfono)
- Transparencia sobre almacenamiento local

### **Comportamiento:**
1. **Primera visita:** Banner visible en parte inferior
2. **Interacción:** Usuario elige entre 3 opciones principales
3. **Configuración:** Modal detallado con checkboxes granulares
4. **Persistencia:** Preferencias guardadas automáticamente
5. **Visitas posteriores:** Banner oculto, preferencias recordadas

## �🎁 Componente Destacado: Popup de Descuento

### **Ubicación:** `components/discount_popup.py`

### **Características Principales:**
- **Posición:** Esquina inferior derecha (fixed)
- **Tamaño:** 320px de ancho, responsive
- **Animación:** Deslizamiento desde abajo
- **Funcionalidad:** Registro de usuarios con 10% descuento
- **✅ Compatible con Reflex 0.9.0**

### **Estados del Popup:**
```python
show_popup: bool = True      # Controla visibilidad
show_form: bool = False      # Alterna vista oferta/formulario
nombre: str = ""             # Campo nombre
email: str = ""              # Campo email  
telefono: str = ""           # Campo teléfono
is_loading: bool = False     # Estado de carga
success_message: str = ""    # Mensaje de éxito
error_message: str = ""      # Mensaje de error
```

### **Métodos Principales:**
- `close_popup()`: Cierra el popup
- `open_register()`: Muestra formulario
- `back_to_offer()`: Vuelve a la oferta
- `submit_registration()`: **⭐ Guarda en base de datos**
- `set_nombre()`, `set_email()`, `set_telefono()`: **✅ Setters explícitos para Reflex 0.9.0**

### **Integración con Base de Datos:**
El popup está completamente integrado con el sistema de base de datos:
1. Valida datos del formulario
2. Verifica emails duplicados
3. Guarda registro en `users.db`
4. Muestra mensajes de feedback
5. Cierra automáticamente en éxito

## 🗄️ Sistema de Base de Datos

### **Ubicación Principal:** `models/user.py` + `utils/database_service.py`

### **Tabla `user_registrations`:**
- `id`: ID único
- `nombre`: Nombre completo
- `email`: Email (único)
- `telefono`: Teléfono
- `source`: Origen del registro
- `is_contacted`: Estado de contacto
- `created_at`: Fecha de creación
- `updated_at`: Fecha de actualización

### **Operaciones Disponibles:**
- ✅ Crear usuario (`save_user_registration()`)
- ✅ Buscar por email (`get_user_by_email()`)
- ✅ Listar usuarios (`get_all_users()`)
- ✅ Marcar contactado (`mark_user_contacted()`)
- ✅ Obtener estadísticas (`get_stats()`)

### **Validaciones Implementadas:**
- Email formato válido
- Teléfono mínimo 9 dígitos
- Nombre obligatorio
- No duplicados por email

## 🧪 Testing y Verificación

### **Scripts Disponibles:**

| Script | Función | Comando |
|--------|---------|---------|
| `check_system.py` | Verificación completa | `python check_system.py` |
| `test_database.py` | Pruebas de BD | `python test_database.py` |
| `test_popup_workflow.py` | Simulación popup | `python test_popup_workflow.py` |
| `view_users.py` | Ver registros | `python view_users.py` |

### **Ejemplo de Verificación:**
```bash
# Verificar que todo funciona
python check_system.py

# Resultado esperado:
# 🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!
# 🚀 Listo para usar en producción
```

## 📊 Monitoreo de Usuarios

### **Ver Registros del Popup:**
```bash
python view_users.py
```

### **Estadísticas Disponibles:**
- Total de usuarios registrados
- Usuarios contactados vs pendientes
- Registros por fuente (popup, formulario, etc.)
- Tasa de conversión

## 🔧 Mejores Prácticas de Reflex Implementadas

### **Variables de Estado (State Variables):**
- ✅ **Uso correcto de `rx.cond()`** para expresiones condicionales
- ✅ **Setters explícitos** para evitar warnings en Reflex 0.9.0
- ✅ **Operadores bitwise** (`~`, `&`, `|`) en lugar de booleanos (`not`, `and`, `or`)

### **Componentes:**
- ✅ **Propiedades válidas** para todos los componentes
- ✅ **Spinner con size correcto** (`size="2"` en lugar de `size="sm"`)
- ✅ **Estados reactivos** sin uso directo de variables en `if/else`

### **Ejemplo de Código Corregido:**
```python
# ❌ INCORRECTO (causa VarTypeError)
_hover={
    "transform": "translateY(-2px)"
} if not PopupState.is_loading else {}

# ✅ CORRECTO (compatible con Reflex)
_hover=rx.cond(
    ~PopupState.is_loading,
    {"transform": "translateY(-2px)"},
    {}
)
```

## 🛠️ Correcciones de Deployment Implementadas

### **🐛 Errores Corregidos para Render:**
- **✅ VarTypeError corregido**: Uso de `rx.cond()` en lugar de expresiones booleanas directas
- **✅ Setters explícitos**: Añadidos métodos `set_nombre()`, `set_email()`, `set_telefono()`
- **✅ Spinner component**: Cambiado `size="sm"` por `size="2"` para compatibilidad
- **✅ Reflex best practices**: Implementación conforme a las últimas versiones

### **🔧 Cambios Técnicos Realizados:**
1. **Expresiones condicionales**: Reemplazadas con `rx.cond()`
2. **Setters del estado**: Añadidos métodos explícitos para cada campo
3. **Componentes Spinner**: Actualizados con propiedades válidas
4. **Operadores bitwise**: Uso de `~` en lugar de `not`

## 🛠️ Próximos Pasos para Completar

1. **✅ Sistema de Base de Datos** - COMPLETADO
2. **✅ Popup de Descuento** - COMPLETADO  
3. **✅ Banner de Cookies RGPD** - COMPLETADO
4. **✅ Compatibilidad Reflex 0.8.14+** - COMPLETADO
5. **✅ Despliegue en Producción** - COMPLETADO
6. **🔄 Páginas Completas** - En desarrollo
7. **🔄 Estilos Finales** - En desarrollo
8. **⏳ Selector de Vehículos** - Pendiente
9. **⏳ Sistema de Email** - Pendiente
10. **⏳ Dashboard Admin** - Pendiente

## 🚀 Estado para Producción

### **✅ Desplegado y Funcionando:**
- **🌐 URL Producción:** https://app-silver-grass.reflex.run
- Sistema de base de datos
- Popup de descuento funcional
- **Banner de cookies RGPD completo**
- Estructura de componentes
- Scripts de verificación
- Documentación completa
- **✅ Compatibilidad con Reflex 0.8.14+** - Sin errores en deployment
- **✅ Cumplimiento legal RGPD** - Banner de cookies funcional

### **🔄 En Desarrollo:**
- Integración completa de páginas
- Estilos responsive finales
- Optimización de rendimiento

## 📞 Contacto y Soporte

Para dudas sobre la implementación o el sistema de base de datos, revisar:
- `DATABASE_DOCUMENTATION.md` - Documentación técnica completa
- Scripts de prueba - Para verificar funcionamiento
- Logs de la aplicación - Para debugging

---
**Equipo Reflex Potenciación de Coches**  
*Sistema de Base de Datos implementado y funcional* ✅  
*Banner de Cookies RGPD desplegado y operativo* 🍪  
*Compatible con Reflex 0.8.14+ y funcionando en producción* 🚀  
*URL Producción: https://app-silver-grass.reflex.run* 🌐