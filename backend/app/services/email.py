from sqlmodel import select
from app.models import EmailTemplate


class emailService:

    def get_all_template(self, user_id, session):
        statement = select(EmailTemplate).where(EmailTemplate.user_id == user_id)
        email_templates = session.exec(statement).all()
        return email_templates if email_templates else []
    
    def get_template_by_id(self, template_id,user_id, session):
        statement = select(EmailTemplate).where((EmailTemplate.id == template_id) & (EmailTemplate.user_id == user_id))
        template = session.exec(statement).first()
        return template if template else {}
    
    def get_template_by_name(self, template_name, user_id, session):
        statement = select(EmailTemplate).where((EmailTemplate.template_name == template_name) & (EmailTemplate.user_id == user_id))
        template = session.exec(statement).first()
        return template if template else {}

    def create_template(self,template_model, user_id, session):
        if self.get_template_by_name(template_name=template_model.template_name, user_id=user_id, session=session):
            return {'message': f'Template is already created with this name {template_model.template_name}'}

        email = EmailTemplate(template_name=template_model.template_name, subject=template_model.subject, body=template_model.body, user_id=user_id)
        session.add(email)
        session.commit()
        session.refresh(email)
        return {'message': 'Email template has been created successfully', 'emailTempale': email}
    
    def remove_template(self, template_id, user_id, session):
        template = self.get_template_by_id(template_id=template_id, user_id=user_id, session=session)
        if not template:
            return {'error': 'Not Found'}
        
        session.delete(template)
        session.commit()
        return {'result': 'Template has been removed successfully'}

    def update_template(self, template_dict, template_id, user_id, session):
        template = self.get_template_by_id(template_id=template_id, user_id=user_id, session=session)
        if not template:
            return {'error': 'Template not found'}
        
        template.subject = template_dict.get('subject', template.subject)
        template.body = template_dict.get('body', template.body)

        session.add(template)
        session.commit()
        session.refresh(template)
        
        return {
            'result': 'template updated successfully',
            'template': template
        }