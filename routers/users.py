from app import models, schemas, utils, database
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/users',
    tags=['Users'])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # hash the password
    hashed_pw = utils.hashed(user.password)
    user.password = hashed_pw
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id: {id} not found')
    return user
