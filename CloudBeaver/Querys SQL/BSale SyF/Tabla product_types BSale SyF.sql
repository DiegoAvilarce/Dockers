CREATE TABLE IF NOT EXISTS api_bsale_syf.product_types (
    id                     INTEGER,
    href                   TEXT,
    name                   TEXT,
    isEditable             INTEGER,
    state                  INTEGER,
    imagestionCategoryId   INTEGER,
    prestashopCategoryId   INTEGER,
    attributes             JSONB, -- Referencia a los atributos del tipo de producto
    timestamp_nifi TIMESTAMPTZ,
    PRIMARY KEY (id)
);

-- Agregar comentarios para explicar los campos de manera breve y profesional
COMMENT ON COLUMN api_bsale_syf.product_types.id IS 'Identificador único del tipo de producto';
COMMENT ON COLUMN api_bsale_syf.product_types.href IS 'Enlace al tipo de producto';
COMMENT ON COLUMN api_bsale_syf.product_types.name IS 'Nombre del tipo de producto';
COMMENT ON COLUMN api_bsale_syf.product_types.isEditable IS 'Indica si el tipo de producto es editable';
COMMENT ON COLUMN api_bsale_syf.product_types.state IS 'Estado del tipo de producto';
COMMENT ON COLUMN api_bsale_syf.product_types.imagestionCategoryId IS 'ID de la categoría en Imagestion asociada al tipo de producto';
COMMENT ON COLUMN api_bsale_syf.product_types.prestashopCategoryId IS 'ID de la categoría en PrestaShop asociada al tipo de producto';
COMMENT ON COLUMN api_bsale_syf.product_types.attributes IS 'Atributos del tipo de producto, almacenados como JSONB';
COMMENT ON COLUMN api_bsale_syf.product_types.timestamp_nifi IS 'Marca de tiempo de la última actualización desde NiFi';
