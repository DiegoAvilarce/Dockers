# MongoDB Docker Setup

Este directorio contiene la configuración de Docker Compose para ejecutar MongoDB con Mongo Express como interfaz web de administración.

## Servicios Incluidos

### 1. MongoDB Server (mongo-server)
- **Imagen**: `mongo:latest`
- **Puerto**: 27017
- **Container**: mongo-server
- **Función**: Base de datos MongoDB principal

### 2. Mongo Express (mongo-client)
- **Imagen**: `mongo-express:latest`
- **Puerto**: 8081
- **Container**: mongo-client
- **Función**: Interfaz web para administrar MongoDB

## Variables de Entorno

Puedes personalizar las credenciales usando variables de entorno o un archivo `.env`:

```bash
# Credenciales de MongoDB
MONGO_DB_ADMIN_USERNAME=admin_db
MONGO_DB_ADMIN_PASSWORD=mongodbpass

# Credenciales de Mongo Express
MONGO_EXPRESS_ADMIN_USERNAME=admin_express
MONGO_EXPRESS_ADMIN_PASSWORD=mongoexpresspass
```

## Uso

### Iniciar los servicios
```bash
docker-compose up -d
```

### Detener los servicios
```bash
docker-compose down
```

### Ver logs
```bash
# Todos los servicios
docker-compose logs -f

# Solo MongoDB
docker-compose logs -f mongo-server

# Solo Mongo Express
docker-compose logs -f mongo-client
```

## Acceso

### MongoDB
- **Host**: localhost
- **Puerto**: 27017
- **Usuario**: admin_db (o el definido en MONGO_DB_ADMIN_USERNAME)
- **Contraseña**: mongodbpass (o el definido en MONGO_DB_ADMIN_PASSWORD)

**Cadena de conexión**:
```
mongodb://admin_db:mongodbpass@localhost:27017/
```

### Mongo Express (Interfaz Web)
- **URL**: http://localhost:8081
- **Usuario**: admin_express (o el definido en MONGO_EXPRESS_ADMIN_USERNAME)
- **Contraseña**: mongoexpresspass (o el definido en MONGO_EXPRESS_ADMIN_PASSWORD)

## Persistencia de Datos

Los datos de MongoDB se almacenan en el volumen `mongodb_data`, lo que garantiza que los datos persistan entre reinicios del contenedor.

## Red

Ambos servicios están conectados a la red `mongodb_network` para permitir la comunicación interna entre contenedores.

## Comandos Útiles

### Conectarse a MongoDB desde la línea de comandos
```bash
docker exec -it mongo-server mongosh -u admin_db -p mongodbpass
```

### Hacer backup de la base de datos
```bash
docker exec mongo-server mongodump -u admin_db -p mongodbpass --authenticationDatabase admin --out /backup
```

### Restaurar backup
```bash
docker exec mongo-server mongorestore -u admin_db -p mongodbpass --authenticationDatabase admin /backup
```

## Troubleshooting

### El contenedor no inicia
1. Verificar que los puertos 27017 y 8081 no estén siendo usados por otros servicios
2. Revisar los logs: `docker-compose logs`

### No se puede conectar a MongoDB
1. Verificar que el contenedor esté ejecutándose: `docker-compose ps`
2. Verificar las credenciales de acceso
3. Asegurarse de que el puerto 27017 esté expuesto correctamente

### Mongo Express no carga
1. Verificar que MongoDB esté ejecutándose correctamente
2. Revisar los logs de Mongo Express: `docker-compose logs mongo-client`
3. Verificar las credenciales de ME_CONFIG_MONGODB_ADMINUSERNAME y ME_CONFIG_MONGODB_ADMINPASSWORD