CREATE TABLE api_buk_chile.role (
    id INTEGER,
    id_employees INTEGER,
    id_jobs INTEGER,
    code VARCHAR(255),
    name VARCHAR(255),
    description TEXT,
    requirements TEXT,
    area_ids TEXT,
    role_family VARCHAR(255),
    timestamp_nifi TIMESTAMPTZ,
    PRIMARY KEY (id, id_jobs)
);

COMMENT ON TABLE api_buk_chile.role IS 'Tabla de roles de empleados con información sobre el rol, requisitos y áreas asociadas';