-- Enable the PostGIS extension for geographic coordinates
CREATE EXTENSION IF NOT EXISTS postgis;

-- Owners table
CREATE TABLE owners (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dogs table (linked to owners)
CREATE TABLE dogs (
    id SERIAL PRIMARY KEY,
    owner_id INT REFERENCES owners(id),
    name VARCHAR(50) NOT NULL,
    breed VARCHAR(50),
    size VARCHAR(20),
    chasing_squirrels_probability INT DEFAULT 100
);

-- Drivers table with spatial data for their live location
CREATE TABLE drivers (
    id SERIAL PRIMARY KEY,
    dog_name VARCHAR(50) NOT NULL, -- The driver is also a dog
    rating DECIMAL(3,2) DEFAULT 5.00,
    is_online BOOLEAN DEFAULT false,
    -- GEOMETRY(Point, 4326) stores actual GPS coordinates (Longitude, Latitude)
    current_location GEOMETRY(Point, 4326) 
);