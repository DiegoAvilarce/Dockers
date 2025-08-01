# Pasos para configurar Kafka y Debezium

## 1. Conectar al contenedor de Debezium

```bash
docker exec -it kafkaydebezium-debezium-1 /bin/bash
```

## 2. Crear conector PostgreSQL

```bash
curl -X POST -H "Accept:application/json" -H "Content-Type:application/json" http://kafkaydebeziumlastest-debezium-1:8083/connectors/ -d '
{
  "name": "cqrs-test-connector-postgres_v2",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres_kafka_v2",
    "database.port": "5432",
    "database.user": "[usuario]",
    "database.password": "[contraseña]",
    "database.dbname" : "kafka_debezium_v2",
    "database.server.name": "dbserver2",
    "plugin.name": "pgoutput",
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable": "false",
    "value.converter.schemas.enable": "false",
    "topic.prefix": "dbserver2",
    "table.include.list": "public.*",
    "publication.autocreate.mode": "filtered",
    "snapshot.mode": "initial",
    "decimal.handling.mode": "string"
  }
}'
```

## 3. Crear conector Oracle con LogMiner

```bash
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" http://localhost:8083/connectors/ -d '{
  "name": "conector_cdc_oracle",
  "config": {
    "connector.class": "io.debezium.connector.oracle.OracleConnector",
    "database.hostname": "[ip_servidor_oracle]",
    "database.port": "1521",
    "database.user": "debezium",
    "database.password": "[contraseña]",
    "database.dbname": "[nombre_bd]",
    "database.server.name": "cdc_oracle_server",
    "table.include.list": "SCHEMA.TABLA_EJEMPLO",
    "snapshot.mode": "initial",
    "topic.prefix": "cdc_oracle_server",
    "database.connection.adapter": "logminer",
    "log.mining.strategy": "online_catalog",
    "log.mining.continuous.mine": "true",
    "schema.history.internal.kafka.bootstrap.servers": "kafka:9092",
    "schema.history.internal.kafka.topic": "schema-changes.cdc_oracle_server",
    "include.schema.changes": "true",
    "schema.history.internal.store.only.captured.tables.ddl": "true"
  }
}'
```

## 4. Comandos de gestión

### Listar conectores
```bash
curl http://kafkaydebeziumlastest-debezium-1:8083/connectors
```

### Eliminar conector
```bash
curl -X DELETE http://localhost:8083/connectors/[nombre_conector]
```

### Eliminar tópicos de Kafka
```bash
kafka-topics.sh --bootstrap-server kafka:9092 --delete --topic [nombre_topico]
```

## 5. Verificar broker de Kafka

```bash
docker exec -it kafka /bin/bash 
kafka-topics.sh --bootstrap-server kafka:9092 --list
```

## 6. Consumir mensajes de Kafka

```bash
docker exec -it kafka /bin/bash

# Para PostgreSQL
kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic dbserver2.public.customer --from-beginning --group consumidor_nifi_1

# Para Oracle
kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic cdc_oracle_server.SCHEMA.TABLA_EJEMPLO --from-beginning --group consumidor_oracle_1
```

## 7. Tablas de ejemplo para pruebas (CloudBeaver)

```sql
CREATE TABLE IF NOT EXISTS Customer
(
    id TEXT NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    country TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Orders
(
    id TEXT NOT NULL PRIMARY KEY,
    customerId TEXT NOT NULL,
    total NUMERIC(10,2) NOT NULL
);

INSERT INTO customer(id,"name",country) values ('1','aaa','ES');
```

## Notas importantes

- Reemplazar `[usuario]`, `[contraseña]`, `[ip_servidor_oracle]`, `[nombre_bd]`, `[nombre_conector]`, `[nombre_topico]` con los valores correspondientes
- Verificar que las IPs de los contenedores sean correctas
- Asegurar que los puertos estén disponibles y configurados correctamente