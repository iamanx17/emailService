from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.models import User,updateUser, loginUser
from app.services.user import userService
from app.core.db import get_session
from app.core.validate import validate_api_key


#User Section
user_router = APIRouter(prefix='/user', tags=['User API'])
user_service = userService()


@user_router.get('/getUser')
def get_user(user_id:int = Depends(validate_api_key),session:Session = Depends(get_session)):
    response = user_service.get_user_by_id(user_id, session)
    return response
    
@user_router.post('/loginUser')
def login_user(user_model: loginUser, session: Session = Depends(get_session)):
    response = user_service.login_user(user_model, session)
    return response


@user_router.post('/createUser')
def create_user(user_model: User, session: Session = Depends(get_session)):
    response = user_service.create_user(user_model, session)
    return response

@user_router.delete('/removeUser')
def remove_user(user_id:int = Depends(validate_api_key), session: Session = Depends(get_session)):
    response = user_service.remove_user(user_id, session)
    return response

@user_router.post('/updateUser')
def update_user(user_model: updateUser, session: Session = Depends(get_session)):
    user_dict = user_model.model_dump()
    response = user_service.update_user(user_dict, session)
    return response