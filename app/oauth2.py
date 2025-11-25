from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import schemas, models, database
from app.config import get_settings
settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
        token: str = Depends(oauth2_scheme), 
        db: Session = Depends(database.get_db)) -> models.User:
    
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid = payload.get("user_id")
        
        if uid is None:
            raise credentials_exc
        
        token_data = schemas.TokenData(id=uid)
    except JWTError:
        raise credentials_exc
    
    user = db.query(models.User).get(token_data.id)
    
    if not user:
        raise credentials_exc
    
    return user
