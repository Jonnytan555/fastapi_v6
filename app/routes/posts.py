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

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    # posts = db.query(models.Post).filter(
    #     models.Post.user_id == current_user.id).all()

    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()

    return posts

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

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    q = (
        db.query(models.Post)
        .filter(models.Post.id == id, models.Post.user_id == current_user.id)
    )

    if q.first() is None:
        raise HTTPException(status_code=404, detail=f"Post {id} not found")
    
    q.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    payload: schemas.PostBase,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    q = (
        db.query(models.Post)
        .filter(models.Post.id == id, models.Post.user_id == current_user.id)
    )

    existing = q.first()

    if existing is None:
        raise HTTPException(status_code=404, detail=f"Post {id} not found")
    
    q.update(payload.model_dump(), synchronize_session=False) # type: ignore
    db.commit()
    db.refresh(existing)

    return existing
