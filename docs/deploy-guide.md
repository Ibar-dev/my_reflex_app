# 🚀 Guía de Deploy - AstroTech App

## 📋 Requisitos Previos

- Servidor con Docker instalado
- Dominio (opcional, para producción)
- Acceso SSH al servidor

## 🔧 Método 1: Deploy Rápido (VPS)

### Paso 1: Preparar el Servidor
```bash
# Instalar Docker (Ubuntu/Debian)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Crear directorio de la aplicación
mkdir -p /var/www/astrotech
cd /var/www/astrotech
```

### Paso 2: Desplegar la Aplicación
```bash
# Clonar el repositorio
git clone <tu-repo-github-url> .

# Iniciar la aplicación
docker-compose up --build -d

# Verificar estado
docker-compose ps
curl http://localhost:3000
```

### Paso 3: Configurar Dominio (Opcional)
```bash
# Editar nginx.prod.conf
nano nginx.prod.conf
# Cambiar "your-domain.com" por tu dominio real

# Deploy con nginx
docker-compose -f docker-compose.prod.yml up -d
```

## ☁️ Método 2: Plataformas Cloud

### Railway (Recomendado para principiantes)
1. **Subir código a GitHub**
2. **Ir a [railway.app](https://railway.app)**
3. **Conectar cuenta GitHub**
4. **Seleccionar repositorio**
5. **Railway detectará Dockerfile automáticamente**
6. **Deploy automático con URL gratuita**

### Render
1. **Subir código a GitHub**
2. **Ir a [render.com](https://render.com)**
3. **Conectar cuenta GitHub**
4. **New > Web Service**
5. **Seleccionar repositorio**
6. **Render detectará Dockerfile**
7. **Deploy automático**

### DigitalOcean App Platform
1. **Subir código a GitHub**
2. **Ir a DigitalOcean > App Platform**
3. **Create App**
4. **Conectar GitHub**
5. **Seleccionar repositorio**
6. **Detectará Dockerfile automáticamente**

## 🔒 Método 3: Producción con HTTPS

### Usando Let's Encrypt (Gratis)
```bash
# Instalar certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal
sudo crontab -e
# Agregar: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Configurar Firewall
```bash
# Permitir HTTP/HTTPS
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow ssh
sudo ufw enable
```

## 📊 Monitoreo y Logs

### Ver Logs
```bash
# Logs de la aplicación
docker-compose logs -f app

# Logs de nginx
docker-compose logs -f nginx

# Logs del sistema
sudo journalctl -u docker -f
```

### Estado del Sistema
```bash
# Estado de contenedores
docker-compose ps

# Uso de recursos
docker stats

# Espacio en disco
df -h
```

## 🔄 Actualizaciones

### Actualizar la Aplicación
```bash
# Pull latest code
git pull

# Reconstruir y reiniciar
docker-compose down
docker-compose up --build -d

# Limpiar imágenes antiguas
docker image prune -f
```

### Backup de Base de Datos
```bash
# Backup de la base de datos
docker exec astrotech-reflex-app cp /app/vehicles_local.db /app/backup_$(date +%Y%m%d_%H%M%S).db

# Copiar al host
docker cp astrotech-reflex-app:/app/backup_*.db ./
```

## 🚨 Troubleshooting

### Problemas Comunes

#### Aplicación no inicia
```bash
# Ver logs de errores
docker-compose logs app

# Verificar puertos
netstat -tlnp | grep :3000
netstat -tlnp | grep :8000
```

#### Errores de memoria
```bash
# Aumentar memoria swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### Problemas de permisos
```bash
# Fix permisos de Docker
sudo usermod -aG docker $USER
sudo chown -R $USER:$USER /var/www/astrotech
```

### Health Check
```bash
# Verificar health status
curl -f http://localhost:3000 || echo "Frontend down"
curl -f http://localhost:8000/health || echo "Backend down"
```

## 📈 Escalado

### Escalado Horizontal
```bash
# Múltiples instancias
docker-compose up --scale app=3 -d
```

### Escalado Vertical
```bash
# Aumentar recursos (en docker-compose.yml)
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 1G
```

## 🌐 Acceso a la Aplicación

Una vez deployed, tu aplicación estará accesible en:
- **Development**: http://localhost:3000
- **Staging**: http://your-staging-domain.com
- **Production**: https://your-domain.com

## 📞 Soporte

Si tienes problemas durante el deploy:
1. Revisa los logs: `docker-compose logs`
2. Verifica la documentación: `docker-instructions.md`
3. Crea un issue en el repositorio
4. Contacta al equipo de soporte

**¡Tu aplicación AstroTech está lista para producción! 🎉**