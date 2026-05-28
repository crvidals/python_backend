# CRM AI Assistant API

Backend profesional para sistema CRM con asistente de IA, construido con FastAPI, PostgreSQL e integración con OpenAI.

## Características

- **FastAPI** con soporte async completo
- **PostgreSQL** como base de datos principal con SQLAlchemy 2.0
- **Alembic** para migraciones de base de datos
- **OpenAI** integrado para asistente de IA
- **Autenticación** con JWT (python-jose)
- **CORS** configurado para múltiples orígenes
- **Docker** y Docker Compose para desarrollo y despliegue
- **Testing** con pytest y pytest-asyncio

## Requisitos

- Python 3.12+
- PostgreSQL 16+
- Docker y Docker Compose (opcional)
- Una API key de OpenAI

## Configuración

1. Clona el repositorio:

```bash
git clone <repository-url>
cd backend
```

2. Crea el archivo `.env` basado en `.env.example`:

```bash
cp .env.example .env
```

3. Edita `.env` con tus credenciales:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/crm_db
OPENAI_API_KEY=tu-api-key-aqui
OPENAI_MODEL=gpt-4o-mini
SECRET_KEY=tu-clave-secreta-para-produccion
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
LOG_LEVEL=INFO
```

## Instalación

### Opción 1: Desarrollo local

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
alembic upgrade head

# Ejecutar seed de datos
python -m app.database.seed.run_seed

# Iniciar el servidor
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Opción 2: Docker Compose

```bash
docker compose up --build
```

Esto levantará PostgreSQL y la API automáticamente con las migraciones y seed aplicados.

## Uso

Una vez iniciado el servidor:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health check**: http://localhost:8000/health

## Estructura del Proyecto

```
backend/
├── app/
│   ├── ai/              # Integración con IA
│   ├── api/
│   │   ├── dependencies/
│   │   └── routes/      # Endpoints de la API
│   ├── core/            # Configuración y excepciones
│   ├── database/        # Modelos, migraciones y seed
│   ├── middleware/       # Middlewares personalizados
│   ├── schemas/         # Esquemas Pydantic
│   ├── services/        # Lógica de negocio
│   └── main.py          # Punto de entrada
├── tests/               # Tests del proyecto
├── alembic.ini          # Configuración de Alembic
├── docker-compose.yml   # Configuración Docker
├── Dockerfile           # Imagen Docker
└── requirements.txt     # Dependencias Python
```

## Testing

```bash
pytest
```

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/api/ai/chat` | Chat con asistente IA |
| GET | `/api/opportunities` | Listar oportunidades |
| POST | `/api/opportunities` | Crear oportunidad |
| GET | `/api/opportunities/{id}` | Obtener oportunidad |
| PUT | `/api/opportunities/{id}` | Actualizar oportunidad |
| DELETE | `/api/opportunities/{id}` | Eliminar oportunidad |

## Licencia

MIT
