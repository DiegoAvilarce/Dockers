# Apache NiFi Docker Setup

Este repositorio contiene la configuración de Docker para ejecutar Apache NiFi con configuración de usuario único y volúmenes persistentes.

## Descripción

Apache NiFi es una plataforma de integración de datos que permite automatizar el flujo de datos entre sistemas. Esta configuración incluye:

- Apache NiFi con interfaz web HTTPS
- Configuración de usuario único para autenticación
- Volúmenes persistentes para datos y configuraciones
- Carpetas montadas para JDBC drivers, archivos de entrada y salida
- Configuración de red personalizada

## Requisitos Previos

- Docker y Docker Compose instalados
- Puerto 8443 disponible para la interfaz web HTTPS
- Variable de entorno `SERVER_IP` configurada (opcional)

## Configuración Inicial

### 1. Variables de Entorno

Puedes configurar las siguientes variables de entorno (opcionales):

```bash
# IP del servidor para acceso externo
export SERVER_IP=tu_ip_del_servidor

# Credenciales personalizadas (si no se especifican, usa valores por defecto)
export SINGLE_USER_CREDENTIALS_USERNAME=tu_usuario
export SINGLE_USER_CREDENTIALS_PASSWORD=tu_contraseña_segura
```

### 2. Estructura de Carpetas

Asegúrate de que existan las siguientes carpetas:

```bash
mkdir -p nifi/jdbc
mkdir -p nifi/input
mkdir -p nifi/output
```

### 3. Configuración de Permisos para Carpeta Output

**IMPORTANTE**: Para que la carpeta `nifi/output` funcione correctamente, debe configurarse con el UID 1000 del sistema (usuario nifi dentro del contenedor).

#### Verificar y Configurar Permisos:

```bash
# Acceder al contenedor
docker exec -it nifi bash

# Verificar permisos dentro del contenedor
ls -la /opt/nifi/output

# Intentar crear el archivo de prueba
touch /opt/nifi/output/test.txt

# Verificar que se creó
ls -la /opt/nifi/output

# Salir del contenedor
exit

# Cambiar el propietario de la carpeta a UID 1000 (usuario nifi)
sudo chown -R 1000:1000 ./nifi/output

# Verificar que el cambio se aplicó
ls -la ./nifi/output
```

## Instalación y Uso

### 1. Iniciar el Servicio

```bash
docker-compose up -d
```

### 2. Verificar que el Contenedor está Ejecutándose

```bash
docker-compose ps
```

### 3. Acceder a la Interfaz Web

Una vez que el contenedor esté ejecutándose, puedes acceder a NiFi en:

- **URL**: `https://localhost:8443/nifi`
- **Usuario**: `nifi` (por defecto) o el configurado en `SINGLE_USER_CREDENTIALS_USERNAME`
- **Contraseña**: `ctsBtRBKHRAx69EqUghvvgEvjnaLjFEB` (por defecto) o la configurada en `SINGLE_USER_CREDENTIALS_PASSWORD`

> **Nota**: El navegador mostrará una advertencia de seguridad debido al certificado autofirmado. Acepta el riesgo para continuar.

## Estructura del Proyecto

```
Apache NiFi/
├── docker-compose.yml    # Configuración de Docker Compose
├── README.md            # Este archivo
└── nifi/                # Directorio para datos y archivos
    ├── jdbc/            # Drivers JDBC personalizados
    ├── input/           # Archivos de entrada para procesamiento
    └── output/          # Archivos de salida (requiere permisos UID 1000)
```

## Configuración de Volúmenes

### Volúmenes Montados
- `./nifi/jdbc` → `/opt/nifi/nifi/jdbc` - Drivers JDBC personalizados
- `./nifi/input` → `/opt/nifi/input` - Archivos de entrada
- `./nifi/output` → `/opt/nifi/output` - Archivos de salida

### Volúmenes Persistentes
- `nifi-logs` - Logs de aplicación
- `nifi-conf` - Configuraciones
- `nifi-content_repository` - Repositorio de contenido
- `nifi-database_repository` - Repositorio de base de datos
- `nifi-flowfile_repository` - Repositorio de flowfiles
- `nifi-provenance_repository` - Repositorio de procedencia
- `nifi-state` - Estado de la aplicación

