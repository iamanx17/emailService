from app.models import User
from sqlmodel import select
from app.core.error import print_error_in_code
import traceback
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from app import constants

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class userService:
    def create_user(self, user_model, session):
        try:
            if self.check_user_by_email(user_model.email, session):
                return {'error': f'User is already created with the email: {user_model.email}'}
            
            user_model.password = self.hash_password(user_model.password)
            session.add(user_model)
            session.commit()
            session.refresh(user_model)
            return {
                'message': 'User has been created successfully',
                'user': user_model
            }

        except Exception as e:
            error_code = traceback.print_exc()
            return print_error_in_code(e, error_code)
        

    def get_user_by_api_key(self, api_key, session):
        try:
            statement = select(User).where(User.api_key == api_key)
            user = session.exec(statement).first()          

            return user if user else None
        except Exception as e:
            error_code = traceback.print_exc()
            return print_error_in_code(e, error_code)

    def check_user_by_email(self, email, session):
        try:
            statement = select(User).where(User.email == email)
            user = session.exec(statement).first()
            return user if user else False

        except Exception as e:
            error_code = traceback.print_exc()
            return print_error_in_code(e, error_code)

    def get_user_by_id(self, user_id, session):
        try:
            statement = select(User).where(User.id == user_id)
            user = session.exec(statement).first()
            if not user:
                return {'error': 'User not found'}
            
            return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'api_key': user.api_key,
                'subscribers': len(user.subscribers),
                'templates_added': len(user.templates),
                'groups_created': len(user.groups)
            }

        except Exception as e:
            error_code = traceback.print_exc()
            return print_error_in_code(e, error_code)

    def login_user(self, user_model, session):
        try:
            user = self.check_user_by_email(user_model.email, session)
            if not user:
                return {'error': f'User not found with the above email: {user_model.email}'}

            if not self.verify_password(user_model.password, user.password):
                return {'error': 'Password not matched, Try again!'}

            payload = {
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(minutes=constants.ACCESS_TOKEN_EXPIRE_TIME_MINUTES)
            }

            access_token = jwt.encode(payload, constants.SECRET_KEY, algorithm=constants.HASH_ALOGRITHM)
            return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'access_token': f"Bearer {access_token}"
            }
        except Exception as e:
            error_code = traceback.print_exc()
            return print_error_in_code(e, error_code)

    def remove_user(self, user_id, session):
        try:

            statement = select(User).where(User.id == user_id)
            user = session.exec(statement).first()
            if not user:
                return {'error': 'User Not found with this Id'}

            session.delete(user)
            session.commit()
            return {'message': 'User has been deleted succcessfully'}

        except Exception as e:
            error_code = traceback.print_exc()
            return print_error_in_code(e, error_code)

    def update_user(self, user_dict, session):
        try:
            email = user_dict.get('email')
            user = self.check_user_by_email(email, session)
            if not user:
                return {'error': 'User doesnt exist with the above email address'}
            
            user.first_name = user_dict.get('first_name', user.first_name)
            user.last_name = user_dict.get('last_name', user.last_name)
            if user_dict.get('password', None):
                user.password = self.hash_password(user_dict.get('password'))

            session.add(user)
            session.commit()
            session.refresh(user)
            return {
                'message': 'User has been updated successfully',
                'user': user
            }

        except Exception as e:
            error_code = traceback.print_exc()
            return print_error_in_code(e, error_code)

    def hash_password(self, password):
        return pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
