import psycopg2
import folium
from folium.plugins import MarkerCluster

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="eatgrass",
    user="postgres",
    password="LuTanu1*",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Extract event data
cur.execute("""
    SELECT event_type, intensity, event_time, 
           ST_Y(location::geometry) AS latitude, 
           ST_X(location::geometry) AS longitude
    FROM events;
""")
events = cur.fetchall()
cur.close()
conn.close()

# Base map
m = folium.Map(location=[48.5848, 37.9980], zoom_start=13)

# Add Clustered Markers
marker_cluster = MarkerCluster().add_to(m)

for event_type, intensity, event_time, lat, lon in events:
    folium.CircleMarker(
        location=[lat, lon],
        radius=5 + intensity / 2,
        popup=f"{event_type.capitalize()} ({event_time}) - Intensity: {intensity}",
        color="black",
        fill=True,
        fill_opacity=0.7
    ).add_to(marker_cluster)

# Save the clustered map
m.save("clustered_map.html")
print("✅ Clustered Map saved as 'clustered_map.html'")