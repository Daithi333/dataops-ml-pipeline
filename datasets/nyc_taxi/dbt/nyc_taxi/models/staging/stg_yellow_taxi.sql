select * from {{ source('nyc_taxi_raw', 'yellow_taxi_data') }}
