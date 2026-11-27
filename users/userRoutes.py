from fastapi import APIRouter
from users.views.createUser import createUser
from users.views.getProfileDetails import getProfileDetails
from documentation.userRoutesAPIDocumentation import *

user_router = APIRouter(prefix="/user")

user_router.add_api_route("/createUser", createUser, methods=["POST"], description=createUserDocumentation, tags=["Login & Signup"])
user_router.add_api_route("/getUserDetails", getProfileDetails, methods=["GET"], description=getUserDetailsDocumentation, tags=["Profile & Account"])
