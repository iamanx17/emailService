from app.models import Groups, Subscribers
from sqlmodel import select
from app.services.email import emailService



class groupService:

    def create_group(self, group_model,user_id, session):
        if self.fetch_group_by_name(group_name=group_model.group_name, user_id=user_id, session=session):
            return {'message':"Group Already Exists"}

        group = Groups(group_name= group_model.group_name, template_id=group_model.template_id, user_id=user_id)
        session.add(group)
        session.commit()
        session.refresh(group)
        return {"message":f"group {group_model.group_name} has been created successfully", 'group':group}
    
    def fetch_group_by_name(self, group_name,user_id, session):
        statement = select(Groups).where((Groups.group_name == group_name) & (Groups.user_id == user_id))
        groups = session.exec(statement).first()
        return groups if groups else {}
    
    def fetch_group_by_id(self, group_id, user_id, session):
        statement = select(Groups).where((Groups.id == group_id) & (Groups.user_id == user_id))
        group = session.exec(statement).first()
        return group if group else {}
    
    def fetch_all_group(self, user_id, session):
        statement = select(Groups).where(Groups.user_id == user_id)
        groups = session.exec(statement).all()
        return groups
    
    def update_group(self, group_dict, group_id, user_id, session):
        group = self.fetch_group_by_id(group_id=group_id, user_id=user_id, session=session)
        if not group:
            return {"message": f"Group {group_id} has not found"}
        
        group.group_name = group_dict.get('group_name', group.group_name)
        group.template_id = group_dict.get('template_id', group.template_id)

        session.add(group)
        session.commit()
        session.refresh(group)
        return {'message':'group has been updated successfully', 'group': group}
    
    def remove_group(self, group_id, user_id, session):
        group = self.fetch_group_by_id(group_id=group_id, user_id=user_id, session=session)
        if not group:
            return {'error': 'Group has not found'}
        
        session.delete(group)
        session.commit()
        return {'message': 'Group has been deleted successfully'}

    def add_subscribers_in_group(self, group_name, subscriber_list, user_id, session):
        group = self.fetch_group_by_name(group_name=group_name, user_id=user_id, session=session)
        if not group:
            return {'error': 'Group not Found'}
        
        statement = select(Subscribers).where(Subscribers.email.in_(subscriber_list), Subscribers.user_id == user_id)
        subscribers = session.exec(statement).all()

        for sub in subscribers:
            sub.group_id = group.id

        session.add_all(subscribers)
        session.commit()
        return {'message': 'Subscribers has been added'}
    
    def fetch_subscribers(self, group_name,user_id, session):
        group = self.fetch_group_by_name(group_name=group_name, user_id=user_id, session=session)
        if not group:
            return {'error': 'Group has not found'}
        
        return {
            'id': group.id,
            'group_name': group.group_name,
            'template_id': group.template_id,
            'members': [member for member in group.members]
        }
    
    def remove_subscriber_from_group(self, group_name,subscribers_list, user_id, session):
        group = self.fetch_group_by_name(group_name=group_name, user_id=user_id, session=session)
        if not group:
            return {'error': 'Group has not found'}
        
        statement = select(Subscribers).where(Subscribers.email.in_(subscribers_list), Subscribers.user_id == user_id)
        subscribers = session.exec(statement).all()

        for sub in subscribers:
            sub.group_id = None
        
        session.add_all(subscribers)
        session.commit()
        return {'message': 'Subscribers has been removed successfully '}
    
    def set_group_template(self, template_id, group_id, user_id, session):
        group = self.fetch_group_by_id(group_id=group_id, user_id=user_id, session= session)
        if not group:
            return {'error': 'Group not found'}
        
        template_id = emailService().get_template_by_id(template_id=template_id, user_id=user_id, session=session)
        if not template_id:
            return {'error': 'Template has not found'}
        
        group.template_id = template_id
        session.add(group)
        session.commit()
        session.refresh(group)
        return group