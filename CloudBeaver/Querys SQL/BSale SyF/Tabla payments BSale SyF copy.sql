CREATE TABLE api_bsale_syf.payments (
    id INT,
    href TEXT,
    recordDate BIGINT,
    amount FLOAT,
    operationNumber TEXT,
    accountingDate TEXT,
    checkDate BIGINT,
    checkNumber INT,
    checkAmount FLOAT,
    checkTaken BOOLEAN,
    isCreditPayment BOOLEAN,
    createdAt BIGINT,
    state BOOLEAN,
    externalId TEXT,
    payment_type JSONB,
    document JSONB,
    documents TEXT,
    office JSONB,
    user_ JSONB,
    timestamp_nifi TIMESTAMPTZ,
    PRIMARY KEY (id)
);

