-- Tabla principal basada en el schema AVRO
CREATE TABLE api_buk_chile.employees (
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
    rut VARCHAR(20),
    code_sheet VARCHAR(100),
    email VARCHAR(255),
    personal_email VARCHAR(255),
    
    -- Información de dirección
    address TEXT,
    street VARCHAR(255),
    street_number VARCHAR(20),
    office_number VARCHAR(20),
    city VARCHAR(100),
    district VARCHAR(100),
    location_id INTEGER,
    region VARCHAR(100),
    office_phone VARCHAR(20),
    phone VARCHAR(20),
    
    -- Información personal
    gender VARCHAR(10),
    birthday DATE, -- o VARCHAR si prefieres mantener como string
    university VARCHAR(255),
    degree VARCHAR(255),
    active_since DATE, -- o VARCHAR
    created_at TEXT, -- o VARCHAR
    status VARCHAR(50),
    
    -- Información de pago
    payment_method VARCHAR(100),
    payment_period VARCHAR(50),
    advance_payment VARCHAR(100),
    bank VARCHAR(100),
    account_type VARCHAR(50),
    account_number VARCHAR(50),
    
    -- Información laboral
    private_role BOOLEAN,
    progressive_vacations_start DATE, -- o VARCHAR
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
    active_until DATE, -- o VARCHAR
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
COMMENT ON TABLE api_buk_chile.employees IS 'Tabla principal de empleados con información personal, laboral y familiar';
COMMENT ON COLUMN api_buk_chile.employees.person_id IS 'ID único de la persona';
COMMENT ON COLUMN api_buk_chile.employees.id IS 'Primary Key con ID único del empleado';
COMMENT ON COLUMN api_buk_chile.employees.rut IS 'RUT del empleado (formato chileno)';
COMMENT ON COLUMN api_buk_chile.employees.custom_attributes IS 'Atributos personalizados en formato JSON';
COMMENT ON COLUMN api_buk_chile.employees.current_job IS 'Información del trabajo actual en formato JSON';
COMMENT ON COLUMN api_buk_chile.employees.jobs IS 'Historial de trabajos en formato JSON';
COMMENT ON COLUMN api_buk_chile.employees.family_responsabilities IS 'Responsabilidades familiares en formato JSON';
COMMENT ON COLUMN api_buk_chile.employees.timestamp_nifi IS 'Marca de tiempo que indica cuándo fue procesado el registro por Apache NiFi';