# Guía de Deployment - AstroTech

## Pre-requisitos
- Python 3.8 o superior
- pip instalado
- Node.js 16+ (se instala automáticamente por Reflex)

## Instalación Local

### 1. Clonar y preparar el entorno
```bash
# Navegar al directorio frontend
cd frontend

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# En Windows:
.venv\Scripts\activate
# En Linux/Mac:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt