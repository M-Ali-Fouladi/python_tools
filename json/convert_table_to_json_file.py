import sqlite3
import json

# Connect to the SQLite database
conn = sqlite3.connect('mydatabase.db')  # Replace 'mydatabase.db' with your database file

# Create a cursor
cursor = conn.cursor()

# Execute a query to select data from the table
cursor.execute('SELECT * FROM mytable')  # Replace 'mytable' with your table name

# Fetch all the rows as a list of dictionaries
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
data = [dict(zip(columns, row)) for row in rows]

# Close the cursor and the database connection
cursor.close()
conn.close()

# Convert the data to a JSON object
json_data = json.dumps(data, indent=4)

# Write the JSON data to a file
with open('data.json', 'w') as json_file:
    json_file.write(json_data)

print("Data extracted and saved to 'data.json'.")