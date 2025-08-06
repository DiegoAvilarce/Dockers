CREATE TABLE IF NOT EXISTS api_bc_brasil.series (
    seriesId              TEXT,
    dataHoraCotacao       TEXT,
    date_formato          DATE,
    timestamp_formato     TIMESTAMP(3),
    cotacaoCompra         FLOAT,
    cotacaoVenda          FLOAT,
    timestamp_nifi        TIMESTAMPTZ,
    PRIMARY KEY (seriesId, dataHoraCotacao)
);

COMMENT ON COLUMN api_bc_brasil.series.seriesId IS 'Identificador único de la serie';
COMMENT ON COLUMN api_bc_brasil.series.dataHoraCotacao IS 'Fecha y hora de la cotización en formato de cadena';
COMMENT ON COLUMN api_bc_brasil.series.date_formato IS 'Fecha de la cotización en formato DATE seteada desde NiFi';
COMMENT ON COLUMN api_bc_brasil.series.timestamp_formato IS 'Marca de tiempo de la cotización en formato TIMESTAMPTZ';
COMMENT ON COLUMN api_bc_brasil.series.cotacaoCompra IS 'Valor de la cotización de compra';
COMMENT ON COLUMN api_bc_brasil.series.cotacaoVenda IS 'Valor de la cotización de venta';
COMMENT ON COLUMN api_bc_brasil.series.timestamp_nifi IS 'Marca de tiempo de la última actualización desde NiFi';