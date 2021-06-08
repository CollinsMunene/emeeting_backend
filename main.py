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
from fastapi import Depends, FastAPI, HTTPException,Body,Request,File,UploadFile,Form
from fastapi.middleware.cors import CORSMiddleware
import requests
import webbrowser
from random import randint
import models, schemas, crud # import the files
from database import engine, SessionLocal # import d functions
import base64
import shutil,os

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

@app.get("/get_meeting_by_id/{meeting_id}",tags=["Base Routes"])
def main_get_meeting_by_id(meeting_id,db: Session = Depends(get_db)):
    meeting = crud.get_meeting_by_id(db,meeting_id=meeting_id)
    return meeting

@app.get("/meeting_documents/{meeting_id}",tags=["Base Routes"])
def main_get_documents_by_meeting_id(meeting_id,db: Session = Depends(get_db)):
    document = crud.get_documents_by_meeting_id(db,meeting_id=meeting_id)
    return document

@app.post("/create_meeting",tags=["Base Routes"])
def main_create_meeting(meetingData: schemas.meetingInfoBase, db: Session = Depends(get_db)):
    return crud.create_meeting(db=db, meetingData=meetingData)

@app.post("/upvote/{meeting_id}",tags=["Voting Routes"])
def main_upvote(meeting_id,db: Session = Depends(get_db)):
    return crud.up_update_meeting_vote_by_meeting_id(db=db, meeting_id=meeting_id)

@app.post("/downvote/{meeting_id}",tags=["Voting Routes"])
def main_downvote(meeting_id,db: Session = Depends(get_db)):
    return crud.down_update_meeting_vote_by_meeting_id(db=db, meeting_id=meeting_id)

@app.post("/upload_documents",tags=["Documents Routes"])
def upload_document_by_meeting_id(meeting_id: int = Form(...),document: UploadFile = File(...), db: Session = Depends(get_db)):
    meeting_details = crud.get_meeting_by_id(db,meeting_id=meeting_id)
    file_location = f"meeting_documents/{document.filename}_{meeting_details.meeting_name}_{meeting_id}"
    filename = f"{document.filename}_{meeting_details.meeting_name}_{meeting_id}"
    with open(file_location, "wb+") as file_object:
        file_object.write(document.file.read())
    return crud.upload_document_by_meeting_id(db=db,meeting_id=meeting_id,document_name=filename)

    