import pandas as pd
import inflection

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    # Remove rows where the passenger count is equal to 0
    # or the trip distance is equal to zero.
    filters = (data["passenger_count"] > 0) & (data["trip_distance"] > 0)

    # Solution to Question 2
    print(f'{filters.sum()} rows left')

    # Create a new column `lpep_pickup_date` by converting
    # `lpep_pickup_datetime` to a date.
    data["lpep_pickup_date"] = data["lpep_pickup_datetime"].dt.date

    # Solution to Question 4
    vendor_ids = data['VendorID'].dropna().unique().tolist()
    print(f"The unique values in `VendorID` are: {vendor_ids}")

    # Solution to Question 5
    regx = data.columns.str.match(r'^[A-Z]')
    num = pd.Series(data.columns[regx]).count()
    print(f'{num} columns to rename to snake case')

    # Rename columns in Camel Case to Snake
    data.rename(columns=inflection.underscore, inplace=True)

    df_final = data.loc[filters]

    return df_final


@test
def test_vendor_id_col_present(output, *args) -> None:
    fail_msg = "`vendor_id` should be a column"
    assert "vendor_id" in output.columns, fail_msg


@test
def test_passenger_count_greater_than_0(output, *args) -> None:
    fail_msg = "There are rows with `passenger_count` of 0"
    assert not (output["passenger_count"] == 0).any(), fail_msg


@test
def test_trip_distance_greater_than_0(output, *args) -> None:
    fail_msg = "There are rows with `trip_distance` of 0"
    assert not (output["trip_distance"] == 0).any(), fail_msg
