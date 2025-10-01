from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List
from services.auth import verify_token
from models.notes import FolderOut, FolderCreate, NoteOut, NoteCreate
import services.notes as service

router = APIRouter(prefix="/notes", tags=["notes"])


# -----------------------------
# FOLDERS
# -----------------------------
@router.post("/folders", response_model=FolderOut)
def create_folder(folder: FolderCreate, token: dict = Depends(verify_token)):
    user_id = token.get("user_id")
    new_folder = service.create_folder(user_id, folder.name, folder.parent_id)
    if not new_folder:
        raise HTTPException(403, "Pasta pai inválida ou sem permissão")
    return new_folder


@router.get("/folders", response_model=List[FolderOut])
def list_folders(token: dict = Depends(verify_token)):
    user_id = token.get("user_id")
    return service.list_folders(user_id)


@router.delete("/folders/{folder_id}")
def delete_folder(folder_id: int, token: dict = Depends(verify_token)):
    user_id = token.get("user_id")
    ok = service.delete_folder(user_id, folder_id)
    if not ok:
        raise HTTPException(404, "Pasta não encontrada ou sem permissão")
    return {"message": "Pasta (e conteúdos) deletada com sucesso"}


# -----------------------------
# NOTES
# -----------------------------
@router.post("/notes", response_model=NoteOut)
def create_note(note: NoteCreate, token: dict = Depends(verify_token)):
    user_id = token.get("user_id")
    new_note = service.create_note(user_id, note.folder_id, note.title, note.content)
    if not new_note:
        raise HTTPException(403, "Sem permissão para criar nota nesta pasta")
    return new_note


@router.get("/notes/{folder_id}", response_model=List[NoteOut])
def list_notes(folder_id: int, token: dict = Depends(verify_token)):
    user_id = token.get("user_id")
    return service.list_notes(user_id, folder_id)


@router.delete("/notes/{note_id}")
def delete_note(note_id: int, token: dict = Depends(verify_token)):
    user_id = token.get("user_id")
    ok = service.delete_note(user_id, note_id)
    if not ok:
        raise HTTPException(404, "Nota não encontrada ou sem permissão")
    return {"message": "Nota deletada com sucesso"}