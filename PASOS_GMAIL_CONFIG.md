# 🚀 CONFIGURACIÓN GMAIL - PASO A PASO

## ✅ **Estado actual:**
- ❌ `.env.example` eliminado
- ✅ `.env` configurado y listo
- ✅ Simple Browser abierto en: https://myaccount.google.com/security

## 📋 **SIGUE ESTOS PASOS EXACTOS:**

### **1. Iniciar sesión en Gmail** 🔐
- Ya tienes abierto: https://myaccount.google.com/security
- **Inicia sesión** con: `astrotechreprogramaciones@gmail.com`
- Introduce la contraseña de la cuenta

### **2. Habilitar verificación en 2 pasos** 📱
- En la página de seguridad, busca: **"Verificación en 2 pasos"**
- Si NO está activada:
  - Haz clic en **"Verificación en 2 pasos"**
  - Sigue las instrucciones para configurar tu teléfono
  - **¡IMPORTANTE!** Este paso es OBLIGATORIO para generar App Passwords

### **3. Generar App Password** 🔑
- Una vez habilitada la verificación en 2 pasos
- Busca: **"Contraseñas de aplicaciones"** (App Passwords)
- Haz clic en **"Contraseñas de aplicaciones"**
- Selecciona **"Otra (nombre personalizado)"**
- Escribe: **"AstroTech Website"**
- Haz clic en **"GENERAR"**

### **4. Copiar la contraseña** 📋
Google te mostrará algo como:
```
abcd efgh ijkl mnop
```
**¡COPIA ESTA CONTRASEÑA!**

### **5. Actualizar .env** ⚙️
**Abre el archivo `.env` y reemplaza:**
```bash
SENDER_PASSWORD=xxxx-xxxx-xxxx-xxxx
```

**Por tu contraseña real (SIN ESPACIOS):**
```bash
SENDER_PASSWORD=abcdefghijklmnop
```

### **6. Reiniciar servidor** 🔄
En la terminal ejecuta:
```bash
# Detén el servidor (Ctrl+C si está corriendo)
# Luego reinicia:
reflex run
```

## ✅ **Verificación final**

Cuando reinicies, deberías ver:
```
📧 Configuración SMTP activada - emails se enviarán realmente
📧 Servidor: smtp.gmail.com:587
📧 Desde: astrotechreprogramaciones@gmail.com
```

## 🎯 **¡Ya puedes probar!**

1. Ve a: http://localhost:3000
2. Selecciona un vehículo
3. Haz clic en "Solicitar Presupuesto"
4. Completa el formulario
5. **¡Los emails llegarán realmente a tu bandeja!**

---

**🔥 Una vez hagas esto, el sistema estará 100% funcional y enviando emails reales**