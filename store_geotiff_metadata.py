import psycopg2
import rasterio
from shapely.geometry import box
from rasterio.crs import CRS as RioCRS
from datetime import datetime, timezone  # added timezone import

# Path to your renamed GeoTIFF
tiff_path = "C:\\Users\\anon\\OneDrive\\Desktop\\eatgrass\\bakhmut_image.tif" 

# Connect to Postgres
conn = psycopg2.connect(
    dbname="eatgrass",
    user="postgres",
    password="LuTanu1*",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Create table if not exists
cur.execute("""
CREATE TABLE IF NOT EXISTS scenes (
    id SERIAL PRIMARY KEY,
    filename TEXT,
    captured_at TIMESTAMP,
    footprint GEOMETRY(POLYGON, 4326)
)
""")

# Read GeoTIFF metadata
with rasterio.open(tiff_path) as src:
    bounds = src.bounds
    footprint_geom = box(*bounds)
    filename = tiff_path.split("\\")[-1]

# Insert scene metadata with timezone-aware UTC timestamp
cur.execute("""
INSERT INTO scenes (filename, captured_at, footprint)
VALUES (%s, %s, ST_GeomFromText(%s, 4326))
""", (
    filename,
    datetime.now(timezone.utc),  # replaced deprecated datetime.utcnow()
    footprint_geom.wkt
))

conn.commit()
cur.close()
conn.close()

print("✅ Scene metadata stored in PostGIS.")
