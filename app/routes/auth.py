from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, models, security, oauth2

router = APIRouter(
    prefix="/auth",
    tags=['Authentication'])

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), 
          db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(
        models.User.username == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=404, detail="Invalid Credentials")
    
    if not security.verify_password(user_credentials.password, user.hashed):
        raise HTTPException(
            status_code=404, detail="Invalid Credentials")
    
    accesss_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access token": accesss_token, "token_type": "bearer"}

