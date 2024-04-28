import sqlite3
import pandas as pd

# Reconnect to your SQLite database
conn1 = sqlite3.connect('albums.db')
conn2 = sqlite3.connect('artists.db')
conn3 = sqlite3.connect('tracks.db')

# Execute a query to retrieve some rows
df1 = pd.read_sql_query("SELECT artist_id, album_type, id as album_id, name FROM albums LIMIT 10", conn1)
df2 = pd.read_sql_query("SELECT id as artist_id, name, genres FROM artists LIMIT 10", conn2)
df3 = pd.read_sql_query("SELECT artists_id, id as track_id, album_id, name FROM tracks LIMIT 10", conn3)

# Display the results
print(df1)
print(df2)
print(df3)

# Close the connection
conn1.close()
conn2.close()
conn3.close()
