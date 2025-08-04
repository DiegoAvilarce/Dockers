-- Tabla de trabajos basada en el schema de API BUK Perú
CREATE TABLE api_buk_peru.jobs (
    id INTEGER,
    id_employees INTEGER, 
    company_id INTEGER,
    start_date DATE,
    end_date DATE,
    area_id INTEGER,
    contract_term TEXT,
    notice_date DATE,
    contract_type TEXT,
    employment_regimen TEXT,
    worker_type TEXT,
    fola_insurance TEXT,
    fola_plan TEXT,
    periodicity TEXT,
    ria_regimen BOOLEAN,
    t_register_kind TEXT,
    t_register_special_regimen TEXT,
    regular_hours NUMERIC,
    cost_center TEXT,
    active_until DATE,
    project TEXT,
    currency_code TEXT,
    without_wage BOOLEAN,
    
    -- Campos tipo JSON o estructuras complejas
    days TEXT, -- Lista de días abreviados (l, m, w, etc.)
    boss JSONB,
    dias_laborales TEXT, -- Lista de días laborales (parece duplicado de days)
    role JSONB,
    cost_centers TEXT, -- Array de centros de costo como TEXT
    
    -- Marca de tiempo de ingestión
    timestamp_nifi TIMESTAMPTZ,
    PRIMARY KEY (id)
);

-- Comentarios para documentar la tabla
COMMENT ON TABLE api_buk_peru.jobs IS 'Tabla que almacena información de trabajos en Buk Perú, incluyendo detalles del empleado, contrato y asignaciones.';
COMMENT ON COLUMN api_buk_peru.jobs.id IS 'ID único del trabajo';
COMMENT ON COLUMN api_buk_peru.jobs.id_employees IS 'ID del empleado asociado al trabajo';
COMMENT ON COLUMN api_buk_peru.jobs.company_id IS 'ID de la empresa';
COMMENT ON COLUMN api_buk_peru.jobs.area_id IS 'ID del área de trabajo';
COMMENT ON COLUMN api_buk_peru.jobs.contract_term IS 'Término del contrato';
COMMENT ON COLUMN api_buk_peru.jobs.employment_regimen IS 'Régimen de empleo (general, etc.)';
COMMENT ON COLUMN api_buk_peru.jobs.worker_type IS 'Tipo de trabajador';
COMMENT ON COLUMN api_buk_peru.jobs.fola_insurance IS 'Seguro FOLA';
COMMENT ON COLUMN api_buk_peru.jobs.fola_plan IS 'Plan FOLA';
COMMENT ON COLUMN api_buk_peru.jobs.ria_regimen IS 'Régimen RIA (boolean)';
COMMENT ON COLUMN api_buk_peru.jobs.t_register_kind IS 'Tipo de registro (empleado, etc.)';
COMMENT ON COLUMN api_buk_peru.jobs.t_register_special_regimen IS 'Régimen especial de registro';
COMMENT ON COLUMN api_buk_peru.jobs.regular_hours IS 'Horas regulares de trabajo';
COMMENT ON COLUMN api_buk_peru.jobs.days IS 'Días de trabajo en formato JSON array';
COMMENT ON COLUMN api_buk_peru.jobs.boss IS 'Información del jefe en formato JSON';
COMMENT ON COLUMN api_buk_peru.jobs.dias_laborales IS 'Días laborales en formato JSON array';
COMMENT ON COLUMN api_buk_peru.jobs.role IS 'Información del rol en formato JSON';
COMMENT ON COLUMN api_buk_peru.jobs.cost_centers IS 'Centros de costo en formato JSON array';
COMMENT ON COLUMN api_buk_peru.jobs.timestamp_nifi IS 'Marca de tiempo que indica cuándo fue procesado el registro por Apache NiFi';