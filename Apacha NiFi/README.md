# Apache NiFi Docker Setup

Este repositorio contiene la configuración de Docker para ejecutar Apache NiFi con PostgreSQL como base de datos.

## Descripción

Apache NiFi es una plataforma de integración de datos que permite automatizar el flujo de datos entre sistemas. Esta configuración incluye:

- Apache NiFi con interfaz web
- PostgreSQL como base de datos backend
- Configuración de usuario único para autenticación

## Requisitos Previos

- Docker y Docker Compose instalados
- Puertos disponibles (revisar docker-compose.yml para los puertos específicos)

## Instalación y Configuración

### 1. Configuración de Variables de Entorno

Copia el archivo de ejemplo y configura las variables:

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus valores:

```bash
# Credenciales de usuario único para NiFi
SINGLE_USER_CREDENTIALS_USERNAME=tu_usuario
SINGLE_USER_CREDENTIALS_PASSWORD=tu_contraseña_segura

# Configuración de PostgreSQL
POSTGRES_USER=tu_usuario_db
POSTGRES_PASSWORD=tu_contraseña_db
POSTGRES_DB=nifi_postgres
```

### 2. Iniciar los Servicios

```bash
docker-compose up -d
```

### 3. Acceder a NiFi

Una vez que los contenedores estén ejecutándose, puedes acceder a NiFi en:
- **URL**: `https://localhost:8443/nifi`
- **Usuario**: El configurado en `SINGLE_USER_CREDENTIALS_USERNAME`
- **Contraseña**: La configurada en `SINGLE_USER_CREDENTIALS_PASSWORD`

## Estructura del Proyecto

```
Apacha NiFi/
├── docker-compose.yml    # Configuración de Docker Compose
├── .env                  # Variables de entorno (no incluido en git)
├── .env.example         # Ejemplo de variables de entorno
├── .gitignore           # Archivos ignorados por git
├── README.md            # Este archivo
└── nifi/                # Directorio para datos persistentes de NiFi
```

## Comandos Útiles

### Gestión de Contenedores
```bash
# Iniciar servicios
docker-compose up -d

# Detener servicios
docker-compose down

# Ver logs
docker-compose logs -f

# Reiniciar servicios
docker-compose restart

# Ver estado de contenedores
docker-compose ps
```

### Limpieza
```bash
# Detener y eliminar contenedores, redes y volúmenes
docker-compose down -v

# Eliminar imágenes no utilizadas
docker system prune -a
```

## Configuración Avanzada

### Volúmenes Persistentes
Los datos de NiFi se almacenan en el directorio `./nifi/` para persistencia entre reinicios.

### Base de Datos PostgreSQL
La base de datos PostgreSQL se utiliza para almacenar metadatos y configuraciones de NiFi. Las credenciales se comparten con otros servicios como Gitea si están configurados.

## Solución de Problemas

### Puerto ya en uso
Si encuentras errores de puertos en uso, verifica qué servicios están ejecutándose:
```bash
netstat -an | findstr :8443
```

### Problemas de permisos
En sistemas Windows, asegúrate de que Docker Desktop tenga permisos para acceder a la carpeta del proyecto.

### Logs de contenedores
Para diagnosticar problemas:
```bash
docker-compose logs nifi
docker-compose logs postgres
```

## Seguridad

- Cambia las contraseñas por defecto antes de usar en producción
- Usa contraseñas seguras (mínimo 12 caracteres con mayúsculas, minúsculas, números y símbolos)
- Considera usar HTTPS con certificados válidos en entornos de producción
- El archivo `.env` está excluido del control de versiones por seguridad

## Respaldo y Restauración

### Crear Respaldo
```bash
# Respaldo de la base de datos
docker-compose exec postgres pg_dump -U $POSTGRES_USER $POSTGRES_DB > backup.sql

# Respaldo de configuraciones de NiFi
docker-compose exec nifi tar -czf /tmp/nifi-backup.tar.gz /opt/nifi/nifi-current/conf
docker cp $(docker-compose ps -q nifi):/tmp/nifi-backup.tar.gz ./nifi-backup.tar.gz
```

### Restaurar Respaldo
```bash
# Restaurar base de datos
docker-compose exec postgres psql -U $POSTGRES_USER $POSTGRES_DB < backup.sql
```

## Recursos Adicionales

- [Documentación oficial de Apache NiFi](https://nifi.apache.org/docs.html)
- [Guía de administración de NiFi](https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html)
- [Docker Hub - Apache NiFi](https://hub.docker.com/r/apache/nifi)

## Contribución

Para contribuir a este proyecto:
1. Haz un fork del repositorio
2. Crea una rama para tu feature
3. Realiza los cambios necesarios
4. Crea un pull request

## Licencia

Este proyecto está bajo la licencia Apache 2.0 (misma que Apache NiFi).