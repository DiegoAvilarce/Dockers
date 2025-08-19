CREATE OR REPLACE PROCEDURE LANDING.PUBLIC.CREATE_TARGET_FROM_CDC(
  TABLA_CDC STRING,
  TABLA_TARGET STRING,
  DATABASE_CDC STRING,
  SCHEMA_CDC STRING,
  DATABASE_TARGET STRING,
  SCHEMA_TARGET STRING
)
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
  sql_insert STRING;
  full_cdc_table STRING;
  full_target_table STRING;
  rows_processed NUMBER DEFAULT 0;
BEGIN
  -- Construir nombres completos
  full_cdc_table := DATABASE_CDC || '.' || SCHEMA_CDC || '.' || TABLA_CDC;
  full_target_table := DATABASE_TARGET || '.' || SCHEMA_TARGET || '.' || TABLA_TARGET;
  
  -- INSERT ordenado por kafka_offset
  sql_insert := 
    'INSERT INTO ' || full_target_table || ' ' ||
    'SELECT * EXCLUDE (procesado) ' ||
    'FROM ' || full_cdc_table || ' ' ||
    'WHERE op IN (''r'', ''c'') AND (procesado = FALSE OR procesado IS NULL) ' ||
    'ORDER BY tipo DESC,ts_ms DESC, kafka_offset asc';
  
  EXECUTE IMMEDIATE sql_insert;
  rows_processed := SQLROWCOUNT;
  
  -- Marcar como procesados
  EXECUTE IMMEDIATE 
    'UPDATE ' || full_cdc_table || ' ' ||
    'SET procesado = TRUE ' ||
    'WHERE op IN (''r'', ''c'') AND (procesado = FALSE OR procesado IS NULL)';
  
  RETURN 'Procesados ' || rows_processed || ' registros de ' || full_cdc_table || ' hacia ' || full_target_table;
END;
$$;
