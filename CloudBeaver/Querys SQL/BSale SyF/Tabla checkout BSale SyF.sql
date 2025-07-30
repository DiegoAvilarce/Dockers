CREATE TABLE api_bsale_syf.checkout (
    id                     INTEGER,
    token                  TEXT,
    clientName             TEXT,
    clientLastName         TEXT,
    clientEmail            TEXT,
    clientPhone            TEXT,
    id_tipo_documento_tributario INTEGER,
    dynamicAttributes      JSONB,
    extrasUserData        JSONB, -- Datos adicionales del usuario
    clientStreet           TEXT,
    clientCityZone         TEXT,
    clientPostcode         TEXT,
    cartId                 INTEGER,
    cartDetails            TEXT, 
    createAt               BIGINT,
    shippingCost           NUMERIC,
    isMafs                 BOOLEAN,
    discountCost           NUMERIC,
    active                 BOOLEAN,
    shippingComment        TEXT,
    totalCart              NUMERIC,
    pickStoreId            INTEGER,
    pickName               TEXT,
    pickCode               TEXT,
    id_venta_documento_tributario INTEGER,
    documentNumber         INTEGER,
    documentToken          TEXT,
    storeId                INTEGER,
    storeName              TEXT,
    marketId               INTEGER,
    isService              BOOLEAN,
    withdrawStore          BOOLEAN,
    payProcess             TEXT, -- Estado del proceso de pago
    payResponse            TEXT, -- Respuesta del proceso de pago
    nameTypeDocument       TEXT, -- Nombre del tipo de documento
    stName                 TEXT, -- Nombre del estado del checkout
    cuponArray             JSONB, -- Información de cupones aplicados
    total                  NUMERIC, -- Total del checkout
    clientId               INTEGER, -- ID del cliente
    url                    TEXT, -- URL del checkout
    notificationStatus     TEXT, -- Estado de la notificación
    orderStatus            INTEGER, -- Estado del pedido
    courierId              INTEGER, -- ID del servicio de mensajería
    courierData            JSONB, -- Datos del servicio de mensajería
    currency               JSONB, -- Información de la moneda
    fileUrl                TEXT, -- URL del archivo asociado al checkout
    timestamp_nifi          TIMESTAMPTZ,
    PRIMARY KEY (id)
);
-- Comentarios de tabla
COMMENT ON TABLE api_bsale_syf.checkout IS 'Tabla que almacena los datos del checkout de BSale SyF';

