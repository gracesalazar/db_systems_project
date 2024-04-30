import sqlite3
import pandas as pd
from tabulate import tabulate

# Reconnect to your SQLite database
conn = sqlite3.connect('music.db')

# Set option to not cut off the output
pd.set_option('display.max_columns', None)

# Queries:

# Songs by Madonna that were released after the year 1999 sorted by popularity
df1 = pd.read_sql_query("""
                            SELECT t.name as track_name, al.release_date as album_release_date
                            FROM tracks t, albums al, artists ar
                            WHERE (ar.name = 'Madonna' and (STRFTIME('%Y', al.release_date) > '1999') 
                            and t.album_id = al.id and ar.id = al.artist_id)
                            ORDER BY t.popularity DESC
                            LIMIT 10""", conn)

# All releases of Material Girl by Madonna, ordered by release date
df2 = pd.read_sql_query("""
                            SELECT t.name as track_name, al.name as album_name, al.release_date as album_release_date
                            FROM tracks t, albums al, artists ar
                            WHERE (ar.name = 'Madonna' and t.name = 'Material Girl' and t.album_id = al.id and ar.id = al.artist_id)
                            ORDER BY STRFTIME('%Y', al.release_date) ASC
                            """, conn)

# All tracks by Alvvays, ordered by release year
df3 = pd.read_sql_query("""
                            SELECT t.name as track_name, STRFTIME('%Y', al.release_date) as year, t.popularity as track_popularity
                            FROM tracks t, albums al, artists ar
                            WHERE ar.name = 'Alvvays' and t.album_id = al.id and ar.id = al.artist_id
                            ORDER BY STRFTIME('%Y', al.release_date) ASC
                            """, conn)

# The most popular track by Alvvays
df4 = pd.read_sql_query("""
                            SELECT t.name as track_name, MAX(t.popularity) as track_popularity, STRFTIME('%Y', al.release_date) as year
                            FROM tracks t, albums al, artists ar
                            WHERE ar.name = 'Alvvays' and t.album_id = al.id and ar.id = al.artist_id
                            """, conn)

# Top 10 most popular tracks by indie pop artists
df5 = pd.read_sql_query("""
                            SELECT t.name AS track_name, ar.name AS artist_name, al.name AS album_name, STRFTIME('%Y', al.release_date) AS year
                            FROM tracks t, albums al, artists ar
                            WHERE (ar.genres LIKE '%indie pop%' OR '%indie-pop%') AND t.album_id = al.id AND ar.id = al.artist_id
                            ORDER BY t.popularity DESC
                            LIMIT 10
                            """, conn)
# Another approach using JOIN ON operation
# df5 = pd.read_sql_query("""
#                         SELECT 
#                             t.name as track_name, 
#                             ar.name as artist_name, 
#                             al.name as album_name, 
#                             STRFTIME('%Y', al.release_date) as year
#                         FROM 
#                             tracks t
#                             JOIN albums al ON t.album_id = al.id
#                             JOIN artists ar ON al.artist_id = ar.id
#                         WHERE 
#                             ar.genres LIKE '%indie pop%' or '%indie-pop%'
#                         ORDER BY 
#                             t.popularity DESC
#                         LIMIT 10
#                         """, conn)


# Examples using SUBQUERIES
# Top 10 most popular tracks by Fleetwood Mac
df6 = pd.read_sql_query("""
                        SELECT t.name as track_name
                        FROM tracks t
                        WHERE t.album_id IN (
                            SELECT al.id 
                            FROM albums al
                            JOIN artists ar ON al.artist_id = ar.id
                            WHERE ar.name = 'Fleetwood Mac')
                        ORDER BY t.popularity DESC
                        LIMIT 10
                        """, conn)
# Average duration in minutes of tracks from Fleetwood Mac albums released before 1975
df7 = pd.read_sql_query("""
                        SELECT (AVG(t.duration_ms)/60000) as avg_time_minutes 
                        FROM tracks t
                        WHERE t.album_id IN (
                            SELECT al.id 
                            FROM albums al
                            JOIN artists ar ON al.artist_id = ar.id
                            WHERE STRFTIME('%Y', al.release_date) < '1975' AND ar.name = 'Fleetwood Mac')
                        """, conn)


