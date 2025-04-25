from fastapi import FastAPI
from app.api.routes import auth, protected  # Import your auth routes

app = FastAPI()

# Include the authentication router
app.include_router(auth.router)

# Include the protected routes router
app.include_router(protected.router, prefix="/auth", tags=["protected"])