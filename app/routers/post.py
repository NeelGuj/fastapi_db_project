from fastapi import Response, status, HTTPException, Depends, APIRouter
from app import models, schemas, oauth2
from app.database import  get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func


router=APIRouter( prefix="/posts", tags=["Posts"])
# using prefix="/posts" we can remove /posts from every route in requests.
# using tags=["Posts"] helps us to group the requests in docs


# We are getting all the posts here.
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user), 
    limit: int = 5, 
    skip: int = 0, 
    search: Optional[str] = ""
):
    query = db.query(models.Post, func.count(models.Vote.user_id).label("votes"))\
              .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)\
              .group_by(models.Post.id)

    # First cheching if search is provided or not.
    if search:
        query = query.filter(models.Post.title.ilike(f"%{search}%"))

    # Apply pagination (limit and skip) 
    query = query.limit(limit).offset(skip)
    posts = query.all()
    return posts

# We are creating posts here.
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # print(current_user.email)   we can get the email or id of the current user who is logged in
    new_post=models.Post(owner_id=current_user.id, **post.model_dump())  # we added owner_id to the post we want to create.
    # We can also add owner_id using:
    # new_post_data = post.model_dump()
    # new_post_data['owner_id'] = current_user.id
    # new_post = models.Post(**new_post_data)  # we automatically added owner_id to the post we want to create
    db.add(new_post)  
    db.commit()
    db.refresh(new_post)   
    return new_post
  

# We are getting a single post by passing the id of the post in the URL.
# @router.get("/{id}", response_model=schemas.PostResponse)  # for without votes.
@router.get("/{id}", response_model=schemas.PostOut)  
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
    # post=db.query(models.Post).filter(models.Post.id==id).first()   # for without votes.
    post = db.query(models.Post, func.count(models.Vote.user_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if post is None:   #or if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    
    # if post.owner_id != current_user.id:   # This make sure that the current user(logged in) can only see or get the post created by him/her.
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the requested action.")

    return post  


# We are deleting the post with particular id here.
@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post=db.query(models.Post).filter(models.Post.id==id).first()
   
    if post is None:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} not found.")
    
    if post.owner_id != current_user.id:   # This make sure that the current user(logged in) can only delete the post created by him/her.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the requested action.")

    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



# We are updating the post with particular id here.
@router.put("/{id}",  status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  
    post_to_update = db.query(models.Post).filter(models.Post.id == id).first()
    
    if post_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found.")
    
    if post_to_update.owner_id != current_user.id:    # This make sure that the current user(logged in) can only update the post created by him/her.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the requested action.")

    post_to_update.title = post.title
    post_to_update.content = post.content
    post_to_update.published = post.published
    
     
    db.commit()
    db.refresh(post_to_update)    
    return post_to_update


# Patch request to partial update the post.
@router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def patch_post(id: int, post: schemas.PostPatch, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_to_update = db.query(models.Post).filter(models.Post.id == id).first()

    if post_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found.")
    
    if post_to_update.owner_id != current_user.id:    # This make sure that the current user(logged in) can only update the post created by him/her.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the requested action.")

    if post.title is not None:
        post_to_update.title = post.title
    if post.content is not None:
        post_to_update.content = post.content
    if post.published is not None:
        post_to_update.published = post.published
    db.commit()
    db.refresh(post_to_update)
    return  post_to_update

