# 📧 Configuración del Formulario de Contacto con Email Real

## 🎯 Objetivo
El formulario de contacto ahora envía emails reales al dueño de la página cuando un usuario completa el formulario.

## ⚙️ Configuración Requerida

### 1. **Configurar Variables de Entorno**

Crea un archivo `.env` en la raíz del proyecto:

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus credenciales reales:

```env
SENDER_EMAIL=tu-email@gmail.com
SENDER_PASSWORD=tu-password-de-aplicacion-gmail
RECIPIENT_EMAIL=donde-quieres-recibir-los-mensajes@tudominio.com
```

### 2. **Configurar Gmail (Recomendado)**

Para usar Gmail como servidor SMTP:

1. **Habilitar 2FA** en tu cuenta de Gmail
2. **Generar contraseña de aplicación**:
   - Ve a [Configuración de Google Account](https://myaccount.google.com/security)
   - Seguridad > Verificación en dos pasos
   - Contraseñas de aplicaciones
   - Genera una nueva para "Correo"
   - Usa esa contraseña en `SENDER_PASSWORD`

### 3. **Proveedores Alternativos**

Si no quieres usar Gmail, puedes configurar otros proveedores editando `utils/email_service.py`:

**Outlook/Hotmail:**
```python
SMTP_SERVER = "smtp-mail.outlook.com"
SMTP_PORT = 587
```

**Yahoo:**
```python
SMTP_SERVER = "smtp.mail.yahoo.com"  
SMTP_PORT = 587
```

**Sendgrid (Recomendado para producción):**
```python
SMTP_SERVER = "smtp.sendgrid.net"
SMTP_PORT = 587
SENDER_EMAIL = "apikey"  # Literal "apikey"
SENDER_PASSWORD = "tu-api-key-de-sendgrid"
```

## 🚀 Funcionalidades Implementadas

### ✅ **Envío Real de Emails**
- Los datos del formulario se envían por email al destinatario configurado
- Email HTML con formato profesional
- Información completa del contacto

### ✅ **Validación Robusta**
- Validación de campos requeridos
- Formato de email correcto
- Validación de teléfonos españoles
- Mensajes de error específicos

### ✅ **Experiencia de Usuario**
- Estados de carga durante el envío
- Confirmación visual de envío exitoso
- Manejo de errores con mensajes claros
- Limpieza automática del formulario

### ✅ **Seguridad**
- Credenciales en variables de entorno
- Validación del lado del servidor
- Logging de errores para debugging

## 📧 Formato del Email

El email que recibirás incluye:

```
🚗 AstroTech - Nuevo Contacto

👤 Nombre: [Nombre del usuario]
📧 Email: [Email del usuario]  
📱 Teléfono: [Teléfono del usuario]
💬 Mensaje: [Mensaje del usuario]

Fecha: [Fecha y hora del envío]
```

## 🧪 Cómo Probar

1. **Configura las variables de entorno**
2. **Ejecuta la aplicación:**
   ```bash
   reflex run
   ```
3. **Ve al formulario de contacto**
4. **Completa todos los campos**
5. **Haz clic en "Enviar Mensaje"**
6. **Revisa tu email** (puede tardar unos minutos)

## 🔧 Troubleshooting

### Email no se envía:
- ✅ Verifica que las credenciales en `.env` sean correctas
- ✅ Confirma que la contraseña de aplicación de Gmail esté bien
- ✅ Revisa la consola de Reflex para ver errores

### Gmail rechaza el login:
- ✅ Asegúrate de usar la contraseña de aplicación, no tu contraseña normal
- ✅ Verifica que la verificación en dos pasos esté habilitada

### Email llega a spam:
- ✅ Normal en primeros envíos
- ✅ Marca como "No es spam" para futuros emails
- ✅ Considera usar SendGrid para producción

## 📁 Archivos Principales

- **`utils/email_service.py`**: Servicio de envío de emails
- **`state/contact_state.py`**: Estado del formulario con envío real
- **`components/contact.py`**: Componente visual del formulario
- **`.env.example`**: Plantilla de configuración
- **`.env`**: Tu configuración real (no subir a git)

## 🎉 ¡Listo!

Tu formulario de contacto ahora:
- ✅ Envía emails reales
- ✅ Valida todos los campos
- ✅ Maneja errores elegantemente
- ✅ Proporciona feedback al usuario
- ✅ Es seguro y profesional