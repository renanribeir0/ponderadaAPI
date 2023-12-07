# app/api/stories.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import async_session
from .. import crud, schemas, database
from app.gpt import generate_story_part
import httpx

router = APIRouter()

@router.post("/stories/", response_model=schemas.Story)
def create_story(story: schemas.StoryCreate, db: Session = Depends(async_session)):
    return crud.create_story(db=db, story=story)

@router.post("/stories/{story_id}/generate/", response_model=schemas.Story)
async def generate_story_part(story_id: int, prompt: str, db: Session = Depends(async_session)):
    db_story = crud.get_story(db=db, story_id=story_id)
    if db_story:
        new_part = generate_story_part(prompt)
        if new_part:
            db_story.content += "\n" + new_part
            db.commit()
            db.refresh(db_story)
            return db_story
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")
    
    # Obter a parte da história do ChatGPT
    chat_gpt_response = await request_chat_gpt(prompt)
    story_part = chat_gpt_response.get("choices", [{"text": ""}])[0]["text"]
    
    # Adicionar a parte da história ao conteúdo da história em questão
    db_story.content += "\n" + story_part  # Adicione a parte da história ao conteúdo existente
    
    # Atualizar a história no banco de dados
    updated_story = crud.update_story(db=db, story_id=story_id, updated_story=db_story)
    
    return updated_story

@router.get("/stories/", response_model=List[schemas.Story])
def get_all_stories(db: Session = Depends(async_session)):
    return crud.get_all_stories(db=db)

@router.get("/stories/{story_id}", response_model=schemas.Story)
def get_story(story_id: int, db: Session = Depends(async_session)):
    db_story = crud.get_story(db=db, story_id=story_id)
    if db_story is None:
        raise HTTPException(status_code=404, detail="Story not found")
    return db_story

@router.put("/stories/{story_id}", response_model=schemas.Story)
def update_story(story_id: int, story: schemas.StoryCreate, db: Session = Depends(async_session)):
    db_story = crud.update_story(db=db, story_id=story_id, updated_story=story)
    if db_story is None:
        raise HTTPException(status_code=404, detail="Story not found")
    return db_story

@router.delete("/stories/{story_id}", response_model=bool)
def delete_story(story_id: int, db: Session = Depends(async_session)):
    success = crud.delete_story(db=db, story_id=story_id)
    if not success:
        raise HTTPException(status_code=404, detail="Story not found")
    return True
