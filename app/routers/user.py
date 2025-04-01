from fastapi import status, HTTPException, Depends, APIRouter
from app import models, schemas, utils
from app.database import engine, get_db
from sqlalchemy.orm import Session
from typing import List

router=APIRouter( prefix="/users", tags=["Users"])
# using prefix="/users" we can remove /users from every route in requests.
# using tags=["Users"] helps us to group the requests in docs

# Creating a user.
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate ,db: Session = Depends(get_db)):
    # hash the password
    hashed_password=utils.hash(user.password)
    user.password= hashed_password
    new_user=models.User(**user.model_dump())  
    db.add(new_user) 
    db.commit()
    db.refresh(new_user)   
    return new_user


# Retreving a user with id
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user= db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    
    return user
