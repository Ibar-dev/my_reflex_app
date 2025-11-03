# 📋 ARCHIVOS QUE DEBES MODIFICAR MANUALMENTE

## 🔴 OBLIGATORIO: Actualizar Contraseña

### **Archivo: `.env`**
**Ubicación:** Raíz del proyecto

**QUÉ HACER:**
Busca esta línea:
```env
DB_PASSWORD=TU_PASSWORD_AQUI
```

Cámbiala por tu contraseña real de Supabase:
```env
DB_PASSWORD=tu_contraseña_real_aqui
```

**También actualiza esta línea:**
```env
DATABASE_URL=postgresql://postgres:TU_PASSWORD_AQUI@db.piexexjrjdgkunlezwcv.supabase.co:5432/postgres
```

Por:
```env
DATABASE_URL=postgresql://postgres:tu_contraseña_real_aqui@db.piexexjrjdgkunlezwcv.supabase.co:5432/postgres
```

### **¿Dónde encontrar tu contraseña?**
1. Ve a: https://supabase.com/dashboard
2. Selecciona tu proyecto
3. Ve a: **Settings → Database**
4. Busca la sección **Connection String**
5. Copia la contraseña (está en la URI de conexión)

---

## 🟡 OPCIONAL: Migrar la Aplicación

### **Archivo: `state/vehicle_state_simple.py`**
**Ubicación:** `state/vehicle_state_simple.py`

**QUÉ HACER:**
Cambia la línea de importación:

**ANTES:**
```python
from utils.vehicle_data_simple import get_vehicle_fuel_types
```

**DESPUÉS:**
```python
from utils.vehicle_data_supabase import get_vehicle_fuel_types
```

**Líneas a cambiar (aproximadamente línea 12):**
```python
# CAMBIAR ESTO:
from utils.vehicle_data_simple import (
    get_vehicle_fuel_types,
    get_vehicle_brands,
    get_vehicle_models,
    get_vehicle_versions
)

# POR ESTO:
from utils.vehicle_data_supabase import (
    get_vehicle_fuel_types,
    get_vehicle_brands,
    get_vehicle_models,
    get_vehicle_versions
)
```

---

## ✅ DESPUÉS DE ACTUALIZAR

### **1. Instalar Dependencias**
Ejecuta en tu terminal:
```bash
python install_supabase.py
```

O manualmente:
```bash
pip install python-dotenv psycopg2-binary
```

### **2. Probar Conexión**
```bash
python utils/supabase_connection.py
```

Deberías ver:
```
✅ Conexión exitosa
⏰ Hora actual del servidor: 2025-11-03 ...
```

### **3. Crear Tabla de Vehículos**
```bash
python utils/create_vehicles_table.py
```

Cuando pregunte si quieres insertar datos, escribe `s` (sí).

### **4. Verificar Todo**
```bash
python test_supabase_integration.py
```

Deberías ver:
```
✅ Conexión: OK
📊 Total vehículos: 130+
⛽ Tipos de combustible: ['Diesel', 'Gasolina']
```

### **5. Reiniciar el Servidor Reflex**
```bash
# Detén el servidor actual (Ctrl+C)
reflex run
```

---

## 📋 RESUMEN DE CAMBIOS

| Archivo | Cambio Necesario | Obligatorio |
|---------|------------------|-------------|
| `.env` | Actualizar contraseña | ✅ SÍ |
| `state/vehicle_state_simple.py` | Cambiar import | ⚠️ Opcional* |

*Si no cambias el import, seguirá usando SQLite local. Si quieres usar Supabase, debes cambiarlo.

---

## 🎯 COMANDOS EN ORDEN

Ejecuta estos comandos en este orden:

```bash
# 1. Instalar dependencias
python install_supabase.py

# 2. Probar conexión (después de actualizar .env)
python utils/supabase_connection.py

# 3. Crear tabla y datos
python utils/create_vehicles_table.py

# 4. Verificar integración
python test_supabase_integration.py

# 5. Reiniciar servidor
reflex run
```

---

## ❓ ¿NECESITAS AYUDA?

Si algo no funciona:
1. Lee `SUPABASE_INTEGRATION.md` (guía completa)
2. Revisa que tu contraseña en `.env` es correcta
3. Verifica que tu proyecto de Supabase está activo
4. Comprueba los logs en `astrotech.log`

---

**¡Eso es todo!** 🎉

Después de actualizar `.env` con tu contraseña, ejecuta los comandos y tendrás Supabase funcionando.
