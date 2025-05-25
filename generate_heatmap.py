import psycopg2
import folium
from folium.plugins import HeatMap
from datetime import datetime, timedelta

# === Time Filter Setup ===
end_time = datetime.now()
start_time = end_time - timedelta(days=1)

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="eatgrass",
    user="postgres",
    password="LuTanu1*",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Fetch event data within time range
cur.execute("""
    SELECT ST_Y(location::geometry), ST_X(location::geometry), intensity
    FROM events
    WHERE event_time BETWEEN %s AND %s;
""", (start_time, end_time))
rows = cur.fetchall()

cur.close()
conn.close()

# Prepare heatmap data (lat, lon, intensity)
heat_data = [[lat, lon, intensity] for lat, lon, intensity in rows]

# Generate Heatmap
m = folium.Map(location=[48.5848, 37.9980], zoom_start=13)
HeatMap(heat_data, radius=15, blur=10, min_opacity=0.5).add_to(m)

# Save map
m.save("heatmap.html")
print("✅ Heatmap saved as 'heatmap.html'")
