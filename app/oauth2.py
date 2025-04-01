from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app import schemas, models
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# secret_key
# algorithm
# expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode= data.copy()

    expire= datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    
# we have made copy of the original data as to_encode because we will manupulate the 
# data and we don't want our original data to change.


def verify_access_token(token: str, credential_exception):
    try:
        payload= jwt.decode(token, SECRET_KEY, [ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credential_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credential_exception
    return token_data   
# token_data is nothing but the id of the user making request. We can return multiple fields if we want.


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token= verify_access_token(token, credential_exception)
    user=db.query(models.User).filter(models.User.id==token.id).first()
    return user  
#it will return a user or current_user object which contain all the information and we can access them by user.id or user.email.
# status_code=status.HTTP_401_UNAUTHORIZED will produce  "detail": "Not authenticated" if token is not provided.
# status_code=status.HTTP_401_UNAUTHORIZED will produce  "detail="Could not validate credentials" if token is not correct or expired.



'''In Postman we need to get token by login and hardcode it in the Authorization Token field to access end points or requests.
To solve this problem we wrote a script in the Scripts section in the Login User request that will auatomatically
retrive the token into JWT variabl. Thus we only need to write {{JWT}} in the Authorization Token field of the requests or end points 
we want to make'''