-- Tabla principal basada en el schema de API BUK Perú
CREATE TABLE api_buk_peru.employees (
    -- Campos básicos de persona
    person_id INTEGER,
    id INTEGER,
    picture_url TEXT,
    first_name VARCHAR(255),
    surname VARCHAR(255),
    second_surname VARCHAR(255),
    full_name VARCHAR(255),
    document_type VARCHAR(50),
    document_number VARCHAR(50),
    code_sheet VARCHAR(100),
    email VARCHAR(255),
    personal_email VARCHAR(255),
    
    -- Información de dirección (campos específicos de Perú)
    address TEXT,
    location_id INTEGER,
    provincia VARCHAR(100),
    distrito VARCHAR(100),
    departamento VARCHAR(100),
    office_phone VARCHAR(20),
    phone VARCHAR(20),
    
    -- Información personal
    gender VARCHAR(10),
    birthday DATE,
    university VARCHAR(255),
    degree VARCHAR(255),
    education_end_date DATE,
    education_status VARCHAR(100),
    active_since DATE,
    status VARCHAR(50),
    
    -- Información de pago
    payment_method VARCHAR(100),
    bank VARCHAR(100),
    account_type VARCHAR(50),
    account_number VARCHAR(50),
    company_payment_bank VARCHAR(100),
    company_bank_account_number VARCHAR(50),
    
    -- Información laboral
    private_role BOOLEAN,
    progressive_vacations_start DATE,
    nationality VARCHAR(100),
    country_code VARCHAR(5),
    civil_status VARCHAR(50),
    health_company VARCHAR(100),
    pension_regime VARCHAR(100),
    pension_fund VARCHAR(100),
    afc VARCHAR(100),
    retired BOOLEAN,
    retirement_regime VARCHAR(100),
    
    -- Campos de terminación
    active_until DATE,
    termination_reason VARCHAR(255),
    
    -- Campos complejos como JSONB
    custom_attributes JSONB,
    current_job JSONB,
    jobs JSONB, --- en un UpdateRecord de NiFi ponemos /jobs con valor escapeJson(/jobs[0])
    family_responsabilities JSONB, --escapeJson(/family_responsabilities[0])
    timestamp_nifi TIMESTAMPTZ,
    PRIMARY KEY (id)
);

-- Comentarios para documentar la tabla
COMMENT ON TABLE api_buk_peru.employees IS 'Tabla de empleados de API BUK Perú con información personal, laboral y familiar';
COMMENT ON COLUMN api_buk_peru.employees.person_id IS 'ID único de la persona';
COMMENT ON COLUMN api_buk_peru.employees.id IS 'Primary Key con ID único del empleado';
COMMENT ON COLUMN api_buk_peru.employees.document_number IS 'Número de documento (DNI para Perú)';
COMMENT ON COLUMN api_buk_peru.employees.provincia IS 'Provincia del empleado (división administrativa de Perú)';
COMMENT ON COLUMN api_buk_peru.employees.distrito IS 'Distrito del empleado (división administrativa de Perú)';
COMMENT ON COLUMN api_buk_peru.employees.departamento IS 'Departamento del empleado (división administrativa de Perú)';
COMMENT ON COLUMN api_buk_peru.employees.education_end_date IS 'Fecha de finalización de estudios';
COMMENT ON COLUMN api_buk_peru.employees.education_status IS 'Estado de educación del empleado';
COMMENT ON COLUMN api_buk_peru.employees.company_payment_bank IS 'Banco de pago de la empresa';
COMMENT ON COLUMN api_buk_peru.employees.company_bank_account_number IS 'Número de cuenta bancaria de la empresa';
COMMENT ON COLUMN api_buk_peru.employees.custom_attributes IS 'Atributos personalizados en formato JSON';
COMMENT ON COLUMN api_buk_peru.employees.current_job IS 'Información del trabajo actual en formato JSON';
COMMENT ON COLUMN api_buk_peru.employees.jobs IS 'Historial de trabajos en formato JSON';
COMMENT ON COLUMN api_buk_peru.employees.family_responsabilities IS 'Responsabilidades familiares en formato JSON';
COMMENT ON COLUMN api_buk_peru.employees.timestamp_nifi IS 'Marca de tiempo que indica cuándo fue procesado el registro por Apache NiFi';