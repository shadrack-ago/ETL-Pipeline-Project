import dlt
from dlt.sources.sql_database import sql_database

def load_entire_salesdb():
    # Create a dlt source that loads ALL tables from salesdb
    source = sql_database()  # No .with_resources() loads all tables

    # Create pipeline
    pipeline = dlt.pipeline(
        pipeline_name="salesdb_to_duckdb",
        destination="duckdb",
        dataset_name="salesdb_data"
    )

    # Run with replace disposition (overwrites existing data)
    load_info = pipeline.run(source, write_disposition="replace")
    
    # Print load info
    print(load_info)
    print(f"Loaded tables: {list(pipeline.default_schema.tables.keys())}")

if __name__ == '__main__':
    load_entire_salesdb()