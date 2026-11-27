from datetime import datetime, timezone
from fastapi import Request, Body
from fastapi.responses import JSONResponse
from core.database import users_collection
from helper_function.tokenCreator import tokenCreator

async def createUser(request: Request, body: dict = Body(
    example={
        "name": "Test User",
        "email": "test@example.com",
    }
)):
    try:
        body = await request.json()
        name = body.get("name")
        email = body.get("email")
        if not name or not email:
            return JSONResponse({"msg": "name and email are required"}, status_code=400)

        existingUser = await users_collection.find_one({"email": email})
        if existingUser:
            userId = str(existingUser["_id"])
        else:
            now = datetime.now(timezone.utc)
            result = await users_collection.insert_one({
                "name": name,
                "email": email,
                "createdAt": now,
                "updatedAt": now,
            })
            userId = str(result.inserted_id)

        token = await tokenCreator({"id": userId})
        return JSONResponse({"msg": "success", "token": token}, status_code=200)
    except Exception as err:
        return JSONResponse({"msg": str(err)}, status_code=500)
