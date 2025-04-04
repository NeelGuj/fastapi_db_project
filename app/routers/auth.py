from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, utils, oauth2

router = APIRouter(prefix="/login", tags=["Authentication"])

@router.post("/", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm) ,db: Session = Depends(get_db)):
    # OAuth2PasswordReque stores attempted user access credentials in from of username (not email) and password
    # thus models.User.email == user_credentials.username 
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    access_token= oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token":access_token, "token_type":"bearer"}


