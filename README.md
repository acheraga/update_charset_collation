## Explanation
This Python script helps manage database foreign keys (including composite keys) during a collation change process. Here's how it works:

### Export Foreign Keys:

Connects to your MySQL database
Retrieves all foreign key constraints from INFORMATION_SCHEMA
Handles composite keys by grouping columns that belong to the same constraint
Stores the complete definition of each foreign key including table names, column names, and referenced columns


### Drop Foreign Keys:

Removes all foreign key constraints from their respective tables
This is necessary because changing collation with foreign keys in place can cause issues
Each constraint is dropped individually using ALTER TABLE statements


### Change Collation:

Changes the collation of all tables to the specified collation (default: utf8mb4_unicode_ci)
Converts each table's character set and collation
Also updates the collation for individual text/string columns (VARCHAR, TEXT, etc.)


### Restore Foreign Keys:

Recreates all the foreign key constraints using the definitions stored in step 1 
For composite keys, it correctly includes all columns in the constraint

## installation
This approach ensures that changing the collation of your database won't cause problems with foreign key constraints, especially when dealing with composite keys (foreign keys that involve multiple columns).
To use this script, you'll need to:

- Install the mysql-connector-python package (pip install mysql-connector-python SQLAlchemy)
- Update the database connection parameters in engine = create_engine('mysql+pymysql://....
- Optionally modify the collation :
  - new_collation="utf8mb4_unicode_ci"
  - new_charset="utf8mb4"   

