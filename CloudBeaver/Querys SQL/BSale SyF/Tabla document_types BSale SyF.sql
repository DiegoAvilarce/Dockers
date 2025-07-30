CREATE TABLE IF NOT EXISTS api_bsale_syf.document_types (
    id                     INTEGER,
    href                   TEXT,
    name                   TEXT,
    initialNumber          INTEGER,
    codeSii                TEXT,
    isElectronicDocument   INTEGER,
    breakdownTax           INTEGER,
    use                    INTEGER,
    isSalesNote            INTEGER,
    isExempt               INTEGER,
    restrictsTax           INTEGER,
    useClient              INTEGER,
    messageBodyFormat      TEXT,
    thermalPrinter         INTEGER,
    state                  INTEGER,
    copyNumber             INTEGER,
    isCreditNote           INTEGER,
    continuedHigh          INTEGER,
    ledgerAccount          TEXT,
    ipadPrint              INTEGER,
    ipadPrintHigh          INTEGER,
    restrictClientType     INTEGER,
    useMaxDays             INTEGER,
    maxDays                INTEGER,
    book_type              JSONB, -- Referencia al tipo de libro asociado
    timestamp_nifi TIMESTAMPTZ,
    PRIMARY KEY (id)
);

-- Agregar comentarios para explicar los campos de manera breve y profesional
COMMENT ON COLUMN api_bsale_syf.document_types.id IS 'Identificador único del tipo de documento';
COMMENT ON COLUMN api_bsale_syf.document_types.href IS 'Enlace al tipo de documento';
COMMENT ON COLUMN api_bsale_syf.document_types.name IS 'Nombre del tipo de documento';
COMMENT ON COLUMN api_bsale_syf.document_types.initialNumber IS 'Número inicial del tipo de documento';
COMMENT ON COLUMN api_bsale_syf.document_types.codeSii IS 'Código SII del tipo de documento';
COMMENT ON COLUMN api_bsale_syf.document_types.isElectronicDocument IS 'Indica si el documento es electrónico';
COMMENT ON COLUMN api_bsale_syf.document_types.breakdownTax IS 'Indica si el documento desglosa impuestos';
COMMENT ON COLUMN api_bsale_syf.document_types.use IS 'Uso del tipo de documento';
COMMENT ON COLUMN api_bsale_syf.document_types.isSalesNote IS 'Indica si el documento es una nota de venta';
COMMENT ON COLUMN api_bsale_syf.document_types.isExempt IS 'Indica si el documento es exento de impuestos';
COMMENT ON COLUMN api_bsale_syf.document_types.restrictsTax IS 'Indica si el documento restringe impuestos';
COMMENT ON COLUMN api_bsale_syf.document_types.useClient IS 'Indica si el documento utiliza cliente';
COMMENT ON COLUMN api_bsale_syf.document_types.messageBodyFormat IS 'Formato del cuerpo del mensaje del documento';
COMMENT ON COLUMN api_bsale_syf.document_types.thermalPrinter IS 'Indica si el documento se imprime en impresora térmica';
COMMENT ON COLUMN api_bsale_syf.document_types.state IS 'Estado del tipo de documento';
COMMENT ON COLUMN api_bsale_syf.document_types.copyNumber IS 'Número de copias del tipo de documento';
COMMENT ON COLUMN api_bsale_syf.document_types.isCreditNote IS 'Indica si el documento es una nota de crédito';
COMMENT ON COLUMN api_bsale_syf.document_types.continuedHigh IS 'Indica si el documento tiene alta continua';
COMMENT ON COLUMN api_bsale_syf.document_types.ledgerAccount IS 'Cuenta contable asociada al tipo de documento';
COMMENT ON COLUMN api_bsale_syf.document_types.ipadPrint IS 'Indica si el documento se imprime en iPad';
COMMENT ON COLUMN api_bsale_syf.document_types.ipadPrintHigh IS 'Indica si el documento tiene alta de impresión en iPad';
COMMENT ON COLUMN api_bsale_syf.document_types.restrictClientType IS 'Tipo de cliente restringido para el documento';
COMMENT ON COLUMN api_bsale_syf.document_types.useMaxDays IS 'Indica si se utiliza un máximo de días para el documento';
COMMENT ON COLUMN api_bsale_syf.document_types.maxDays IS 'Número máximo de días para el documento';
COMMENT ON COLUMN api_bsale_syf.document_types.book_type IS 'Tipo de libro asociado al documento, almacenado como JSONB';
COMMENT ON COLUMN api_bsale_syf.document_types.timestamp_nifi IS 'Marca de tiempo de la última actualización desde NiFi';