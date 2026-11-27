from core.routes import api_router
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from middleware.timeMeasureMiddleware import ExecutionTimeMiddleware
from middleware.AuthMiddleware import AuthMiddleware

app = FastAPI()

# Updated CORS origins to include HTTPS domain
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    # "https://your-domain.com",   # Production HTTPS
    # "*",                         # For development only, allows all origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # If we convert it to allow_origins=["*"] it will allow all origins
    allow_credentials=True,
    # allow_credentials=False, # For development only, when origins is "*", credentials cannot be true
    allow_methods=["*"],
    allow_headers=["token", "content-type"],
)

# Add the custom middleware
app.add_middleware(AuthMiddleware)

# Prints a line per request ("API /user/getUserDetails took 0.0034 seconds")
# and adds the X-Execution-Time response header.
app.add_middleware(ExecutionTimeMiddleware)

# Include all routes
app.include_router(api_router)


async def check():
    return {"msg": "ok"}

app.add_api_route("/check", check, methods=["GET"], tags=["Health"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

    # =====================================================================
    # COMMAND REFERENCE
    # =====================================================================
    #
    #   Local:
    #     uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    #
    #   Docker:
    #     docker build -t fastapi-app .
    #     docker run -d --env-file .env -p 8000:8000 fastapi-app
    #
    # --- Regenerate requirements.txt (PowerShell) --------------------------
    #     pip freeze | Out-File -FilePath requirements.txt -Encoding ascii
