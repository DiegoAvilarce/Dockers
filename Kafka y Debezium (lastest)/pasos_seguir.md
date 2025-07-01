# 📋 Guía Paso a Paso - Configuración Kafka y Debezium

Esta guía te llevará a través del proceso completo para configurar Debezium con PostgreSQL y consumir los cambios de datos a través de Kafka.

## 🎯 Objetivos

- Configurar un conector Debezium para PostgreSQL
- Crear tablas de ejemplo en la base de datos
- Consumir mensajes de Kafka con los cambios de datos (CDC)

## 📝 Prerequisitos

✅ Docker Compose ejecutándose con todos los servicios  
✅ Todos los contenedores en estado "healthy"  
✅ Acceso a la interfaz de Kafka UI en http://localhost:9000  

---

## 🚀 Paso 1: Preparar el Entorno

### 1.1 Verificar que todos los servicios estén corriendo

```bash
docker-compose ps
```

Deberías ver todos los servicios en estado `Up`:
- kafka
- postgres_kafka_v2
- debezium
- schema-registry
- redis
- kafka-ui

---

## 🔗 Paso 2: Configurar el Conector Debezium

### 2.1 Acceder al contenedor de Debezium

```bash
docker exec -it kafkaydebeziumlastest-debezium-1 /bin/bash
```

> 💡 **Nota**: El nombre del contenedor puede variar según tu configuración. Usa `docker ps` para verificar el nombre exacto.

### 2.2 Crear el conector PostgreSQL

Ejecuta el siguiente comando cURL dentro del contenedor de Debezium:

> ⚠️ **Importante**: Actualiza las credenciales de la base de datos con tus valores reales antes de ejecutar el comando.

```bash
curl -X POST -H "Accept:application/json" -H "Content-Type:application/json" \
http://kafkaydebeziumlastest-debezium-1:8083/connectors/ -d '{
  "name": "cqrs-test-connector-postgres_v2",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres_kafka_v2",
    "database.port": "5432",
    "database.user": "TU_USUARIO_DB",
    "database.password": "TU_PASSWORD_DB",
    "database.dbname": "TU_NOMBRE_DB",
    "database.server.name": "dbserver2",
    "plugin.name": "pgoutput",
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable": "false",
    "value.converter.schemas.enable": "false",
    "topic.prefix": "dbserver2",
    "table.include.list": "public.*",
    "publication.autocreate.mode": "filtered",
    "snapshot.mode": "initial"
  }
}'
```

### Variables a reemplazar:
- `TU_USUARIO_DB`: Usuario de PostgreSQL
- `TU_PASSWORD_DB`: Contraseña de PostgreSQL  
- `TU_NOMBRE_DB`: Nombre de la base de datos

### 2.3 Verificar el estado del conector

```bash
curl -X GET http://kafkaydebeziumlastest-debezium-1:8083/connectors/cqrs-test-connector-postgres_v2/status
```

Deberías ver un estado `RUNNING` para confirmar que el conector está funcionando correctamente.

---

## 🗄️ Paso 3: Preparar la Base de Datos

### 3.1 Conectarse a PostgreSQL

Puedes usar CloudBeaver (si está disponible) o conectarte directamente:

```bash
docker exec -it postgres_kafka_v2 psql -U TU_USUARIO_DB -d TU_NOMBRE_DB
```

### 3.2 Crear las tablas de ejemplo

```sql
-- Tabla de clientes
CREATE TABLE IF NOT EXISTS Customer (
    id TEXT NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    country TEXT NOT NULL
);

-- Tabla de pedidos
CREATE TABLE IF NOT EXISTS Orders (
    id TEXT NOT NULL PRIMARY KEY,
    customerId TEXT NOT NULL,
    total NUMERIC(10,2) NOT NULL
);
```

### 3.3 Insertar datos de prueba

```sql
-- Insertar un cliente de ejemplo
INSERT INTO customer(id, name, country) VALUES ('1', 'Juan Pérez', 'ES');

-- Insertar un pedido de ejemplo
INSERT INTO orders(id, customerId, total) VALUES ('1', '1', 99.99);
```

---

## 📡 Paso 4: Consumir Mensajes de Kafka

### 4.1 Verificar que el broker de Kafka esté activo

Primero, accede al contenedor de Kafka y verifica que el broker esté funcionando:

```bash
docker exec -it kafka /bin/bash 
kafka-topics.sh --bootstrap-server kafka:9092 --list
```

### 4.2 Consumir mensajes de Kafka para ver los cambios de DML

Una vez verificado que el broker está activo, ejecuta Kafka para ver los mensajes que se están enviando con los DML de la base de datos.

Accede al contenedor de Kafka:

```bash
docker exec -it kafka /bin/bash
```

### 4.3 Consumir mensajes de la tabla Customer

```bash
kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic dbserver2.public.customer --from-beginning
```

### 4.4 Consumir mensajes de la tabla Orders

En otra terminal, ejecuta:

```bash
kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic dbserver2.public.orders --from-beginning
```

