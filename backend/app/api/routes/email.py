from fastapi import APIRouter, Depends, BackgroundTasks
from sqlmodel import Session
from app.core.validate import validate_api_key
from app.core.db import get_session
from app.models import createOrUpdateEmail, SendEmailModel
from app.services.email import emailService
from app.services.subscribers import subscriberService
from app.services.group import groupService
from app.services.email import emailService
from app.core.email import send_email



email_router = APIRouter(prefix='/email', tags=['Email API'])
email_service = emailService()

@email_router.get('/getAll')
def get_all_email_templates(user_id:int = Depends(validate_api_key), session: Session = Depends(get_session)):
    response = email_service.get_all_template(user_id=user_id, session=session)
    return response

@email_router.get('get/{template_id}')
def get_template_by_id(template_id:int, user_id:int = Depends(validate_api_key), session: Session = Depends(get_session)):
    response = email_service.get_template_by_id(template_id=template_id, user_id=user_id, session=session)
    return response

@email_router.post('/createTemplate')
def create_email_template(template_model:createOrUpdateEmail,user_id:int = Depends(validate_api_key),  session: Session = Depends(get_session)):
    response = email_service.createTemplate(template_model=template_model, user_id=user_id, session=session)
    return response

@email_router.delete('/removeTemplate/{template_id}')
def remove_email_template(template_id:str,user_id:int = Depends(validate_api_key), sesison:Session = Depends(get_session)):
    response = email_service.remove_template(template_id=template_id, user_id=user_id, session=sesison)
    return response

@email_router.post('/updateTemplate/{template_id}')
def update_email_template(template_model:createOrUpdateEmail, template_id:str, user_id:int = Depends(validate_api_key), session:Session = Depends(get_session)):
    template_dict = template_model.model_dump()
    response = email_service.update_template(template_dict=template_dict, template_id=template_id, user_id=user_id, session=session)
    return response

@email_router.post('/sendMail/Sub/{subscriber_id}/template/{template_id}')
async def send_email_by_subscriber_id(background_task: BackgroundTasks,subscriber_id: str, template_id: str, user_id:int = Depends(validate_api_key), session:Session = Depends(get_session)):
    subscriber = subscriberService().get_subscriber_by_id(subscriber_id=subscriber_id, user_id=user_id, session=session)
    if not subscriber:
        return {'error': 'Subscriber not found'}
    
    email_template = emailService().get_template_by_id(template_id=template_id, user_id=user_id, session=session)
    if not email_template:
        return {'error': 'Template not found'}
    
    subject = email_template.subject
    body = email_template.body
    email = [subscriber.email]
    schema = SendEmailModel(email_list=email, subject=subject, body=body)
    background_task.add_task(send_email, schema)
    return {'message': 'Email will be sent to users in few minutes'}

    

@email_router.post('/sendMail/Group/{group_id}')
def send_email_by_group(background_task:BackgroundTasks, group_id:str,user_id:int = Depends(validate_api_key), session: Session = Depends(get_session)):
    group = groupService().fetch_group_by_id(group_id=group_id, user_id=user_id, session=session)
    if not group:
        return {'error': 'Group has not found'}
    
    members = group.members
    recipients = [sub.email for sub in members]
    subject = group.template.subject
    body = group.template.body

    schema = SendEmailModel(email_list=recipients, subject=subject, body=body)
    background_task.add_task(send_email, schema)
    return {'message': 'Email will be sent to users in few minutes'}
