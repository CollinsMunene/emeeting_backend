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
from fastapi import Depends, FastAPI, HTTPException, Body, Request, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import requests
import webbrowser
from random import randint
import models
import schemas
import crud  # import the files
from database import engine, SessionLocal  # import d functions
import base64
import shutil
import os
from fastapi.responses import FileResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-Meetings API's",
    version="1.0",
    description="E-Meetings Application"
)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# register new user route


@app.post("/register", tags=["Auth routes"])
def create_user(user: schemas.userInfo, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="email already registered")
    return crud.create_user(db=db, user=user)

# login user route


@app.post("/login", tags=["Auth routes"])
def main_login(userData: schemas.userInfo, db: Session = Depends(get_db)):
    user = crud.login(db, userData=userData)
    return user

# Create a new meeting route


@app.post("/create_meeting", tags=["Meeting Routes"])
def main_create_meeting(meetingData: schemas.meetingInfoBase, db: Session = Depends(get_db)):
    return crud.create_meeting(db=db, meetingData=meetingData)

# get all meetings route


@app.get("/get_all_meetings", tags=["Meeting Routes"])
def main_get_all_meetings(db: Session = Depends(get_db)):
    meetings = crud.get_all_meetings(db)
    return meetings

# get specific meeting route


@app.get("/get_meeting_by_id/{meeting_id}", tags=["Meeting Routes"])
def main_get_meeting_by_id(meeting_id, db: Session = Depends(get_db)):
    meeting = crud.get_meeting_by_id(db, meeting_id=meeting_id)
    return meeting

# get meeting document for a specific meeting route


@app.get("/meeting_documents/{meeting_id}", tags=["Meeting Routes"])
def main_get_documents_by_meeting_id(meeting_id, db: Session = Depends(get_db)):
    document = crud.get_documents_by_meeting_id(db, meeting_id=meeting_id)
    return document

# Update meeting details route


@app.post("/update_meeting/{meeting_id}", tags=["Meeting Routes"])
def main_update_meeting(meetingData: schemas.meetingInfoBase, meeting_id, db: Session = Depends(get_db)):
    return crud.update_meeting(db=db, meetingData=meetingData, meeting_id=meeting_id)

# Create meeting issue route


@app.post("/create_meeting_issue", tags=["Meeting Issue Routes"])
def main_create_meeting_issue(meetingIssueData: schemas.meetingIssueInfo, db: Session = Depends(get_db)):
    return crud.create_meeting_issue(db=db, meetingIssueData=meetingIssueData)

# get meeting issues for a specific meeting route


@app.get("/meeting_issues/{meeting_id}", tags=["Meeting Issue Routes"])
def main_get_issue_by_meeting_id(meeting_id, db: Session = Depends(get_db)):
    issue = crud.get_issue_by_meeting_id(db, meeting_id=meeting_id)
    return issue

# Vote yes to a meeting issue route


@app.post("/upvote/{meeting_issues_id}/{users_id}", tags=["Voting Routes"])
def main_upvote(meeting_issues_id, users_id, db: Session = Depends(get_db)):
    return crud.up_update_meeting_vote_by_meeting_id(db=db, meeting_issues_id=meeting_issues_id, users_id=users_id)

# Vote no to a meeting issue route


@app.post("/downvote/{meeting_issues_id}/{users_id}", tags=["Voting Routes"])
def main_downvote(meeting_issues_id, users_id, db: Session = Depends(get_db)):
    return crud.down_update_meeting_vote_by_meeting_id(db=db, meeting_issues_id=meeting_issues_id, users_id=users_id)

# Get all participants who have voted on a meeting issue route


@app.get("/get_all_participants/{meeting_id}", tags=["Voting Routes"])
def main_get_all_meeting_participants(meeting_id, db: Session = Depends(get_db)):
    participants = crud.get_all_participants_by_meeting_id(
        db, meeting_id=meeting_id)
    return participants

# Get all participants who have voted on a meeting issue by the user id and issue id route


@app.get("/get_participant_info/{users_id}/{meeting_issues_id}", tags=["Voting Routes"])
def main_get_all_participants_by_user_issue(users_id, meeting_issues_id, db: Session = Depends(get_db)):
    participant_info = crud.get_participants_by_meeting_issue_user_id(
        db, users_id=users_id, meeting_issues_id=meeting_issues_id)
    return participant_info

# Upload documents route


@app.post("/upload_documents", tags=["Documents Routes"])
def upload_document_by_meeting_id(meeting_id: int = Form(...), document: UploadFile = File(...), db: Session = Depends(get_db)):
    meeting_details = crud.get_meeting_by_id(db, meeting_id=meeting_id)
    file_location = f"meeting_documents/{meeting_details.meeting_name}_{document.filename}"
    filename = f"{meeting_details.meeting_name}_{document.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(document.file.read())
    return crud.upload_document_by_meeting_id(db=db, meeting_id=meeting_id, document_name=filename)

# Get document


@app.get("/download/{document_name}", tags=["Documents Routes"])
def downloadDocument(document_name, db: Session = Depends(get_db)):
    # DEPENDS ON WHERE YOUR FILE LOCATES
    file_path = os.getcwd() + "/meeting_documents/" + document_name
    return FileResponse(path=file_path, media_type='application/octet-stream', filename=document_name)
