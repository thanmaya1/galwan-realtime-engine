import redis

r = redis.Redis(host='localhost', port=6379, db=0)
pubsub = r.pubsub()
pubsub.subscribe('bakhmut_events')

print("Listening for events on 'bakhmut_events' channel...")

for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"Received event: {message['data'].decode('utf-8')}")
