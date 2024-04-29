import sqlite3
import pandas as pd
from tabulate import tabulate

# Reconnect to your SQLite database
conn = sqlite3.connect('music.db')

pd.set_option('display.max_columns', None)

# Execute a query to retrieve some rows
# df1 = pd.read_sql_query("SELECT artist_id, album_type, id as album_id, name FROM albums LIMIT 10", conn)
# df2 = pd.read_sql_query("SELECT id as artist_id, name, genres FROM artists LIMIT 10", conn)
# df3 = pd.read_sql_query("SELECT artists_id, id as track_id, album_id, name FROM tracks LIMIT 10", conn)
# df4 = pd.read_sql_query("SELECT t.name as track_name, al.name as album_name, ar.name as artist_name FROM tracks t, albums al, artists ar WHERE t.album_id = al.id and al.artist_id = ar.id LIMIT 20", conn)

# Songs by Madonna that were released after the year 1999 sorted by popularity
df1 = pd.read_sql_query("""SELECT track_name, album_release_date
                            FROM all_tracks
                            WHERE (artist_name = 'Madonna' and STRFTIME('%Y', album_release_date) > '1999')
                            ORDER BY track_popularity DESC
                            LIMIT 10""", conn)

# All releases of Material Girl by Madonna, ordered by release date
df2 = pd.read_sql_query("""SELECT track_name, album_name, album_release_date
                            FROM all_tracks
                            WHERE (artist_name = 'Madonna' and track_name = 'Material Girl')
                            ORDER BY STRFTIME('%Y', album_release_date) ASC
                            """, conn)

# All tracks by Alvvays, ordered by release year
df3 = pd.read_sql_query("""SELECT track_name, STRFTIME('%Y', album_release_date) as year, track_popularity
                            FROM all_tracks
                            WHERE artist_name = 'Alvvays'
                            ORDER BY STRFTIME('%Y', album_release_date) ASC
                            """, conn)

# The most popular track by Alvvays
df4 = pd.read_sql_query("""SELECT track_name, MAX(track_popularity) as track_popularity, STRFTIME('%Y', album_release_date) as year
                            FROM all_tracks
                            WHERE artist_name = 'Alvvays'
                            """, conn)

# Top 10 most popular tracks by indie pop artists
df5 = pd.read_sql_query("""SELECT track_name, artist_name, album_name, STRFTIME('%Y', album_release_date) as year
                            FROM all_tracks
                            WHERE artist_genres LIKE '%indie pop%' or '%indie-pop%'
                            ORDER BY track_popularity DESC
                            LIMIT 10
                            """, conn)

# Display the results/DataFrames using tabulate
# Options: can choose a different format such as 'psql', 'html', 'latex', etc.
print(tabulate(df1, headers='keys', tablefmt='psql'))
print(tabulate(df2, headers='keys', tablefmt='psql'))
print(tabulate(df3, headers='keys', tablefmt='psql'))
print(tabulate(df4, headers='keys', tablefmt='psql'))
print(tabulate(df5, headers='keys', tablefmt='psql'))

# Close the connection
conn.close()
