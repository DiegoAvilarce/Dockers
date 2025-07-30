CREATE TABLE api_buk_chile.roles (
    id INTEGER,
    code VARCHAR(255),
    name VARCHAR(255),
    description TEXT,
    requirements TEXT,
    area_ids TEXT,
    role_family JSONB,
    timestamp_nifi TIMESTAMPTZ,
    PRIMARY KEY (id)
);

COMMENT ON TABLE api_buk_chile.roles IS 'Tabla maestra de roles';