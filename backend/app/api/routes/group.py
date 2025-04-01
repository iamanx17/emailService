from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.models import groupCreateOrUpdate, addOrRemoveSubscriber
from app.core.db import get_session
from app.core.validate import validate_api_key
from app.services.group import groupService



group_router = APIRouter(prefix='/group', tags=['Group API'])
group_service = groupService()
#Groups Section

@group_router.post('/create')
def create_group(group_model:groupCreateOrUpdate, user_id:int = Depends(validate_api_key), session:Session = Depends(get_session)):
    response = group_service.create_group(group_model=group_model, user_id=user_id, session=session)
    return response

@group_router.get('/getAll')
def fetch_all_group(user_id:int = Depends(validate_api_key), session:Session = Depends(get_session)):
    response = group_service.fetch_all_group(user_id=user_id, session=session)
    return response

@group_router.post('/update/{group_id}')
def update_group(group_model:groupCreateOrUpdate, user_id:int = Depends(validate_api_key), session:Session = Depends(get_session)):
    group_dict = group_model.model_dump()
    response = group_service.update_group(group_dict=group_dict, user_id=user_id, session=session)
    return response

@group_router.delete('/delete/{group_id}')
def delete_group(group_id:int, user_id:int = Depends(validate_api_key), session: Session = Depends(get_session)):
    response = group_service.remove_group(group_id=group_id, user_id=user_id, session=session)
    return response

@group_router.get('/get/{group_name}')
def get_details_of_group(group_name: str,user_id:int = Depends(validate_api_key), session:Session = Depends(get_session)):
    response = group_service.fetch_group_all_details(group_name=group_name, user_id=user_id, session=session)
    return response

@group_router.post('/addSub/In/{group_name}')
def add_subscribers_in_group(sub_model:addOrRemoveSubscriber, group_name:str, user_id:int= Depends(validate_api_key), session: Session = Depends(get_session)):
    sub_list = sub_model.subscribers_list
    response = group_service.add_subscribers_in_group(group_name=group_name, subscriber_list=sub_list, user_id=user_id, session=session)
    return response
    

@group_router.post('/removeSub/From/{group_name}')
def remove_subscribers_from_group(sub_model: addOrRemoveSubscriber,group_name:str, user_id:int = Depends(validate_api_key), session: Session = Depends(get_session)):
    sub_list = sub_model.subscribers_list
    response = group_service.remove_subscriber_from_group(group_name=group_name, user_id=user_id, subscribers_list=sub_list, session=session)
    return response

@group_router.post('/setTemplate/{template_name}/{group_name}')
def set_template_for_group(template_name:str, group_name:str, user_id:int = Depends(validate_api_key), session:Session = Depends(get_session)):
    response = group_service.set_group_template(template_name=template_name, group_name=group_name, user_id=user_id, session=session)
    return response