
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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

# PUT: Update an existing user
@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserCreate):

    # Find the user
    for existing_user in users:

        if existing_user["id"] == user_id:

            # Check duplicate email
            for other_user in users:
                if (
                    other_user["id"] != user_id
                    and other_user.get("email") == user.email
                ):
                    raise HTTPException(
                        status_code=409,
                        detail="Email already exists"
                    )

            # Update user details
            existing_user["name"] = user.name
            existing_user["email"] = user.email
            existing_user["role"] = user.role

            return {
                "message": "User updated successfully",
                "user": existing_user
            }

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )



# POST: Create a new user
@app.post("/users", status_code=201)
def create_user(user: UserCreate):

    # Check whether email already exists
    for existing_user in users:
        if existing_user.get("email") == user.email:
            raise HTTPException(
                status_code=409,
                detail="Email already exists"
            )

    # Generate new ID
    new_id = max(u["id"] for u in users) + 1

    # Create new user
    new_user = {
        "id": new_id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }

    # Add user to list
    users.append(new_user)

    return {
        "message": "User created successfully",
        "user": new_user
    }
