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
    # Load data from the source
    # Run with append disposition (default)
    # load_info = pipeline.run(source)

    # Run with replace disposition (overwrites existing data)
    load_info = pipeline.run(source, write_disposition="replace")
    
    # Print load info
    print(load_info)
    print(f"Loaded tables: {list(pipeline.default_schema.tables.keys())}")

if __name__ == '__main__':
    load_entire_salesdb()



# For Loading data incrementally  (Ignore this section)

# import dlt
# from dlt.sources.sql_database import sql_database
# from sqlalchemy import inspect

# def get_incremental_columns(engine, table_name):
#     """Auto-detect timestamp/primary key columns for incremental loading"""
#     inspector = inspect(engine)
#     columns = inspector.get_columns(table_name)
#     incremental_candidates = [
#         col['name'] for col in columns 
#         if col['type'].python_type in (int, pendulum.DateTime)
#     ]
#     return incremental_candidates[:1]  # Use first candidate found

# def load_all_tables_incrementally():
#     # Initialize with SQLAlchemy engine to inspect tables
#     engine = sql_database().engine
#     inspector = inspect(engine)
    
#     # Load all tables
#     source = sql_database()
#     pipeline = dlt.pipeline(
#         pipeline_name="auto_incremental",
#         destination="duckdb",
#         dataset_name="sales_auto_incremental"
#     )

#     # Auto-configure incremental for each table
#     for table_name in inspector.get_table_names():
#         incremental_cols = get_incremental_columns(engine, table_name)
#         if incremental_cols:
#             resource = source.with_resources(table_name).resources[table_name]
#             resource.apply_hints(
#                 incremental=dlt.sources.incremental(incremental_cols[0])
#             )

#     # Run with append disposition
#     load_info = pipeline.run(source, write_disposition="append")
#     print(load_info)

# if __name__ == "__main__":
#     load_all_tables_incrementally()