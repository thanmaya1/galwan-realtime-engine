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


![image](https://github.com/user-attachments/assets/42480fb3-2a3e-4d4e-ad08-4aa3f6c6275f)


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
3. **Simulate Real-Time Insertion**

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

## 📸 Sample Screenshot
![image](https://github.com/user-attachments/assets/071a85de-bc15-42cc-b9f3-42393717a717)
![image](https://github.com/user-attachments/assets/38de009f-b430-4620-9298-ef57b4cad862)
![image](https://github.com/user-attachments/assets/18fe7581-0ff9-4d42-a21e-274fa371e08e)
![image](https://github.com/user-attachments/assets/7f21b6d1-b4bd-4a87-8b8c-8e537227220a)
![image](https://github.com/user-attachments/assets/f37c48db-8d2e-4c36-b5c9-9cbc19a5f956)

## 🔭 Vision
This is a foundation for:

Disaster monitoring

Conflict intelligence

Urban safety systems

Built using simple, non-Dockerized tools for fast prototyping and full transparency.

## 🤖 Author
Made with 💻 and 🌍 by Thanmaya

