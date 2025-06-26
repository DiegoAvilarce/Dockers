# Kafka y Debezium (Latest) - Docker Setup

Este proyecto configura un entorno completo de streaming de datos usando Apache Kafka y Debezium para Change Data Capture (CDC) con PostgreSQL.

## 🏗️ Arquitectura

El stack incluye los siguientes componentes:

- **Apache Kafka** (Bitnami) - Plataforma de streaming distribuida
- **Debezium Connect** - Conector CDC para capturar cambios en PostgreSQL
- **PostgreSQL 13** - Base de datos fuente con configuración de replicación lógica
- **Schema Registry** (Confluent) - Gestión de esquemas de datos
- **Redis** - Cache en memoria para datos temporales
- **Kafka UI** - Interfaz web para monitoreo y administración de Kafka

## 🚀 Servicios Incluidos

### Kafka (Puerto 9092, 29092)
- Configuración KRaft (sin Zookeeper)
- Listeners internos y externos
- ID de cluster: `abcdefghijklmnopqrstuv`

### PostgreSQL (Puerto 5432)
- Usuario: `postgres` (configurable via ENV)
- Base de datos: `postgres` (configurable via ENV)
- Configuración de replicación lógica habilitada
- WAL level configurado para streaming

### Debezium Connect (Puerto 8083)
- Conectores para PostgreSQL
- Configuración JSON para keys y values
- REST API para gestión de conectores

### Schema Registry (Puerto 8081)
- Gestión centralizada de esquemas
- Integración con Kafka

### Redis (Puerto 6379)
- Contraseña: `SUPER_SECRET_PASSWORD`
- Configuración persistente

### Kafka UI (Puerto 9000)
- Interfaz web para administración
- Visualización de topics, mensajes y esquemas
- Acceso: http://localhost:9000

## 📋 Prerrequisitos

- Docker y Docker Compose instalados
- Al menos 4GB de RAM disponible
- Puertos 5432, 6379, 8081, 8083, 9000, 9092, 29092 disponibles

## 🛠️ Instalación y Configuración

### 1. Iniciar los servicios

```bash
docker-compose up -d
```

### 2. Verificar que todos los servicios estén funcionando

```bash
docker-compose ps
```

### 3. Configurar variables de entorno (opcional)

Puedes crear un archivo `.env` para personalizar las credenciales:

```env
POSTGRES_USER=tu_usuario
POSTGRES_PASSWORD=tu_contraseña
POSTGRES_DB=tu_base_de_datos
```

## 🔗 Configuración de Conectores

Para configurar Debezium y conectar PostgreSQL con Kafka, sigue los pasos detallados en el archivo `pasos_seguir.md`.

## 📊 Monitoreo

### Kafka UI
- URL: http://localhost:9000
- Visualiza topics, particiones, mensajes y consumidores

### Debezium REST API
- URL: http://localhost:8083
- Endpoints principales:
  - `GET /connectors` - Lista conectores
  - `POST /connectors` - Crear conector
  - `GET /connectors/{name}/status` - Estado del conector

### Schema Registry
- URL: http://localhost:8081
- Endpoints principales:
  - `GET /subjects` - Lista esquemas
  - `GET /subjects/{subject}/versions` - Versiones de esquema

## 🗂️ Estructura de Topics

Los topics de Kafka siguen el patrón: `{database.server.name}.{schema}.{table}`

Ejemplo: `dbserver2.public.customer`

## 🔍 Troubleshooting

### Problemas Comunes

1. **Puerto en uso**: Verificar que los puertos no estén ocupados
2. **Memoria insuficiente**: Aumentar la memoria disponible para Docker
3. **Conectores no responden**: Verificar logs de Debezium
4. **PostgreSQL no acepta conexiones**: Verificar configuración de replicación

### Logs Útiles

```bash
# Ver logs de Kafka
docker-compose logs kafka

# Ver logs de Debezium
docker-compose logs debezium

# Ver logs de PostgreSQL
docker-compose logs postgres
```

## 📚 Recursos Adicionales

- [Documentación de Debezium](https://debezium.io/documentation/)
- [Guía de Kafka](https://kafka.apache.org/documentation/)
- [PostgreSQL Logical Replication](https://www.postgresql.org/docs/current/logical-replication.html)

## 🤝 Contribución

Para contribuir a este proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Crea un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT.