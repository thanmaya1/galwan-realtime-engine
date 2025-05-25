import redis
import psycopg2
import json
from datetime import datetime

# Redis setup
r = redis.Redis(host='localhost', port=6379, db=0)
pubsub = r.pubsub()
pubsub.subscribe('bakhmut_events')

# PostGIS setup
conn = psycopg2.connect(
    dbname="eatgrass",
    user="postgres",
    password="LuTanu1*",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Create events table if not exists
cur.execute("""
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    event_type TEXT,
    intensity INT,
    event_time TIMESTAMP,
    location GEOMETRY(POINT, 4326)
)
""")
conn.commit()

print("Listening for events on 'bakhmut_events' and storing to PostGIS...")

for message in pubsub.listen():
    if message['type'] != 'message':
        continue

    try:
        event = json.loads(message['data'].decode('utf-8'))
        event_type = event.get('type')
        intensity = event.get('intensity')
        timestamp = datetime.fromtimestamp(event.get('timestamp'))
        lat = event.get('lat')
        lon = event.get('lon')

        if None in (event_type, intensity, timestamp, lat, lon):
            print("⚠️ Missing event data, skipping:", event)
            continue

        cur.execute("""
        INSERT INTO events (event_type, intensity, event_time, location)
        VALUES (%s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
        """, (event_type, intensity, timestamp, lon, lat))

        conn.commit()
        print(f"✅ Inserted event: {event_type} at ({lat}, {lon})")

    except Exception as e:
        print("❌ Error processing event:", e, "Data:", message['data'])

cur.close()
conn.close()
