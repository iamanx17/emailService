from fastapi import APIRouter
from app.api.routes.email import email_router
from app.api.routes.group import group_router
from app.api.routes.subscriber import sub_router
from app.api.routes.user import user_router



app_router = APIRouter()

app_router.include_router(user_router)
app_router.include_router(sub_router)
app_router.include_router(group_router)
app_router.include_router(email_router)