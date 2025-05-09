-- Database: <TEST_DB_NAME>

-- DROP DATABASE IF EXISTS <TEST_DB_NAME>;

CREATE DATABASE <TEST_DB_NAME>
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'C'
    LC_CTYPE = 'C'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

ALTER DEFAULT PRIVILEGES FOR ROLE postgres REVOKE ALL ON TABLES FROM postgres;

ALTER DEFAULT PRIVILEGES FOR ROLE postgres
GRANT DELETE, INSERT, REFERENCES, SELECT, TRIGGER, TRUNCATE, UPDATE ON TABLES TO postgres;

ALTER DEFAULT PRIVILEGES FOR ROLE postgres
GRANT TRUNCATE ON TABLES TO test_default_priv_user;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres
GRANT MAINTAIN ON TABLES TO test_default_priv_user WITH GRANT OPTION;

ALTER DEFAULT PRIVILEGES FOR ROLE postgres
GRANT UPDATE ON SEQUENCES TO test_default_priv_user WITH GRANT OPTION;

ALTER DEFAULT PRIVILEGES FOR ROLE postgres
GRANT EXECUTE ON FUNCTIONS TO test_default_priv_user WITH GRANT OPTION;

ALTER DEFAULT PRIVILEGES FOR ROLE postgres
GRANT USAGE ON TYPES TO test_default_priv_user WITH GRANT OPTION;
