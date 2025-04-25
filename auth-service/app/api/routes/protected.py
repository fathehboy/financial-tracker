# protected.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt  # Use jose for JWT decoding
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Your OAuth2PasswordBearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Fetch SECRET_KEY from environment variables
SECRET_KEY = os.getenv("SECRET_KEY")  # Assuming your .env has a variable SECRET_KEY
ALGORITHM = "HS256"  # Replace with your chosen algorithm

router = APIRouter()

# Dependency for verifying token and extracting current user
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Decode the token using the secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # Extract the 'sub' field (which should be the username)
        if username is None:
            raise HTTPException(status_code=403, detail="Could not validate credentials")
        return username
    except JWTError:
        # Handle token decoding error
        raise HTTPException(status_code=403, detail="Invalid or expired token")

# Protected route that requires a valid token
@router.get("/protected")
async def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Welcome {current_user}, your token is valid."}
