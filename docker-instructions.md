# Dockerización de AstroTech App

## Estructura de Archivos Docker

```
my_reflex_app/
├── Dockerfile              # Configuración del contenedor
├── docker-compose.yml      # Orquestación de servicios
├── .dockerignore          # Archivos a ignorar en build
├── nginx.conf             # Configuración de nginx (opcional)
├── docker-instructions.md # Este archivo
└── vehicles_local.db      # Base de datos local
```

## Comandos Docker

### Desarrollo
```bash
# Construir y ejecutar contenedor
docker-compose up --build

# Ejecutar en modo detached (background)
docker-compose up -d --build

# Ver logs
docker-compose logs -f app

# Detener contenedores
docker-compose down

# Limpiar imágenes y contenedores
docker system prune -a
```

### Producción
```bash
# Ejecutar con nginx
docker-compose --profile production up --build -d

# Escalar la aplicación
docker-compose up -d --scale app=2
```

### Monitoreo
```bash
# Ver estado de contenedores
docker-compose ps

# Acceder al contenedor
docker-compose exec app bash

# Ver recursos utilizados
docker stats
```

## Configuración de Puertos

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Nginx (producción)**: http://localhost:80

## Variables de Entorno

Las siguientes variables están configuradas:
- `DATABASE_URL=sqlite:///app/vehicles_local.db`
- `PYTHONPATH=/app`
- `PYTHONUNBUFFERED=1`

## Volúmenes

- Base de datos: `./vehicles_local.db:/app/vehicles_local.db`
- Logs: `./logs:/app/logs`

## Deploy con Docker

### Opción 1: Docker Hub
```bash
# Construir imagen
docker build -t astrotech-reflex-app .

# Taggear para Docker Hub
docker tag astrotech-reflex-app username/astrotech-reflex-app

# Subir a Docker Hub
docker push username/astrotech-reflex-app
```

### Opción 2: Docker Swarm o Kubernetes
El archivo `docker-compose.yml` está listo para ser usado con:
- Docker Swarm
- Kubernetes (con kompose)
- Docker Cloud
- Google Cloud Run
- AWS ECS

### Opción 3: VPS con Docker
```bash
# En el servidor
git clone <repo-url>
cd my_reflex_app
docker-compose up -d --build
```

## Troubleshooting

### Problemas comunes
1. **Puertos en uso**: Cambiar puertos en docker-compose.yml
2. **Permisos**: Ejecutar con `sudo` si es necesario
3. **Build fallido**: Limpiar caché `docker builder prune`
4. **Contenedor no inicia**: Verificar logs `docker-compose logs app`

### Depuración
```bash
# Ver logs en tiempo real
docker-compose logs -f

# Acceder al contenedor
docker-compose exec app bash

# Ver configuración
docker-compose config
```

## Optimizaciones

- Imagen base slim para menor tamaño
- Multi-stage build (para producción)
- Caché de dependencias de Python
- Health checks automáticos
- Restart policy configurable