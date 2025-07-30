CREATE TABLE api_buk_chile.overtime_types (
    id INTEGER,
    name TEXT,
    proporcion FLOAT,
    category INTEGER,
    timestamp_nifi TIMESTAMPTZ,
    PRIMARY KEY (id)
);

-- Comentarios para documentar la tabla
COMMENT ON TABLE api_buk_chile.overtime_types IS 'Tabla de tipos de horas extras con información de proporción y categoría';
COMMENT ON COLUMN api_buk_chile.overtime_types.id IS 'Primary Key con ID único del tipo de hora extra';
COMMENT ON COLUMN api_buk_chile.overtime_types.name IS 'Nombre del tipo de hora extra';
COMMENT ON COLUMN api_buk_chile.overtime_types.proporcion IS 'Proporción del tipo de hora extra';
COMMENT ON COLUMN api_buk_chile.overtime_types.category IS 'Categoría del tipo de hora extra';
COMMENT ON COLUMN api_buk_chile.overtime_types.timestamp_nifi IS 'Marca de tiempo de la hora extra procesada por NiFi';