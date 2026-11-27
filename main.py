
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException

app = FastAPI()

# Define the structure of incoming user data
class UserCreate(BaseModel):
    name: str
    email: str
    role: str


# Temporary user storage
users = [
    {"id": 1, "name": "Teja", "role": "Admin"},
    {"id": 2, "name": "Rahul", "role": "Developer"},
    {"id": 3, "name": "Priya", "role": "Tester"}
]


# GET: Welcome endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to my User Management API",
        "status": "Running"
    }


# GET: Retrieve all users
@app.get("/users")
def get_users():
    return users


# POST: Create a new user
@app.post("/users", status_code=201)
def create_user(user: UserCreate):

    @app.post("/users", status_code=201)
def create_user(user: UserCreate):

    # Check whether email already exists
    for existing_user in users:
        if existing_user.get("email") == user.email:
            raise HTTPException(
                status_code=409,
                detail="Email already exists"
            )

    new_id = max(u["id"] for u in users) + 1

    new_user = {
        "id": new_id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }

    users.append(new_user)

    return {
        "message": "User created successfully",
        "user": new_user
    }
