CREATE TABLE api_buk_chile.process_periods (
    id INTEGER,
    month DATE,
    end_date DATE,
    status TEXT,
    timestamp_nifi TIMESTAMPTZ,
    PRIMARY KEY (id)
);

-- Comentarios para documentar la tabla
COMMENT ON TABLE api_buk_chile.process_periods IS 'Tabla de períodos de procesamiento con información de mes, fecha de finalización y estado';
COMMENT ON COLUMN api_buk_chile.process_periods.id IS 'Primary Key con ID único del período de procesamiento';
COMMENT ON COLUMN api_buk_chile.process_periods.month IS 'Mes del período de procesamiento';
COMMENT ON COLUMN api_buk_chile.process_periods.end_date IS 'Fecha de finalización del período de procesamiento';
COMMENT ON COLUMN api_buk_chile.process_periods.status IS 'Estado del período de procesamiento';
COMMENT ON COLUMN api_buk_chile.process_periods.timestamp_nifi IS 'Marca de tiempo del período de procesamiento procesado por NiFi';
