CREATE TABLE api_buk_chile.jobs (
    id INTEGER,
    id_employees INTEGER, 
    company_id INTEGER,
    area_id INTEGER,
    contract_type TEXT,
    start_date DATE,
    end_date DATE,
    notice_date DATE,
    contract_finishing_date_1 DATE,
    contract_finishing_date_2 DATE,
    weekly_hours NUMERIC,
    cost_center TEXT,
    active_until DATE,
    periodicity TEXT,
    frequency TEXT,
    working_schedule_type TEXT,
    location_id INTEGER,
    without_wage BOOLEAN,
    zone_assignment BOOLEAN,
    contract_subscription_date DATE,
    project TEXT,
    currency_code TEXT,
    reward_concept TEXT,
    reward_payment_period TEXT,
    reward_description TEXT,
    grado_sector_publico_chile TEXT,
    estamento_sector_publico_chile TEXT,
    -- Campos tipo JSON o estructuras complejas
    days TEXT, -- Lista de días abreviados (l, m, w, etc.)
    boss JSONB,
    contractual_stipulation JSONB,
    contractual_detail JSONB,
    role JSONB,
    custom_attributes JSONB,
    -- Marca de tiempo de ingestión (opcional)
    timestamp_nifi TIMESTAMPTZ,
    PRIMARY KEY (id)
);

-- Definición de la tabla api_buk_chile.jobs
COMMENT ON TABLE api_buk_chile.jobs IS 'Tabla que almacena información de trabajos en Buk Chile, incluyendo detalles del empleado, contrato y asignaciones.';