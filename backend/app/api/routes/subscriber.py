from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.models import CreateOrUpdateSubscriber
from app.core.db import get_session
from app.core.validate import validate_api_key
from app.services.subscribers import subscriberService



sub_router = APIRouter(prefix='/subscriber', tags=['Subscriber API'])
sub_service = subscriberService()

#Subscribers section

@sub_router.post('/create')
def add_subscribers(sub_model: CreateOrUpdateSubscriber, user_id:int = Depends(validate_api_key), session: Session = Depends(get_session)):
    response = sub_service.create_subscriber(sub_model=sub_model, session=session, user_id=user_id)
    return response

@sub_router.get('/getAll')
def fetch_all_subscribers(user_id: int = Depends(validate_api_key), session:Session = Depends(get_session)):
    response = sub_service.get_all_subscriber(user_id=user_id, session=session)
    return response

@sub_router.get('/get/{subscriber_id}')
def get_subscriber(subscriber_id:int, user_id:int = Depends(validate_api_key), session: Session = Depends(get_session)):
    response = sub_service.get_subscriber_by_id(subscriber_id=subscriber_id, user_id=user_id, session=session)
    return response

@sub_router.delete('/remove/{subscriber_id}')
def remove_subscriber(subscriber_id:int, user_id: int = Depends(validate_api_key), session: Session = Depends(get_session)):
    response = sub_service.remove_subscriber(sub_id=subscriber_id, user_id=user_id, session=session)
    return response

@sub_router.post('/update/{subscriber_id}')
def update_subscriber(sub_model: CreateOrUpdateSubscriber, subscriber_id:str, user_id:int = Depends(validate_api_key),  session: Session = Depends(get_session)):
    response = sub_service.update_subscriber(sub_model=sub_model, sub_id = subscriber_id, user_id=user_id, session=session)
    return response

@sub_router.post('/change/{subscriber_id}/status/{status}')
def set_active_or_inactive_subscriber(status:bool, subscriber_id:str, user_id:int = Depends(validate_api_key), session: Session = Depends(get_session)):
    response = sub_service.set_active_inactive(status = status,sub_id=subscriber_id, user_id=user_id, session=session)
    return response