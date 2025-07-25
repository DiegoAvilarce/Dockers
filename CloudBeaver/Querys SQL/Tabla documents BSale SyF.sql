CREATE TABLE bsale_syf.documents (
    id                     INTEGER,
    href                   TEXT,
    emission_date          BIGINT,
    expiration_date        BIGINT,
    generation_date        BIGINT,
    number                 INTEGER,
    serial_number          TEXT,
    tracking_number        TEXT,
    total_amount           INTEGER,
    net_amount             INTEGER,
    tax_amount             INTEGER,
    exempt_amount          INTEGER,
    not_exempt_amount      INTEGER,
    export_total_amount    INTEGER,
    export_net_amount      INTEGER,
    export_tax_amount      INTEGER,
    export_exempt_amount   INTEGER,
    commission_rate        NUMERIC,
    commission_net_amount  INTEGER,
    commission_tax_amount  INTEGER,
    commission_total_amount INTEGER,
    percentage_tax_withheld NUMERIC,
    purchase_tax_amount    INTEGER,
    purchase_total_amount  INTEGER,
    address                TEXT,
    municipality           TEXT,
    city                   TEXT,
    url_timbre             TEXT,
    url_public_view        TEXT,
    url_pdf                TEXT,
    url_public_view_original TEXT,
    url_pdf_original       TEXT,
    token                  TEXT,
    state                  INTEGER,
    commercial_state       INTEGER,
    cancellation_status    INTEGER,
    cancellation_date      TEXT,
    url_xml                TEXT,
    ted                    TEXT,
    sales_id               INTEGER,
    informed_sii           INTEGER,
    response_msg_sii       TEXT,
    -- Campos anidados como JSONB
    document_type          JSONB,
    client                 JSONB,
    office                 JSONB,
    user_                  JSONB,--@davila: se le cambia el nombre ya que user es un comando reservado. Se debe cambiar el nombre desde NiFi
    coin                   JSONB,
    pricelist              JSONB,
    references_            JSONB, --@davila: se le cambia el nombre ya que references es un comando reservado. Se debe cambiar el nombre desde NiFi
    document_taxes         JSONB,
    details                JSONB,
    sellers                JSONB,
    attributes             JSONB,
    timestamp_nifi TIMESTAMPTZ,
    PRIMARY KEY (id)
);
