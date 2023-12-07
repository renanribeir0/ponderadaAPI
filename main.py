# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, database
from app.gpt import generate_story_part

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def get_all_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db=db)

@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db=db, user_id=user_id, updated_user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}", response_model=bool)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = crud.delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return True


@app.post("/stories/", response_model=schemas.Story)
def create_story(story: schemas.StoryCreate, db: Session = Depends(get_db)):
    return crud.create_story(db=db, story=story)

@app.post("/stories/{story_id}/generate/", response_model=schemas.Story)
async def add_story_part(story_id: int, prompt: str, db: Session = Depends(get_db)):
    db_story = crud.get_story(db=db, story_id=story_id)
    if db_story:
        new_part = generate_story_part(prompt)
        if new_part:
            db_story.description += "\n" + new_part
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

@app.get("/stories/", response_model=List[schemas.Story])
def get_all_stories(db: Session = Depends(get_db)):
    return crud.get_all_stories(db=db)

@app.get("/stories/{story_id}", response_model=schemas.Story)
def get_story(story_id: int, db: Session = Depends(get_db)):
    db_story = crud.get_story(db=db, story_id=story_id)
    if db_story is None:
        raise HTTPException(status_code=404, detail="Story not found")
    return db_story

@app.put("/stories/{story_id}", response_model=schemas.Story)
def update_story(story_id: int, story: schemas.StoryCreate, db: Session = Depends(get_db)):
    db_story = crud.update_story(db=db, story_id=story_id, updated_story=story)
    if db_story is None:
        raise HTTPException(status_code=404, detail="Story not found")
    return db_story

@app.delete("/stories/{story_id}", response_model=bool)
def delete_story(story_id: int, db: Session = Depends(get_db)):
    success = crud.delete_story(db=db, story_id=story_id)
    if not success:
        raise HTTPException(status_code=404, detail="Story not found")
    return True

