from fastapi import Header, Depends, HTTPException, status
from sqlmodel import Session
from app.services.user import userService
from app import constants
from app.core.db import get_session
import jwt


user_service = userService()



def validate_api_key(session:Session = Depends(get_session), Authorization: str = Header()):
    if 'Bearer'.lower() in Authorization.lower():
        try:

            token = Authorization.split()[1]
            payload = jwt.decode(token, constants.SECRET_KEY, algorithms=[constants.HASH_ALOGRITHM])
            
            if not payload:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid access token')
            
            user_id = payload.get('user_id')
            user = user_service.get_user_by_id(user_id, session)
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid access token')
            return user_id
        
        except jwt.InvalidSignatureError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid access token')

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    user = user_service.get_user_by_api_key(Authorization, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid API Key')
    
    return user.id
