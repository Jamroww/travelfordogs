import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point
from sqlalchemy import create_engine

# Connect to the local PostGIS database
engine = create_engine("postgresql+psycopg2://admin:secretpassword@localhost:5432/dog_dispatch")

num_drivers = 1000

# Dog names for our drivers
names = ["Rex", "Bella", "Max", "Luna", "Charlie", "Daisy", "Buddy", "Lucy", "Rocky", "Zoe"]
dog_names = np.random.choice(names, num_drivers)

# Ratings between 4.00 and 5.00
ratings = np.round(np.random.uniform(4.0, 5.0, num_drivers), 2)

# 80% chance a driver is currently online and accepting rides
is_online = np.random.choice([True, False], num_drivers, p=[0.8, 0.2])

# Center coordinates around Baltimore, MD
center_lon, center_lat = -76.6122, 39.2904

# Generate random coordinates using a normal distribution for realistic clustering
lons = np.random.normal(center_lon, 0.05, num_drivers)
lats = np.random.normal(center_lat, 0.05, num_drivers)
geometry = [Point(lon, lat) for lon, lat in zip(lons, lats)]

# Build the standard DataFrame
df = pd.DataFrame({
    "dog_name": dog_names,
    "rating": ratings,
    "is_online": is_online
})

# Convert to a GeoDataFrame and set the coordinate reference system (WGS 84)
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# Rename the active geometry column to match our PostGIS schema
gdf = gdf.rename_geometry('current_location')

print(f"Pushing {num_drivers} mock drivers to the database...")

# Push directly to PostGIS, appending to the existing table
gdf.to_postgis(name="drivers", con=engine, if_exists="append", index=False)

print("Database seeded successfully.")