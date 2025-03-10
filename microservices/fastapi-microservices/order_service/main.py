from fastapi import FastAPI
import requests
app=FastAPI()


# Sample order data
orders_db = {
    101: {"id": 101, "user_id": 1, "product": "Laptop", "price": 1200},
    102: {"id": 102, "user_id": 2, "product": "Phone", "price": 800},
}

USER_SERVICE_URL="http://127.0.0.1:8001/users"

@app.get("/orders/{order_id}")
def get_order(order_id:int):
    """Fetch order details along with user information"""
    order = orders_db.get(order_id)
    if not order:
        return {"error": "Order not found"}, 404
    
    #Fetch uswer details from user service
    user_response = requests.get(f"{USER_SERVICE_URL}/{order['user_id']}")
    if user_response.status_code==200:
        user_data=user_response.json()
        order['user']=user_data
        return order
    return {"error": "User not found"}, 500