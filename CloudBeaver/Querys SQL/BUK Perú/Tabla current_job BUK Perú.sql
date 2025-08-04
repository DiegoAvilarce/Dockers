-- Tabla de trabajos actuales basada en el schema de API BUK Perú
CREATE TABLE api_buk_peru.current_job (
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
    frequency TEXT,
    working_schedule_type TEXT,
    zone_assignment BOOLEAN,
    union_info TEXT,
    project TEXT,
    previous_job_id INTEGER,
    ria_regimen BOOLEAN,
    t_register_kind TEXT,
    t_register_special_regimen TEXT,
    regular_hours NUMERIC,
    cost_center TEXT,
    active_until DATE,
    currency_code TEXT,
    without_wage BOOLEAN,
    
    -- Campos tipo JSON o estructuras complejas
    days TEXT, -- Lista de días abreviados (l, m, w, etc.)
    boss JSONB,
    dias_laborales TEXT, -- Lista de días laborales
    role JSONB,
    cost_centers TEXT, -- Array de centros de costo como TEXT
    
    -- Marca de tiempo de ingestión
    timestamp_nifi TIMESTAMPTZ,
    PRIMARY KEY (id)
);

-- Comentarios para documentar la tabla
COMMENT ON TABLE api_buk_peru.current_job IS 'Tabla que almacena información del trabajo actual de empleados en Buk Perú';
COMMENT ON COLUMN api_buk_peru.current_job.id IS 'ID único del trabajo actual';
COMMENT ON COLUMN api_buk_peru.current_job.id_employees IS 'ID del empleado asociado al trabajo actual';
COMMENT ON COLUMN api_buk_peru.current_job.company_id IS 'ID de la empresa';
COMMENT ON COLUMN api_buk_peru.current_job.area_id IS 'ID del área de trabajo';
COMMENT ON COLUMN api_buk_peru.current_job.contract_term IS 'Término del contrato';
COMMENT ON COLUMN api_buk_peru.current_job.employment_regimen IS 'Régimen de empleo (general, etc.)';
COMMENT ON COLUMN api_buk_peru.current_job.worker_type IS 'Tipo de trabajador';
COMMENT ON COLUMN api_buk_peru.current_job.fola_insurance IS 'Seguro FOLA';
COMMENT ON COLUMN api_buk_peru.current_job.fola_plan IS 'Plan FOLA';
COMMENT ON COLUMN api_buk_peru.current_job.periodicity IS 'Periodicidad del trabajo';
COMMENT ON COLUMN api_buk_peru.current_job.frequency IS 'Frecuencia del trabajo';
COMMENT ON COLUMN api_buk_peru.current_job.working_schedule_type IS 'Tipo de horario de trabajo';
COMMENT ON COLUMN api_buk_peru.current_job.zone_assignment IS 'Asignación por zona';
COMMENT ON COLUMN api_buk_peru.current_job.union_info IS 'Información del sindicato';
COMMENT ON COLUMN api_buk_peru.current_job.previous_job_id IS 'ID del trabajo anterior';
COMMENT ON COLUMN api_buk_peru.current_job.ria_regimen IS 'Régimen RIA (boolean)';
COMMENT ON COLUMN api_buk_peru.current_job.t_register_kind IS 'Tipo de registro (empleado, etc.)';
COMMENT ON COLUMN api_buk_peru.current_job.t_register_special_regimen IS 'Régimen especial de registro';
COMMENT ON COLUMN api_buk_peru.current_job.regular_hours IS 'Horas regulares de trabajo';
COMMENT ON COLUMN api_buk_peru.current_job.days IS 'Días de trabajo en formato JSON array';
COMMENT ON COLUMN api_buk_peru.current_job.boss IS 'Información del jefe en formato JSON';
COMMENT ON COLUMN api_buk_peru.current_job.dias_laborales IS 'Días laborales en formato JSON array';
COMMENT ON COLUMN api_buk_peru.current_job.role IS 'Información del rol en formato JSON';
COMMENT ON COLUMN api_buk_peru.current_job.cost_centers IS 'Centros de costo en formato JSON array';
COMMENT ON COLUMN api_buk_peru.current_job.timestamp_nifi IS 'Marca de tiempo que indica cuándo fue procesado el registro por Apache NiFi';