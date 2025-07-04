# 🌬️ Apache Airflow con Docker Compose

Esta carpeta contiene la configuración completa de Apache Airflow usando Docker Compose con arquitectura CeleryExecutor, incluyendo PostgreSQL, Redis y CloudBeaver integrado.

## 📋 Tabla de Contenidos

- [Arquitectura](#arquitectura)
- [Servicios Incluidos](#servicios-incluidos)
- [Configuración](#configuración)
- [Instalación](#instalación)
- [Uso](#uso)
- [Monitoreo](#monitoreo)
- [Troubleshooting](#troubleshooting)

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Airflow UI    │    │   Scheduler     │    │  DAG Processor  │
│   (Port 8080)   │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
         ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
         │    Workers      │    │   Triggerer    │    │   API Server    │
         │   (Celery)      │    │   (Sensors)    │    │                 │
         └─────────────────┘    └─────────────────┘    └─────────────────┘
                 │                       │                       │
                 └───────────────────────┼───────────────────────┘
                                         │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │     Redis       │    │   CloudBeaver   │
│   (Database)    │    │ (Message Broker)│    │  (Port 8978)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Servicios Incluidos

### Core de Airflow
- **airflow-apiserver**: Servidor API y interfaz web (Puerto 8080)
- **airflow-scheduler**: Programador de tareas y DAGs
- **airflow-dag-processor**: Procesador de archivos DAG
- **airflow-worker**: Ejecutor de tareas usando Celery
- **airflow-triggerer**: Manejo de sensores asíncronos
- **airflow-init**: Inicialización y configuración inicial

### Infraestructura
- **postgres**: Base de datos PostgreSQL 13
- **redis**: Message broker Redis 7.2 para Celery
- **cloudbeaver**: Interfaz web para administración de bases de datos (Puerto 8978)

### Servicios Opcionales
- **airflow-cli**: CLI de Airflow para debugging (perfil: debug)
- **flower**: Monitor de Celery (perfil: flower, Puerto 5555)

## ⚙️ Configuración

### Variables de Entorno Requeridas

Crear archivo `.env` en esta carpeta:

```env
# Base de datos PostgreSQL
POSTGRES_USER=airflow
POSTGRES_PASSWORD=tu_password_seguro
POSTGRES_DB=airflow

# Usuario administrador de Airflow
_AIRFLOW_WWW_USER_USERNAME=admin
_AIRFLOW_WWW_USER_PASSWORD=tu_admin_password_seguro

# CloudBeaver
CB_ADMIN_NAME=admin
CB_ADMIN_PASSWORD=tu_cloudbeaver_password_seguro

# UID del usuario (Linux/Mac - opcional en Windows)
AIRFLOW_UID=1001

# Dependencias adicionales de Python (opcional)
_PIP_ADDITIONAL_REQUIREMENTS=
```

### Directorios Importantes

```
Airflow/
├── docker-compose.yaml     # Configuración principal
├── README.md              # Este archivo
├── .env                   # Variables de entorno
├── dags/                  # Coloca tus DAGs aquí
├── plugins/               # Plugins personalizados
├── logs/                  # Logs de ejecución
└── config/                # Configuración personalizada
```

## 🚀 Instalación

### 1. Configurar Variables de Entorno
```cmd
REM Copiar archivo de ejemplo (si existe)
copy .env.example .env

REM Editar variables según tu configuración
notepad .env
```

### 2. Construir e Inicializar
```cmd
REM Construir imagen personalizada
docker-compose build

REM Inicializar base de datos y configuración
docker-compose up airflow-init
```

### 3. Levantar Servicios
```cmd
REM Levantar todos los servicios
docker-compose up -d

REM Verificar estado
docker-compose ps
```

## 💻 Uso

### Acceso a Interfaces Web

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| **Airflow UI** | http://localhost:8080 | Usuario: admin<br>Contraseña: (desde .env) |
| **CloudBeaver** | http://localhost:8978 | Usuario: admin<br>Contraseña: (desde .env) |
| **Flower** | http://localhost:5555 | Sin autenticación |

### Comandos Útiles

```cmd
REM Ver logs en tiempo real
docker-compose logs -f airflow-scheduler

REM Acceder al CLI de Airflow
docker-compose run --rm airflow-cli bash

REM Habilitar Flower (monitor de Celery)
docker-compose --profile flower up -d

REM Ejecutar comando específico de Airflow
docker-compose run --rm airflow-cli airflow dags list

REM Reiniciar un servicio específico
docker-compose restart airflow-scheduler
```

### Gestión de DAGs

```cmd
REM Listar DAGs
docker-compose exec airflow-scheduler airflow dags list

REM Ejecutar DAG manualmente
docker-compose exec airflow-scheduler airflow dags trigger example_dag

REM Ver estado de DAG
docker-compose exec airflow-scheduler airflow dags state example_dag 2025-01-01
```

## 📊 Monitoreo

### Verificar Estado de Servicios
```cmd
REM Estado general
docker-compose ps

REM Logs de servicios específicos
docker-compose logs postgres
docker-compose logs redis
docker-compose logs airflow-scheduler

REM Recursos del sistema
docker stats
```

### Health Checks
Todos los servicios tienen health checks configurados:
- **PostgreSQL**: `pg_isready`
- **Redis**: `redis-cli ping`
- **Airflow Services**: HTTP endpoints específicos

### Conexión a Base de Datos
**Desde CloudBeaver:**
- Host: `postgres`
- Puerto: `5432`
- Base de datos: `airflow` (o valor de POSTGRES_DB)
- Usuario: `airflow` (o valor de POSTGRES_USER)
- Contraseña: (valor de POSTGRES_PASSWORD)

## 🔧 Troubleshooting

### Problemas Comunes

#### Error de Permisos (Linux/Mac)
```bash
# Configurar UID correcto (solo Linux/Mac)
echo "AIRFLOW_UID=$(id -u)" >> .env
```

#### Servicios no Inician
```cmd
REM Verificar recursos del sistema
docker system df
docker system prune

REM Revisar logs de inicialización
docker-compose logs airflow-init
```

#### Base de Datos no Conecta
```cmd
REM Verificar PostgreSQL
docker-compose exec postgres pg_isready -U airflow

REM Reiniciar base de datos
docker-compose restart postgres
```

#### DAGs no Aparecen
```cmd
REM Verificar archivos en directorio dags/
dir dags\

REM Revisar logs del DAG processor
docker-compose logs airflow-dag-processor
```

### Comandos de Diagnóstico

```cmd
REM Verificar conectividad de red
docker-compose exec airflow-scheduler ping postgres
docker-compose exec airflow-scheduler ping redis

REM Verificar configuración de Airflow
docker-compose exec airflow-scheduler airflow config list

REM Test de conexión a base de datos
docker-compose exec airflow-scheduler airflow db check
```

## 🔄 Mantenimiento

### Actualización
```cmd
REM Detener servicios
docker-compose down

REM Actualizar imágenes
docker-compose pull

REM Reconstruir imagen personalizada
docker-compose build --no-cache

REM Reiniciar servicios
docker-compose up -d
```

### Backup
```cmd
REM Backup de base de datos
docker-compose exec postgres pg_dump -U airflow airflow > backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.sql

REM Backup de configuración (usar herramientas como 7zip o WinRAR)
```

### Limpieza
```cmd
REM Detener y remover contenedores
docker-compose down

REM Remover volúmenes (¡CUIDADO: Elimina datos!)
docker-compose down -v

REM Limpiar imágenes no utilizadas
docker image prune -f
```

## 📝 Notas Importantes

- ⚠️ **Desarrollo**: Esta configuración es para desarrollo local
- 🔒 **Seguridad**: Cambiar contraseñas por defecto en producción
- 💾 **Persistencia**: Los datos se guardan en volúmenes Docker
- 🚀 **Recursos**: Requiere mínimo 4GB RAM y 2 CPUs
- 📊 **Ejemplos**: Los DAGs de ejemplo están habilitados por defecto
- 🪟 **Windows**: Comandos adaptados para Windows CMD/PowerShell

---
*Configuración actualizada: Julio 2025*