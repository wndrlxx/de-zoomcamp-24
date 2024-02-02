from pandas import DataFrame
import pyarrow as pa
import pyarrow.parquet as pq
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

# set the GCP environment variable on the Docker container
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/key.json"

project_id = 'data-zoomcamp-2024'
# NOTE: bucket must already exist or this will fail!!
bucket_name = '2024-02-01-green-taxi-mage'
folder = 'green_taxi'
root_path = f'{bucket_name}/{folder}'

@data_exporter
def export_parquet_to_google_cloud_storage(df: DataFrame, **kwargs) -> None:
    # Construct a pyarrow.Table from pandas DataFrame
    table = pa.Table.from_pandas(df)

    # Solution to Question 6
    # NOTE: `+1` to count the root folder
    print(df['lpep_pickup_date'].unique().size + 1)

    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=['lpep_pickup_date'],
        filesystem=pa.fs.GcsFileSystem()
    )