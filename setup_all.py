import pandas as pd
import sqlite3

# Function to execute an SQL file
def execute_sql_file(conn, file_path):
    with open(file_path, 'r') as file:
        sql_script = file.read()
    conn.executescript(sql_script)

# Function to insert DataFrame into SQLite in smaller chunks
def df_to_sqlite(df, conn, table_name, chunksize=100):
    for i in range(0, len(df), chunksize):
        df.iloc[i:i+chunksize].to_sql(table_name, conn, if_exists='append', index=False)

# Path to your SQL and CSV files
sql_file_path = 'schema.sql'
csv_file_path1 = 'data_sources/spotify_albums.csv'
csv_file_path2 = 'data_sources/spotify_artists.csv'
csv_file_path3 = 'data_sources/spotify_tracks.csv'

# Connect to SQLite database (or create if it doesn't exist)
conn = sqlite3.connect('music.db')

# Execute the SQL script to create the schema
execute_sql_file(conn, sql_file_path)

# Read the CSV file into a pandas DataFrame
# Specify which columns to import
desired_columns1 = ['album_type', 'artist_id', 'id', 'name', 'release_date', 'total_tracks']
df1 = pd.read_csv(csv_file_path1, usecols=desired_columns1)
desired_columns2 = ['genres', 'id', 'name']
df2 = pd.read_csv(csv_file_path2, usecols=desired_columns2)
desired_columns3 = ['album_id', 'artists_id', 'duration_ms', 'id', 'name', 'track_number', 'popularity']
df3 = pd.read_csv(csv_file_path3, usecols=desired_columns3)

# Convert genres and artists_id from string representation of list to a string
df2['genres'] = df2['genres'].apply(lambda x: ','.join(eval(x)) if isinstance(x, str) and x.startswith('[') else x)
df3['artists_id'] = df3['artists_id'].apply(lambda x: ','.join(eval(x)) if isinstance(x, str) and x.startswith('[') else x)

# Insert the data into the database table in smaller chunks
df_to_sqlite(df1, conn, 'albums', chunksize=100) # Adjust the chunksize as necessary
df_to_sqlite(df2, conn, 'artists', chunksize=100)
df_to_sqlite(df3, conn, 'tracks', chunksize=100)

# # Track to Album table
# df4 = pd.read_sql_query("SELECT t.id as track_id, t.name as track_name, t.duration_ms as track_duration, t.track_number as track_number, al.id as album_id, al.name as album_name, al.release_date as album_release_date, al.total_tracks as album_total_tracks FROM tracks t, albums al WHERE t.album_id = al.id", conn)
# df_to_sqlite(df4, conn, 'track_album', chunksize=100)

# # Album to Genre table
# df5 = pd.read_sql_query("SELECT al.id as album_id, al.name as album_name, al.release_date as album_release_date, al.total_tracks as album_total_tracks, ar.genres as genres FROM albums al, artists ar WHERE al.artist_id = ar.id", conn)
# df_to_sqlite(df5, conn, 'album_genre', chunksize=100)

# # Track to Artist table
# df6 = pd.read_sql_query("SELECT t.id as track_id, t.name as track_name, t.duration_ms as track_duration, t.track_number as track_number, ar.id as artist_id, ar.name as artist_name FROM tracks t, artists ar, albums al WHERE t.album_id = al.id and al.artist_id = ar.id", conn)
# df_to_sqlite(df6, conn, 'track_artist', chunksize=100)

# Close the database connection
conn.close()
