from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from uuid import uuid4, UUID
from typing import Dict

app = FastAPI()

# In-memory storage (hashmap)
users_db: Dict[UUID, dict] = {}

# Pydantic model for input validation
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int

class UserUpdate(BaseModel):
    name: str = None
    email: EmailStr = None
    age: int = None

class UserResponse(UserCreate):
    id: UUID

# Create a user (POST)
@app.post("/users/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    user_id = uuid4()
    new_user = {"id": user_id, "name": user.name, "email": user.email, "age": user.age}
    users_db[user_id] = new_user
    return new_user

# Get all users (GET)
@app.get("/users/", response_model=list[UserResponse])
def get_users():
    return list(users_db.values())

# Get a user by ID (GET)
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: UUID):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

# Update a user (PUT)
@app.put("/users/{user_id}", response_model=UserResponse)
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

# Delete a user (DELETE)
@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: UUID):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    del users_db[user_id]
    return {"message": "User deleted successfully"}

# Run the API with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
