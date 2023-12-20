from fastapi import FastAPI, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List
import uvicorn
from schemas.user import UserRegistration, UserDetails

app = FastAPI()

MONGODB_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGODB_URL)
db = client["xpay_db"]

users_collection = db["users"]
profiles_collection = db["profiles"]



@app.post("/registration")
async def register_user(user_data: UserRegistration):
    user_exist = await users_collection.find_one({"$or": [{"email": user_data.email}, {"phone": user_data.phone}]})
    if user_exist:
        raise HTTPException(status_code=400, detail="Email or phone already registered")
    inserted_user = await users_collection.insert_one(user_data.dict())

    profile_data = {"user_id": inserted_user.inserted_id, "profile_picture": user_data.profile_picture}
    await profiles_collection.insert_one(profile_data)

    return {"message": "User registered successfully"}

@app.get("/get_user/{user_id}")
async def get_user_details(user_id: str):
    print("type()", type(user_id))
    user_data = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    profile_data = await profiles_collection.find_one({"user_id": ObjectId(user_id)})

    user_details = UserDetails(
        user_id=str(user_data["_id"]),
        full_name=user_data["full_name"],
        email=user_data["email"],
        phone=user_data["phone"],
        profile_picture=profile_data["profile_picture"],
    )
    return {"user_data": user_details, "status_code": status.HTTP_200_OK}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="debug" , host = "0.0.0.0" , reload= True)