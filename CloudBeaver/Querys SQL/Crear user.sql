CREATE ROLE user1 LOGIN PASSWORD 'password';
GRANT CONNECT ON DATABASE bi_postgres TO user1; -- Otorgar privilegios de conexión a la BD
GRANT USAGE ON SCHEMA api_buk_chile TO user1; --Dar permiso de uso sobre el esquema
GRANT SELECT ON ALL TABLES IN SCHEMA api_buk_chile TO user1; -- Otorgar SELECT sobre todas las tablas existentes del esquema

--Dar SELECT automático sobre futuras tablas
ALTER DEFAULT PRIVILEGES IN SCHEMA api_buk_chile
GRANT SELECT ON TABLES TO user1;


-- Ver qué roles tiene asignado `daryen` (por ejemplo si es SUPERUSER o tiene otros atributos)
SELECT rolname, rolsuper, rolcreaterole, rolcreatedb, rolcanlogin
FROM pg_roles
WHERE rolname = 'user1';

-- Ver privilegios sobre esquemas y tablas que tiene daryen
SELECT grantee, privilege_type, table_schema, table_name
FROM information_schema.role_table_grants
WHERE grantee = 'user1';

-- Ver privilegios sobre las bases de datos
SELECT dat.datname AS database_name,
       has_database_privilege(rol.rolname, dat.datname, 'CONNECT') AS can_connect,
       has_database_privilege(rol.rolname, dat.datname, 'TEMP') AS can_temp
FROM pg_database dat, pg_roles rol
WHERE rol.rolname = 'user1';