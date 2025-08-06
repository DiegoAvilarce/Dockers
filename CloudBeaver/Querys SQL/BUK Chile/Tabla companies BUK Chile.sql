CREATE TABLE api_buk_chile.companies (
    id INTEGER NOT NULL,
    name TEXT,
    address TEXT,
    commune TEXT,
    city TEXT,
    company_email TEXT,
    company_business TEXT,
    rut TEXT,
    legal_agents JSONB, -- escapeJson(/legal_agents[0])
    custom_attributes JSONB,
    company_banks JSONB, --escapeJson(/company_banks[0])
    timestamp_nifi TIMESTAMPTZ,
    PRIMARY KEY (id)
);

-- Comentarios para documentar la tabla
COMMENT ON TABLE api_buk_chile.companies IS 'Tabla principal de empresas con información corporativa y bancaria';
COMMENT ON COLUMN api_buk_chile.companies.id IS 'Primary Key con ID único de la empresa';
COMMENT ON COLUMN api_buk_chile.companies.name IS 'Nombre completo de la empresa';
COMMENT ON COLUMN api_buk_chile.companies.address IS 'Dirección principal de la empresa';
COMMENT ON COLUMN api_buk_chile.companies.commune IS 'Comuna donde se ubica la empresa';
COMMENT ON COLUMN api_buk_chile.companies.city IS 'Ciudad donde se ubica la empresa';
COMMENT ON COLUMN api_buk_chile.companies.company_email IS 'Email corporativo de la empresa';
COMMENT ON COLUMN api_buk_chile.companies.company_business IS 'Giro o actividad comercial de la empresa';
COMMENT ON COLUMN api_buk_chile.companies.rut IS 'RUT de la empresa (formato chileno)';
COMMENT ON COLUMN api_buk_chile.companies.legal_agents IS 'Agentes legales de la empresa en formato JSON';
COMMENT ON COLUMN api_buk_chile.companies.custom_attributes IS 'Atributos personalizados en formato JSON';
COMMENT ON COLUMN api_buk_chile.companies.company_banks IS 'Bancos asociados a la empresa en formato JSON';
COMMENT ON COLUMN api_buk_chile.companies.timestamp_nifi IS 'Marca de tiempo que indica cuándo fue procesado el registro por Apache NiFi';