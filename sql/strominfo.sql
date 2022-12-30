\set ON_ERROR_STOP on
\set QUIET 1
set client_encoding='unicode';
set client_min_messages='warning';
BEGIN;
CREATE SCHEMA IF NOT EXISTS strominfo;
ALTER DATABASE strominfo SET search_path TO strominfo;
SET search_path TO strominfo;

-- \i functions.sql
\i schema.sql
-- \i triggers.sql
-- \i foreign_keys.sql
-- \i views.sql
-- \i defaultdata.sql
-- \i indexes.sql
\i default_values.sql

COMMIT;
