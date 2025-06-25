# Kafka y Debezium - Guía de Configuración

## 1. Configurar Conexión de Debezium a PostgreSQL

### Paso 1: Acceder al contenedor de Debezium
```bash
docker exec -it kafkaydebezium-debezium-1 /bin/bash
```

### Paso 2: Crear la conexión a PostgreSQL
**Nota:** Asegúrate de editar los valores de configuración antes de ejecutar:
- `tu_usuario_aqui`: Tu usuario de PostgreSQL
- `tu_password_aqui`: Tu contraseña de PostgreSQL  
- `tu_bd_aqui`: El nombre de tu base de datos

```bash
curl -X POST \
  -H "Accept:application/json" \
  -H "Content-Type:application/json" \
  http://kafkaydebezium-debezium-1:8083/connectors/ \
  -d '{
    "name": "cqrs-test-connector-postgres",
    "config": {
      "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
      "database.hostname": "postgres",
      "database.port": "5432",
      "database.user": "tu_usuario_aqui",
      "database.password": "tu_password_aqui",
      "database.dbname": "tu_bd_aqui",
      "database.server.name": "dbserver1",
      "plugin.name": "pgoutput",
      "value.converter": "org.apache.kafka.connect.json.JsonConverter"
    }
  }'
```

## 2. Monitorear Mensajes en Kafka

### Paso 1: Acceder al contenedor de Kafka
```bash
docker exec -it kafka /bin/bash
```

### Paso 2: Consumir mensajes de la tabla customer
```bash
kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic dbserver1.public.customer --from-beginning
```

## 3. Configuración de Base de Datos (CloudBeaver)

### Crear tablas de ejemplo:

```sql
-- Tabla Customer
CREATE TABLE IF NOT EXISTS Customer (
    id TEXT NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    country TEXT NOT NULL
);

-- Tabla Orders
CREATE TABLE IF NOT EXISTS Orders (
    id TEXT NOT NULL PRIMARY KEY,
    customerId TEXT NOT NULL,
    total NUMERIC(10,2) NOT NULL
);
```

### Insertar datos de prueba:
```sql
INSERT INTO customer(id, "name", country) 
VALUES ('1', 'aaa', 'ES');
```

## Notas Importantes:
- Los cambios DML (INSERT, UPDATE, DELETE) en la tabla `customer` serán automáticamente capturados por Debezium
- Los mensajes aparecerán en el tópico de Kafka: `dbserver1.public.customer`
- Asegúrate de que PostgreSQL tenga habilitada la replicación lógica


