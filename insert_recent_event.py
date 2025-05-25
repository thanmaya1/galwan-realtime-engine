import psycopg2
from datetime import datetime, timezone
from shapely.geometry import Point
from shapely import wkb

# Set recent event timestamp (e.g., now)
event_time = datetime.now(timezone.utc)

# Define event details
event_type = 'drone_sighting'   # Change to 'shelling' or 'troop_movement' if needed
intensity = 6
latitude = 48.5838
longitude = 37.9990

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="eatgrass",
    user="postgres",
    password="LuTanu1*",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Insert recent event
cur.execute("""
    INSERT INTO events (event_type, intensity, event_time, location)
    VALUES (%s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326));
""", (event_type, intensity, event_time, longitude, latitude))

conn.commit()
cur.close()
conn.close()

print("✅ Inserted recent event for testing 15-minute filter.")
