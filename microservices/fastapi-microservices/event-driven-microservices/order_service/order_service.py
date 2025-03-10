from fastapi import FastAPI
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from event_bus.event_bus import EventBus
import threading

app = FastAPI()
event_bus = EventBus("order_created")

# In-memory storage
orders = {}

def handle_user_created(user):
    """Process user_created event by creating an order."""
    order_id = len(orders) + 1
    order = {"order_id": order_id, "user_id": user["user_id"], "status": "Created"}
    orders[order_id] = order
    print(f"🛒 Order created for user {user['user_id']}: {order}")

    # Publish order_created event
    event_bus.publish("order_created", order)

# Start listening for `user_created` event in a separate thread
threading.Thread(target=lambda: EventBus("user_created").subscribe(handle_user_created), daemon=True).start()

@app.get("/order/{order_id}")
def get_order(order_id: int):
    return orders.get(order_id, {"error": "Order not found"})
