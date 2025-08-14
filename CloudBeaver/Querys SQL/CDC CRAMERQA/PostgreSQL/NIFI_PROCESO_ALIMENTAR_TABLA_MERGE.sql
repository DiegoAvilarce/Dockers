-- Función wrapper para procesar merges (arrays de arrays)
CREATE OR REPLACE FUNCTION LANDING_CRAMERQA.NIFI_PROCESO_ALIMENTAR_TABLA_MERGE(
    json_data_merge JSONB,
    target_table TEXT,
    excluded_fields TEXT[] DEFAULT ARRAY['op', 'tipo', 'ts_ms', 'kafka_offset', 'uuid_nifi']::TEXT[]
) 
RETURNS VOID AS $$
DECLARE
    single_change JSONB;
    change_count INTEGER := 0;
    processed_count INTEGER := 0;
    error_count INTEGER := 0;
BEGIN
    -- Verificar si el JSON es un array de arrays (merge) o un array simple
    IF jsonb_typeof(json_data_merge) = 'array' THEN
        -- Contar total de cambios
        SELECT jsonb_array_length(json_data_merge) INTO change_count;
        
        RAISE NOTICE 'Procesando merge con % cambios', change_count;
        
        -- Iterar sobre cada elemento del merge
        FOR i IN 0..(change_count - 1) LOOP
            BEGIN
                single_change := json_data_merge -> i;
                
                -- Verificar si el elemento es un array (cambio individual) o un objeto
                IF jsonb_typeof(single_change) = 'array' THEN
                    -- Es un cambio individual (array con before/after)
                    RAISE NOTICE 'Procesando cambio %/%', (i + 1), change_count;
                    
                    -- Llamar a la función original
                    PERFORM LANDING_CRAMERQA.NIFI_PROCESO_ALIMENTAR_TABLA_REGISTRO(
                        single_change,
                        target_table,
                        excluded_fields
                    );
                    
                    processed_count := processed_count + 1;
                    
                ELSE
                    -- Es un objeto individual, envolver en array y procesar
                    RAISE NOTICE 'Procesando objeto individual %/%', (i + 1), change_count;
                    
                    PERFORM LANDING_CRAMERQA.NIFI_PROCESO_ALIMENTAR_TABLA_REGISTRO(
                        jsonb_build_array(single_change),
                        target_table,
                        excluded_fields
                    );
                    
                    processed_count := processed_count + 1;
                END IF;
                
            EXCEPTION WHEN others THEN
                error_count := error_count + 1;
                RAISE WARNING 'Error procesando cambio %/%: %', (i + 1), change_count, SQLERRM;
                -- Continuar con el siguiente cambio
            END;
        END LOOP;
        
        RAISE NOTICE 'Merge completado: % procesados exitosamente, % errores', processed_count, error_count;
        
    ELSE
        -- No es un array, probablemente un objeto individual
        RAISE NOTICE 'Datos no son array, procesando como cambio individual';
        
        PERFORM LANDING_CRAMERQA.NIFI_PROCESO_ALIMENTAR_TABLA_REGISTRO(
            jsonb_build_array(json_data_merge),
            target_table,
            excluded_fields
        );
    END IF;
    
EXCEPTION WHEN others THEN
    RAISE EXCEPTION 'Error fatal en procesamiento de merge: %', SQLERRM;
END;

$$ LANGUAGE plpgsql;