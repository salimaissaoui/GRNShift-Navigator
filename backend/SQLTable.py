import pandas as pd
import psycopg2

# Step 1: Read the Excel file
file_path = r'C:\Users\Salim\Downloads\GRNShift-Navigator\backend\Data\Sustainable Technology Database.xlsx'
data = pd.read_excel(file_path)

# Step 2: Connect to PostgreSQL
dbname = 'postgres'
user = 'postgres'
password = 'Green'
host = 'localhost'
port = '5432'  # Default is 5432

conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
cur = conn.cursor()

# Step 3: Create table (if necessary)
create_table_query = """
CREATE TABLE IF NOT EXISTS sustainable_technology (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT
);
"""
cur.execute(create_table_query)
conn.commit()

# Step 4: Insert data
insert_query = """
INSERT INTO sustainable_technology (technology, category, description) VALUES (%s, %s, %s);
"""

for index, row in data.iterrows():
    cur.execute(insert_query, (row['Technology'], row['Category'], row['Description']))

conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
