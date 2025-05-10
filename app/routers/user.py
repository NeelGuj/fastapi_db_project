from fastapi import status, HTTPException, Depends, APIRouter, Body
from app import models, schemas, utils, oauth2
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


# Retrieving all users
@router.get("/", response_model=List[schemas.UserOut])
def get_all_users(db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    users = db.query(models.User).all()
    return users



# Getting the current logged in user details.
@router.get("/me", response_model=schemas.UserOut)
def get_current_user_details(current_user: models.User = Depends(oauth2.get_current_user)):
    return current_user



# Retreving a user with id
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user= db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    
    return user




@router.patch("/", response_model=schemas.UserOut)
def update_user(
    user_update: schemas.UserUpdate, 
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    user_query = db.query(models.User).filter(models.User.id == current_user.id)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.email:
        user.email = user_update.email

    if user_update.password:
        hashed_password = utils.hash(user_update.password)
        user.password = hashed_password

    db.commit()
    db.refresh(user)
    return user
