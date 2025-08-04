CREATE TABLE IF NOT EXISTS api_bc_peru.series (
    seriesId              TEXT,
    title                 TEXT,
    descripEsp            TEXT,
    name_date             TEXT,
    date_formato          DATE,
    values                FLOAT,
    timestamp_nifi        TIMESTAMPTZ,
    PRIMARY KEY (seriesId, name_date)
);

COMMENT ON COLUMN api_bc_peru.series.seriesId IS 'Identificador único de la serie';
COMMENT ON COLUMN api_bc_peru.series.title IS 'Título de la serie';
COMMENT ON COLUMN api_bc_peru.series.descripEsp IS 'Descripción de la serie en español';
COMMENT ON COLUMN api_bc_peru.series.name_date IS 'Fecha del índice en formato de cadena';
COMMENT ON COLUMN api_bc_peru.series.date_formato IS 'Fecha del índice en formato DATE seteada desde NiFi';
COMMENT ON COLUMN api_bc_peru.series.values IS 'Valor de la serie';
COMMENT ON COLUMN api_bc_peru.series.timestamp_nifi IS 'Marca de tiempo de la última actualización desde NiFi';