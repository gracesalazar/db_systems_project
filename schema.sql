
CREATE TABLE albums (
    album_type VARCHAR(50),
    artist_id VARCHAR(255),
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    release_date DATE,
    total_tracks INT
);

CREATE TABLE artists (
    genres TEXT, -- Assuming this can be stored as text
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE tracks (
    album_id VARCHAR(255), -- Assuming this is related to an album ID
    artists_id TEXT, -- Assuming this is a list of artist IDs and can be stored as text
    duration_ms FLOAT,
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    track_number VARCHAR(50)
);