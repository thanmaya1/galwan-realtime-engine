import psycopg2
import folium
from datetime import datetime, timedelta, timezone
from branca.element import Template, MacroElement

# === Time Filter Setup ===
end_time = datetime.now(timezone.utc)
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

# Extract filtered event data
cur.execute("""
    SELECT event_type, intensity, event_time, 
           ST_Y(location::geometry) AS latitude, 
           ST_X(location::geometry) AS longitude
    FROM events
    WHERE event_time BETWEEN %s AND %s;
""", (start_time, end_time))

events = cur.fetchall()
cur.close()
conn.close()

# Base map
m = folium.Map(location=[48.5848, 37.9980], zoom_start=13)

# Color coding
color_map = {
    "shelling": "red",
    "troop_movement": "blue",
    "drone_sighting": "green"
}

# Create Feature Groups
feature_groups = {etype: folium.FeatureGroup(name=etype.capitalize()) for etype in color_map}
for fg in feature_groups.values():
    m.add_child(fg)

# Add Markers with animation for new events (≤15 min old)
for event_type, intensity, event_time, lat, lon in events:
    fg = feature_groups.get(event_type)
    event_time = event_time.replace(tzinfo=timezone.utc)
    is_recent = (end_time - event_time).total_seconds() <= 900

    folium.CircleMarker(
        location=[lat, lon],
        radius=7 + intensity / 2 if is_recent else 5 + intensity / 2,
        popup=f"{event_type.capitalize()} ({event_time}) - Intensity: {intensity}",
        color=color_map.get(event_type, "gray"),
        weight=3 if is_recent else 1,
        dash_array="5,5" if is_recent else None,
        fill=True,
        fill_opacity=0.9 if is_recent else 0.6
    ).add_to(fg)

# Layer Control
folium.LayerControl(collapsed=False).add_to(m)

# Legend
legend_html = """
<div style="
    position: fixed; 
    bottom: 50px; left: 50px; width: 250px; height: 180px; 
    background-color: white; 
    border: 2px solid grey; 
    box-shadow: 3px 3px 10px rgba(0,0,0,0.3);
    z-index:9999; 
    font-size:14px;
    padding: 10px;
    ">
    <b>Event Legend</b><br>
    <table style="width:100%; border-collapse: collapse;">
        <tr><td style="width:20px; height:20px; background:red;"></td><td>🟥 Shelling</td></tr>
        <tr><td style="width:20px; height:20px; background:blue;"></td><td>🟦 Troop Movement</td></tr>
        <tr><td style="width:20px; height:20px; background:green;"></td><td>🟩 Drone Sighting</td></tr>
    </table>
    <hr>
    <b>Dashed Outline:</b> ≤ 15 min old<br>
    <b>Thicker Radius:</b> Higher Intensity
</div>
"""
legend = MacroElement()
legend._template = Template(legend_html)
m.get_root().add_child(legend)

# Save
m.save("filtered_map.html")
print("✅ Filtered Map saved as 'filtered_map.html' with Time Filter and New Event Highlighting")
