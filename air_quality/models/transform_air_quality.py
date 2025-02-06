import pandas as pd
from datetime import datetime

def model(dbt, session):
# Transformations:
#     1. Converts Unix timestamp to date and time columns
#     2. Adds AQI category labels based on AQI values

    # Configure as a table materialization
    dbt.config(
        materialized="table",
        packages=["pandas"]
    )
    
    # Load raw data from Snowflake
    df = session.table("raw_air_pollution_data").to_pandas()
    
    # Split datetime into date and time columns
    df['Datetime'] = pd.to_datetime(df['MEASUREMENT_DATE'], unit='s')
    df['MEASUREMENT_DATE'] = df['Datetime'].dt.date
    df['Time'] = df['Datetime'].dt.time
    df.drop('Datetime', axis=1, inplace=True)
    
    # Define AQI category mapping
    aqi_categories = {
        1: 'Good',
        2: 'Fair',
        3: 'Moderate',
        4: 'Poor',
        5: 'Very Poor',
        6: 'Hazardous'
    }
    
    # Add AQI category labels
    df['aqi_category'] = df['AQI'].map(aqi_categories).fillna('Unknown')
    
    # Convert back to Snowflake DataFrame
    transformed_df = session.create_dataframe(df)
    
    return transformed_df