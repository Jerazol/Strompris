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
