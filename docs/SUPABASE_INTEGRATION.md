# 🗄️ Guía de Integración con Supabase

## 📋 Descripción General

Este documento describe cómo integrar AstroTech con Supabase para gestionar la base de datos de vehículos usando PostgreSQL en la nube.

---

## 🎯 Objetivos

- ✅ Conectar la aplicación con Supabase PostgreSQL
- ✅ Crear tabla de vehículos con marcas españolas
- ✅ Implementar sistema de consultas eficiente
- ✅ Reemplazar SQLite local por base de datos en la nube

---

## 📦 Archivos Creados

### 1. **`.env`** (actualizado)
Configuración de credenciales de Supabase.

**Variables añadidas:**
```env
SUPABASE_URL=https://piexexjrjdgkunlezwcv.supabase.co
SUPABASE_KEY=sbp_cbb2e381d1c44fcb8975f1272390433684c46451
DB_USER=postgres
DB_PASSWORD=TU_PASSWORD_AQUI  # 🔴 DEBES CAMBIARLO
DB_HOST=db.piexexjrjdgkunlezwcv.supabase.co
DB_PORT=5432
DB_NAME=postgres
DATABASE_URL=postgresql://postgres:TU_PASSWORD_AQUI@db.piexexjrjdgkunlezwcv.supabase.co:5432/postgres
```

### 2. **`utils/supabase_connection.py`**
Gestor de conexión a Supabase PostgreSQL.

**Funciones principales:**
- `SupabaseConnection.connect()` - Establece conexión
- `SupabaseConnection.execute_query()` - Ejecuta SELECT
- `SupabaseConnection.execute_update()` - Ejecuta INSERT/UPDATE/DELETE
- `test_connection()` - Prueba la conexión

### 3. **`utils/create_vehicles_table.py`**
Script para crear la tabla de vehículos e insertar datos de ejemplo.

**Funciones principales:**
- `create_vehicles_table()` - Crea tabla con índices
- `insert_sample_vehicles()` - Inserta 130+ vehículos de marcas españolas

**Marcas incluidas:**
- Audi, BMW, Mercedes-Benz, Volkswagen
- SEAT, Renault, Peugeot, Ford, Opel
- Toyota, Honda, Nissan, Hyundai, Kia

### 4. **`utils/vehicle_data_supabase.py`**
Servicio para consultar vehículos desde Supabase.

**Funciones principales:**
- `get_vehicle_fuel_types()` - Tipos de combustible (Diesel, Gasolina)
- `get_vehicle_brands(fuel_type)` - Marcas por combustible
- `get_vehicle_models(fuel_type, brand)` - Modelos por marca
- `get_vehicle_versions(fuel_type, brand, model)` - Versiones específicas
- `get_vehicle_count()` - Total de vehículos
- `search_vehicles(search_term)` - Búsqueda por texto
- `add_vehicle()` - Añadir nuevo vehículo

### 5. **`test_supabase_integration.py`**
Script de prueba completo para verificar la integración.

### 6. **`install_supabase.py`**
Script de instalación automática de dependencias.

### 7. **`requirements.txt`** (actualizado)
Dependencias añadidas:
```
psycopg2-binary>=2.9.9
supabase>=2.0.0
```

---

## 🚀 Instalación Paso a Paso

### **Paso 1: Instalar Dependencias**

```bash
# Opción A: Instalación automática
python install_supabase.py

# Opción B: Instalación manual
pip install python-dotenv psycopg2-binary
```

### **Paso 2: Configurar Credenciales**

1. Ve a tu proyecto en Supabase: https://supabase.com/dashboard
2. Navega a: **Settings → Database**
3. Busca la sección **Connection String**
4. Copia tu contraseña
5. Actualiza el archivo `.env`:
   ```env
   DB_PASSWORD=tu_contraseña_real_aqui
   DATABASE_URL=postgresql://postgres:tu_contraseña_real_aqui@db.piexexjrjdgkunlezwcv.supabase.co:5432/postgres
   ```

### **Paso 3: Probar Conexión**

```bash
python utils/supabase_connection.py
```

**Salida esperada:**
```
✅ Conexión exitosa
⏰ Hora actual del servidor: 2025-11-03 12:00:00
```

### **Paso 4: Crear Tabla de Vehículos**

```bash
python utils/create_vehicles_table.py
```

Esto creará:
- ✅ Tabla `vehicles` con campos optimizados
- ✅ Índices para búsquedas rápidas
- ✅ Trigger de actualización automática
- ✅ 130+ vehículos de ejemplo (opcional)

### **Paso 5: Verificar Integración**

```bash
python test_supabase_integration.py
```

**Salida esperada:**
```
✅ Conexión: OK
📊 Total vehículos: 130+
⛽ Tipos de combustible: ['Diesel', 'Gasolina']
🚗 Marcas: 15+
✅ Sistema 100% funcional
```

---

## 🔄 Migrar la Aplicación a Supabase

### **Opción 1: Reemplazar el Servicio (Recomendado)**

