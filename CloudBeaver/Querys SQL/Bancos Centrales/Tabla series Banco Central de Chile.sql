CREATE TABLE IF NOT EXISTS api_bc_chile.series (
    seriesId              TEXT,
    descripIng            TEXT,
    descripEsp            TEXT,
    indexDateString       TEXT,
    date_formato          DATE,
    value                 NUMERIC(10, 3),
    statusCode            TEXT,
    timestamp_nifi        TIMESTAMPTZ,
    PRIMARY KEY (seriesId, indexDateString)
);

COMMENT ON COLUMN api_bc_chile.series.seriesId IS 'Identificador único de la serie';
COMMENT ON COLUMN api_bc_chile.series.descripIng IS 'Descripción de la serie en inglés';
COMMENT ON COLUMN api_bc_chile.series.descripEsp IS 'Descripción de la serie en español';
COMMENT ON COLUMN api_bc_chile.series.indexDateString IS 'Fecha del indice en formato de cadena';
COMMENT ON COLUMN api_bc_chile.series.date_formato IS 'Fecha del índice en formato DATE seteada desde NiFi';
COMMENT ON COLUMN api_bc_chile.series.value IS 'Valor de la serie';
COMMENT ON COLUMN api_bc_chile.series.statusCode IS 'Código de estado de la serie';
COMMENT ON COLUMN api_bc_chile.series.timestamp_nifi IS 'Marca de tiempo de la última actualización desde NiFi';