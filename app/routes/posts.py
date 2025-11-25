from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from .. import models, schemas, database, oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    dependencies=[Depends(oauth2.get_current_user)],
)


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(database.get_db),
             current_user: models.User = Depends(oauth2.get_current_user)):
    result = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .outerjoin(models.Vote, models.Vote.post_id == models.Post.id)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )

    if not result:
        raise HTTPException(404, "Post not found")

    post, votes = result
    return {"Post": post, "votes": votes}


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(database.get_db),
              current_user: models.User = Depends(oauth2.get_current_user)):

    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .outerjoin(models.Vote, models.Vote.post_id == models.Post.id)
        .group_by(models.Post.id)
        .all()
    )

    return [{"Post": post, "votes": votes} for post, votes in results]


@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(
    payload: schemas.PostCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post = models.Post(**payload.model_dump(), user_id=current_user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.delete("/{id}", status_code=204)
def delete_post(id: int, db: Session = Depends(database.get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(404, "Post not found")

    if post.user_id != current_user.id:
        raise HTTPException(403, "Not authorised")

    db.delete(post)
    db.commit()


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, payload: schemas.PostBase,
                db: Session = Depends(database.get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(404, "Post not found")

    if post.user_id != current_user.id:
        raise HTTPException(403, "Not authorised")

    for key, value in payload.model_dump().items():
        setattr(post, key, value)

    db.commit()
    db.refresh(post)
    return post
