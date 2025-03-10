from fastapi import FastAPI

app = FastAPI()

# Sample user data
users_db = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    """Fetch user details by ID"""
    user = users_db.get(user_id)
    if user:
        return user
    return {"error": "User not found"}, 404
