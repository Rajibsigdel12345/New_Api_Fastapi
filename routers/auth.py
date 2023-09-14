
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentiction'])


@router.post('/login', response_model=schemas.TokenResponse)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Invalid email or password')
    if not (utils.verify_password(user_credentials.password, user.password)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid email or password')
    # create a token
    access_token = oauth2.create_access_token(data={'user_id': user.id})
    return {"access_token": access_token, "token_type": "bearer"}
