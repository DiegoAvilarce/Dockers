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
├── Dockerfile             # Imagen personalizada de Airflow
├── .env                   # Variables de entorno
├── dags/                  # Coloca tus DAGs aquí
├── plugins/               # Plugins personalizados
├── logs/                  # Logs de ejecución
└── config/
    └── airflow.cfg        # Configuración personalizada
```

## 🚀 Instalación

### 1. Configurar Variables de Entorno
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar variables según tu configuración
nano .env
```

### 2. Construir e Inicializar
```bash
# Construir imagen personalizada
docker-compose build

# Inicializar base de datos y configuración
docker-compose up airflow-init
```

### 3. Levantar Servicios
```bash
# Levantar todos los servicios
docker-compose up -d

# Verificar estado
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

```bash
# Ver logs en tiempo real
docker-compose logs -f airflow-scheduler

# Acceder al CLI de Airflow
docker-compose run --rm airflow-cli bash

# Habilitar Flower (monitor de Celery)
docker-compose --profile flower up -d

# Ejecutar comando específico de Airflow
docker-compose run --rm airflow-cli airflow dags list

# Reiniciar un servicio específico
docker-compose restart airflow-scheduler
```

### Gestión de DAGs

```bash
# Listar DAGs
docker-compose exec airflow-scheduler airflow dags list

# Ejecutar DAG manualmente
docker-compose exec airflow-scheduler airflow dags trigger example_dag

# Ver estado de DAG
docker-compose exec airflow-scheduler airflow dags state example_dag 2023-01-01
```

## 📊 Monitoreo

### Verificar Estado de Servicios
```bash
# Estado general
docker-compose ps

# Logs de servicios específicos
docker-compose logs postgres
docker-compose logs redis
docker-compose logs airflow-scheduler

# Recursos del sistema
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
# Configurar UID correcto
echo "AIRFLOW_UID=$(id -u)" >> .env
```

#### Servicios no Inician
```bash
# Verificar recursos del sistema
docker system df
docker system prune

# Revisar logs de inicialización
docker-compose logs airflow-init
```

#### Base de Datos no Conecta
```bash
# Verificar PostgreSQL
docker-compose exec postgres pg_isready -U airflow

# Reiniciar base de datos
docker-compose restart postgres
```

#### DAGs no Aparecen
```bash
# Verificar permisos en directorio dags/
ls -la dags/

# Revisar logs del DAG processor
docker-compose logs airflow-dag-processor
```

### Comandos de Diagnóstico

```bash
# Verificar conectividad de red
docker-compose exec airflow-scheduler ping postgres
docker-compose exec airflow-scheduler ping redis

# Verificar configuración de Airflow
docker-compose exec airflow-scheduler airflow config list

# Test de conexión a base de datos
docker-compose exec airflow-scheduler airflow db check
```

## 🔄 Mantenimiento

### Actualización
```bash
# Detener servicios
docker-compose down

# Actualizar imágenes
docker-compose pull

# Reconstruir imagen personalizada
docker-compose build --no-cache

# Reiniciar servicios
docker-compose up -d
```

### Backup
```bash
# Backup de base de datos
docker-compose exec postgres pg_dump -U airflow airflow > backup_$(date +%Y%m%d).sql

# Backup de configuración
tar -czf airflow_config_$(date +%Y%m%d).tar.gz config/ dags/ plugins/
```

### Limpieza
```bash
# Detener y remover contenedores
docker-compose down

# Remover volúmenes (¡CUIDADO: Elimina datos!)
docker-compose down -v

# Limpiar imágenes no utilizadas
docker image prune -f
```

## 📝 Notas Importantes

- ⚠️ **Desarrollo**: Esta configuración es para desarrollo local
- 🔒 **Seguridad**: Cambiar contraseñas por defecto en producción
- 💾 **Persistencia**: Los datos se guardan en volúmenes Docker
- 🚀 **Recursos**: Requiere mínimo 4GB RAM y 2 CPUs
- 📊 **Ejemplos**: Los DAGs de ejemplo están habilitados por defecto

---
*Configuración actualizada: Junio 2025*