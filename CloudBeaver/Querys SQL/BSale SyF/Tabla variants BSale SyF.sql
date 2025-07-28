CREATE TABLE IF NOT EXISTS api_bsale_syf.variants (
    id                     INTEGER,
    href                   TEXT,
    description            TEXT,
    unlimitedStock         INTEGER,
    allowNegativeStock     INTEGER,
    state                  INTEGER,
    barCode                TEXT,
    code                   TEXT,
    imagestionCenterCost   INTEGER,
    imagestionAccount      INTEGER,
    imagestionConceptCod   INTEGER,
    imagestionProyectCod   INTEGER,
    imagestionCategoryCod  INTEGER,
    imagestionProductId    INTEGER,
    serialNumber           INTEGER,
    isLot                  INTEGER,
    prestashopCombinationId INTEGER,
    prestashopValueId      INTEGER,
    product                JSONB, -- Referencia al producto
    attribute_values       JSONB, -- Valores de los atributos
    costs                  JSONB, -- Costos asociados a la variante
    discounts              JSONB, -- Descuentos asociados a la variante
    prices                 JSONB, -- Precios asociados a la variante
    timestamp_nifi TIMESTAMPTZ,
    PRIMARY KEY (id)
);

-- Agregar comentarios para explicar los campos de manera breve y profesional
COMMENT ON COLUMN api_bsale_syf.variants.id IS 'Identificador único de la variante';
COMMENT ON COLUMN api_bsale_syf.variants.href IS 'Enlace a la variante';
COMMENT ON COLUMN api_bsale_syf.variants.description IS 'Descripción de la variante';
COMMENT ON COLUMN api_bsale_syf.variants.unlimitedStock IS 'Indica si la variante tiene stock ilimitado';
COMMENT ON COLUMN api_bsale_syf.variants.allowNegativeStock IS 'Indica si se permite stock negativo para la variante';
COMMENT ON COLUMN api_bsale_syf.variants.state IS 'Estado de la variante';
COMMENT ON COLUMN api_bsale_syf.variants.barCode IS 'Código de barras de la variante';
COMMENT ON COLUMN api_bsale_syf.variants.code IS 'Código de la variante';
COMMENT ON COLUMN api_bsale_syf.variants.imagestionCenterCost IS 'Centro de costos asociado a la variante en el sistema de gestión';
COMMENT ON COLUMN api_bsale_syf.variants.imagestionAccount IS 'Cuenta contable asociada a la variante en el sistema de gestión';
COMMENT ON COLUMN api_bsale_syf.variants.imagestionConceptCod IS 'Código del concepto asociado a la variante en el sistema de gestión';
COMMENT ON COLUMN api_bsale_syf.variants.imagestionProyectCod IS 'Código del proyecto asociado a la variante en el sistema de gestión';
COMMENT ON COLUMN api_bsale_syf.variants.imagestionCategoryCod IS 'Código de la categoría asociada a la variante en el sistema de gestión';
COMMENT ON COLUMN api_bsale_syf.variants.imagestionProductId IS 'ID del producto asociado a la variante en el sistema de gestión';
COMMENT ON COLUMN api_bsale_syf.variants.serialNumber IS 'Número de serie de la variante';
COMMENT ON COLUMN api_bsale_syf.variants.isLot IS 'Indica si la variante es un lote';
COMMENT ON COLUMN api_bsale_syf.variants.prestashopCombinationId IS 'ID de la combinación de PrestaShop asociada a la variante';
COMMENT ON COLUMN api_bsale_syf.variants.prestashopValueId IS 'ID del valor de PrestaShop asociado a la variante';
COMMENT ON COLUMN api_bsale_syf.variants.product IS 'Referencia al producto al que pertenece la variante, almacenada como JSONB';
COMMENT ON COLUMN api_bsale_syf.variants.attribute_values IS 'Valores de los atributos asociados a la variante, almacenados como JSONB';
COMMENT ON COLUMN api_bsale_syf.variants.costs IS 'Costos asociados a la variante, almacenados como JSONB';
COMMENT ON COLUMN api_bsale_syf.variants.discounts IS 'Descuentos asociados a la variante, almacenados como JSONB';
COMMENT ON COLUMN api_bsale_syf.variants.prices IS 'Precios asociados a la variante, almacenados como JSONB';
COMMENT ON COLUMN api_bsale_syf.variants.timestamp_nifi IS 'Marca de tiempo de la última actualización desde NiFi';

