from fastapi import FastAPI
import sys
import os
import threading
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from event_bus.event_bus import EventBus

app = FastAPI()
event_bus = EventBus("payment_processed")

# In-memory payment storage
payments = {}

def handle_order_created(order):
    """Process order_created event by handling payment."""
    payment_id = order["order_id"]
    payments[payment_id] = "Completed"
    print(f"💳 Payment processed for Order {payment_id}")

    # Publish payment_processed event
    event_bus.publish("payment_processed", {"order_id": payment_id, "status": "Completed"})

def start_event_listener():
    """Continuously listen for 'order_created' events."""
    print("📥 Listening for events on 'order_created' queue...")
    event_bus = EventBus("order_created")
    
    while True:  # Keep the process alive
        try:
            event_bus.subscribe(handle_order_created)
        except Exception as e:
            print(f"⚠️ Event listener error: {e}")
            time.sleep(5)  # Wait before retrying

# Start event listener in a separate thread
event_listener_thread = threading.Thread(target=start_event_listener, daemon=True)
event_listener_thread.start()

@app.get("/payment/{payment_id}")
def get_payment_status(payment_id: int):
    return {"payment_id": payment_id, "status": payments.get(payment_id, "Not Found")}
