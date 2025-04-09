from fastapi import Response, status, HTTPException, Depends, APIRouter
from app import models, schemas, oauth2
from app.database import  get_db
from sqlalchemy.orm import Session


router=APIRouter( prefix="/vote", tags=["Vote"])

'''
Vote Route 
■ Path will be at "/vote" 
■ The user id will be extracted from the JWT token 
■ The body will contain the id of the post the user is voting on as well as the direction of the vote. 
{ 
post_id: 1432 
dir: 0 
} 
■ A vote direction of 1 means we want to add a vote, a direction of O means we want to delete a vote. 
'''


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user) ):
    
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:   # or if post is none:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist.")

    vote_query= db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)  #Check if vote already exists.
    found_vote= vote_query.first()
    if (vote.dir==1):
        if found_vote:    # If vote already exists, raise an error.
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        new_vote=models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return{"meessage": "Successfully added vote."}
    else:   # vote.dir==0
        if found_vote is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote for the post not exists.")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted vote."}
    
