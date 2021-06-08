'''
/**
 * @author Collins Munene

 * @email cmunene@devligence.com

 * @create date 2021-05-22 15:33:00
 * 
 * (c) Copyright by Devligence Limited.
 */
'''
 
from typing import List

import uvicorn
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException,Body,Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import webbrowser
from random import randint
import models, schemas, crud # import the files
from database import engine, SessionLocal # import d functions
import base64

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "E-Meetings API's",
    version = "1.0",
    description = "E-Meetings Application"
)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#  Dependency


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
@app.get("/get_all_meetings",tags=["Base Routes"])
def main_get_all_meetings(db: Session = Depends(get_db)):
    meetings = crud.get_all_meetings(db)
    return meetings

@app.get("/meeting_documents/{meeting_id}",tags=["Base Routes"])
def main_get_documents_by_meeting_id(meeting_id,db: Session = Depends(get_db)):
    hospital = crud.get_documents_by_meeting_id(db,meeting_id=meeting_id)
    return hospital

@app.post("/create_meeting",tags=["Base Routes"])
def main_create_meeting(meetingData: schemas.meetingInfoBase, db: Session = Depends(get_db)):
    return crud.create_meeting(db=db, meetingData=meetingData)

@app.post("/upvote/{meeting_id}",tags=["Voting Routes"])
def main_upvote(meeting_id,db: Session = Depends(get_db)):
    return crud.up_update_meeting_vote_by_meeting_id(db=db, meeting_id=meeting_id)

@app.post("/downvote/{meeting_id}",tags=["Voting Routes"])
def main_upvote(meeting_id,db: Session = Depends(get_db)):
    return crud.down_update_meeting_vote_by_meeting_id(db=db, meeting_id=meeting_id)

@app.post("/upload_documents",tags=["Documents Routes"])
def upload_document_by_meeting_id(documentData: schemas.meetingDocuments, db: Session = Depends(get_db)):
    return crud.create_meeting(db=db, documentData=documentData)

    