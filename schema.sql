CREATE TABLE albums (
    album_type VARCHAR(50),
    artist_id VARCHAR(255),
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    release_date DATE,
    total_tracks INT
);

CREATE TABLE artists (
    genres TEXT,
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE tracks (
    album_id VARCHAR(255),
    artists_id TEXT,
    duration_ms FLOAT,
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    track_number VARCHAR(50),
    popularity FLOAT
);

-- -- one-to-one: track to album
-- CREATE TABLE track_album (
--     track_id VARCHAR(255) PRIMARY KEY,
--     track_name TEXT,
--     track_duration FLOAT,
--     track_number VARCHAR(50),
--     album_id VARCHAR(255),
--     album_name TEXT,
--     album_release_date DATE,
--     album_total_tracks VARCHAR(50)
-- );

-- -- many-to-many: album to genre
-- CREATE TABLE album_genre (
--     album_id VARCHAR(255),
--     album_name TEXT,
--     album_release_date DATE,
--     album_total_tracks VARCHAR(50),
--     genres TEXT
-- );

-- -- one-to-many: track to artist
-- CREATE TABLE track_artist (
--     track_id VARCHAR(255) PRIMARY KEY,
--     track_name TEXT,
--     track_duration FLOAT,
--     track_number VARCHAR(50),
--     artist_id VARCHAR(255),
--     artist_name VARCHAR(255)
-- );
