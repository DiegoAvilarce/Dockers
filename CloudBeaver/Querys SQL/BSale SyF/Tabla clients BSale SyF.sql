CREATE TABLE IF NOT EXISTS api_bsale_syf.clients (
    id                     INTEGER,
    href                   TEXT,
    firstName              TEXT,
    lastName               TEXT,
    email                  TEXT,
    code                   TEXT,
    phone                  TEXT,
    company                TEXT,
    note                   TEXT,
    facebook               TEXT,
    twitter                TEXT,
    hasCredit              INTEGER,
    maxCredit              NUMERIC(10, 2),
    state                  INTEGER,
    activity               TEXT,
    city                   TEXT,
    commerciallyBlocked    INTEGER,
    municipality           TEXT,
    address                TEXT,
    companyOrPerson        INTEGER,
    accumulatePoints       INTEGER,
    points                 NUMERIC(10, 2),
    pointsUpdated          TIMESTAMPTZ,
    sendDte                INTEGER,
    isForeigner            INTEGER,
    prestashopClienId      INTEGER,
    createdAt              TEXT,
    updatedAt              TEXT,
    contacts               JSONB, -- Referencia a los contactos del cliente
    attributes             JSONB, -- Atributos del cliente
    addresses              JSONB, -- Direcciones del cliente
    timestamp_nifi         TIMESTAMPTZ,
    PRIMARY KEY (id)
);

-- Agregar comentarios para explicar los campos de manera breve y profesional
COMMENT ON COLUMN api_bsale_syf.clients.id IS 'Identificador único del cliente';
COMMENT ON COLUMN api_bsale_syf.clients.href IS 'Enlace al cliente';
COMMENT ON COLUMN api_bsale_syf.clients.firstName IS 'Nombre del cliente';
COMMENT ON COLUMN api_bsale_syf.clients.lastName IS 'Apellido del cliente';
COMMENT ON COLUMN api_bsale_syf.clients.email IS 'Correo electrónico del cliente';
COMMENT ON COLUMN api_bsale_syf.clients.code IS 'Código del cliente';
COMMENT ON COLUMN api_bsale_syf.clients.phone IS 'Teléfono del cliente';
COMMENT ON COLUMN api_bsale_syf.clients.company IS 'Nombre de la empresa del cliente';
COMMENT ON COLUMN api_bsale_syf.clients.note IS 'Nota adicional sobre el cliente';
COMMENT ON COLUMN api_bsale_syf.clients.facebook IS 'Perfil de Facebook del cliente';
COMMENT ON COLUMN api_bsale_syf.clients.twitter IS 'Perfil de Twitter del cliente';
COMMENT ON COLUMN api_bsale_syf.clients.hasCredit IS 'Indica si el cliente tiene crédito';
COMMENT ON COLUMN api_bsale_syf.clients.maxCredit IS 'Límite máximo de crédito del cliente';
COMMENT ON COLUMN api_bsale_syf.clients.state IS 'Estado del cliente';
COMMENT ON COLUMN api_bsale_syf.clients.activity IS 'Actividad o giro del cliente';
COMMENT ON COLUMN api_bsale_syf.clients.city IS 'Ciudad del cliente';
COMMENT ON COLUMN api_bsale_syf.clients.commerciallyBlocked IS 'Indica si el cliente está bloqueado comercialmente';
COMMENT ON COLUMN api_bsale_syf.clients.municipality IS 'Municipio del cliente';
COMMENT ON COLUMN api_bsale_syf.clients.address IS 'Dirección del cliente';
COMMENT ON COLUMN api_bsale_syf.clients.companyOrPerson IS 'Indica si el cliente es una empresa o una persona';
COMMENT ON COLUMN api_bsale_syf.clients.accumulatePoints IS 'Indica si el cliente acumula puntos';
COMMENT ON COLUMN api_bsale_syf.clients.points IS 'Puntos acumulados por el cliente';
COMMENT ON COLUMN api_bsale_syf.clients.pointsUpdated IS 'Fecha de la última actualización de puntos del cliente';
COMMENT ON COLUMN api_bsale_syf.clients.sendDte IS 'Indica si se envían DTE al cliente';
COMMENT ON COLUMN api_bsale_syf.clients.isForeigner IS 'Indica si el cliente es extranjero';
COMMENT ON COLUMN api_bsale_syf.clients.prestashopClienId IS 'ID del cliente en PrestaShop';
COMMENT ON COLUMN api_bsale_syf.clients.createdAt IS 'Fecha de creación del cliente';
COMMENT ON COLUMN api_bsale_syf.clients.updatedAt IS 'Fecha de la última actualización del cliente';    
COMMENT ON COLUMN api_bsale_syf.clients.contacts IS 'Referencias a los contactos del cliente, almacenadas como JSONB';
COMMENT ON COLUMN api_bsale_syf.clients.attributes IS 'Atributos del cliente, almacenados como JSONB';
COMMENT ON COLUMN api_bsale_syf.clients.addresses IS 'Direcciones del cliente, almacenadas como JSONB';
COMMENT ON COLUMN api_bsale_syf.clients.timestamp_nifi IS 'Marca de tiempo de la última actualización desde NiFi';

