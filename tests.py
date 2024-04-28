import sqlite3
import pandas as pd

# Reconnect to your SQLite database
conn = sqlite3.connect('music.db')

# Execute a query to retrieve some rows
df1 = pd.read_sql_query("SELECT artist_id, album_type, id as album_id, name FROM albums LIMIT 10", conn)
df2 = pd.read_sql_query("SELECT id as artist_id, name, genres FROM artists LIMIT 10", conn)
df3 = pd.read_sql_query("SELECT artists_id, id as track_id, album_id, name FROM tracks LIMIT 10", conn)

# Display the results
print(df1)
print(df2)
print(df3)

# Close the connection
conn.close()
