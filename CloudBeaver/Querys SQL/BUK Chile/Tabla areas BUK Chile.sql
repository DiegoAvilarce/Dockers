CREATE TABLE api_buk_chile.areas (
    id INTEGER NOT NULL,
    name TEXT,
    address TEXT,
    status TEXT,
    city TEXT,
    children_area JSONB, -- escapeJson(/children_area[0])
    cost_center TEXT,
    department JSONB, 
    custom_attributes JSONB,
    parent_area JSONB,
    timestamp_nifi TIMESTAMPTZ,
    PRIMARY KEY (id)
);

-- Comentarios para documentar la tabla
COMMENT ON TABLE api_buk_chile.areas IS 'Tabla de áreas organizacionales con información departamental y centro de costos';
COMMENT ON COLUMN api_buk_chile.areas.id IS 'Primary Key con ID único del área';
COMMENT ON COLUMN api_buk_chile.areas.name IS 'Nombre del área';
COMMENT ON COLUMN api_buk_chile.areas.address IS 'Dirección del área';
COMMENT ON COLUMN api_buk_chile.areas.status IS 'Estado del área (active/inactive)';
COMMENT ON COLUMN api_buk_chile.areas.city IS 'Ciudad donde se ubica el área';
COMMENT ON COLUMN api_buk_chile.areas.children_area IS 'Áreas hijas en formato JSON';
COMMENT ON COLUMN api_buk_chile.areas.cost_center IS 'Código del centro de costos';
COMMENT ON COLUMN api_buk_chile.areas.department IS 'Información del departamento y división en formato JSON';
COMMENT ON COLUMN api_buk_chile.areas.custom_attributes IS 'Atributos personalizados en formato JSON';