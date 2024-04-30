# Module 3 Solutions

### Question 1

Solution: 840,402

```SQL
SELECT
    COUNT(*)
FROM
    nytaxi.external_green_tripdata
```

### Question 2

Solution: 0 MB for the External Table and 6.41MB for the Materialized Table

```SQL
-- This query will process 0 B when run.
SELECT
  COUNT(DISTINCT `PULocationID`)
FROM
  nytaxi.external_green_tripdata

-- This query will process 6.41 MB when run.
SELECT
  COUNT(DISTINCT `PULocationID`)
FROM
  nytaxi.green_tripdata_non_partitioned
```

### Question 3

Solution: 1,622

```SQL
SELECT
  COUNT(*)
FROM
  nytaxi.green_tripdata_non_partitioned
WHERE
  fare_amount = 0
```

### Question 4

Solution: Partition by `lpep_pickup_datetime` Cluster on `PUlocationID`

### Question 5

Solution: 12.82 MB for non-partitioned table and 1.12 MB for the partitioned table

```SQL
# non-partitioned table
# "This query will process 12.82 MB when run."
SELECT
  COUNT(DISTINCT `PULocationID`)
FROM
  nytaxi.green_tripdata_non_partitioned
WHERE
  DATE(lpep_pickup_datetime) BETWEEN '2022-06-01'
  AND '2022-06-30'

# partitioned table
# "This query will process 1.12 MB when run."
SELECT
  COUNT(DISTINCT `PULocationID`)
FROM
  nytaxi.green_tripdata_partitioned_clustered
WHERE
  DATE(lpep_pickup_datetime) BETWEEN '2022-06-01'
  AND '2022-06-30'
```

### Question 6

Solution: GCP Bucket

### Question 7

Solution: False
