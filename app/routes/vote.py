from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models, schemas, database, oauth2

router = APIRouter(
    prefix="/vote",
    tags=["Vote"],
    dependencies=[Depends(oauth2.get_current_user)],
)

def get_db() -> Session:
    return database.get_db() # type: ignore

@router.post("/", status_code=201)
def vote(vote: schemas.Vote,
         db: Session = Depends(database.get_db),
         current_user: models.User = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail=f"Post with id: {vote.post_id} does not exist"
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id
    )

    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=409,
                detail="You have already voted on this post"
            )

        new_vote = models.Vote(
            post_id=vote.post_id,
            user_id=current_user.id
        )
        db.add(new_vote)
        db.commit()

        return {"message": "Successfully added vote"}

    else:
        if not found_vote:
            raise HTTPException(
                status_code=404,
                detail="Vote does not exist"
            )

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully deleted vote"}