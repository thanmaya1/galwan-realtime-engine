import redis
import time
import json
import random

# Connect to local Redis
r = redis.Redis(host='localhost', port=6379, db=0)

def random_event():
    event = {
        "type": random.choice(["shelling", "drone_sighting", "troop_movement"]),
        "lat": 48.5848 + random.uniform(-0.02, 0.02),  # Bakhmut area
        "lon": 37.9980 + random.uniform(-0.02, 0.02),
        "timestamp": time.time(),
        "intensity": random.randint(1, 10)
    }
    return event

def main():
    while True:
        event = random_event()
        r.publish("bakhmut_events", json.dumps(event))
        print(f"Published event: {event}")
        time.sleep(1)  # 1 event per second

if __name__ == "__main__":
    main()
