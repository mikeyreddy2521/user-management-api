
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Welcome to my User Management API",
        "status": "Running"
    }

@app.get("/users")
def get_users():
    return [
        {"id": 1, "name": "Teja", "role": "Admin"},
        {"id": 2, "name": "Rahul", "role": "Developer"},
        {"id": 3, "name": "Priya", "role": "Tester"}
    ] 
