# Gitea - Git con sabor propio

![Gitea Logo](https://gitea.io/images/gitea.png)

## Descripción

Gitea es un servicio de Git autoalojado ligero escrito en Go. Proporciona una interfaz web para administrar repositorios Git, usuarios, organizaciones, issues, pull requests y más.

## Características principales

- 🚀 **Ligero y rápido**: Escrito en Go, mínimo uso de recursos
- 🔐 **Autenticación**: Soporte para múltiples métodos de autenticación
- 📊 **Issues y Pull Requests**: Sistema completo de seguimiento de issues
- 👥 **Organizaciones**: Gestión de equipos y organizaciones
- 🔧 **Webhooks**: Integración con servicios externos
- 📱 **API REST**: API completa para integración
- 🐳 **Docker-ready**: Fácil despliegue con Docker

## Configuración

### Variables de entorno

Crea un archivo `.env` en la misma carpeta que el `docker-compose.yml` con las siguientes variables:

```env
# ID de usuario y grupo (usa tu UID/GID del sistema)
USER_UID=1000
USER_GID=1000

# Configuración del dominio
GITEA_DOMAIN=localhost
GITEA_ROOT_URL=http://localhost:3000
GITEA_SSH_DOMAIN=localhost
```

### Para obtener tu UID y GID en Linux/Mac:
```bash
id -u  # UID
id -g  # GID
```

### En Windows con WSL:
```bash
wsl id -u
wsl id -g
```

### Configuración de dominio local (Windows)

Para acceder a Gitea usando un nombre de dominio personalizado en lugar de `localhost`, puedes usar el archivo `setup-host.bat` incluido:

1. **Ejecutar como administrador**: Haz clic derecho en `setup-host.bat` y selecciona "Ejecutar como administrador"
2. **Configuración automática**: El script agregará automáticamente la entrada `127.0.0.1 gitea.local` al archivo hosts de Windows
3. **Acceso**: Después podrás acceder a Gitea en `http://gitea.local:3000`

**Nota**: Recuerda actualizar las variables de entorno para que coincidan con el nuevo dominio:
```env
GITEA_DOMAIN=gitea.local
GITEA_ROOT_URL=http://gitea.local:3000
GITEA_SSH_DOMAIN=gitea.local
```

## Instalación y uso

### 1. Iniciar el servicio

```bash
docker-compose up -d
```

### 2. Acceder a Gitea

- **Interfaz web**: http://localhost:3000
- **SSH**: Puerto 222 (localhost:222)

### 3. Configuración inicial

Al acceder por primera vez, Gitea te pedirá completar la configuración inicial:

1. **Base de datos**: SQLite (por defecto) o configura una externa
2. **Configuración del servidor**: Los valores se tomarán de las variables de entorno
3. **Cuenta de administrador**: Crea la primera cuenta administrativa

### 4. Comandos útiles

```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f gitea

# Detener servicios
docker-compose down

# Reiniciar servicios
docker-compose restart

# Backup de datos
docker-compose exec gitea gitea dump

# Actualizar Gitea
docker-compose pull
docker-compose up -d
```

## Estructura de archivos

```
Gitea/
├── docker-compose.yml          # Configuración de Docker Compose
├── README.md                   # Este archivo
├── .env                        # Variables de entorno (crear)
└── gitea/                      # Datos persistentes
    ├── git/                    # Repositorios Git
    ├── gitea/                  # Base de datos y configuración
    └── ssh/                    # Claves SSH del servidor
```

## Configuración avanzada

### SSH

Los repositorios están disponibles vía SSH en el puerto 222:

```bash
# Clonar un repositorio
git clone ssh://git@localhost:222/usuario/repositorio.git

# Configurar SSH para el puerto personalizado
# Agregar a ~/.ssh/config:
Host gitea
    HostName localhost
    Port 222
    User git
```

### Configuración personalizada

Puedes modificar la configuración editando el archivo:
```
./gitea/gitea/conf/app.ini
```

Después de modificar la configuración, reinicia el contenedor:
```bash
docker-compose restart gitea
```

## Backup y restauración

### Crear backup

```bash
# Backup completo
docker-compose exec gitea gitea dump

# El archivo se guardará en ./gitea/
```

### Restaurar backup

```bash
# Detener el servicio
docker-compose down

# Restaurar desde backup
docker-compose run --rm gitea gitea restore --from /data/gitea-dump-xxxxxxxxx.zip

# Reiniciar el servicio
docker-compose up -d
```

## Solución de problemas

### Permisos

Si tienes problemas de permisos, asegúrate de que las variables `USER_UID` y `USER_GID` coincidan con tu usuario del sistema.

### Puerto ocupado

Si el puerto 3000 está ocupado, modifica el mapeo en `docker-compose.yml`:
```yaml
ports:
  - "3001:3000"  # Cambiar puerto externo
  - "222:22"
```

### Logs

Para ver los logs detallados:
```bash
docker-compose logs -f gitea
```

## Recursos adicionales

- [Documentación oficial de Gitea](https://docs.gitea.io/)
- [GitHub del proyecto](https://github.com/go-gitea/gitea)
- [Comunidad Gitea](https://discourse.gitea.io/)

## Licencia

Gitea está licenciado bajo MIT License.

---

**Nota**: Este setup está optimizado para desarrollo local. Para producción, considera configurar HTTPS, base de datos externa y otras medidas de seguridad.