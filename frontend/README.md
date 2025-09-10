# Frontend AstroTech - Reflex

Este es el frontend de la aplicación AstroTech, desarrollado con Python y Reflex.

## 📁 Estructura del Proyecto

```
frontend/
├── app.py                 # Aplicación principal de Reflex
├── README.md             # Este archivo
├── components/            # Componentes reutilizables
│   ├── __init__.py
│   ├── header.py         # Barra de navegación (VACÍO - Solo comentarios)
│   ├── footer.py         # Pie de página (VACÍO - Solo comentarios)
│   └── vehicle_selector.py # Selector de vehículos (VACÍO - Solo comentarios)
├── pages/                # Páginas principales
│   ├── __init__.py
│   ├── home.py          # Página de inicio (VACÍO - Solo comentarios)
│   ├── services.py      # Página de servicios (VACÍO - Solo comentarios)
│   ├── about.py         # Página Acerca de (VACÍO - Solo comentarios)
│   └── contact.py       # Página de contacto (VACÍO - Solo comentarios)
├── state/               # Gestión de estado
│   ├── __init__.py
│   ├── global_state.py  # Estado global (VACÍO - Solo comentarios)
│   ├── vehicle_state.py # Estado del selector (VACÍO - Solo comentarios)
│   └── contact_state.py # Estado del formulario (VACÍO - Solo comentarios)
├── utils/               # Funciones auxiliares
│   ├── __init__.py
│   └── vehicle_data.py  # Datos de vehículos (VACÍO - Solo comentarios)
├── assets/              # Archivos estáticos
│   └── styles.css       # Estilos personalizados (VACÍO - Solo comentarios)
└── tests/               # Pruebas unitarias
    └── __init__.py
```

## 🎯 Estado Actual

**IMPORTANTE**: Todos los archivos están actualmente **VACÍOS** excepto por comentarios explicativos detallados.

### ✅ Lo que está listo:
- ✅ Estructura de carpetas completa
- ✅ Archivos creados con comentarios explicativos
- ✅ Documentación detallada en cada archivo
- ✅ Imports comentados para futura implementación
- ✅ TODOs marcados para desarrollo

### 🚧 Lo que falta por implementar:
- 🚧 Lógica de componentes
- 🚧 Páginas funcionales
- 🚧 Estados reactivos
- 🚧 Datos de vehículos
- 🚧 Estilos CSS
- 🚧 Imágenes (se agregarán en el futuro)

## 📋 Comentarios en Archivos

Cada archivo contiene comentarios detallados que explican:

### 🧩 Components/
- **header.py**: Barra de navegación con logo, menú y CTA
- **footer.py**: Pie de página con información de empresa
- **vehicle_selector.py**: Selector paso a paso de vehículos

### 📄 Pages/
- **home.py**: Página principal con hero section y selector
- **services.py**: Información detallada de servicios
- **about.py**: Información de empresa y equipo
- **contact.py**: Formulario de contacto funcional

### ⚙️ State/
- **global_state.py**: Navegación global y scroll
- **vehicle_state.py**: Estado del selector de vehículos
- **contact_state.py**: Estado del formulario de contacto

### 🔧 Utils/
- **vehicle_data.py**: Datos de vehículos por marca/modelo/año

## 🚀 Próximos Pasos para el Equipo

### 1. **Implementar Componentes Base**
```bash
# Descomentar imports en app.py
# Implementar header.py
# Implementar footer.py
```

### 2. **Crear Estados Reactivos**
```bash
# Implementar global_state.py
# Implementar vehicle_state.py
# Implementar contact_state.py
```

### 3. **Desarrollar Páginas**
```bash
# Implementar home.py
# Implementar services.py
# Implementar about.py
# Implementar contact.py
```

### 4. **Añadir Datos y Estilos**
```bash
# Implementar vehicle_data.py
# Desarrollar styles.css
# Añadir imágenes en assets/
```

## 🛠️ Tecnologías a Utilizar

- **Reflex**: Framework principal de Python
- **Python 3.8+**: Lenguaje de programación
- **CSS3**: Estilos personalizados
- **JavaScript**: Para funcionalidades avanzadas

## 📖 Documentación en Archivos

Cada archivo incluye:
- **Descripción detallada** de su propósito
- **Funcionalidades** que debe implementar
- **Dependencias** con otros archivos
- **TODOs** específicos para desarrollo
- **Ejemplos** de estructura esperada

## 🔗 Integración con Backend

El frontend está preparado para integrarse con el backend que está en la carpeta `../backend/`:
- API endpoints para datos de vehículos
- Envío de formularios de contacto
- Autenticación de usuarios (si es necesaria)

## 📞 Contacto del Equipo

Para dudas sobre la estructura o implementación, consultar los comentarios detallados en cada archivo o contactar al equipo de desarrollo.

---

**Nota**: Esta estructura está diseñada para ser desarrollada por múltiples miembros del equipo de forma paralela, ya que cada archivo tiene responsabilidades bien definidas y documentadas.