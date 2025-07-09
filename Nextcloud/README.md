# Nextcloud Docker Setup

Este repositorio contiene la configuración de Docker para desplegar Nextcloud con MariaDB.

## Requisitos

- Docker
- Docker Compose

## Configuración

1. Copia el archivo de ejemplo de variables de entorno:
   ```bash
   cp env.example .env
   ```

2. Edita el archivo `.env` con tus configuraciones:
   - Cambia el puerto si es necesario (por defecto 8080)
   - Configura las credenciales de administrador
   - Agrega los dominios confiables (IPs de tus servidores)
   - Configura las credenciales de la base de datos

## Variables de Entorno

### Configuración de Nextcloud
- `NEXTCLOUD_PORT`: Puerto donde se ejecutará Nextcloud
- `NEXTCLOUD_ADMIN_USER`: Usuario administrador de Nextcloud
- `NEXTCLOUD_ADMIN_PASSWORD`: Contraseña del administrador
- `NEXTCLOUD_TRUSTED_DOMAINS`: Dominios e IPs confiables (separados por comas)

### Configuración de Base de Datos
- `MARIADB_ROOT_PASSWORD`: Contraseña root de MariaDB
- `MARIADB_USER`: Usuario de la base de datos para Nextcloud
- `MARIADB_PASSWORD`: Contraseña del usuario de Nextcloud
- `MARIADB_NAME`: Nombre de la base de datos

## Uso

1. Inicia los servicios:
   ```bash
   docker-compose up -d
   ```

2. Accede a Nextcloud en: `http://localhost:PUERTO` (donde PUERTO es el valor configurado en NEXTCLOUD_PORT)

3. Para detener los servicios:
   ```bash
   docker-compose down
   ```

## Estructura

- `docker-compose.yml`: Configuración de los servicios Docker
- `.env`: Variables de entorno (no incluido en el repositorio)
- `env.example`: Ejemplo de variables de entorno

## Notas Importantes

- Asegúrate de cambiar todas las contraseñas por defecto
- Agrega todas las IPs desde las cuales accederás a Nextcloud en `NEXTCLOUD_TRUSTED_DOMAINS`
- Los datos se almacenan en volúmenes Docker persistentes

## Solución de Problemas

### Configuración Manual de Dominios Confiables

Si las IPs configuradas en `NEXTCLOUD_TRUSTED_DOMAINS` no son tomadas correctamente, puedes configurarlas manualmente editando el archivo de configuración:

```bash
# Copiar a tu carpeta de usuario
docker cp nextcloud-nextcloud-1:/var/www/html/config/config.php ~/nextcloud_config.php

# Editar archivo
nano ~/nextcloud_config.php

# En la siguiente parte debes ingresar las IP
'trusted_domains' =>
  array (
    0 => 'localhost',
    1 => '192.xxx.x.xx',          // tu IP local
    2 => 'nextcloud.midominio.cl' // o dominio
  ),

# Y lo vuelves a meter con 
docker cp ~/nextcloud_config.php nextcloud-nextcloud-1:/var/www/html/config/config.php
```

Después de realizar estos cambios, reinicia el contenedor:
```bash
docker-compose restart nextcloud
```