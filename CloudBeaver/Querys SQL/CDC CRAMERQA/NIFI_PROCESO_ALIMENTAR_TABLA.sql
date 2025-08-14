CREATE OR REPLACE FUNCTION LANDING_CRAMERQA.NIFI_PROCESO_ALIMENTAR_TABLA(
    json_data JSONB,
    target_table TEXT,  -- nombre de la tabla destino
    excluded_fields TEXT[] DEFAULT ARRAY['op', 'tipo', 'ts_ms', 'kafka_offset', 'uuid_nifi']::TEXT[]
) 
RETURNS VOID AS $$
DECLARE
    before_data_original JSONB;
    after_data_original  JSONB;
    before_data_filtered JSONB;
    after_data_filtered  JSONB;
    valid_columns TEXT[];
    date_columns  TEXT[];
    operation     TEXT;
    sql_stmt      TEXT;
    field         TEXT;
BEGIN

    -- Normalizar todas las keys del JSON a minúsculas
    json_data := (
      SELECT jsonb_agg(lowercase_keys.elem)
      FROM jsonb_array_elements(json_data) elem
      CROSS JOIN LATERAL (
        SELECT jsonb_object_agg(lower(key), value) AS elem
        FROM jsonb_each(elem)
      ) lowercase_keys
    );

    ------------------------------------------------------------
    -- Extraer datos originales con todos los campos
    ------------------------------------------------------------
    SELECT elem
    INTO before_data_original
    FROM jsonb_array_elements(json_data) elem
    WHERE elem->>'tipo' = 'before'
    LIMIT 1;

    SELECT elem
    INTO after_data_original
    FROM jsonb_array_elements(json_data) elem
    WHERE elem->>'tipo' = 'after'
    LIMIT 1;

    -- Si no hay registro 'before' pero sí 'after', usar 'after' para before_data_original
    IF before_data_original IS NULL AND after_data_original IS NOT NULL THEN
        before_data_original := after_data_original;
    END IF;
    
    -- Si no hay registro 'after' pero sí 'before', usar 'before' para after_data_original  
    IF after_data_original IS NULL AND before_data_original IS NOT NULL THEN
        after_data_original := before_data_original;
    END IF;

    ------------------------------------------------------------
    -- Consultar columnas válidas de la tabla destino
    ------------------------------------------------------------
    EXECUTE format(
        'SELECT array_agg(column_name)::text[] 
         FROM information_schema.columns 
         WHERE table_schema = %L AND table_name = %L',
         split_part(target_table, '.', 1),  -- schema
         split_part(target_table, '.', 2)   -- table
    ) INTO valid_columns;

    ------------------------------------------------------------
    -- Consultar columnas que sean de tipo fecha/timestamp
    ------------------------------------------------------------
    EXECUTE format(
        'SELECT array_agg(column_name)::text[] 
         FROM information_schema.columns 
         WHERE table_schema = lower(%L) 
           AND table_name = lower(%L) 
           AND data_type IN (''timestamp without time zone'', 
                             ''timestamp with time zone'', 
                             ''date'')',
        split_part(target_table, '.', 1),
        split_part(target_table, '.', 2)
    ) INTO date_columns;

    ------------------------------------------------------------
    -- Filtrar JSON para solo incluir columnas existentes
    ------------------------------------------------------------
    after_data_original := after_data_original - ARRAY(
        SELECT key 
        FROM jsonb_object_keys(after_data_original) key
        WHERE key <> ALL(valid_columns)
    );

    before_data_original := before_data_original - ARRAY(
        SELECT key 
        FROM jsonb_object_keys(before_data_original) key
        WHERE key <> ALL(valid_columns)
    );

    ------------------------------------------------------------
    -- Convertir epoch ms a timestamp para columnas de fecha
    ------------------------------------------------------------
    FOREACH field IN ARRAY date_columns LOOP
        IF (after_data_original ? field) THEN
            BEGIN
                after_data_original := jsonb_set(
                    after_data_original,
                    ARRAY[field],
                    to_jsonb(to_timestamp((after_data_original->>field)::bigint::double precision / 1000))
                );
            EXCEPTION WHEN others THEN
                -- Ignorar si no es numérico
            END;
        END IF;

        IF (before_data_original ? field) THEN
            BEGIN
                before_data_original := jsonb_set(
                    before_data_original,
                    ARRAY[field],
                    to_jsonb(to_timestamp((before_data_original->>field)::bigint::double precision / 1000))
                );
            EXCEPTION WHEN others THEN
                -- Ignorar si no es numérico
            END;
        END IF;
    END LOOP;

    ------------------------------------------------------------
    -- Crear versiones filtradas para WHERE
    ------------------------------------------------------------
    before_data_filtered := before_data_original;
    after_data_filtered  := after_data_original;

    FOREACH field IN ARRAY excluded_fields LOOP
        before_data_filtered := before_data_filtered - field;
        after_data_filtered  := after_data_filtered - field;
    END LOOP;

    ------------------------------------------------------------
    -- Determinar operación
    ------------------------------------------------------------
    operation := COALESCE((json_data -> 0)->>'op', after_data_original->>'op');

    CASE operation
        WHEN 'c', 'r' THEN
            -- INSERT dinámico
            EXECUTE format(
                'INSERT INTO %s SELECT * FROM jsonb_populate_record(NULL::%s, $1)',
                target_table,
                target_table
            ) USING after_data_original;

        WHEN 'u' THEN
            -- UPDATE dinámico
            DECLARE
                set_clause TEXT := '';
                where_clause TEXT := '';
                key TEXT;
                value JSONB;
            BEGIN
                -- Construir SET clause
                FOR key, value IN SELECT * FROM jsonb_each(after_data_original) LOOP
                    IF set_clause != '' THEN
                        set_clause := set_clause || ', ';
                    END IF;
                    
                    IF value = 'null'::jsonb THEN
                        set_clause := set_clause || format('%I = NULL', key);
                    ELSE
                        set_clause := set_clause || format('%I = %L', key, value #>> '{}');
                    END IF;
                END LOOP;
                
                -- Construir WHERE clause
                FOR key, value IN SELECT * FROM jsonb_each(before_data_filtered) LOOP
                    IF where_clause != '' THEN
                        where_clause := where_clause || ' AND ';
                    END IF;
                    
                    IF value = 'null'::jsonb THEN
                        where_clause := where_clause || format('%I IS NULL', key);
                    ELSE
                        where_clause := where_clause || format('%I = %L', key, value #>> '{}');
                    END IF;
                END LOOP;
                
                sql_stmt := format('UPDATE %s SET %s WHERE %s', target_table, set_clause, where_clause);
                
                RAISE NOTICE 'UPDATE SQL: %', sql_stmt;
                
                EXECUTE sql_stmt;
            END;

        WHEN 'd' THEN
            -- DELETE dinámico
            DECLARE
                where_clause TEXT := '';
                key TEXT;
                value JSONB;
            BEGIN
                -- Construir WHERE clause
                FOR key, value IN SELECT * FROM jsonb_each(before_data_filtered) LOOP
                    IF where_clause != '' THEN
                        where_clause := where_clause || ' AND ';
                    END IF;
                    
                    IF value = 'null'::jsonb THEN
                        where_clause := where_clause || format('%I IS NULL', key);
                    ELSE
                        where_clause := where_clause || format('%I = %L', key, value #>> '{}');
                    END IF;
                END LOOP;
                
                sql_stmt := format('DELETE FROM %s WHERE %s', target_table, where_clause);
                
                RAISE NOTICE 'DELETE SQL: %', sql_stmt;
                
                EXECUTE sql_stmt;
            END;
    END CASE;

END;
$$ LANGUAGE plpgsql;