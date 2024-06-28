import pandas as pd
import psycopg2

# Step 1: Read the Excel file with correct headers
csv_file_path = r'C:\Users\Salim\Downloads\GRNShift-Navigator\backend\Data\Sustainable Technology Database.xlsx'
data = pd.read_excel(csv_file_path, header=1)

# Strip leading and trailing spaces from column names
data.columns = data.columns.str.strip()

# Display the columns to confirm the structure
print("Columns after stripping:", data.columns)
print("First few rows of the data:\n", data.head())

# Step 2: Connect to PostgreSQL
dbname = 'postgres'
user = 'postgres'
password = 'Grnshift'
host = 'database-2.ctwgq2kqgrl6.us-east-2.rds.amazonaws.com'
port = '5432'  # Default is 5432

conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
cur = conn.cursor()

# Step 3: Create table (if necessary)
create_table_query = """
CREATE TABLE IF NOT EXISTS sustainable_technology (
    id SERIAL PRIMARY KEY,
    brand TEXT,
    model TEXT,
    product_sku TEXT,
    applications TEXT,
    unit_price TEXT,
    payment_plans TEXT,
    warranty TEXT,
    solar_cells TEXT,
    cell_configuration TEXT,
    rated_power TEXT,
    cell_efficiency TEXT,
    operating_temperature TEXT,
    weight TEXT,
    height TEXT,
    width TEXT,
    length TEXT,
    open_circuit_voltage_voc TEXT,
    maximum_power_voltage TEXT,
    temp_coefficient_of_voc TEXT,
    cable_length TEXT,
    front_surface TEXT,
    back_cover TEXT
);
"""
cur.execute(create_table_query)
conn.commit()

# Step 4: Insert data
insert_query = """
INSERT INTO sustainable_technology (
    brand, model, product_sku, applications, unit_price, payment_plans, warranty, 
    solar_cells, cell_configuration, rated_power, cell_efficiency, operating_temperature,
    weight, height, width, length, open_circuit_voltage_voc, maximum_power_voltage, 
    temp_coefficient_of_voc, cable_length, front_surface, back_cover) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""



# Debugging step: print first few rows to confirm data
print("Data to be inserted:\n", data.head())

# Ensure the column names are correct
expected_columns = [
    'Brand', 'Model', 'Product SKU', 'Applications', 'Unit Price', 'Payment Plans',
    'Warranty', 'Solar Cells', 'Cell Configuration', 'Rated Power', 'Cell Efficiency',
    'Operating Temperature', 'Weight', 'Height', 'Width', 'Length',
    'Open Circuit Voltage - VOC', 'Maximum Power Voltage', 'Temp Coefficient of VOC',
    'Cable Length', 'Front Surface', 'Back Cover'
]

if not all(col in data.columns for col in expected_columns):
    print("Error: DataFrame does not contain expected columns.")
    print("Expected columns:", expected_columns)
    print("Actual columns:", data.columns)
else:
    for index, row in data.iterrows():
        try:
            cur.execute(insert_query, (
                row['Brand'], row['Model'], row['Product SKU'], row['Applications'], row['Unit Price'], row['Payment Plans'], 
                row['Warranty'], row['Solar Cells'], row['Cell Configuration'], row['Rated Power'], row['Cell Efficiency'], 
                row['Operating Temperature'], row['Weight'], row['Height'], row['Width'], row['Length'], 
                row['Open Circuit Voltage - VOC'], row['Maximum Power Voltage'], row['Temp Coefficient of VOC'], 
                row['Cable Length'], row['Front Surface'], row['Back Cover']
            ))
        except Exception as e:
            print(f"Error inserting row {index}: {e}")
            print(row)
            # Print out the specific value causing the error if possible
            for col in expected_columns:
                print(f"{col}: {row[col]}")

    conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
