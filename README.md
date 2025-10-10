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

## 🎁 Componente Destacado: Popup de Descuento

### **Ubicación:** `components/discount_popup.py`

### **Características Principales:**
- **Posición:** Esquina inferior derecha (fixed)
- **Tamaño:** 320px de ancho, responsive
- **Animación:** Deslizamiento desde abajo
- **Funcionalidad:** Registro de usuarios con 10% descuento

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

## 🛠️ Próximos Pasos para Completar

1. **✅ Sistema de Base de Datos** - COMPLETADO
2. **✅ Popup de Descuento** - COMPLETADO  
3. **🔄 Páginas Completas** - En desarrollo
4. **🔄 Estilos Finales** - En desarrollo
5. **⏳ Selector de Vehículos** - Pendiente
6. **⏳ Sistema de Email** - Pendiente
7. **⏳ Dashboard Admin** - Pendiente

## 🚀 Estado para Producción

### **✅ Listo para Usar:**
- Sistema de base de datos
- Popup de descuento funcional
- Estructura de componentes
- Scripts de verificación
- Documentación completa

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

## 🎁 Componente Destacado: Popup de Descuento

### **Ubicación:** `components/discount_popup.py`

### **Características Principales:**
- **Posición:** Esquina inferior derecha (fixed)
- **Tamaño:** 320px de ancho, responsive
- **Animación:** Deslizamiento desde abajo
- **Funcionalidad:** Registro de usuarios con 10% descuento

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

## 🛠️ Próximos Pasos para Completar

1. **✅ Sistema de Base de Datos** - COMPLETADO
2. **✅ Popup de Descuento** - COMPLETADO  
3. **🔄 Páginas Completas** - En desarrollo
4. **🔄 Estilos Finales** - En desarrollo
5. **⏳ Selector de Vehículos** - Pendiente
6. **⏳ Sistema de Email** - Pendiente
7. **⏳ Dashboard Admin** - Pendiente

## 🚀 Estado para Producción

### **✅ Listo para Usar:**
- Sistema de base de datos
- Popup de descuento funcional
- Estructura de componentes
- Scripts de verificación
- Documentación completa

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
