from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas, database, oauth2, security
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


@router.post('/login')
def login(
        user_credentials: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(database.get_db)
):
    user = db.query(models.email).filter(
        models.User.email == user_credentials.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=404, detail="Invalid Credentials")

    if not security.verify_password(user_credentials.password, user.hashed):
        raise HTTPException(
            status_code=404, detail="Invalid Credentials")

    access_token = oauth2.create_access_token(
        data={"user_id": user.id}
    )

    return {"access_token": access_token, "token_type": "bearer"}


