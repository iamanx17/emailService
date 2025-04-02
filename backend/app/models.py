from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr, BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

#User who will signup, login, create group, add subscribers
class User(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    email: EmailStr = Field(unique=True)
    password: Optional[str] = Field(default=None)
    api_key: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    timedelta: Optional[datetime] = Field(default_factory=datetime.utcnow)

    subscribers: List['Subscribers'] = Relationship(back_populates='user')
    templates: List['EmailTemplate'] = Relationship(back_populates='user')
    groups: List['Groups'] = Relationship(back_populates='user')

class loginUser(SQLModel):
    email: EmailStr
    password: str

class updateUser(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    password: Optional[str] = None


# People who have subscribed the newsletter 
class Subscribers(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: Optional[str]= Field(default=None)
    last_name: Optional[str] = Field(default=None)
    email: EmailStr = Field(unique=True)
    is_active: bool = Field(default=True)
    user_id: int = Field(foreign_key='user.id')
    timedelta: Optional[datetime] = Field(default_factory=datetime.utcnow)

    user: User =  Relationship(back_populates='subscribers')
    group_id: Optional[int] = Field(default=None, foreign_key='groups.id')
    group: Optional['Groups'] = Relationship(back_populates='members')

class CreateOrUpdateSubscriber(SQLModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr


# Pre Email Templates that will be sent to the subscribers at the scheduled time
class EmailTemplate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    template_name: str = Field(default=None)
    subject: str = Field(default='')
    body: str = Field(default='')
    timedelta: Optional[datetime] = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key='user.id')

    user: User = Relationship(back_populates='templates')
    groups: List["Groups"] = Relationship(back_populates='template')


class createOrUpdateEmail(SQLModel):
    template_name: str
    subject: str
    body:str


# Group which holds the list of subscribers and Email Templates set for this particular member of this group
class Groups(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    group_name: str = Field(default=None)
    timedelta: Optional[datetime] = Field(default_factory=datetime.utcnow)
    template_id: Optional[int] = Field(foreign_key='emailtemplate.id')
    user_id:int = Field(foreign_key='user.id')

    template: EmailTemplate = Relationship(back_populates='groups')
    members: List['Subscribers'] = Relationship(back_populates='group')
    user: User = Relationship(back_populates='groups')

class groupCreateOrUpdate(SQLModel):
    template_id: Optional[int] = None
    group_name: str
    
class addOrRemoveSubscriber(SQLModel):
    subscribers_list: List[EmailStr]

class SendEmailModel(BaseModel):
    email_list: List[EmailStr]
    subject: str
    body: str