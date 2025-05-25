# 🛰️ Real-Time Geospatial Event Engine: Bakhmut Edition

**Code Name:** `eatgrass`  
**Focus Region:** Bakhmut, Ukraine  
**Purpose:** Real-time mapping of critical geospatial events using satellite, sensor, and social intelligence.

---

## 📍 Project Features

- 🔴 **Time-Filtered Map** — shows only recent events (last 24 hours)
- 🔵 **Clustered Map** — aggregates event locations for zoomed-out clarity
- 🟢 **Heatmap** — visualizes intensity of activity across regions
- 🕒 **Time Slider Map** — lets you scrub through events by time

Each event is stored in PostgreSQL with PostGIS. Redis pub-sub used for real-time simulation.

---

## 🧠 Tech Stack

| Component       | Tech Used                     |
|----------------|-------------------------------|
| Backend         | Python, psycopg2              |
| Database        | PostgreSQL + PostGIS          |
| Messaging       | Redis (pub-sub simulation)    |
| Visualization   | Folium, Leaflet.js, HTML/CSS  |
| Satellite Data  | Sentinel Hub API (S2 imagery) |

---

## 🗂️ File Structure

eatgrass/
├── bakhmut_aoi.py # AOI polygon definition
├── download_scene.py # Fetch Sentinel-2 imagery
├── convert_to_geotiff.py # Convert satellite images to GeoTIFF
├── redis_simulator.py # Publishes simulated events to Redis
├── redis_subscriber.py # Subscribes to Redis and prints live events
├── redis_to_postgis.py # Inserts Redis events into PostGIS
├── insert_old_event.py # Test event from past (for filtering)
├── insert_recent_event.py # Test event from now (for display)
├── generate_filtered_map.py # Shows last 24hr events only
├── generate_clustered_map.py # Cluster view of events
├── generate_heatmap.py # Heatmap of event intensity
├── time_slider_map.py # Interactive timeline map
├── dashboard.html # Clean landing page for maps
├── filtered_map.html
├── clustered_map.html
├── heatmap.html
├── time_slider_map.html
├── requirements.txt
└── README.md

---

## 🚀 How to Run

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
2. **Set Up PostgreSQL with PostGIS**

Create a database eatgrass and a table:
CREATE EXTENSION postgis;

CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    event_type TEXT,
    intensity INTEGER,
    event_time TIMESTAMP,
    location GEOMETRY(Point, 4326)
);
3. **Simulate Real-Time Insertion

Run:


python redis_simulator.py
python redis_to_postgis.py
4. **Generate All Maps**

python generate_filtered_map.py
python generate_clustered_map.py
python generate_heatmap.py
python time_slider_map.py

5. **Launch Dashboard**

Open dashboard.html in browser.

📸## Sample Screenshot

🔭 ## Vision
This is a foundation for:

Disaster monitoring

Conflict intelligence

Urban safety systems

Built using simple, non-Dockerized tools for fast prototyping and full transparency.

🤖 ## Author
Made with 💻 and 🌍 by Thanmaya

