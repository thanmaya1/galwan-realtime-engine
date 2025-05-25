import psycopg2
import folium
from folium.plugins import TimestampedGeoJson
from datetime import datetime
import json

# === Database connection ===
def get_events():
    conn = psycopg2.connect(
        dbname="eatgrass",
        user="postgres",
        password="LuTanu1*",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT event_type, intensity, event_time, 
               ST_Y(location::geometry) AS latitude, 
               ST_X(location::geometry) AS longitude
        FROM events
        WHERE event_time >= NOW() - INTERVAL '7 days'
        ORDER BY event_time;
    """)
    events = cur.fetchall()
    cur.close()
    conn.close()
    return events

# === Prepare GeoJSON Features for TimestampedGeoJson ===
def build_geojson_features(events):
    features = []
    color_map = {
        "shelling": "red",
        "troop_movement": "blue",
        "drone_sighting": "green"
    }

    for event_type, intensity, event_time, lat, lon in events:
        # Format event_time to ISO 8601 (date + time)
        timestamp = event_time.isoformat()

        feature = {
            "type": "Feature",
            "properties": {
                "time": timestamp,
                "popup": f"{event_type.capitalize()} ({event_time.strftime('%Y-%m-%d %H:%M')}) - Intensity: {intensity}",
                "style": {
                    "color": color_map.get(event_type, "gray"),
                    "radius": 5 + intensity / 2,
                    "fillColor": color_map.get(event_type, "gray"),
                    "fillOpacity": 0.7,
                }
            },
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            }
        }
        features.append(feature)
    return features

def main():
    events = get_events()

    # Base map centered on your AOI
    m = folium.Map(location=[48.5848, 37.9980], zoom_start=13)

    features = build_geojson_features(events)
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    TimestampedGeoJson(
        geojson,
        period='P1D',  # 1 day interval
        add_last_point=True,
        auto_play=False,
        loop=False,
        max_speed=1,
        loop_button=True,
        date_options='YYYY-MM-DD',
        time_slider_drag_update=True
    ).add_to(m)

    # Add legend HTML
    legend_html = """
    <div style="
        position: fixed; 
        bottom: 50px; left: 50px; width: 250px; height: 150px; 
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
        <b>Marker Size:</b> Event Intensity
    </div>
    """
    from branca.element import Template, MacroElement
    legend = MacroElement()
    legend._template = Template(legend_html)
    m.get_root().add_child(legend)

    # Save to file
    m.save("timeslider_map.html")
    print("✅ Time-slider map saved as 'timeslider_map.html'")

if __name__ == "__main__":
    main()
