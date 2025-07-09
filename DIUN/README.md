# DIUN - Docker Image Update Notifier

DIUN (Docker Image Update Notifier) es una herramienta que monitorea automáticamente las actualizaciones de imágenes Docker y envía notificaciones cuando hay nuevas versiones disponibles.

## ¿Qué hace DIUN?

- **Monitoreo automático**: Verifica periódicamente si hay nuevas versiones de las imágenes Docker en uso
- **Notificaciones**: Envía alertas cuando detecta actualizaciones disponibles
- **Integración con Docker**: Se conecta directamente al daemon de Docker para obtener información de los contenedores

## Configuración

### Archivos principales

- `docker-compose.yml`: Configuración del servicio DIUN
- `.env`: Variables de entorno para la configuración

### Variables de entorno importantes

- `DIUN_WATCH_SCHEDULE`: Programación de verificación (formato cron) - actualmente cada 15 minutos
- `DIUN_NOTIF_TEAMS_WEBHOOKURL`: URL del webhook de Microsoft Teams para notificaciones
- `TZ`: Zona horaria configurada (America/Santiago)

### Configuración actual

- **Frecuencia de verificación**: Cada 15 minutos (`*/15 * * * *`)
- **Workers**: 20 procesos paralelos para verificación
- **Jitter**: 30 segundos de variación aleatoria
- **Notificaciones**: Microsoft Teams
- **Monitoreo por defecto**: Habilitado para todos los contenedores Docker

## Uso

### Iniciar el servicio

```bash
docker-compose up -d
```

### Detener el servicio

```bash
docker-compose down
```

### Ver logs

```bash
docker-compose logs -f diun
```

### Verificar estado

```bash
docker-compose ps
```

## Características

- **Detección automática**: Monitorea todos los contenedores Docker por defecto
- **Notificaciones en Teams**: Envía alertas directamente a Microsoft Teams
- **Persistencia**: Los datos se almacenan en el directorio `./data`
- **Zona horaria**: Configurado para Chile (America/Santiago)

## Estructura de archivos

```
DIUN/
├── docker-compose.yml    # Configuración del servicio
├── .env                 # Variables de entorno
├── README.md           # Este archivo
└── data/               # Directorio de datos (creado automáticamente)
```

## Notas importantes

- DIUN requiere acceso al socket de Docker (`/var/run/docker.sock`)
- Las notificaciones se envían a través del webhook configurado de Microsoft Teams
- El servicio se reinicia automáticamente en caso de fallo
- Los datos de configuración se persisten en el directorio local `./data`

## Troubleshooting

### Verificar conexión con Docker
Si DIUN no puede conectarse con Docker, verificar que el socket esté disponible y los permisos sean correctos.

### Problemas con notificaciones
Verificar que la URL del webhook de Teams en el archivo `.env` sea válida y esté funcionando.

### Logs detallados
Para obtener más información sobre el funcionamiento, revisar los logs del contenedor.