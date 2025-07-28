CREATE TABLE api_buk_chile.boss (
    id INTEGER,
    id_employees INTEGER,
    id_jobs INTEGER,
    rut TEXT,
    document_type TEXT,
    document_number TEXT,
    timestamp_nifi TIMESTAMPTZ,
    PRIMARY KEY (id, id_jobs)
);

-- Definición de la tabla api_buk_chile.boss
COMMENT ON TABLE api_buk_chile.boss IS 'Tabla principal de jefes con información de empleados y trabajos asociados';

