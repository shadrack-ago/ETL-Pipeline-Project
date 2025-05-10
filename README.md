MySQL to DuckDB Pipeline Guide
=============================

Prerequisites:
- Python 3.10+
- MySQL Workbench installed
- Terminal/Command Prompt access
- Code Editor (VScode)

Step 0: Virtual Environment Setup
--------------------------------
# Create and activate virtual environment
After installing Python (cd to your prefered project folder, then run>

pip install uv 

python -m venv .venv       # to create virt environment

.\venv\Scripts\activate   # to activate on Windows

source venv/bin/activate  #for Linux/Mac

 Install dlt library
 
uv pip install -U dlt

 Done!

Step 1: Create dlt Project
-------------------------
# Initialize pipeline with DuckDB destination
dlt init sql_database duckdb

Step 2: Configure Pipeline Script
--------------------------------
File: sql_database_pipeline.py

import dlt
from dlt.sources.sql_database import sql_database

def load_mysql_to_duckdb():
    # Load ALL tables (or specify with .with_resources())
    source = sql_database()
    
    pipeline = dlt.pipeline(
        pipeline_name="mysql_to_duckdb", # Change name if needed
        destination="duckdb",
        dataset_name="mysql_data" # Determines output filename
    )
    
    # Run with replace disposition (options: replace/append/merge)
    load_info = pipeline.run(source, write_disposition="replace")
    print(load_info) 
    
    if __name__ == "__main__":
     load_mysql_to_duckdb()  

  

Step 3: Add MySQL Credentials
----------------------------
File: .dlt/secrets.toml

[sources.sql_database.credentials]
drivername = "mysql+pymysql"
database = "salesdb"       # Your database name
username = "root"         # MySQL username
password = "your_password" # MySQL password
host = "localhost"        # Change if remote DB
port = 3306               # Default MySQL port

Step 4: Install Dependencies
---------------------------
# Core packages
pip install dlt
pip install -r requirements.txt
pip install pymysql

Step 5: Run Pipeline
-------------------
# Execute the pipeline
python sql_database_pipeline.py

Expected Output:
- Creates mysql_data.duckdb file
- Prints loaded tables and row counts

Step 6: Explore Data
-------------------
# Query DuckDB directly
duckdb mysql_data.duckdb

DuckDB Commands:
SHOW TABLES;               # List tables
SELECT * FROM orders LIMIT 5; # Sample query
.exit                      # Quit shell

# dlt inspection commands
dlt pipeline mysql_to_duckdb info    # View pipeline state
dlt pipeline mysql_to_duckdb schema  # Show table schemas

Step 7: Modify Loading Behavior
------------------------------
Options for pipeline.run():

1. Full Refresh (default):
write_disposition="replace"

2. Append New Data:
write_disposition="append"

3. Incremental Load:
source.table_name.apply_hints(
    incremental=dlt.sources.incremental("date_column")
)

4. Merge Updates:
write_disposition="merge"

Advanced Options:
- chunk_size=1000 # For large tables
- backend="pyarrow" # Faster for numeric data

Troubleshooting
---------------
# Common fixes:
1. MySQL connection failed:
   - Verify service is running
   - Check credentials in secrets.toml

2. Missing tables:
   - Ensure tables exist in MySQL
   - Check schema permissions

3. Pipeline errors:
   dlt pipeline mysql_to_duckdb sync # Repair state
   dlt pipeline list # Verify pipeline exists

GitHub Integration
-----------------
# To run from your GitHub repo:
git clone [https://github.com/your/repo.git](https://github.com/shadrack-ago/ETL-Pipeline-Project.git)
cd repo
pip install -r requirements.txt
python sql_database_pipeline.py

Dashboard deployed at (https://etl-pipeline-project-gmxxuve2xfyatytxq42jn5.streamlit.app)

Notes:
- Store secrets.toml in .gitignore
- For production: Use environment variables for credentials