# Examples using AGGREGATION
# Total number of tracks by Sade in our database
df8 = pd.read_sql_query("""
                        SELECT ar.name, COUNT(t.id) as total_tracks
                        FROM artists ar
                        JOIN albums al ON ar.id = al.artist_id
                        JOIN tracks t ON al.id = t.album_id
                        WHERE ar.name = 'Sade'
                        GROUP BY ar.id
                        """, conn)
# Longest track from album 'The Bends' by Radiohead
df9 = pd.read_sql_query("""
                        SELECT tr.name as track_name, al.name as album_name, (MAX(t.duration_ms)/60000) as longest_track_duration_minutes
                        FROM albums al, artists ar, tracks tr
                        JOIN tracks t ON al.id = t.album_id
                        WHERE al.name = 'The Bends' and ar.name = 'Radiohead' and tr.name = t.name
                        GROUP BY al.id
                        LIMIT 10
                        """, conn)

# To execute SQL queries
cursor = conn.cursor()


# Example of INSERT query
# Inserting track called 'Movies' by group Weyes Blood

cursor.execute("""INSERT OR REPLACE INTO tracks (album_id, artists_id, duration_ms, id, name, track_number, popularity)
                    VALUES ('000000300400000600000z', '000000200800000900u00s', 352800, '000000id0805000700u00w', 'Movies', '6', 50);""")
conn.commit()

cursor.execute("""INSERT OR REPLACE INTO albums (album_type, artist_id, id, name, release_date, total_tracks)
                    VALUES ('album', '000000200800000900u00s', '000000300400000600000z', 'Titanic Rising', '2019-04-05', 10);""")
conn.commit()

cursor.execute("""INSERT OR REPLACE INTO artists (genres, id, name)
                    VALUES ('soft rock, psychedelic folk, chamber pop, noise, experimental rock', '000000200800000900u00s', 'Weyes Blood');""")
conn.commit()


# Example of UPDATE query
# Adding a genre to group Weyes Blood
cursor.execute("""
                UPDATE artists
                SET genres = genres || ', dream pop'
                WHERE name = 'Weyes Blood' AND id = '000000200800000900u00s';
                """)
conn.commit()

cursor.close()

# Check for new entries in database
df10 = pd.read_sql_query("""
                            SELECT t.name as track_name, al.name as album_name,
                            ar.name as artist_name, STRFTIME('%Y', al.release_date) as year,
                            t.popularity as track_popularity, ar.genres
                            FROM tracks t, albums al, artists ar
                            WHERE ar.name = 'Weyes Blood' and t.name = 'Movies' and t.album_id = al.id and ar.id = al.artist_id
                            """, conn)

# ANALYZE example: Top 3 years with most album releases
df11 = pd.read_sql_query("""
                            SELECT STRFTIME('%Y', al.release_date) as release_year, COUNT(al.id) as total_albums
                            FROM albums al
                            GROUP BY release_year
                            ORDER BY total_albums DESC
                            LIMIT 3
                            """, conn)


# Display the results/DataFrames using tabulate
# Options: can choose a different format such as 'psql', 'html', 'latex', etc.
print(tabulate(df1, headers='keys', tablefmt='psql'))
print(tabulate(df2, headers='keys', tablefmt='psql'))
print(tabulate(df3, headers='keys', tablefmt='psql'))
print(tabulate(df4, headers='keys', tablefmt='psql'))
print(tabulate(df5, headers='keys', tablefmt='psql'))
print(tabulate(df6, headers='keys', tablefmt='psql'))
print(tabulate(df7, headers='keys', tablefmt='psql'))
print(tabulate(df8, headers='keys', tablefmt='psql'))
print(tabulate(df9, headers='keys', tablefmt='psql'))
print(tabulate(df10, headers='keys', tablefmt='psql'))
print(tabulate(df11, headers='keys', tablefmt='psql'))

# Close the connection
conn.close()

