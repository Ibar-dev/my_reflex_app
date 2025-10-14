# 🔧 CONFIGURACIÓN GMAIL APP PASSWORD - PASO A PASO

## ⚠️ IMPORTANTE: DEBES SEGUIR ESTOS PASOS EXACTOS

### 📋 **Paso 1: Acceder a la cuenta de Gmail**
1. Ve a: https://myaccount.google.com/
2. Inicia sesión con: `astrotechreprogramaciones@gmail.com`

### 📋 **Paso 2: Habilitar verificación en 2 pasos**
1. En el menú izquierdo: **"Seguridad"**
2. Busca: **"Verificación en 2 pasos"**
3. Haz clic en **"Comenzar"**
4. Sigue las instrucciones para configurar tu teléfono
5. **¡MUY IMPORTANTE!** Este paso es OBLIGATORIO para generar App Passwords

### 📋 **Paso 3: Generar App Password**
1. Una vez habilitada la verificación en 2 pasos
2. Ve de nuevo a **"Seguridad"**
3. Busca: **"Contraseñas de aplicaciones"** (App Passwords)
4. Haz clic en **"Contraseñas de aplicaciones"**
5. Selecciona **"Otra (nombre personalizado)"**
6. Escribe: **"AstroTech Website"**
7. Haz clic en **"GENERAR"**

### 📋 **Paso 4: Copiar la contraseña generada**
Google te mostrará una contraseña de 16 caracteres como:
```
abcd efgh ijkl mnop
```

### 📋 **Paso 5: Actualizar el archivo .env**
1. Abre el archivo `.env` en el proyecto
2. Reemplaza `xxxx-xxxx-xxxx-xxxx` con la contraseña generada
3. **SIN ESPACIOS**, así:
```
SENDER_PASSWORD=abcdefghijklmnop
```

### 📋 **Paso 6: Reiniciar el servidor**
```bash
# Detén el servidor actual (Ctrl+C)
# Luego reinicia:
reflex run
```

## ✅ **Verificación**

Cuando reinicies `reflex run`, deberías ver en los logs:
```
📧 Configuración SMTP activada - emails se enviarán realmente
```

En lugar de:
```
📧 MODO SIMULACIÓN - Email no enviado
```

## 🚨 **Troubleshooting**

### Error: "Username and password not accepted"
- ✅ Verifica que la verificación en 2 pasos esté habilitada
- ✅ Genera una nueva App Password
- ✅ Copia la contraseña SIN espacios

### Error: "Less secure app access"
- ✅ NO uses tu contraseña normal de Gmail
- ✅ DEBES usar App Password específica

### Email no llega
- ✅ Verifica que `SENDER_EMAIL` sea igual al email que generó la App Password
- ✅ Revisa la carpeta de SPAM en Astrotechreprogramaciones@gmail.com

## 📝 **Notas importantes**

- La App Password es específica para esta aplicación
- Puedes generar múltiples App Passwords si es necesario
- Si cambias la contraseña de Gmail, las App Passwords siguen funcionando
- Para mayor seguridad, puedes revocar App Passwords desde la configuración

---

**🎯 Objetivo**: Conseguir que los emails del formulario lleguen realmente a `Astrotechreprogramaciones@gmail.com`