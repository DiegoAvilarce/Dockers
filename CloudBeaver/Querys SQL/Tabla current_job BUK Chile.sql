-- Tabla principal de trabajos actuales basada en estructura normalizada
CREATE TABLE api_buk_chile.current_job (
    -- Identificadores principales
    id INTEGER PRIMARY KEY,
    id_employees INTEGER, -- Nuevo campo: ID del empleado
    company_id INTEGER,
    area_id INTEGER,
    previous_job_id INTEGER,
    location_id INTEGER,
    
    -- Información básica del trabajo
    periodicity VARCHAR(50),
    frequency VARCHAR(50),
    working_schedule_type VARCHAR(100),
    contract_type VARCHAR(100),
    zone_assignment BOOLEAN,
    union_info VARCHAR(255),
    project VARCHAR(255),
    
    -- Fechas asociadas al trabajo
    start_date DATE,
    end_date DATE,
    notice_date DATE,
    contract_finishing_date_1 DATE,
    contract_finishing_date_2 DATE,
    contract_subscription_date DATE,
    active_until DATE,
    
    -- Información laboral
    weekly_hours DECIMAL(5,2),
    cost_center VARCHAR(50),
    without_wage BOOLEAN,
    
    -- Información monetaria
    currency_code VARCHAR(10),
    reward_concept VARCHAR(255),
    reward_payment_period VARCHAR(100),
    reward_description TEXT,
    
    -- Información sector público Chile
    grado_sector_publico_chile VARCHAR(100),
    estamento_sector_publico_chile VARCHAR(100),
    
    -- Campos complejos como JSONB
    days TEXT, -- Array de días laborales: ["l", "m", "w", "j", "v"]
    boss JSONB, -- Información del jefe: {id, rut, document_type, document_number}
    contractual_stipulation JSONB, -- Estipulaciones del trabajo
    contractual_detail JSONB, -- Detalles específicos del trabajo
    role JSONB, -- Información completa del rol/cargo
    custom_attributes JSONB, -- Atributos personalizados
    
    -- Auditoría
    timestamp_nifi TIMESTAMPTZ
);

-- Comentarios para documentar la tabla
COMMENT ON TABLE api_buk_chile.current_job IS 'Tabla principal de trabajos actuales con información detallada';
COMMENT ON COLUMN api_buk_chile.current_job.id IS 'Identificador único del trabajo actual';
COMMENT ON COLUMN api_buk_chile.current_job.id_employees IS 'ID del empleado asociado al trabajo actual';
COMMENT ON COLUMN api_buk_chile.current_job.company_id IS 'ID de la empresa en la que se desempeña el trabajador';
COMMENT ON COLUMN api_buk_chile.current_job.area_id IS 'ID del área o departamento del trabajador';
COMMENT ON COLUMN api_buk_chile.current_job.previous_job_id IS 'ID del trabajo anterior inmediato si existe';
COMMENT ON COLUMN api_buk_chile.current_job.location_id IS 'ID de la ubicación física asociada al trabajo';
COMMENT ON COLUMN api_buk_chile.current_job.periodicity IS 'Periodicidad de la posición (mensual, anual, etc.)';
COMMENT ON COLUMN api_buk_chile.current_job.frequency IS 'Frecuencia de pagos o evaluaciones';
COMMENT ON COLUMN api_buk_chile.current_job.working_schedule_type IS 'Tipo de jornada laboral que aplica al trabajo';
COMMENT ON COLUMN api_buk_chile.current_job.contract_type IS 'Tipo de relación contractual (Indefinido, Plazo fijo, etc.)';
COMMENT ON COLUMN api_buk_chile.current_job.zone_assignment IS 'Indica si el trabajo tiene asignación de zona';
COMMENT ON COLUMN api_buk_chile.current_job.union_info IS 'Información sobre afiliación sindical';
COMMENT ON COLUMN api_buk_chile.current_job.project IS 'Proyecto específico al cual está asignado el trabajador';
COMMENT ON COLUMN api_buk_chile.current_job.start_date IS 'Fecha de inicio del trabajo actual';
COMMENT ON COLUMN api_buk_chile.current_job.end_date IS 'Fecha de término del trabajo actual (si aplica)';
COMMENT ON COLUMN api_buk_chile.current_job.notice_date IS 'Fecha en que se notificó el término (si corresponde)';
COMMENT ON COLUMN api_buk_chile.current_job.contract_finishing_date_1 IS 'Primera fecha considerada para finalizar el trabajo';
COMMENT ON COLUMN api_buk_chile.current_job.contract_finishing_date_2 IS 'Segunda fecha considerada para finalizar el trabajo';
COMMENT ON COLUMN api_buk_chile.current_job.contract_subscription_date IS 'Fecha de formalización del acuerdo laboral';
COMMENT ON COLUMN api_buk_chile.current_job.active_until IS 'Fecha hasta la cual se considera activo el trabajo';
COMMENT ON COLUMN api_buk_chile.current_job.weekly_hours IS 'Cantidad de horas semanales pactadas';
COMMENT ON COLUMN api_buk_chile.current_job.cost_center IS 'Centro de costos asociado al trabajo';
COMMENT ON COLUMN api_buk_chile.current_job.without_wage IS 'Indica si el trabajo no tiene remuneración asociada';
COMMENT ON COLUMN api_buk_chile.current_job.currency_code IS 'Código de la moneda usada para la remuneración';
COMMENT ON COLUMN api_buk_chile.current_job.reward_concept IS 'Concepto de remuneración principal';
COMMENT ON COLUMN api_buk_chile.current_job.reward_payment_period IS 'Periodicidad del pago de remuneraciones';
COMMENT ON COLUMN api_buk_chile.current_job.reward_description IS 'Descripción detallada de la remuneración';
COMMENT ON COLUMN api_buk_chile.current_job.grado_sector_publico_chile IS 'Grado en el sector público (Chile)';
COMMENT ON COLUMN api_buk_chile.current_job.estamento_sector_publico_chile IS 'Estamento funcional en el sector público (Chile)';
COMMENT ON COLUMN api_buk_chile.current_job.days IS 'Días laborales en formato JSON array';
COMMENT ON COLUMN api_buk_chile.current_job.boss IS 'Información del jefe directo del trabajador';
COMMENT ON COLUMN api_buk_chile.current_job.contractual_stipulation IS 'Estipulaciones laborales específicas del trabajo';
COMMENT ON COLUMN api_buk_chile.current_job.contractual_detail IS 'Detalles adicionales sobre la posición laboral';
COMMENT ON COLUMN api_buk_chile.current_job.role IS 'Información estructurada del rol o cargo del trabajador';
COMMENT ON COLUMN api_buk_chile.current_job.custom_attributes IS 'Atributos personalizados asociados al trabajo';
COMMENT ON COLUMN api_buk_chile.current_job.timestamp_nifi IS 'Marca de tiempo de la última actualización desde NiFi';
