# 📧 Configuración de Email - AstroTech

## ✅ ¿Qué está implementado?

- **Formulario de contacto funcional** que envía emails a: `Astrotechreprogramaciones@gmail.com`
- **Validación completa** de campos (nombre, email, teléfono, mensaje)
- **Modo simulación** por defecto (los emails se muestran en logs)
- **Integración con "Solicitar Presupuesto"** que pre-rellena el formulario

## 🔧 Configuración para Producción

### Paso 1: El archivo .env ya está creado
El archivo `.env` ya está configurado con los valores correctos para AstroTech.

### Paso 2: Configurar Gmail App Password
1. Ve a tu cuenta de Gmail
2. Habilita la verificación en 2 pasos
3. Genera un "App Password" específico para esta aplicación
4. Tutorial: https://support.google.com/accounts/answer/185833

### Paso 3: Actualizar la contraseña en .env
Edita el archivo `.env` y reemplaza:
```bash
SENDER_PASSWORD=xxxx-xxxx-xxxx-xxxx
```
Con tu App Password real de 16 caracteres (sin espacios ni guiones).

## 🚀 Cómo Funciona

### En Desarrollo (Modo Simulación)
- Sin archivo `.env`: Los emails se muestran en la consola/logs
- Útil para testing sin envío real

### En Producción
- Con `.env` configurado: Emails se envían realmente
- Destino fijo: `Astrotechreprogramaciones@gmail.com`

## 📝 Formato del Email

Los emails incluyen:
- **Remitente**: El email configurado en SENDER_EMAIL
- **Destinatario**: Astrotechreprogramaciones@gmail.com
- **Asunto**: "Nuevo contacto desde web - [Nombre]"
- **Contenido HTML** con:
  - Nombre, email, teléfono del contacto
  - Mensaje completo
  - Timestamp de recepción
  - Diseño responsive

## 🧪 Testing

### Modo Simulación (por defecto)
```bash
reflex run
# Llena el formulario → logs mostrarán el email completo
```

### Modo Real (con .env)
```bash
# Configura .env primero
reflex run
# Llena el formulario → email se envía realmente
```

## 🔍 Logs de Debug

En la consola verás:
```
📧 Enviando email a Astrotechreprogramaciones@gmail.com...
✅ Email enviado correctamente: Email enviado correctamente
```

O en modo simulación:
```
📧 MODO SIMULACIÓN - Email no enviado (falta configuración SMTP)
📧 Para: Astrotechreprogramaciones@gmail.com
📧 Asunto: Nuevo contacto desde web - Juan Pérez
📧 Contenido: [HTML completo]
```

## 🚨 Seguridad

- **NO** incluyas credenciales reales en el repositorio
- Usa **App Passwords**, no contraseñas normales
- El archivo `.env` está en `.gitignore`
- En producción, usa variables de entorno del servidor

## 📋 Checklist de Implementación

- [x] Servicio de email completo
- [x] Integración con formulario de contacto  
- [x] Validación de campos
- [x] Modo simulación para desarrollo
- [x] Documentación y configuración
- [x] Logs informativos
- [x] Diseño HTML del email
- [x] Manejo de errores

**Estado**: ✅ **LISTO PARA USAR**