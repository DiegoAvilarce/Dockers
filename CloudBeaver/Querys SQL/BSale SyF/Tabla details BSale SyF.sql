CREATE TABLE api_bsale_syf.details (
    id                     INTEGER,
    id_documents          INTEGER, -- ID del documento al que pertenece el detalle
    href                   TEXT,
    lineNumber             INTEGER,
    quantity               NUMERIC,
    netUnitValue           INTEGER,
    netUnitValueRaw        NUMERIC,
    totalUnitValue         INTEGER,
    netAmount              INTEGER,
    taxAmount              INTEGER,
    totalAmount            INTEGER,
    netDiscount            INTEGER,
    totalDiscount          INTEGER,
    variant                JSONB, -- Variantes del producto
    note                   TEXT,
    relatedDetailId        INTEGER, -- ID del detalle relacionado
    timestamp_nifi TIMESTAMPTZ,
    PRIMARY KEY (id)
);

COMMENT ON COLUMN api_bsale_syf.details.id IS 'Identificador único del detalle';
COMMENT ON COLUMN api_bsale_syf.details.id_documents IS 'ID del documento al que pertenece el detalle';
COMMENT ON COLUMN api_bsale_syf.details.href IS 'Enlace al detalle';
COMMENT ON COLUMN api_bsale_syf.details.lineNumber IS 'Número de línea del detalle';
COMMENT ON COLUMN api_bsale_syf.details.quantity IS 'Cantidad del producto en el detalle';
COMMENT ON COLUMN api_bsale_syf.details.netUnitValue IS 'Valor neto unitario del producto';
COMMENT ON COLUMN api_bsale_syf.details.netUnitValueRaw IS 'Valor neto unitario del producto sin redondear';
COMMENT ON COLUMN api_bsale_syf.details.totalUnitValue IS 'Valor total unitario del producto';
COMMENT ON COLUMN api_bsale_syf.details.netAmount IS 'Monto neto del detalle';
COMMENT ON COLUMN api_bsale_syf.details.taxAmount IS 'Monto del impuesto aplicado al detalle';
COMMENT ON COLUMN api_bsale_syf.details.totalAmount IS 'Monto total del detalle';
COMMENT ON COLUMN api_bsale_syf.details.netDiscount IS 'Descuento neto aplicado al detalle';
COMMENT ON COLUMN api_bsale_syf.details.totalDiscount IS 'Descuento total aplicado al detalle';
COMMENT ON COLUMN api_bsale_syf.details.variant IS 'Variantes del producto, almacenadas como JSONB';
COMMENT ON COLUMN api_bsale_syf.details.note IS 'Nota adicional del detalle';
COMMENT ON COLUMN api_bsale_syf.details.relatedDetailId IS 'ID del detalle relacionado, si aplica';
COMMENT ON COLUMN api_bsale_syf.details.timestamp_nifi IS 'Marca de tiempo de la última actualización desde NiFi';
COMMENT ON TABLE api_bsale_syf.details IS 'Tabla que almacena los detalles de los documentos de BSale SyF';