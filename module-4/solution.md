# Module 4

## Solution 1

What happens when we execute `dbt build --vars '{'is_test_run':'true'}'`

- It applies a limit 100 only to our staging models

## Solution 2

What is the code that our CI job will run?

- The code from a development branch requesting a merge to main

## Solution 3

What is the count of records in the model `fact_fhv_trips` after running all dependencies with the test run variable disabled (:false)?

- 22998722

```SQL
SELECT
  COUNT(*)
FROM
  production.fct_fhv_trips

-- 23014060
```

## Solution 4

What is the service that had the most rides during the month of July 2019 month with the biggest amount of rides after building a tile for the `fact_fhv_trips` table?

- Yellow

[View Dashboard](https://lookerstudio.google.com/reporting/e21ae513-5d9e-42e3-a2bf-0539cbaa5696/page/gH9pD)
