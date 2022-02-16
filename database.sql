DROP TABLE pricing.spotprice;
CREATE TABLE pricing.spotprice (
  price_hour    TIMESTAMP WITH TIME ZONE,
  price         NUMERIC(10,8),
  valid_from    TIMESTAMP WITH TIME ZONE,
  valid_to      TIMESTAMP WITH TIME ZONE,
  PRIMARY KEY (price_hour)
);


DROP TABLE usage.hourlyusage;
CREATE TABLE usage.hourlyusage (
  start_time    TIMESTAMP WITH TIME ZONE,
  usage         NUMERIC(10,8),
  end_time      TIMESTAMP WITH TIME ZONE,
  PRIMARY KEY (start_time)
);




CREATE OR REPLACE FUNCTION monthly_cost(year integer, month integer, rebate integer)
RETURNS TABLE (
  usage NUMERIC,strompris NUMERIC,nettleie NUMERIC,rabatt NUMERIC,strom_total NUMERIC,totalt NUMERIC
)
AS $$
SELECT
  round(sum(usage),2) usage,
  round(sum(usage_price),2) strompris,
  round(sum(nettleie),2) nettleie,
  round(sum(tot_rabatt),2) rabatt,
  round(sum(hourly_price),2) strom_total,
  round(sum(hourly_price)*1.25+sum(nettleie) + 29+115, 2) AS totalt
FROM (
  SELECT
    price_hour,
    price,
    usage,
    usage_price,
    nettleie,
    rabatt_per_kw,
    tot_rabatt,
    usage_price-tot_rabatt AS hourly_price
  FROM (
    SELECT
      price_hour,
      price,
      usage,
      (price+0.0599)*usage AS usage_price,
      usage*0.448 AS nettleie,
      GREATEST((price-0.70),0)*((cast ($3 as numeric))/100) AS rabatt_per_kw,
      GREATEST((price-0.70),0)*((cast ($3 as numeric))/100)*usage AS tot_rabatt
    FROM
      spotprice LEFT JOIN
      hourlyusage ON (price_hour=start_time)
    WHERE
      price_hour >= make_timestamptz($1, $2, 1, 0, 0, 0) AND
      price_hour < make_timestamptz($1, $2, 1, 0, 0, 0)+INTERVAL '1 month'
  ) AS hourly_pricing
) AS foo;$$
LANGUAGE SQL
IMMUTABLE;


CREATE OR REPLACE FUNCTION monthly_cost(year integer, month integer, rebate numeric, monthly_avg numeric)
RETURNS TABLE (
  usage NUMERIC,strompris NUMERIC,nettleie NUMERIC,rabatt NUMERIC,strom_total NUMERIC,totalt NUMERIC
)
AS $$
SELECT
  round(sum(usage),2) usage,
  round(sum(usage_price),2) strompris,
  round(sum(nettleie),2) nettleie,
  round(sum(tot_rabatt),2) rabatt,
  round(sum(hourly_price),2) strom_total,
  round(sum(hourly_price)*1.25+sum(nettleie) + 29+115, 2) AS totalt
FROM (
  SELECT
    price_hour,
    price,
    usage,
    usage_price,
    nettleie,
    rabatt_per_kw,
    tot_rabatt,
    usage_price-tot_rabatt AS hourly_price
  FROM (
    SELECT
      price_hour,
      price,
      usage,
      (price+0.0599)*usage AS usage_price,
      usage*0.448 AS nettleie,
      ($4 - 0.70)*($3/100) AS rabatt_per_kw,
      ($4 - 0.70)*($3/100)*usage AS tot_rabatt
    FROM
      spotprice LEFT JOIN
      hourlyusage ON (price_hour=start_time)
    WHERE
      price_hour >= make_timestamptz($1, $2, 1, 0, 0, 0) AND
      price_hour < make_timestamptz($1, $2, 1, 0, 0, 0)+INTERVAL '1 month'
  ) AS hourly_pricing
) AS foo;$$
LANGUAGE SQL
IMMUTABLE;

CREATE OR REPLACE FUNCTION monthly_avg(year INTEGER, month INTEGER)
RETURNS NUMERIC
AS $$
SELECT avg(price)
FROM spotprice
WHERE
  price_hour >= make_timestamptz($1, $2, 1, 0, 0, 0) AND
  price_hour < make_timestamptz($1, $2, 1, 0, 0, 0)+INTERVAL '1 month';

$$
LANGUAGE SQL
IMMUTABLE;
