from sqlmodel import select
from app.models import Subscribers



class subscriberService:

    def create_subscriber(self, sub_model, session, user_id):
        if self.get_subscriber_by_email(sub_model.email, user_id=user_id, session=session):
            return {'error': 'Subscriber already exists'}


        sub = Subscribers(first_name=sub_model.first_name, last_name=sub_model.last_name, email=sub_model.email,user_id=user_id)
        session.add(sub)
        session.commit()
        session.refresh(sub)
        return {'message': 'Subscriber has been added successfully', 'subscribers': sub}

    def get_all_subscriber(self, user_id, session):
        statement = select(Subscribers).where(Subscribers.user_id == user_id)
        subscribers = session.exec(statement).all()

        subscribers_list = []
        for sub in subscribers:
            subscribers_list.append({
                'id': sub.id,
                'first_name': sub.first_name,
                'last_name': sub.last_name,
                'email': sub.email,
                'is_active': sub.is_active,
                'timedelta': sub.timedelta,
                'group_id': sub.group_id
            })
        return {'result': subscribers_list}

    def get_subscriber_by_id(self, subscriber_id, user_id, session):
        statement = select(Subscribers).where((Subscribers.id == subscriber_id) & (Subscribers.user_id == user_id))
        sub = session.exec(statement).first()
        if not sub:
            return {'error': f'No Subscriber exists with the subscriber id {subscriber_id}'}
        
        return {'result': sub}
    
    def remove_subscriber(self, sub_id, user_id, session):
        result = self.get_subscriber_by_id(subscriber_id=sub_id, user_id=user_id, session=session)
        if not result.get('result', None):
            return {'result': f'No Subscriber exists with the subscriber id {sub_id}'}
        

        session.delete(result.get('result'))
        session.commit()
        return {'result': 'Subscriber has been removed successfully'}
    
    def update_subscriber(self, sub_model, sub_id, session, user_id):
        result = self.get_subscriber_by_id(subscriber_id=sub_id,user_id=user_id, session=session)
        if not result.get('result'):
            return {'error': f"No Subscriber exists with the subscriber id {sub_id}"}
        
        sub = result.get('result')
        sub_model_dict = sub_model.model_dump()
        sub.first_name = sub_model_dict.get('first_name', sub.first_name)
        sub.last_name = sub_model_dict.get('last_name', sub.last_name)

        session.add(sub)
        session.commit()
        session.refresh(sub)
        return {'result': 'Subscriber has been updated sucessfully', 'subscriber': sub}
    
    def set_active_inactive(self,status, sub_id, user_id, session):
        result = self.get_subscriber_by_id(subscriber_id=sub_id, user_id=user_id, session=session)
        if not result.get('result', None):
            return {'error': f'No subscriber exists with the subscriber id {sub_id}'}
        
        sub = result.get('result')
        sub.is_active = status
        session.add(sub)
        session.commit()
        session.refresh(sub)
        return {'result': 'Subscriber active level has been changed', 'subscriber': sub}
    
    def get_subscriber_by_email(self, email, user_id, session):
        statement = select(Subscribers).where((Subscribers.email == email) & (Subscribers.user_id == user_id))
        subscriber = session.exec(statement).first()    
        return subscriber if subscriber else None
    
        
    
