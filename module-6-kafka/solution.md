# Module 6

## Solution 1

```console
$ rpk version
v22.3.5 (rev 28b2443)
```

## Solution 2

```console
$ rpk topic create test-topic
TOPIC       STATUS
test-topic  OK
```

## Solution 3

```console
In [7]: producer.bootstrap_connected()
Out[7]: True
```

## Solution 4

- Sending the messages

```python
send_start = time.time()
topic_name = 'test-topic'

for i in range(10):
    message = {'number': i}
    producer.send(topic_name, value=message)
    print(f"Sent: {message}")
    time.sleep(0.05)

send_stop = time.time()
flush_start = time.time()
producer.flush()
flush_stop = time.time()
print(f'send took {(send_stop - send_start):.2f} seconds')
print(f'flush took {(flush_stop - flush_start):.2f} seconds')
# send took 0.54 seconds
# flush took 0.00 seconds
```

## Solution 5

- 22 seconds

```console
$ rpk topic create green-trips
TOPIC        STATUS
green-trips  OK
```

```python
start = time.time()

for row in df_green.itertuples(index=False):
    row_dict = {col: getattr(row, col) for col in row._fields}
    message = row_dict
    producer.send("green-trips", value=message)
    # break

end = time.time()

producer.flush()

print(f'send took {round(end - start)} seconds')

# send took 22 seconds
```

## Solution 6

```shell
Row(lpep_pickup_datetime='2019-10-01 00:26:02', lpep_dropoff_datetime='2019-10-01 00:39:58', PULocationID=112, DOLocationID=196, passenger_count=1.0, trip_distance=5.88, tip_amount=0.0)
```

## Solution 7

- 74