CREATE TABLE api_buk_peru.boss (
    id INTEGER,
    id_employees INTEGER,
    id_jobs INTEGER,
    document_type TEXT,
    document_number TEXT,
    timestamp_nifi TIMESTAMPTZ,
    PRIMARY KEY (id, id_jobs)
);

-- Comentarios para documentar la tabla
COMMENT ON TABLE api_buk_peru.boss IS 'Tabla que almacena información de jefes en Buk Perú, incluyendo detalles del empleado y trabajo asociado.';
COMMENT ON COLUMN api_buk_peru.boss.id IS 'ID único del jefe';
COMMENT ON COLUMN api_buk_peru.boss.id_employees IS 'ID del empleado asociado al jefe';
COMMENT ON COLUMN api_buk_peru.boss.id_jobs IS 'ID del trabajo asociado al jefe';
COMMENT ON COLUMN api_buk_peru.boss.document_type IS 'Tipo de documento del jefe (DNI, RUT, etc.)';
COMMENT ON COLUMN api_buk_peru.boss.document_number IS 'Número de documento del jefe';
COMMENT ON COLUMN api_buk_peru.boss.timestamp_nifi IS 'Marca de tiempo que indica cuándo fue procesado el registro por Apache NiFi';