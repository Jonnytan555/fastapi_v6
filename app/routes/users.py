from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas, database, oauth2
from ..security import hash_password, verify_password

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.UserResponse, status_code=201)
def create_user(payload: schemas.UserCreate, db: Session = Depends(database.get_db)):
    
    if db.query(models.User).filter(models.User.email == payload.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")
    
    user = models.User(email=payload.email, password=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=schemas.Token)
def login_user(payload: schemas.UserLoginJSON, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == payload.username).first()

    if not user or not verify_password(payload.password, user.password): # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    token = oauth2.create_access_token({"user_id": user.id})

    return {"access_token": token, "token_type": "bearer"}

