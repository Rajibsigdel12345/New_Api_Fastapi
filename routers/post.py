
from app import models, schemas, database, oauth2
from typing import List, Optional
from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


# def get_posts(db: Session = Depends(database.get_db), Limit: int = 10, skip: int = 0, search: Optional[str] = ''):


@router.get("/", response_model=List[schemas.PostOut])
# @router.get('/')
def get_posts(db: Session = Depends(database.get_db), Limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    # posts = db.query(models.Post).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    # results = [tuple(row) for row in results]
    # results = db.query(models.Post).join(
    #     models.Vote, models.Vote.user_id == models.Post.id, isouter=True).group_by(models.Post.id)
    # results = list({'Post': row[0], "votes": row[1]} for row in results)
    # print(results[0])
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user)
    new_post = models.Post(User_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # print(post.model_dump())  # .dict deprecated
    return new_post


@router.get('/{id}', response_model=schemas.PostOut)
def get_posts(id: int, db: Session = Depends(database.get_db)):

    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    Post = post_query.first()
    if Post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} doesnt exists')
    if Post.User_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"you cant delete this post")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    Post = post_query.first()
    if Post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} doesnt exists')
    if (Post.User_id != current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"you cant update this post")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return Post
