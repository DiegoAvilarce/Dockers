# Guía Paso a Paso: Actualización NiFi 2.4.0 a 2.5.0

## PASO 1: Ubicarte en la carpeta correcta

### 1.1 Abrir terminal y navegar al directorio
```bash
# Navegar a tu carpeta específica de NiFi
cd "/home/qsenseadmin/Dockers/Apache NiFi"
```

### 1.2 Verificar que estás en el lugar correcto
```bash
# Verificar que el archivo docker-compose.yml existe
ls -la docker-compose.yml

# Verificar el estado actual de NiFi
docker-compose ps
```

## PASO 2: Crear backup completo

### 2.1 Crear directorio de backup
```bash
# Crear directorio con fecha actual
BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p ./backup_nifi_$BACKUP_DATE
echo "Backup se guardará en: backup_nifi_$BACKUP_DATE"
```

### 2.2 Parar NiFi para backup consistente
```bash
# Parar el contenedor de NiFi
docker-compose down

# Verificar que se detuvo
docker-compose ps
```

### 2.3 Backup de carpetas locales
```bash
# Respaldar carpeta nifi local (si existe)
if [ -d "./nifi" ]; then
    cp -r ./nifi ./backup_nifi_$BACKUP_DATE/nifi_local
    echo "✓ Carpetas locales respaldadas"
else
    echo "No hay carpeta ./nifi para respaldar"
fi

# Backup del docker-compose.yml
cp docker-compose.yml ./backup_nifi_$BACKUP_DATE/docker-compose.yml.backup
```

### 2.4 Backup de volúmenes Docker (MUY IMPORTANTE)
```bash
# Respaldar configuración de NiFi (flujos, settings, etc.)
docker run --rm \
    -v nifi-conf:/source:ro \
    -v $(pwd)/backup_nifi_$BACKUP_DATE:/backup \
    alpine tar czf /backup/nifi-conf.tar.gz -C /source .

# Respaldar repositorio de contenido
docker run --rm \
    -v nifi-content_repository:/source:ro \
    -v $(pwd)/backup_nifi_$BACKUP_DATE:/backup \
    alpine tar czf /backup/nifi-content_repository.tar.gz -C /source .

# Respaldar base de datos interna
docker run --rm \
    -v nifi-database_repository:/source:ro \
    -v $(pwd)/backup_nifi_$BACKUP_DATE:/backup \
    alpine tar czf /backup/nifi-database_repository.tar.gz -C /source .

# Respaldar repositorio de flowfiles
docker run --rm \
    -v nifi-flowfile_repository:/source:ro \
    -v $(pwd)/backup_nifi_$BACKUP_DATE:/backup \
    alpine tar czf /backup/nifi-flowfile_repository.tar.gz -C /source .

# Respaldar estado de procesadores
docker run --rm \
    -v nifi-state:/source:ro \
    -v $(pwd)/backup_nifi_$BACKUP_DATE:/backup \
    alpine tar czf /backup/nifi-state.tar.gz -C /source .
```

### 2.5 Verificar backup
```bash
# Ver contenido del backup
ls -la ./backup_nifi_$BACKUP_DATE/

# Ver tamaño del backup
du -sh ./backup_nifi_$BACKUP_DATE/
```

## PASO 3: Actualizar docker-compose.yml

### 3.1 Editar el archivo
```bash
# Opción 1: Usar nano
nano docker-compose.yml

# Opción 2: Usar vim
vim docker-compose.yml

# Opción 3: Usar tu editor preferido
```

### 3.2 Cambio a realizar
**BUSCAR esta línea:**
```yaml
image: apache/nifi:latest
```

**CAMBIAR por:**
```yaml
image: apache/nifi:2.5.0
```

### 3.3 Guardar el archivo
- **En nano**: `Ctrl+X`, luego `Y`, luego `Enter`
- **En vim**: `Esc`, luego `:wq`, luego `Enter`

## PASO 4: Descargar nueva imagen

### 4.1 Descargar imagen NiFi 2.5.0
```bash
# Descargar la nueva imagen
docker pull apache/nifi:2.5.0

# Verificar que se descargó
docker images | grep nifi
```

### 4.2 Limpiar imagen anterior (opcional)
```bash
# Eliminar imagen anterior para liberar espacio
docker image rm apache/nifi:latest
```

## PASO 5: Iniciar NiFi con nueva versión

### 5.1 Iniciar contenedor
```bash
# Iniciar NiFi con la nueva configuración
docker-compose up -d

# Ver el estado
docker-compose ps
```

### 5.2 Monitorear inicio
```bash
# Ver logs para asegurar que inicie correctamente
docker-compose logs -f nifi

# Presiona Ctrl+C para salir de los logs cuando veas que inició correctamente
```

### 5.3 Esperar a que inicie completamente
```bash
# NiFi puede tardar 2-5 minutos en estar completamente disponible
# Puedes verificar el estado con:
docker-compose logs nifi | grep "NiFi has started"
```

## PASO 6: Verificar la actualización

### 6.1 Acceder a la interfaz web
- Abrir navegador en: `https://tu-servidor-ip:8443/nifi`
- O si es local: `https://localhost:8443/nifi`

### 6.2 Verificar versión
- En la esquina inferior derecha de la interfaz web debería aparecer "2.5.0"

### 6.3 Verificar flujos
- Revisar que todos tus flujos de trabajo están presentes
- Verificar que los procesadores funcionan correctamente

## PASO 7: Limpieza (opcional)

### 7.1 Si todo funciona correctamente
```bash
# Después de confirmar que todo funciona (esperar al menos 24h)
# Puedes eliminar el backup si quieres
# rm -rf ./backup_nifi_$BACKUP_DATE
```

## PASO 8: En caso de problemas (rollback)

### 8.1 Si algo falla, volver a la versión anterior
```bash
# Parar NiFi
docker-compose down

# Cambiar imagen de vuelta en docker-compose.yml
nano docker-compose.yml
# Cambiar: image: apache/nifi:2.5.0
# Por: image: apache/nifi:2.4.0

# Restaurar configuración si es necesario
cp ./backup_nifi_$BACKUP_DATE/docker-compose.yml.backup docker-compose.yml

# Reiniciar
docker-compose up -d
```

## Comandos de verificación útiles

```bash
# Ver estado de contenedores
docker-compose ps

# Ver logs de NiFi
docker-compose logs nifi

# Ver versión de imagen actual
docker inspect nifi | grep Image

# Ver volúmenes de NiFi
docker volume ls | grep nifi

# Ver uso de recursos
docker stats nifi
```

## Notas importantes:

1. **Tiempo**: El proceso completo puede tardar 15-30 minutos
2. **Backup**: NO elimines el backup hasta estar seguro de que todo funciona
3. **Acceso web**: NiFi tardará unos minutos en estar disponible después del inicio
4. **Credenciales**: Mantiene las mismas credenciales que configuraste