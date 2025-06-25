# 🚀 Kafka y Debezium - Change Data Capture (CDC)

Esta carpeta contiene una configuración completa de Apache Kafka con Debezium para captura de cambios de datos (CDC) desde PostgreSQL, incluyendo Schema Registry, Redis y herramientas de administración.

## 📋 Tabla de Contenidos

- [Arquitectura](#arquitectura)
- [Servicios Incluidos](#servicios-incluidos)
- [Configuración](#configuración)
- [Instalación](#instalación)
- [Configuración de Debezium](#configuración-de-debezium)
- [Monitoreo y Pruebas](#monitoreo-y-pruebas)
- [Casos de Uso](#casos-de-uso)
- [Troubleshooting](#troubleshooting)

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                        Kafka Ecosystem                         │
├─────────────────┬───────────────┬───────────────┬───────────────┤
│   Zookeeper     │     Kafka     │ Schema Reg.   │ Kafka Manager │
│   Port: 2181    │ Ports: 9092   │ Port: 8081    │ Port: 9000    │
│                 │       29092   │               │               │
└─────────────────┴───────────────┴───────────────┴───────────────┘
                           │
                           │ CDC Events
                           │
┌─────────────────────────┼─────────────────────────────────────────┐
│        Debezium         │                Redis                    │
│     Port: 8083          │             Port: 6379                  │
│   (Kafka Connect)       │            (Cache/Queue)                │
└─────────────────────────┼─────────────────────────────────────────┘
                           │
                           │ Source Database
                           │
┌─────────────────────────┴─────────────────────────────────────────┐
│                    PostgreSQL 13                                 │
│                   Port: 5432                                     │
│              (Logical Replication)                               │
└───────────────────────────────────────────────────────────────────┘
```

## 🚀 Servicios Incluidos

### Core Kafka Stack
- **Zookeeper**: Coordinación de cluster Kafka
- **Kafka**: Message broker principal
- **Schema Registry**: Gestión de esquemas Avro
- **Kafka Manager**: Interfaz web de administración

### CDC y Storage
- **Debezium**: Plataforma CDC para captura de cambios
- **PostgreSQL**: Base de datos source con replicación lógica
- **Redis**: Cache y cola de mensajes

## ⚙️ Configuración

### Variables de Entorno

Crear archivo `.env` en esta carpeta:

```env
# PostgreSQL Configuration
POSTGRES_USER=kafka_user
POSTGRES_PASSWORD=tu_password_seguro
POSTGRES_DB=kafka_debezium

# Redis Configuration
REDIS_PASSWORD=SUPER_SECRET_PASSWORD

# Debezium Configuration
DEBEZIUM_GROUP_ID=debezium-cluster
```

### Puertos Expuestos

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| Kafka | 9092, 29092 | Broker interno y externo |
| Zookeeper | 2181 | Coordinación de cluster |
| Debezium | 8083 | Kafka Connect REST API |
| Schema Registry | 8081 | Gestión de esquemas |
| PostgreSQL | 5432 | Base de datos source |
| Redis | 6379 | Cache y mensajería |
| Kafka Manager | 9000 | Web UI de administración |

## 🚀 Instalación

### 1. Configurar Variables de Entorno
```bash
# Crear archivo .env con configuración personalizada
cat > .env << EOF
POSTGRES_USER=kafka_user
POSTGRES_PASSWORD=mi_password_seguro
POSTGRES_DB=kafka_debezium
REDIS_PASSWORD=mi_redis_password
EOF
```

### 2. Levantar el Stack Completo
```bash
# Iniciar todos los servicios
docker-compose up -d

# Verificar estado de servicios
docker-compose ps

# Ver logs de inicialización
docker-compose logs -f
```

### 3. Verificar Conectividad
```bash
# Test Kafka
docker-compose exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --list

# Test PostgreSQL
docker-compose exec postgres psql -U kafka_user -d kafka_debezium -c "SELECT version();"

# Test Debezium
curl -H "Accept:application/json" localhost:8083/
```

## 🔧 Configuración de Debezium

### 1. Preparar Base de Datos

**Crear tablas de ejemplo:**
```sql
-- Conectar a PostgreSQL
docker-compose exec postgres psql -U kafka_user -d kafka_debezium

-- Crear tabla Customer
CREATE TABLE IF NOT EXISTS Customer (
    id TEXT NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla Orders
CREATE TABLE IF NOT EXISTS Orders (
    id TEXT NOT NULL PRIMARY KEY,
    customerId TEXT NOT NULL,
    total NUMERIC(10,2) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar datos de prueba
INSERT INTO customer(id, name, country) 
VALUES 
  ('1', 'Juan Pérez', 'ES'),
  ('2', 'Ana García', 'MX'),
  ('3', 'Carlos López', 'AR');
```

### 2. Crear Conector Debezium

```bash
# Acceder al contenedor Debezium
docker-compose exec debezium bash

# Crear conector PostgreSQL
curl -X POST \
  -H "Accept:application/json" \
  -H "Content-Type:application/json" \
  http://localhost:8083/connectors/ \
  -d '{
    "name": "postgres-kafka-connector",
    "config": {
      "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
      "database.hostname": "postgres",
      "database.port": "5432",
      "database.user": "kafka_user",
      "database.password": "mi_password_seguro",
      "database.dbname": "kafka_debezium",
      "database.server.name": "dbserver1",
      "plugin.name": "pgoutput",
      "table.include.list": "public.customer,public.orders",
      "value.converter": "org.apache.kafka.connect.json.JsonConverter",
      "key.converter": "org.apache.kafka.connect.json.JsonConverter",
      "value.converter.schemas.enable": "false",
      "key.converter.schemas.enable": "false"
    }
  }'
```

### 3. Verificar Conector

```bash
# Listar conectores
curl -H "Accept:application/json" localhost:8083/connectors/

# Verificar estado del conector
curl -H "Accept:application/json" localhost:8083/connectors/postgres-kafka-connector/status
```

## 📊 Monitoreo y Pruebas

### Monitorear Tópicos de Kafka

```bash
# Listar todos los tópicos
docker-compose exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --list

# Consumir mensajes de Customer
docker-compose exec kafka kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic dbserver1.public.customer \
  --from-beginning

# Consumir mensajes de Orders
docker-compose exec kafka kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic dbserver1.public.orders \
  --from-beginning
```

### Pruebas de CDC

```sql
-- Ejecutar en PostgreSQL para generar eventos
docker-compose exec postgres psql -U kafka_user -d kafka_debezium

-- INSERT (evento CREATE)
INSERT INTO customer(id, name, country) VALUES ('4', 'María Rodríguez', 'CO');

-- UPDATE (evento UPDATE)
UPDATE customer SET country = 'PE' WHERE id = '1';

-- DELETE (evento DELETE)
DELETE FROM customer WHERE id = '2';
```

### Kafka Manager Web UI

- **URL**: http://localhost:9000
- **Funciones**:
  - Gestión visual de clusters
  - Monitoreo de tópicos
  - Configuración de particiones
  - Métricas en tiempo real

## 🎯 Casos de Uso

### 1. Event Sourcing
```bash
# Consumir todos los eventos para reconstruir estado
docker-compose exec kafka kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic dbserver1.public.customer \
  --from-beginning \
  --property print.timestamp=true
```

### 2. Real-time Analytics
```bash
# Stream de eventos para análisis
docker-compose exec kafka kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic dbserver1.public.orders \
  --property print.key=true \
  --property print.value=true
```

### 3. Data Synchronization
```bash
# Sincronización entre sistemas
curl -X POST localhost:8083/connectors/ \
  -H "Content-Type: application/json" \
  -d @sink-connector-config.json
```

## 🔍 Comandos Útiles

### Gestión de Conectores
```bash
# Listar conectores
curl localhost:8083/connectors

# Pausar conector
curl -X PUT localhost:8083/connectors/postgres-kafka-connector/pause

# Reanudar conector
curl -X PUT localhost:8083/connectors/postgres-kafka-connector/resume

# Eliminar conector
curl -X DELETE localhost:8083/connectors/postgres-kafka-connector
```

### Gestión de Kafka
```bash
# Crear tópico manualmente
docker-compose exec kafka kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create \
  --topic mi-topico \
  --partitions 3 \
  --replication-factor 1

# Describir tópico
docker-compose exec kafka kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --describe \
  --topic dbserver1.public.customer
```

### Monitoreo
```bash
# Ver logs de Debezium
docker-compose logs -f debezium

# Ver métricas de Kafka
docker-compose exec kafka kafka-run-class.sh kafka.tools.JmxTool \
  --object-name kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec \
  --jmx-url service:jmx:rmi:///jndi/rmi://localhost:9999/jmxrmi
```

## 🔧 Troubleshooting

### Problemas Comunes

#### Debezium no Conecta a PostgreSQL
```bash
# Verificar conectividad
docker-compose exec debezium ping postgres

# Verificar logs de PostgreSQL
docker-compose logs postgres

# Verificar configuración de replicación
docker-compose exec postgres psql -U kafka_user -d kafka_debezium \
  -c "SHOW wal_level; SHOW max_wal_senders; SHOW max_replication_slots;"
```

#### Kafka no Recibe Mensajes
```bash
# Verificar estado del conector
curl localhost:8083/connectors/postgres-kafka-connector/status

# Verificar tópicos creados
docker-compose exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --list

# Verificar logs de Kafka Connect
docker-compose logs debezium
```

#### Schema Registry Issues
```bash
# Verificar esquemas registrados
curl localhost:8081/subjects

# Ver configuración de compatibilidad
curl localhost:8081/config
```

### Comandos de Diagnóstico

```bash
# Estado completo del stack
docker-compose ps
docker-compose logs --tail=50

# Verificar red interna
docker network inspect kafkaydebezium_debezium_net

# Test de conectividad entre servicios
docker-compose exec kafka ping zookeeper
docker-compose exec debezium ping postgres
docker-compose exec debezium ping kafka
```

## 📈 Optimización y Producción

### Configuración de Performance
```yaml
# En docker-compose.yml, ajustar para producción:
kafka:
  environment:
    - KAFKA_HEAP_OPTS=-Xmx1G -Xms1G
    - KAFKA_CFG_NUM_NETWORK_THREADS=8
    - KAFKA_CFG_NUM_IO_THREADS=8
    - KAFKA_CFG_SOCKET_SEND_BUFFER_BYTES=102400
    - KAFKA_CFG_SOCKET_RECEIVE_BUFFER_BYTES=102400
```

### Monitoreo Avanzado
```bash
# Métricas de Debezium
curl localhost:8083/connectors/postgres-kafka-connector/metrics

# JMX Metrics de Kafka
docker-compose exec kafka kafka-run-class.sh kafka.tools.JmxTool \
  --object-name kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec
```

### Backup y Recuperación
```bash
# Backup de configuración de conectores
curl localhost:8083/connectors/postgres-kafka-connector/config > connector-backup.json

# Backup de tópicos (usando Kafka Tools)
docker-compose exec kafka kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic dbserver1.public.customer \
  --from-beginning > customer-backup.json
```

## 🔄 Integración con Otros Servicios

### Conexión con Airflow
```python
# Ejemplo de DAG para procesar eventos CDC
from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from kafka import KafkaConsumer

def process_cdc_events():
    consumer = KafkaConsumer('dbserver1.public.customer',
                           bootstrap_servers=['localhost:29092'])
    # Procesar eventos...
```

### Integración con CloudBeaver
Para visualizar los datos que están siendo capturados:
1. Conectar CloudBeaver a la base PostgreSQL
2. Monitorear las tablas que están siendo replicadas
3. Verificar el WAL y slots de replicación

## 📝 Esquema de Eventos CDC

### Estructura de Mensaje Debezium
```json
{
  "before": null,
  "after": {
    "id": "1",
    "name": "Juan Pérez",
    "country": "ES",
    "created_at": 1640995200000
  },
  "source": {
    "version": "1.4.2.Final",
    "connector": "postgresql",
    "name": "dbserver1",
    "db": "kafka_debezium",
    "table": "customer"
  },
  "op": "c",
  "ts_ms": 1640995200123
}
```

### Tipos de Operaciones
- `c`: CREATE (INSERT)
- `u`: UPDATE
- `d`: DELETE
- `r`: READ (snapshot inicial)

## 🆘 Comandos de Emergencia

```bash
# Reinicio completo del stack
docker-compose down && docker-compose up -d

# Limpiar volúmenes (¡ELIMINA DATOS!)
docker-compose down -v
docker volume prune -f

# Recrear conector desde cero
curl -X DELETE localhost:8083/connectors/postgres-kafka-connector
# Luego ejecutar el curl de creación nuevamente

# Reset completo de Kafka
docker-compose exec kafka kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --delete --topic dbserver1.public.customer
```

## 🔗 Referencias y Documentación

- [Debezium Documentation](https://debezium.io/documentation/)
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Confluent Schema Registry](https://docs.confluent.io/platform/current/schema-registry/)
- [PostgreSQL Logical Replication](https://www.postgresql.org/docs/13/logical-replication.html)

---
*Configuración actualizada: Junio 2025*
*Stack: Kafka 2.x + Debezium 1.4 + PostgreSQL 13 + Redis 7*