---

## 🧪 Paso 5: Probar el CDC (Change Data Capture)

### 5.1 Realizar cambios en la base de datos

Desde PostgreSQL, ejecuta algunos comandos DML:

```sql
-- Actualizar un cliente
UPDATE customer SET name = 'Juan Carlos Pérez' WHERE id = '1';

-- Insertar un nuevo cliente
INSERT INTO customer(id, name, country) VALUES ('2', 'María García', 'MX');

-- Insertar un nuevo pedido
INSERT INTO orders(id, customerId, total) VALUES ('2', '2', 150.75);

-- Eliminar un pedido
DELETE FROM orders WHERE id = '1';
```

### 5.2 Observar los cambios en Kafka

Los consumidores de Kafka deberían mostrar automáticamente los mensajes JSON con los cambios realizados.

---

## 🖥️ Paso 6: Usar Kafka UI (Opcional)

### 6.1 Acceder a la interfaz web

Visita: http://localhost:9000

### 6.2 Explorar los topics

- Ve a la sección "Topics"
- Busca los topics: `dbserver2.public.customer` y `dbserver2.public.orders`
- Examina los mensajes y su estructura JSON

---

## 🔍 Verificación y Troubleshooting

### ✅ Checklist de Verificación

- [ ] Todos los contenedores están corriendo
- [ ] El conector Debezium está en estado RUNNING
- [ ] Las tablas fueron creadas correctamente
- [ ] Los topics de Kafka están recibiendo mensajes
- [ ] Los consumidores muestran los cambios en tiempo real

### 🚨 Problemas Comunes

#### Error: "Connector already exists"
```bash
# Eliminar el conector existente
curl -X DELETE http://kafkaydebeziumlastest-debezium-1:8083/connectors/cqrs-test-connector-postgres_v2
```

#### Error: "Database connection failed"
- Verificar que PostgreSQL esté corriendo
- Comprobar las credenciales en el conector
- Verificar que la base de datos exista

#### No se ven mensajes en Kafka
- Verificar que el conector esté en estado RUNNING
- Comprobar que las tablas tengan datos
- Verificar la configuración de `table.include.list`

### 📊 Comandos Útiles

```bash
# Ver todos los conectores
curl -X GET http://localhost:8083/connectors

# Ver configuración de un conector
curl -X GET http://localhost:8083/connectors/cqrs-test-connector-postgres_v2/config

# Eliminar conector
curl -X DELETE http://localhost:8083/connectors/cqrs-test-connector-postgres_v2

# Ver topics disponibles
docker exec kafka kafka-topics.sh --bootstrap-server kafka:9092 --list

# Eliminar topics
docker exec kafka kafka-topics.sh --bootstrap-server kafka:9092 --delete --topic dbserver2.public.orders

```

---

## 🔐 Configuración de Seguridad

### Variables de Entorno Recomendadas

Para mayor seguridad, considera usar variables de entorno en lugar de hardcodear credenciales:

```bash
export DB_USER="tu_usuario"
export DB_PASSWORD="tu_password"
export DB_NAME="tu_base_de_datos"
```

Luego modifica el comando cURL para usar estas variables:

```bash
curl -X POST -H "Accept:application/json" -H "Content-Type:application/json" \
http://kafkaydebeziumlastest-debezium-1:8083/connectors/ -d "{
  \"name\": \"cqrs-test-connector-postgres_v2\",
  \"config\": {
    \"connector.class\": \"io.debezium.connector.postgresql.PostgresConnector\",
    \"database.hostname\": \"postgres_kafka_v2\",
    \"database.port\": \"5432\",
    \"database.user\": \"$DB_USER\",
    \"database.password\": \"$DB_PASSWORD\",
    \"database.dbname\": \"$DB_NAME\",
    \"database.server.name\": \"dbserver2\",
    \"plugin.name\": \"pgoutput\",
    \"key.converter\": \"org.apache.kafka.connect.json.JsonConverter\",
    \"value.converter\": \"org.apache.kafka.connect.json.JsonConverter\",
    \"key.converter.schemas.enable\": \"false\",
    \"value.converter.schemas.enable\": \"false\",
    \"topic.prefix\": \"dbserver2\",
    \"table.include.list\": \"public.*\",
    \"publication.autocreate.mode\": \"filtered\",
    \"snapshot.mode\": \"initial\",
    \"decimal.handling.mode\": \"string\"
  }
}"
```

---

## 🎉 ¡Felicitaciones!

Has configurado exitosamente un pipeline de Change Data Capture usando Kafka y Debezium. Ahora puedes:

- Capturar cambios de PostgreSQL en tiempo real
- Procesar streams de datos con Kafka
- Monitorear el sistema a través de Kafka UI
- Escalar horizontalmente agregando más conectores o consumidores

## 📚 Próximos Pasos

- Explorar conectores para otras bases de datos
- Implementar procesamiento de streams con Kafka Streams
- Configurar alertas y monitoreo avanzado
- Integrar con herramientas de análisis en tiempo real