Actualiza `state/vehicle_state_simple.py` para usar Supabase:

```python
# ANTES (SQLite local)
from utils.vehicle_data_simple import (
    get_vehicle_fuel_types,
    get_vehicle_brands,
    # ...
)

# DESPUÉS (Supabase)
from utils.vehicle_data_supabase import (
    get_vehicle_fuel_types,
    get_vehicle_brands,
    # ...
)
```

**Ventajas:**
- ✅ Cambio mínimo (solo 1 línea)
- ✅ API idéntica
- ✅ Sin cambios en componentes

### **Opción 2: Actualizar Automáticamente**

Crea un alias en `utils/vehicle_data_simple.py`:

```python
# Reexportar funciones de Supabase
from .vehicle_data_supabase import (
    get_vehicle_fuel_types,
    get_vehicle_brands,
    get_vehicle_models,
    get_vehicle_versions,
    get_vehicle_count,
)

# Mantener compatibilidad con código existente
__all__ = [
    'get_vehicle_fuel_types',
    'get_vehicle_brands',
    'get_vehicle_models',
    'get_vehicle_versions',
    'get_vehicle_count',
]
```

**Ventajas:**
- ✅ Cero cambios en código existente
- ✅ Migración transparente

---

## 🗄️ Estructura de la Tabla

```sql
CREATE TABLE vehicles (
    id SERIAL PRIMARY KEY,
    fuel_type VARCHAR(50) NOT NULL CHECK (fuel_type IN ('Diesel', 'Gasolina')),
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(150) NOT NULL,
    version VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Índices creados:**
- `idx_fuel_type` - Búsqueda por combustible
- `idx_brand` - Búsqueda por marca
- `idx_model` - Búsqueda por modelo
- `idx_fuel_brand_model` - Búsqueda combinada

---

## 🎯 Casos de Uso

### **1. Consultar Tipos de Combustible**
```python
from utils.vehicle_data_supabase import get_vehicle_fuel_types

fuel_types = get_vehicle_fuel_types()
# ['Diesel', 'Gasolina']
```

### **2. Consultar Marcas por Combustible**
```python
from utils.vehicle_data_supabase import get_vehicle_brands

brands = get_vehicle_brands('Diesel')
# ['Audi', 'BMW', 'Mercedes-Benz', 'Volkswagen', ...]
```

### **3. Consultar Modelos**
```python
from utils.vehicle_data_supabase import get_vehicle_models

models = get_vehicle_models('Diesel', 'Audi')
# ['A3', 'A4', 'Q3', 'Q5']
```

### **4. Consultar Versiones**
```python
from utils.vehicle_data_supabase import get_vehicle_versions

versions = get_vehicle_versions('Diesel', 'Audi', 'A3')
# ['2.0 TDI 150CV', '2.0 TDI 184CV S-Tronic']
```

### **5. Añadir Vehículo**
```python
from utils.vehicle_data_supabase import add_vehicle

success = add_vehicle(
    fuel_type='Diesel',
    brand='Audi',
    model='A6',
    version='3.0 TDI 272CV Quattro'
)
```

---

## 🔧 Solución de Problemas

### **Error: psycopg2 no instalado**
```bash
pip install psycopg2-binary
```

### **Error: No se puede conectar a Supabase**
1. Verifica tu contraseña en `.env`
2. Comprueba que el proyecto de Supabase está activo
3. Verifica tu conexión a internet

### **Error: Tabla no existe**
```bash
python utils/create_vehicles_table.py
```

### **Error: Base de datos vacía**
Ejecuta la inserción de datos:
```bash
python utils/create_vehicles_table.py
# Selecciona 's' cuando pregunte por insertar datos
```

---

## 📊 Ventajas de Usar Supabase

| Característica | SQLite Local | Supabase PostgreSQL |
|---------------|-------------|---------------------|
| **Escalabilidad** | Limitada | ✅ Ilimitada |
| **Acceso remoto** | ❌ No | ✅ Sí |
| **Backup automático** | ❌ Manual | ✅ Automático |
| **Concurrencia** | Limitada | ✅ Alta |
| **Búsqueda** | Básica | ✅ Avanzada (índices) |
| **Tiempo real** | ❌ No | ✅ Sí (con Supabase SDK) |
| **Costo** | Gratis | Gratis (hasta 500MB) |

---

## 📝 Próximos Pasos

1. ✅ Configurar credenciales en `.env`
2. ✅ Probar conexión
3. ✅ Crear tabla de vehículos
4. ✅ Insertar datos de ejemplo
5. ✅ Verificar integración
6. ⏳ Actualizar aplicación para usar Supabase
7. ⏳ Desplegar en producción

---

## 🆘 Soporte

Si tienes problemas:

1. Verifica los logs: `astrotech.log`
2. Ejecuta el test: `python test_supabase_integration.py`
3. Revisa la documentación de Supabase: https://supabase.com/docs

---

**Creado por:** AstroTech Dev Team  
**Fecha:** Noviembre 2025  
**Versión:** 1.0
