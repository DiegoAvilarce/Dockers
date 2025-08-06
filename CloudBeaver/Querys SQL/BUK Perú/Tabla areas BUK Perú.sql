CREATE TABLE api_buk_peru.areas (
    id INTEGER NOT NULL,
    name TEXT,
    address TEXT,
    status TEXT,
    provincia TEXT,
    children_area JSONB, -- escapeJson(/children_area[0])
    cost_center TEXT,
    department JSONB,
    custom_attributes JSONB,
    parent_area JSONB,
    timestamp_nifi TIMESTAMPTZ,
    PRIMARY KEY (id)
);

-- Comentarios para documentar la tabla
COMMENT ON TABLE api_buk_peru.areas IS 'Tabla de áreas organizacionales con información departamental y centro de costos';
COMMENT ON COLUMN api_buk_peru.areas.id IS 'Primary Key con ID único del área';
COMMENT ON COLUMN api_buk_peru.areas.name IS 'Nombre del área';
COMMENT ON COLUMN api_buk_peru.areas.address IS 'Dirección del área';
COMMENT ON COLUMN api_buk_peru.areas.status IS 'Estado del área (active/inactive)';
COMMENT ON COLUMN api_buk_peru.areas.provincia IS 'Provincia del área';
COMMENT ON COLUMN api_buk_peru.areas.children_area IS 'Áreas hijas en formato JSON';
COMMENT ON COLUMN api_buk_peru.areas.cost_center IS 'Código del centro de costos';
COMMENT ON COLUMN api_buk_peru.areas.department IS 'Información del departamento y división en formato JSON';
COMMENT ON COLUMN api_buk_peru.areas.custom_attributes IS 'Atributos personalizados en formato JSON';