-- Comentarios de columnas (ordenados según aparecen en la tabla)
COMMENT ON COLUMN api_bsale_syf.checkout.id IS 'Identificador único del checkout';
COMMENT ON COLUMN api_bsale_syf.checkout.token IS 'Token único del checkout';
COMMENT ON COLUMN api_bsale_syf.checkout.clientName IS 'Nombre del cliente';
COMMENT ON COLUMN api_bsale_syf.checkout.clientLastName IS 'Apellido del cliente';
COMMENT ON COLUMN api_bsale_syf.checkout.clientEmail IS 'Correo electrónico del cliente';
COMMENT ON COLUMN api_bsale_syf.checkout.clientPhone IS 'Teléfono del cliente';
COMMENT ON COLUMN api_bsale_syf.checkout.id_tipo_documento_tributario IS 'ID del tipo de documento tributario';
COMMENT ON COLUMN api_bsale_syf.checkout.dynamicAttributes IS 'Atributos dinámicos del checkout, almacenados como JSONB';
COMMENT ON COLUMN api_bsale_syf.checkout.extrasUserData IS 'Datos adicionales del usuario, almacenados como JSONB';
COMMENT ON COLUMN api_bsale_syf.checkout.clientStreet IS 'Dirección (calle) del cliente';
COMMENT ON COLUMN api_bsale_syf.checkout.clientCityZone IS 'Ciudad/zona del cliente';
COMMENT ON COLUMN api_bsale_syf.checkout.clientPostcode IS 'Código postal del cliente';
COMMENT ON COLUMN api_bsale_syf.checkout.cartId IS 'ID del carrito asociado al checkout';
COMMENT ON COLUMN api_bsale_syf.checkout.cartDetails IS 'Detalles del carrito, almacenados como texto';
COMMENT ON COLUMN api_bsale_syf.checkout.createAt IS 'Fecha y hora de creación del checkout (en formato UNIX timestamp)';
COMMENT ON COLUMN api_bsale_syf.checkout.shippingCost IS 'Costo de envío del checkout';
COMMENT ON COLUMN api_bsale_syf.checkout.isMafs IS 'Indica si el checkout es MAFS (Multi-Attribute Fulfillment Service)';
COMMENT ON COLUMN api_bsale_syf.checkout.discountCost IS 'Costo del descuento aplicado al checkout';
COMMENT ON COLUMN api_bsale_syf.checkout.active IS 'Indica si el checkout está activo';
COMMENT ON COLUMN api_bsale_syf.checkout.shippingComment IS 'Comentario sobre el envío del checkout';
COMMENT ON COLUMN api_bsale_syf.checkout.totalCart IS 'Total del carrito asociado al checkout';
COMMENT ON COLUMN api_bsale_syf.checkout.pickStoreId IS 'ID de la tienda de recogida';
COMMENT ON COLUMN api_bsale_syf.checkout.pickName IS 'Nombre de la persona que recoge el pedido';
COMMENT ON COLUMN api_bsale_syf.checkout.pickCode IS 'Código de recogida del pedido';
COMMENT ON COLUMN api_bsale_syf.checkout.id_venta_documento_tributario IS 'ID del documento tributario de la venta asociada al checkout';
COMMENT ON COLUMN api_bsale_syf.checkout.documentNumber IS 'Número del documento tributario';
COMMENT ON COLUMN api_bsale_syf.checkout.documentToken IS 'Token del documento tributario';
COMMENT ON COLUMN api_bsale_syf.checkout.storeId IS 'ID de la tienda asociada al checkout';
COMMENT ON COLUMN api_bsale_syf.checkout.storeName IS 'Nombre de la tienda asociada al checkout';
COMMENT ON COLUMN api_bsale_syf.checkout.marketId IS 'ID del mercado asociado al checkout';
COMMENT ON COLUMN api_bsale_syf.checkout.isService IS 'Indica si el checkout es un servicio';
COMMENT ON COLUMN api_bsale_syf.checkout.withdrawStore IS 'Indica si el checkout permite la recogida en tienda';
COMMENT ON COLUMN api_bsale_syf.checkout.payProcess IS 'Estado del proceso de pago del checkout';
COMMENT ON COLUMN api_bsale_syf.checkout.payResponse IS 'Respuesta del proceso de pago';
COMMENT ON COLUMN api_bsale_syf.checkout.nameTypeDocument IS 'Nombre del tipo de documento tributario';
COMMENT ON COLUMN api_bsale_syf.checkout.stName IS 'Nombre del estado del checkout';
COMMENT ON COLUMN api_bsale_syf.checkout.cuponArray IS 'Información de los cupones aplicados al checkout, almacenada como JSONB';
COMMENT ON COLUMN api_bsale_syf.checkout.total IS 'Total del checkout';
COMMENT ON COLUMN api_bsale_syf.checkout.clientId IS 'ID del cliente asociado al checkout';
COMMENT ON COLUMN api_bsale_syf.checkout.url IS 'URL del checkout';
COMMENT ON COLUMN api_bsale_syf.checkout.notificationStatus IS 'Estado de la notificación del checkout';
COMMENT ON COLUMN api_bsale_syf.checkout.orderStatus IS 'Estado del pedido asociado al checkout';
COMMENT ON COLUMN api_bsale_syf.checkout.courierId IS 'ID del servicio de mensajería asociado al checkout';
COMMENT ON COLUMN api_bsale_syf.checkout.courierData IS 'Datos del servicio de mensajería, almacenados como JSONB';
COMMENT ON COLUMN api_bsale_syf.checkout.currency IS 'Información de la moneda utilizada en el checkout, almacenada como JSONB';
COMMENT ON COLUMN api_bsale_syf.checkout.fileUrl IS 'URL del archivo asociado al checkout';
COMMENT ON COLUMN api_bsale_syf.checkout.timestamp_nifi IS 'Marca de tiempo de la última actualización desde NiFi';