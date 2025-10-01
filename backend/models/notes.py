from pydantic import BaseModel
from typing import Optional

class FolderCreate(BaseModel):
    name: str
    parent_id: Optional[int] = None

class FolderOut(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]

class NoteCreate(BaseModel):
    title: str
    content: str
    folder_id: int

class NoteOut(BaseModel):
    id: int
    title: str
    content: str
    folder_id: int