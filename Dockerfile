# Usar Python 3.11 como base (más estable que 3.14 para Reflex)
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt primero para caché de Docker
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar archivos del proyecto
COPY . .

# Exponer puerto para la aplicación
EXPOSE 8000
EXPOSE 3000

# Variables de entorno
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Comando para ejecutar la aplicación
CMD ["reflex", "run", "--backend-host", "0.0.0.0", "--backend-port", "8000", "--frontend-port", "3000"]