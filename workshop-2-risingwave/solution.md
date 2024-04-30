# Workshop 2 Solution

### Solution 0

```SQL
CREATE MATERIALIZED VIEW pickup_zone_of_last_dropoff AS
SELECT
  tpep_dropoff_datetime,
  tz.zone
FROM
  trip_data td
JOIN
  taxi_zone tz
ON
  td.dolocationid = tz.location_id
WHERE
  tpep_dropoff_datetime = (
    SELECT
      MAX(tpep_dropoff_datetime) AS last_dropoff_datetime
    FROM
      trip_data
  );

-- tpep_dropoff_datetime |      zone      
-- -----------------------+----------------
-- 2022-01-03 17:24:54   | Midtown Center
-- (1 row)
```

### Solution 1

- Yorkville East, Steinway

```SQL
CREATE MATERIALIZED VIEW agg_trip_data AS
WITH agg_trip_time AS (
SELECT
  pulocationid, 
  dolocationid,
  COUNT(*) AS trip_count,
  AVG(tpep_dropoff_datetime - tpep_pickup_datetime) AS avg_trip_time,
  MIN(tpep_dropoff_datetime - tpep_pickup_datetime) AS min_trip_time,
  MAX(tpep_dropoff_datetime - tpep_pickup_datetime) AS max_trip_time
FROM
  trip_data td
GROUP BY
  1,2
)
SELECT
  putz.zone AS pu_zone,
  dotz.zone AS do_zone,
  avg_trip_time,
  min_trip_time,
  max_trip_time
FROM
  agg_trip_time att
JOIN
  taxi_zone putz
ON
  att.pulocationid = putz.location_id
JOIN
  taxi_zone dotz
ON
  att.dolocationid = dotz.location_id
ORDER BY
  avg_trip_time DESC
LIMIT
  1;

SELECT * FROM agg_trip_data;

--     pu_zone     | do_zone  | avg_trip_time | min_trip_time | max_trip_time 
-- ----------------+----------+---------------+---------------+---------------
--  Yorkville East | Steinway | 23:59:33      | 23:59:33      | 23:59:33
-- (1 row)
```

```SQL
-- Bonus (no marks): Create an MV which can identify anomalies in the data. For example, if the average trip time between two zones is 1 minute, but the max trip time is 10 minutes and 20 minutes respectively.

```

### Solution 2

- 1

```SQL
CREATE MATERIALIZED VIEW agg_trip_data AS
WITH agg_trip_time AS (
SELECT
  pulocationid, 
  dolocationid,
  COUNT(*) AS trip_count,
  AVG(tpep_dropoff_datetime - tpep_pickup_datetime) AS avg_trip_time,
  MIN(tpep_dropoff_datetime - tpep_pickup_datetime) AS min_trip_time,
  MAX(tpep_dropoff_datetime - tpep_pickup_datetime) AS max_trip_time
FROM
  trip_data td
GROUP BY
  1,2
)
SELECT
  putz.zone AS pu_zone,
  dotz.zone AS do_zone,
  trip_count,
  avg_trip_time,
  min_trip_time,
  max_trip_time
FROM
  agg_trip_time att
JOIN
  taxi_zone putz
ON
  att.pulocationid = putz.location_id
JOIN
  taxi_zone dotz
ON
  att.dolocationid = dotz.location_id
ORDER BY
  avg_trip_time DESC
LIMIT
  1;

SELECT * FROM agg_trip_data;

--     pu_zone     | do_zone  | trip_count | avg_trip_time | min_trip_time | max_trip_time 
-- ----------------+----------+------------+---------------+---------------+---------------
--  Yorkville East | Steinway |          1 | 23:59:33      | 23:59:33      | 23:59:33
-- (1 row)
```

### Solution 3

- LaGuardia Airport, Lincoln Square East, JFK Airport

```SQL
CREATE MATERIALIZED VIEW last_17_hours_pickups AS
WITH last_pickup_datetime AS (
SELECT
  MAX(tpep_pickup_datetime) AS last_pickup_datetime
 FROM
  trip_data td
)
SELECT
  pulocationid,
  COUNT(*)
FROM
  trip_data, last_pickup_datetime  
WHERE
  tpep_pickup_datetime >= last_pickup_datetime - INTERVAL '17 hours'
GROUP BY
  1
ORDER BY
  2 DESC
LIMIT
  3;

SELECT
  count,
  zone
FROM last_17_hours_pickups l 
JOIN taxi_zone t 
ON l.pulocationid = t.location_id;

--  count |        zone         
-- -------+---------------------
--     19 | LaGuardia Airport
--     17 | JFK Airport
--     17 | Lincoln Square East
-- (3 rows)
```
