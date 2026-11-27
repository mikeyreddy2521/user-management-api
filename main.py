
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, Base, SessionLocal
import models

app = FastAPI()

Base.metadata.create_all(bind=engine)


# Database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Incoming user data
class UserCreate(BaseModel):
    name: str
    email: str
    role: str


# GET: Welcome endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to my User Management API",
        "status": "Running"
    }


# GET: Retrieve all users
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
        for user in users
    ]


# POST: Create a new user
@app.post("/users", status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    new_user = models.User(
        name=user.name,
        email=user.email,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "role": new_user.role
        }
    }


# PUT: Update an existing user
@app.put("/users/{user_id}")
def update_user(
    user_id: int,
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if existing_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    duplicate_email = db.query(models.User).filter(
        models.User.email == user.email,
        models.User.id != user_id
    ).first()

    if duplicate_email:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    existing_user.name = user.name
    existing_user.email = user.email
    existing_user.role = user.role

    db.commit()
    db.refresh(existing_user)

    return {
        "message": "User updated successfully",
        "user": {
            "id": existing_user.id,
            "name": existing_user.name,
            "email": existing_user.email,
            "role": existing_user.role
        }
    }


# DELETE: Remove an existing user
@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    existing_user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if existing_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    deleted_user = {
        "id": existing_user.id,
        "name": existing_user.name,
        "email": existing_user.email,
        "role": existing_user.role
    }

    db.delete(existing_user)
    db.commit()

    return {
        "message": "User deleted successfully",
        "user": deleted_user
    }
