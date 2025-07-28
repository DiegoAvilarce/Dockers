
CREATE TABLE IF NOT EXISTS api_bsale_syf.products (
    id                     INTEGER,
    href                   TEXT,
    name                   TEXT,
    description            TEXT,
    classification         INTEGER,
    ledgerAccount          TEXT,
    costCenter             TEXT,
    allowDecimal           INTEGER,
    stockControl           INTEGER,
    printDetailPack        INTEGER,
    state                  INTEGER,
    prestashopProductId    INTEGER,
    presashopAttributeId   INTEGER,
    product_type           JSONB, -- Referencia al tipo de producto
    variants               JSONB, -- Variantes del producto
    product_taxes          JSONB,  -- Impuestos asociados al producto,
    timestamp_nifi TIMESTAMPTZ,
    PRIMARY KEY (id)
);

-- Agregar comentarios para explicar los campos de manera breve y profesional
COMMENT ON COLUMN api_bsale_syf.products.id IS 'Identificador único del producto';
COMMENT ON COLUMN api_bsale_syf.products.href IS 'Enlace al producto';
COMMENT ON COLUMN api_bsale_syf.products.name IS 'Nombre del producto';
COMMENT ON COLUMN api_bsale_syf.products.description IS 'Descripción del producto';
COMMENT ON COLUMN api_bsale_syf.products.classification IS 'Clasificación del producto';
COMMENT ON COLUMN api_bsale_syf.products.ledgerAccount IS 'Cuenta contable asociada al producto';
COMMENT ON COLUMN api_bsale_syf.products.costCenter IS 'Centro de costos asociado al producto';
COMMENT ON COLUMN api_bsale_syf.products.allowDecimal IS 'Indica si el producto permite decimales';
COMMENT ON COLUMN api_bsale_syf.products.stockControl IS 'Indica si se controla el stock del producto';
COMMENT ON COLUMN api_bsale_syf.products.printDetailPack IS 'Indica si se imprime el detalle del paquete del producto';
COMMENT ON COLUMN api_bsale_syf.products.state IS 'Estado del producto';
COMMENT ON COLUMN api_bsale_syf.products.prestashopProductId IS 'ID del producto en PrestaShop';
COMMENT ON COLUMN api_bsale_syf.products.presashopAttributeId IS 'ID del atributo del producto en PrestaShop';
COMMENT ON COLUMN api_bsale_syf.products.product_type IS 'Tipo de producto, almacenado como JSONB';
COMMENT ON COLUMN api_bsale_syf.products.variants IS 'Variantes del producto, almacenadas como JSONB';
COMMENT ON COLUMN api_bsale_syf.products.product_taxes IS 'Impuestos asociados al producto, almacenados como JSONB';
COMMENT ON COLUMN api_bsale_syf.products.timestamp_nifi IS 'Marca de tiempo de la última actualización desde NiFi'; 