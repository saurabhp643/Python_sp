from fastapi import FastAPI
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from event_bus.event_bus import EventBus

app = FastAPI()
event_bus = EventBus("user_created")

@app.post("/create_user/")
def create_user(user_id: int, username: str, email: str):
    user = {"user_id": user_id, "username": username, "email": email}
    print(f"👤 User created: {user}")
    
    # Publish the event
    event_bus.publish("user_created", user)

    return {"message": "User created", "user": user}
