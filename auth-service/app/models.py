from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)  # Added email column
    password_hash = Column(String)
    salt = Column(String)  # Added salt column
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))  # Added last_login column
    failed_login_attempts = Column(Integer, default=0)  # Matches SQL schema
    locked_until = Column(DateTime(timezone=True))  # Added locked_until column
    is_locked = Column(Boolean, default=False)  # This could also be added as a flag
