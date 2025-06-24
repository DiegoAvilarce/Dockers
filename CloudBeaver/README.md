# 🗄️ CloudBeaver con PostgreSQL

Esta carpeta contiene una configuración independiente de CloudBeaver con su propia instancia de PostgreSQL para pruebas y desarrollo de bases de datos.

## 📋 Tabla de Contenidos

- [Arquitectura](#arquitectura)
- [Servicios Incluidos](#servicios-incluidos)
- [Configuración](#configuración)
- [Instalación](#instalación)
- [Uso](#uso)
- [Conexiones de Base de Datos](#conexiones-de-base-de-datos)
- [Troubleshooting](#troubleshooting)

## 🏗️ Arquitectura

```
┌─────────────────────────────────┐
│         CloudBeaver             │
│      (Web Interface)            │
│        Port 8978                │
└─────────────────┬───────────────┘
                  │
                  │ Network: db_network
                  │
┌─────────────────┴───────────────┐
│       PostgreSQL 15             │
│    (Database Server)            │
│        Port 5432                │
│   Container: postgres_db_test   │
└─────────────────────────────────┘
```

## 🚀 Servicios Incluidos

### CloudBeaver
- **Imagen**: `dbeaver/cloudbeaver:latest`
- **Puerto**: 8978
- **Función**: Interfaz web para administración de bases de datos
- **Características**:
  - Soporte multi-base de datos
  - Editor SQL avanzado
  - Gestión visual de esquemas
  - Exportación/importación de datos

### PostgreSQL
- **Imagen**: `postgres:15`
- **Puerto**: 5432 (expuesto)
- **Función**: Base de datos de prueba
- **Características**:
  - Persistencia en volumen Docker
  - Configuración personalizable
  - Acceso directo desde host

## ⚙️ Configuración

### Variables de Entorno Requeridas

Crear archivo `.env` en esta carpeta:

```env
# Base de datos PostgreSQL
POSTGRES_DB=testdb
POSTGRES_USER=testuser
POSTGRES_PASSWORD=tu_password_seguro

# CloudBeaver Admin
CB_ADMIN_NAME=admin
CB_ADMIN_PASSWORD=tu_cloudbeaver_password_seguro
```

### Estructura de Archivos

```
CloudBeaver/
├── docker-compose.yml    # Configuración principal
├── .env                 # Variables de entorno
└── README.md           # Este archivo
```

## 🚀 Instalación

### 1. Configurar Variables de Entorno
```bash
# Crear archivo .env
cat > .env << EOF
POSTGRES_DB=testdb
POSTGRES_USER=testuser
POSTGRES_PASSWORD=mi_password_seguro
CB_ADMIN_NAME=admin
CB_ADMIN_PASSWORD=mi_cloudbeaver_password_seguro
EOF
```

### 2. Levantar Servicios
```bash
# Iniciar todos los servicios
docker-compose up -d

# Verificar estado
docker-compose ps
```

### 3. Primera Configuración
```bash
# Ver logs de CloudBeaver para configuración inicial
docker-compose logs cloudbeaver
```

## 💻 Uso

### Acceso a CloudBeaver
- **URL**: http://localhost:8978
- **Usuario**: admin (o valor de CB_ADMIN_NAME)
- **Contraseña**: (valor de CB_ADMIN_PASSWORD)

### Comandos Útiles

```bash
# Ver estado de servicios
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f

# Acceder a PostgreSQL directamente
docker-compose exec postgres psql -U testuser -d testdb

# Backup de base de datos
docker-compose exec postgres pg_dump -U testuser testdb > backup.sql

# Restaurar backup
cat backup.sql | docker-compose exec -T postgres psql -U testuser -d testdb

# Reiniciar servicios
docker-compose restart
```

## 🔌 Conexiones de Base de Datos

### Conexión Local (PostgreSQL incluido)
**Desde CloudBeaver:**
- **Host**: `postgres`
- **Puerto**: `5432`
- **Base de datos**: `testdb` (o valor de POSTGRES_DB)
- **Usuario**: `testuser` (o valor de POSTGRES_USER)
- **Contraseña**: (valor de POSTGRES_PASSWORD)

**Desde aplicaciones externas:**
- **Host**: `localhost`
- **Puerto**: `5432`
- **Base de datos**: `testdb`
- **Usuario**: `testuser`
- **Contraseña**: (valor de POSTGRES_PASSWORD)

### Conexión a Airflow (si está ejecutándose)
**Para conectar a la base de datos de Airflow:**
- **Host**: `localhost` (o IP del host Docker)
- **Puerto**: `5432` (puerto de PostgreSQL de Airflow)
- **Base de datos**: `airflow`
- **Usuario**: `airflow`
- **Contraseña**: (valor configurado en Airflow)

## 📊 Características de CloudBeaver

### Funcionalidades Principales
- **Editor SQL**: Sintaxis highlighting, autocompletado
- **Navegador de Esquemas**: Exploración visual de tablas y relaciones
- **Gestión de Datos**: CRUD operations con interfaz gráfica
- **Exportación**: Múltiples formatos (CSV, JSON, SQL)
- **Usuarios**: Gestión de accesos y permisos
- **Conexiones**: Soporte para múltiples bases de datos

### Bases de Datos Soportadas
- PostgreSQL
- MySQL/MariaDB
- SQLite
- Oracle
- SQL Server
- MongoDB
- ClickHouse
- Y muchas más...

## 🔧 Troubleshooting

### Problemas Comunes

#### CloudBeaver no Inicia
```bash
# Verificar logs
docker-compose logs cloudbeaver

# Verificar puertos ocupados
netstat -tlnp | grep :8978

# Reiniciar servicio
docker-compose restart cloudbeaver
```

#### No se Puede Conectar a PostgreSQL
```bash
# Verificar estado de PostgreSQL
docker-compose exec postgres pg_isready -U testuser

# Verificar conectividad de red
docker-compose exec cloudbeaver ping postgres

# Revisar logs de PostgreSQL
docker-compose logs postgres
```

#### Problemas de Autenticación
```bash
# Verificar variables de entorno
docker-compose config

# Recrear contenedores con nueva configuración
docker-compose down
docker-compose up -d
```

#### Puerto 8978 Ocupado
```bash
# Verificar proceso usando el puerto
lsof -i :8978

# Cambiar puerto en docker-compose.yml
# Ejemplo: "8979:8978"
```

### Comandos de Diagnóstico

```bash
# Verificar conectividad de red interna
docker network ls
docker network inspect cloudbeaver_db_network

# Test de conexión a base de datos
docker-compose exec postgres psql -U testuser -d testdb -c "SELECT version();"

# Verificar volúmenes
docker volume ls | grep cloudbeaver
```

## 🔄 Mantenimiento

### Backup y Restauración
```bash
# Backup completo
docker-compose exec postgres pg_dumpall -U testuser > full_backup_$(date +%Y%m%d).sql

# Backup de base específica
docker-compose exec postgres pg_dump -U testuser testdb > testdb_backup_$(date +%Y%m%d).sql

# Restaurar backup
cat backup.sql | docker-compose exec -T postgres psql -U testuser -d testdb
```

### Actualización
```bash
# Actualizar imágenes
docker-compose pull

# Recrear contenedores
docker-compose up -d --force-recreate
```

### Limpieza
```bash
# Detener servicios
docker-compose down

# Remover volúmenes (¡CUIDADO: Elimina datos!)
docker-compose down -v

# Limpiar imágenes no utilizadas
docker image prune -f
```

## 🔗 Integración con Otros Servicios

### Conexión a Airflow
Si tienes Airflow ejecutándose, puedes conectar CloudBeaver a su base de datos:

1. **Crear nueva conexión en CloudBeaver**
2. **Configurar**:
   - Host: `host.docker.internal` (Windows/Mac) o IP del host
   - Puerto: 5432
   - Base de datos: airflow
   - Usuario/Contraseña: (de configuración de Airflow)

### Red Compartida
Para conectar con otros servicios Docker:

```yaml
# En docker-compose.yml, usar red externa
networks:
  default:
    external: true
    name: airflow_default
```

## 📝 Notas Importantes

- 🔒 **Seguridad**: Cambiar contraseñas por defecto
- 🌐 **Acceso**: Solo para desarrollo local
- 💾 **Persistencia**: Datos guardados en volúmenes Docker
- 🔌 **Puerto**: PostgreSQL expuesto en puerto 5432
- 🚀 **Performance**: Configuración básica, ajustar para producción

## 🆘 Comandos de Emergencia

```bash
# Reinicio completo
docker-compose down && docker-compose up -d

# Recrear base de datos (¡ELIMINA DATOS!)
docker-compose down -v
docker volume rm cloudbeaver_postgres_data
docker-compose up -d

# Acceso directo a PostgreSQL
docker-compose exec postgres psql -U testuser -d testdb
```

---
*Configuración actualizada: Junio 2025*