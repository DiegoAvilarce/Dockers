CREATE TABLE api_buk_peru.companies (
    id INTEGER NOT NULL,
    name TEXT,
    address TEXT,
    commune TEXT,
    city TEXT,
    company_email TEXT,
    company_business TEXT,
    ruc TEXT,
    legal_agents JSONB,
    custom_attributes JSONB,
    company_banks JSONB,
    timestamp_nifi TIMESTAMPTZ,
    PRIMARY KEY (id)
);

-- Comentarios para documentar la tabla
COMMENT ON TABLE api_buk_peru.companies IS 'Tabla principal de empresas con información corporativa y bancaria';
COMMENT ON COLUMN api_buk_peru.companies.id IS 'Primary Key con ID único de la empresa';
COMMENT ON COLUMN api_buk_peru.companies.name IS 'Nombre completo de la empresa';
COMMENT ON COLUMN api_buk_peru.companies.address IS 'Dirección principal de la empresa';
COMMENT ON COLUMN api_buk_peru.companies.commune IS 'Comuna donde se ubica la empresa';
COMMENT ON COLUMN api_buk_peru.companies.city IS 'Ciudad donde se ubica la empresa';
COMMENT ON COLUMN api_buk_peru.companies.company_email IS 'Email corporativo de la empresa';
COMMENT ON COLUMN api_buk_peru.companies.company_business IS 'Giro o actividad comercial de la empresa';
COMMENT ON COLUMN api_buk_peru.companies.ruc IS 'RUC de la empresa (formato peruano)';
COMMENT ON COLUMN api_buk_peru.companies.legal_agents IS 'Agentes legales de la empresa en formato JSON';
COMMENT ON COLUMN api_buk_peru.companies.custom_attributes IS 'Atributos personalizados en formato JSON';
COMMENT ON COLUMN api_buk_peru.companies.company_banks IS 'Bancos asociados a la empresa en formato JSON';
COMMENT ON COLUMN api_buk_peru.companies.timestamp_nifi IS 'Marca de tiempo que indica cuándo fue procesado el registro por Apache NiFi';