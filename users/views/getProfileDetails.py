from bson import ObjectId
from fastapi import Request, Depends
from fastapi.responses import JSONResponse
from helper_function.apis_requests import get_current_user
from core.database import users_collection

async def getProfileDetails(request: Request, token: str = Depends(get_current_user)):
    try:
        userId = request.state.userId
        userDetails = await users_collection.find_one({"_id": ObjectId(userId)})
        if not userDetails:
            return JSONResponse({"msg": "User not found"}, status_code=404)

        userDetails["_id"] = str(userDetails["_id"])
        userDetails["createdAt"] = userDetails["createdAt"].isoformat()
        userDetails["updatedAt"] = userDetails["updatedAt"].isoformat()
        return JSONResponse({"userDetails": userDetails}, status_code=200)
    except Exception as err:
        return JSONResponse({"msg": str(err)}, status_code=500)
