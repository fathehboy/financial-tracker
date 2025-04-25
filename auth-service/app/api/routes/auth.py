# auth-service/app/api/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import redis
import os
from dotenv import load_dotenv
import logging
from typing import Optional

# Local imports
from app.models import User
from app.schemas.user import UserLogin, UserOut
from app.security import (
    verify_password, 
    create_access_token,
    decode_access_token
)
from app.database import SessionLocal
from app.core.logging_config import logger

# Load environment variables
load_dotenv()

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={401: {"description": "Unauthorized"}}
)

# Redis configuration using your .env values
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASSWORD"),
    ssl=False,  # Important for cloud Redis
    decode_responses=True,
    socket_timeout=5,
    socket_connect_timeout=5
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def verify_redis_connection():
    """Test Redis connection on startup"""
    try:
        return redis_client.ping()
    except redis.ConnectionError:
        logger.critical("Failed to connect to Redis")
        return False

@router.post("/login", response_model=UserOut)
async def login(
    request: Request,
    user: UserLogin, 
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT token with:
    - Rate limiting by IP (5 attempts/15 min)
    - Account lockout after 5 failed attempts
    - Secure Redis token storage
    """
    # Security headers
    headers = {
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff"
    }

    # Rate limiting by IP
    ip_address = request.client.host
    rate_limit_key = f"rate_limit:{ip_address}"
    current_attempts = redis_client.get(rate_limit_key) or 0

    if int(current_attempts) >= 5:
        logger.warning(f"Rate limit exceeded from IP: {ip_address}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Please try again later.",
            headers=headers
        )

    # Get user
    db_user: Optional[User] = db.query(User).filter(
        User.username == user.username
    ).first()

    # Authentication checks
    if not db_user or not verify_password(user.password, db_user.password_hash):
        # Increment counters
        redis_client.incr(rate_limit_key)
        redis_client.expire(rate_limit_key, timedelta(minutes=15))
        
        if db_user:
            db_user.failed_login_attempts += 1
            if db_user.failed_login_attempts >= 5:
                db_user.is_locked = True
                logger.warning(f"Account locked: {user.username}")
            db.commit()
        
        logger.warning(f"Failed login for: {user.username} from {ip_address}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={**headers, "WWW-Authenticate": "Bearer"}
        )

    # Check account lock
    if db_user.is_locked:
        logger.warning(f"Login attempt to locked account: {user.username}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account locked. Contact support.",
            headers=headers
        )

    # Successful login
    db_user.failed_login_attempts = 0  # Reset counter
    db_user.last_login = datetime.utcnow()
    db.commit()
    
    # Generate token (30m expiry as per security.py)
    access_token = create_access_token(
        data={
            "sub": db_user.username,
            "user_id": str(db_user.id)
        }
    )
    
    # Store in Redis (1h expiry)
    redis_client.setex(
        name=f"auth:{db_user.username}",
        time=timedelta(hours=1),
        value=access_token
    )
    
    # Set secure cookies if using browser auth
    response_headers = {
        **headers,
        "Set-Cookie": f"access_token={access_token}; HttpOnly; Secure; SameSite=Strict; Path=/",
        "X-Auth-User": db_user.username
    }
    
    logger.info(f"Successful login: {user.username}")
    response_data = {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 1800,
        "user_id": db_user.id
    }
    return response_data

@router.post("/logout")
async def logout(
    request: Request,
    db: Session = Depends(get_db)
):
    """Secure token invalidation"""
    auth_header = request.headers.get("Authorization")
    token = auth_header.split(" ")[1] if auth_header else None
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No token provided"
        )
    
    try:
        payload = decode_access_token(token)
        if payload and payload.get("sub"):
            # Remove all related keys
            redis_client.delete(f"auth:{payload['sub']}")
            logger.info(f"User logged out: {payload['sub']}")
            return {
                "status": "success",
                "message": "Successfully logged out"
            }
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid token"
    )

@router.get("/health")
async def health_check():
    """Endpoint for service health verification"""
    redis_ok = await verify_redis_connection()
    return {
        "status": "OK" if redis_ok else "Degraded",
        "redis": "Connected" if redis_ok else "Disconnected",
        "timestamp": datetime.utcnow().isoformat()
    }