## Configuración de Red

- **Red**: `nifi_net` (bridge)
- **Puerto**: `8443:8443` (HTTPS)

## Comandos Útiles

### Gestión de Contenedores
```bash
# Iniciar servicios
docker-compose up -d

# Detener servicios
docker-compose down

# Ver logs en tiempo real
docker-compose logs -f nifi

# Reiniciar servicio
docker-compose restart nifi

# Ver estado del contenedor
docker-compose ps
```

### Gestión de Archivos
```bash
# Copiar drivers JDBC a la carpeta correspondiente
cp mi-driver.jar ./nifi/jdbc/

# Listar archivos en carpeta de entrada
ls -la ./nifi/input/

# Verificar archivos de salida
ls -la ./nifi/output/
```

### Acceso al Contenedor
```bash
# Acceder al shell del contenedor
docker exec -it nifi bash

# Verificar configuración de NiFi
docker exec -it nifi cat /opt/nifi/nifi-current/conf/nifi.properties
```

## Configuración Avanzada

### Limitación de Recursos
El contenedor está configurado con:
- **CPU**: Máximo 0.95 cores
- **Memoria**: Máximo 4GB

### Timezone
Configurado para `America/Santiago`. Para cambiar, modifica la variable de entorno `TZ` en el docker-compose.yml.

### Acceso Externo
Para permitir acceso desde otras máquinas, configura la variable `SERVER_IP` con la IP de tu servidor:

```bash
export SERVER_IP=192.168.1.100
docker-compose up -d
```

## Solución de Problemas

### Puerto ya en uso
```bash
# Verificar qué está usando el puerto 8443
netstat -an | findstr :8443
# En Linux/Mac: netstat -an | grep :8443
```

### Problemas de permisos en carpeta output
```bash
# Verificar permisos actuales
ls -la ./nifi/output/

# Aplicar permisos correctos
sudo chown -R 1000:1000 ./nifi/output/
```

### El contenedor no inicia
```bash
# Ver logs detallados
docker-compose logs nifi

# Verificar recursos disponibles
docker system df
```

### Problemas de conexión HTTPS
- Acepta el certificado autofirmado en el navegador
- Verifica que el puerto 8443 no esté bloqueado por firewall

## Backup y Restauración

### Crear Backup
```bash
# Backup de configuraciones
docker run --rm -v nifi-conf:/data -v $(pwd):/backup alpine tar czf /backup/nifi-conf-backup.tar.gz /data

# Backup de datos
docker run --rm -v nifi-content_repository:/data -v $(pwd):/backup alpine tar czf /backup/nifi-content-backup.tar.gz /data
```

### Restaurar Backup
```bash
# Restaurar configuraciones
docker run --rm -v nifi-conf:/data -v $(pwd):/backup alpine tar xzf /backup/nifi-conf-backup.tar.gz -C /

# Restaurar datos
docker run --rm -v nifi-content_repository:/data -v $(pwd):/backup alpine tar xzf /backup/nifi-content-backup.tar.gz -C /
```

## Limpieza

### Detener y Limpiar
```bash
# Detener contenedores
docker-compose down

# Eliminar volúmenes (CUIDADO: se perderán los datos)
docker-compose down -v

# Limpiar imágenes no utilizadas
docker system prune -a
```

## Seguridad

- **Credenciales por defecto**: Cambia las credenciales antes de usar en producción
- **HTTPS**: La interfaz usa HTTPS con certificado autofirmado
- **Acceso**: La autenticación anónima está deshabilitada
- **Red**: El contenedor está en una red bridge aislada

## Recursos Adicionales

- [Documentación oficial de Apache NiFi](https://nifi.apache.org/docs.html)
- [Guía de administración de NiFi](https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html)
- [Docker Hub - Apache NiFi](https://hub.docker.com/r/apache/nifi)
- [NiFi Expression Language Guide](https://nifi.apache.org/docs/nifi-docs/html/expression-language-guide.html)

## Licencia

Este proyecto utiliza Apache NiFi bajo la licencia Apache 2.0.