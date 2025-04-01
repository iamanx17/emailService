from fastapi import FastAPI
from app.api.main import app_router
from app.core.db import init_db



init_db()
app = FastAPI(title='Welcome to Newsletter Manager', description="Send emails to your subscribers", summary='Developed By @iamanx17')
app.include_router(app_router)
