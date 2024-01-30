# Module 1 Solutions

## Question 1. Docker tags

```console
$ docker run --help | grep "Automatically remove the container when it exits"
      --rm                             Automatically remove the container when it exits
```

Solution: `--rm`

## Question 2. Docker run: version of wheel

```console
$ docker run -it python:3.9 bash
root@3f5de14e57f4:/# pip list | grep wheel
wheel      0.42.0
```

Solution: 0.42.0

## Question 3. Count records

```SQL
WITH stg_trips AS (
SELECT
    index,
    TO_CHAR(lpep_pickup_datetime, 'YYYY-MM-DD') AS start_date,
    TO_CHAR(lpep_dropoff_datetime, 'YYYY-MM-DD') AS end_date
FROM
    green_taxi_trips
)
SELECT
    COUNT(*)
FROM
    stg_trips
WHERE
    start_date = '2019-09-18'
    AND end_date = '2019-09-18'
```

Solution: 15612

## Question 4. Largest trip for each day

```SQL
WITH stg_trips AS (
SELECT
    index,
    TO_CHAR(lpep_pickup_datetime, 'YYYY-MM-DD') AS start_date,
    trip_distance
FROM
    green_taxi_trips
)

SELECT
    start_date,
    MAX(trip_distance)
FROM
    stg_trips
GROUP BY
    start_date
ORDER BY
    2 DESC
LIMIT
    1
```

Solution: 2019-09-26

## Question 5. Three biggest pickups

```SQL
-- Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown
-- Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?
WITH stg_trips AS (
    SELECT
        index,
        "PULocationID" AS pu_location_id,
        TO_CHAR(lpep_pickup_datetime, 'YYYY-MM-DD') AS start_date,
        total_amount
    FROM
        green_taxi_trips
), trip_totals AS (
    SELECT
        t.pu_location_id,
        SUM(total_amount) AS total_amount
    FROM
        stg_trips t
    GROUP BY
        1, t.start_date
    HAVING
        t.start_date = '2019-09-18'
    ORDER BY 2 DESC
), stg_zones AS (
    SELECT
        "LocationID" AS location_id,
        "Borough" AS borough,
        "Zone" AS zone
    FROM
        taxi_zones
    WHERE
        "Borough" != 'Unknown'
)

SELECT
    ROUND(SUM(total_amount)) AS total_amount,
    borough
FROM
    trip_totals t
JOIN
    stg_zones s
ON
    t.pu_location_id = s.location_id
GROUP BY
    2
ORDER BY
    1 DESC
LIMIT
    3
```

Solution: "Brooklyn" "Manhattan" "Queens"

## Question 6. Largest trip

```SQL
-- For the passengers picked up in September 2019 in the zone name Astoria
-- which was the drop off zone that had the largest tip?
-- We want the name of the zone, not the id.
WITH stg_taxi_zones AS (
    SELECT
        "LocationID" AS location_id,
        "Borough" AS borough,
        "Zone" AS zone
    FROM
        taxi_zones
), stg_trips AS (
    SELECT
        "PULocationID" AS pu_location_id,
        "DOLocationID" AS do_location_id,
        TO_CHAR(lpep_pickup_datetime, 'YYYY-MM-DD') AS start_date,
        tip_amount
    FROM
        green_taxi_trips
)

SELECT
    pu_zone.zone AS pu_zone,
    do_zone.zone AS do_zone,
    tip_amount
FROM
    stg_trips t
JOIN
    stg_taxi_zones pu_zone
ON
    t.pu_location_id = pu_zone.location_id
JOIN
    stg_taxi_zones do_zone
ON
    t.do_location_id = do_zone.location_id
WHERE
    start_date LIKE '2019-09-%'
    AND pu_zone.zone = 'Astoria'
ORDER BY
    tip_amount DESC
LIMIT 1
```

Solution: JFK Airport

## Question 7. Terraform

Solution:

```console
$ terraform apply

Terraform used the selected providers to generate the following execution plan. Resource
actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.demo_dataset will be created
  + resource "google_bigquery_dataset" "demo_dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "demo_dataset"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = false
      + effective_labels           = (known after apply)
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "US"
      + max_time_travel_hours      = (known after apply)
      + project                    = "data-zoomcamp-2024"
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
      + terraform_labels           = (known after apply)
    }

  # google_storage_bucket.demo-bucket will be created
  + resource "google_storage_bucket" "demo-bucket" {
      + effective_labels            = (known after apply)
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "US"
      + name                        = "terraform-demo-terra-bucket-13024"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + rpo                         = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = (known after apply)
      + uniform_bucket_level_access = (known after apply)
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "AbortIncompleteMultipartUpload"
            }
          + condition {
              + age                   = 1
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_bigquery_dataset.demo_dataset: Creating...
google_storage_bucket.demo-bucket: Creating...
google_bigquery_dataset.demo_dataset: Creation complete after 1s [id=projects/data-zoomcamp-2024/datasets/demo_dataset]
google_storage_bucket.demo-bucket: Creation complete after 1s [id=terraform-demo-terra-bucket-13024]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```
