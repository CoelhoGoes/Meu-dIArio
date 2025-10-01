from fastapi import FastAPI
from routes.auth import router as auth
from routes.notes import router as folders_notes
app = FastAPI()

app.include_router(router=auth)
app.include_router(router=folders_notes)