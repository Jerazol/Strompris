\echo --> *************************** <--
\echo --> Creating main tables
\echo --> *************************** <--

\echo -->     Creating table entsoe_spotprice
CREATE TABLE IF NOT EXISTS entsoe_spotprice (
  start_time  TIMESTAMP WITH TIME ZONE,
  end_time    TIMESTAMP WITH TIME ZONE,
  zone        CHAR(16),
  value       NUMERIC(10,8),
  PRIMARY KEY (start_time)
);


\echo -->     Creating table ffail_spotprice
CREATE TABLE IF NOT EXISTS ffail_spotprice (
  start_time  TIMESTAMP WITH TIME ZONE,
  end_time    TIMESTAMP WITH TIME ZONE,
  value       NUMERIC(10,8),
  PRIMARY KEY (start_time)
);


\echo -->     Creating table power_consumption
CREATE TABLE IF NOT EXISTS power_consumption (
  start_time  TIMESTAMP WITH TIME ZONE,
  end_time    TIMESTAMP WITH TIME ZONE,
  value       NUMERIC(10,8),
  PRIMARY KEY (start_time)
);


\echo -->     Creating table easee_chargerusage
CREATE TABLE IF NOT EXISTS easee_chargerusage (
  start_time  TIMESTAMP WITH TIME ZONE,
  end_time    TIMESTAMP WITH TIME ZONE,
  value       NUMERIC(10,8),
  PRIMARY KEY (start_time)
);


\echo -->     Creating table stromstotte
CREATE TABLE IF NOT EXISTS stromstotte (
    stotte_year smallint NOT NULL,
    stotte_month smallint NOT NULL,
    percent smallint,
    PRIMARY KEY (stotte_year, stotte_month)
);
