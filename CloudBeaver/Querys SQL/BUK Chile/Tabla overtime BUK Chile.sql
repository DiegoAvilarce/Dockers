CREATE TABLE api_buk_chile.overtime (
    id INTEGER,
    day INTEGER,
    month INTEGER,
    year INTEGER,
    hours FLOAT,
    employee_id INTEGER,
    type_id INTEGER,
    centro_costo TEXT,
    timestamp_nifi TIMESTAMPTZ,
    PRIMARY KEY (id)
);

-- Comentarios para documentar la tabla
COMMENT ON TABLE api_buk_chile.overtime IS 'Tabla de horas extras con información de empleados y tipos de horas';
COMMENT ON COLUMN api_buk_chile.overtime.id IS 'Primary Key con ID único de la hora extra';
COMMENT ON COLUMN api_buk_chile.overtime.day IS 'Día del mes de la hora extra';
COMMENT ON COLUMN api_buk_chile.overtime.month IS 'Mes de la hora extra';   
COMMENT ON COLUMN api_buk_chile.overtime.year IS 'Año de la hora extra';
COMMENT ON COLUMN api_buk_chile.overtime.hours IS 'Número de horas extras trabajadas';
COMMENT ON COLUMN api_buk_chile.overtime.employee_id IS 'ID del empleado asociado a la hora extra';
COMMENT ON COLUMN api_buk_chile.overtime.type_id IS 'ID del tipo de hora extra';
COMMENT ON COLUMN api_buk_chile.overtime.centro_costo IS 'Centro de costos asociado a la hora extra';
COMMENT ON COLUMN api_buk_chile.overtime.timestamp_nifi IS 'Marca de tiempo de la hora extra procesada por NiFi';
