from fastapi import FastAPI
from app.database import init_db
from app.routers import auth, users  # Import users router

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with PostgreSQL!"}
