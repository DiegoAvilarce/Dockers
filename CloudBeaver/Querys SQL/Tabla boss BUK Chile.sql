CREATE TABLE api_buk_chile.boss (
    id INTEGER,
    id_employees INTEGER,
    id_jobs INTEGER,
    rut TEXT,
    document_type TEXT,
    document_number TEXT,
    timestamp_nifi TIMESTAMPTZ,
    PRIMARY KEY (id, id_jobs)
);
