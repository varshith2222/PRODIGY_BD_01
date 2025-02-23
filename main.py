from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from uuid import uuid4, UUID
from typing import Dict

app = FastAPI()
users_db: Dict[UUID, dict] = {}  # hashmap

class UserCreate(BaseModel):  # input validation
    name: str
    email: EmailStr
    age: int

class UserUpdate(BaseModel):
    name: str = None
    email: EmailStr = None
    age: int = None

class UserResponse(UserCreate):
    id: UUID

@app.post("/users/", response_model=UserResponse, status_code=201)  # user POST
def create_user(user: UserCreate):
    user_id = uuid4()
    new_user = {"id": user_id, "name": user.name, "email": user.email, "age": user.age}
    users_db[user_id] = new_user
    return new_user

@app.get("/users/", response_model=list[UserResponse])  # Get all users
def get_users():
    return list(users_db.values())

@app.get("/users/{user_id}", response_model=UserResponse)  # Get user by ID
def get_user(user_id: UUID):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@app.put("/users/{user_id}", response_model=UserResponse)  # Update a user using PUT
def update_user(user_id: UUID, user_update: UserUpdate):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    user = users_db[user_id]
    if user_update.name is not None:
        user["name"] = user_update.name
    if user_update.email is not None:
        user["email"] = user_update.email
    if user_update.age is not None:
        user["age"] = user_update.age
    return user

@app.delete("/users/{user_id}", status_code=204)  # Delete a user
def delete_user(user_id: UUID):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return {"message": "User deleted successfully"}

if _name_ == "_main_":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
