# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import stories, users
from typing import List
from . import schemas, crud, database

app = FastAPI()
