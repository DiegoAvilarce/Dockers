# 🐳 Repositorio Docker

Este repositorio contiene configuraciones Docker para servicios de datos y análisis, incluyendo Apache Airflow y CloudBeaver para gestión de bases de datos.

## 📋 Tabla de Contenidos

- [Servicios Disponibles](#servicios-disponibles)
- [Requisitos del Sistema](#requisitos-del-sistema)
- [Instalación y Configuración](#instalación-y-configuración)
- [Apache Airflow](#apache-airflow)
- [CloudBeaver](#cloudbeaver)
- [Variables de Entorno](#variables-de-entorno)
- [Uso](#uso)
- [Troubleshooting](#troubleshooting)
- [Contribución](#contribución)

## 🚀 Servicios Disponibles

### Apache Airflow
- **Descripción**: Plataforma de orquestación de flujos de trabajo de código abierto
- **Puerto**: 8080
- **Executor**: Celery con Redis y PostgreSQL
- **Ubicación**: `./Airflow/`

### CloudBeaver
- **Descripción**: Herramienta web para administración de bases de datos
- **Puerto**: 8978
- **Compatibilidad**: PostgreSQL, MySQL, SQLite y más
- **Ubicación**: `./CloudBeaver/`

## 💻 Requisitos del Sistema

- **Docker**: >= 20.10.0
- **Docker Compose**: >= 2.0.0
- **Memoria RAM**: Mínimo 4GB (recomendado 8GB)
- **CPU**: Mínimo 2 cores
- **Espacio en Disco**: Mínimo 10GB libres

## ⚙️ Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone <url-del-repositorio>
cd "Repositorio Dockers"
```

### 2. Configurar Variables de Entorno
Crea archivos `.env` en cada directorio de servicio:

#### Para Airflow (`./Airflow/.env`):
```env
# Base de datos PostgreSQL
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow_password_secure
POSTGRES_DB=airflow

# Usuario administrador de Airflow
_AIRFLOW_WWW_USER_USERNAME=admin
_AIRFLOW_WWW_USER_PASSWORD=admin_password_secure

# CloudBeaver integrado
CB_ADMIN_NAME=admin
CB_ADMIN_PASSWORD=cloudbeaver_password_secure

# UID del usuario (Linux/Mac)
AIRFLOW_UID=1001
```

#### Para CloudBeaver independiente (`./CloudBeaver/.env`):
```env
# Base de datos PostgreSQL
POSTGRES_DB=testdb
POSTGRES_USER=testuser
POSTGRES_PASSWORD=testpassword_secure

# CloudBeaver
CB_ADMIN_NAME=admin
CB_ADMIN_PASSWORD=cloudbeaver_password_secure
```

## 🌬️ Apache Airflow

### Arquitectura
- **API Server**: Interfaz web y API REST
- **Scheduler**: Programador de tareas
- **Worker**: Ejecutor de tareas con Celery
- **Triggerer**: Manejo de sensores asíncronos
- **DAG Processor**: Procesador de DAGs
- **PostgreSQL**: Base de datos principal
- **Redis**: Message broker para Celery

### Iniciar Airflow
```bash
cd Airflow
docker-compose up -d
```

### Acceso
- **URL**: http://localhost:8080
- **Usuario**: admin (configurable en .env)
- **Contraseña**: admin_password_secure (configurable en .env)

### Directorios Importantes
- `./dags/`: Coloca aquí tus DAGs de Airflow
- `./plugins/`: Plugins personalizados
- `./logs/`: Logs de ejecución
- `./config/`: Configuración personalizada de Airflow

### Comandos Útiles
```bash
# Ver logs
docker-compose logs -f airflow-scheduler

# Acceder al CLI de Airflow
docker-compose run --rm airflow-cli bash

# Habilitar Flower (monitor de Celery)
docker-compose --profile flower up -d
```

## 🗄️ CloudBeaver

### Configuración Standalone
Para usar CloudBeaver de forma independiente con su propia base de datos PostgreSQL:

```bash
cd CloudBeaver
docker-compose up -d
```

### Acceso
- **URL**: http://localhost:8978
- **Usuario**: admin (configurable en .env)
- **Contraseña**: cloudbeaver_password_secure (configurable en .env)

### Conexión a Bases de Datos
CloudBeaver puede conectarse a:
- PostgreSQL de Airflow (host: `postgres`, puerto: 5432)
- PostgreSQL standalone (host: `postgres_db_test`, puerto: 5432)
- Otras bases de datos externas

## 🔧 Variables de Entorno

### Variables Principales de Airflow
| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `POSTGRES_USER` | Usuario de PostgreSQL | airflow |
| `POSTGRES_PASSWORD` | Contraseña de PostgreSQL | airflow |
| `POSTGRES_DB` | Base de datos PostgreSQL | airflow |
| `_AIRFLOW_WWW_USER_USERNAME` | Usuario admin de Airflow | airflow |
| `_AIRFLOW_WWW_USER_PASSWORD` | Contraseña admin de Airflow | airflow |
| `AIRFLOW_UID` | UID del usuario (Linux/Mac) | 1001 |

### Variables de CloudBeaver
| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `CB_ADMIN_NAME` | Usuario administrador | admin |
| `CB_ADMIN_PASSWORD` | Contraseña administrador | - |

## 🚀 Uso

### Iniciar Todos los Servicios
```bash
# Airflow completo
cd Airflow && docker-compose up -d

# CloudBeaver independiente
cd CloudBeaver && docker-compose up -d
```

### Detener Servicios
```bash
# Detener y remover contenedores
docker-compose down

# Detener, remover contenedores y volúmenes
docker-compose down -v
```

### Monitoreo
```bash
# Ver estado de contenedores
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f

# Ver uso de recursos
docker stats
```

## 🔍 Troubleshooting

### Problemas Comunes

#### Error de Permisos (Linux/Mac)
```bash
# Configurar AIRFLOW_UID
echo "AIRFLOW_UID=$(id -u)" >> Airflow/.env
```

#### Puerto ya en Uso
```bash
# Verificar puertos ocupados
netstat -tlnp | grep :8080
netstat -tlnp | grep :8978

# Cambiar puertos en docker-compose.yaml
```

#### Problemas de Memoria
- Aumentar memoria disponible para Docker
- Reducir número de workers en configuración

#### Base de Datos no Conecta
```bash
# Verificar estado de PostgreSQL
docker-compose exec postgres pg_isready -U airflow

# Reiniciar base de datos
docker-compose restart postgres
```

### Logs Útiles
```bash
# Logs de inicialización de Airflow
docker-compose logs airflow-init

# Logs del scheduler
docker-compose logs airflow-scheduler

# Logs de la base de datos
docker-compose logs postgres
```

## 🤝 Contribución

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📝 Notas Importantes

- ⚠️ **Producción**: Esta configuración es para desarrollo local. No usar en producción sin modificaciones de seguridad.
- 🔒 **Seguridad**: Cambiar todas las contraseñas por defecto antes del despliegue.
- 💾 **Volúmenes**: Los datos se persisten en volúmenes Docker nombrados.
- 🔄 **Actualizaciones**: Revisar regularmente las versiones de las imágenes Docker.

## 📞 Soporte

Para problemas o preguntas:
1. Revisar la sección [Troubleshooting](#troubleshooting)
2. Consultar logs del servicio específico
3. Crear un issue en el repositorio

---
*Última actualización: Junio 2025*
