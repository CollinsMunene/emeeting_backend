'''
/**
 * @author Collins Munene

 * @email hillarycollins@protonmail.com

 * @create date 2021-06-8 1:00:00
 * 
 * (c) Collins.
 */
'''
 
from sqlalchemy.orm import Session
import models, schemas
import bcrypt
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
import base64
import hashlib
import os

def create_user(db: Session, user: schemas.userInfo):
    print(user)
    password = user.password
    salt = os.urandom(32) # A new salt for this user
    # hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    print("heyy")
    db_user = models.user_info(email=user.email,password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    response = {"message":"success","status":"OK","data":db_user}
    return response

# Get user by email function
def get_user_by_email(db: Session, email: str):
    return db.query(models.user_info).filter(models.user_info.email == email).first()

# Get user by id function
def get_user_by_id(db: Session, users_id: int):
    db_user = db.query(models.user_info).filter(models.user_info.users_id == users_id).first()
    return db_user

def get_all_participants_by_meeting_id(db:Session,meeting_id:int):
    participants = db.query(models.participant_voting_info).filter(models.participant_voting_info.meeting_id == meeting_id).all()
    for i in range(len(participants)):
        user = get_user_by_id(db,users_id=participants[i].users_id)
        issue = get_meeting_issue_by_id(db,meeting_issues_id=participants[i].meeting_issues_id)
        new_participant_info = {
            "vote":participants[i].vote,
            "user":user,
            "issue":issue
        }
        return new_participant_info

def get_participants_by_meeting_issue_user_id(db:Session,meeting_issues_id:int,users_id:int):
    participants = db.query(models.participant_voting_info).filter(models.participant_voting_info.meeting_issues_id == meeting_issues_id).first()
    participant_final = db.query(models.participant_voting_info).filter(models.participant_voting_info.users_id == users_id).first()
    return participant_final

def login(db: Session, userData: schemas.userInfo):
    print(userData)
    db_user = db.query(models.user_info).filter(models.user_info.email == userData.email).first()
    if db_user:
        passw = bcrypt.checkpw(userData.password.encode('utf-8'),db_user.password.encode('utf-8'))
        print(passw)
        if passw:
            response = {"message":"success","status":"OK","data":db_user}
            return response
        else:
            response = {"message":"failed","status":"OK","data":"Invalid Password"}
            return response
    else:
        response = {"message":"failed","status":"failed","data":"No User"}
        return response

def get_all_meetings(db:Session):
    return db.query(models.meeting_info).all()

def get_meeting_by_id(db:Session,meeting_id: int):
    return db.query(models.meeting_info).filter(models.meeting_info.meeting_id==meeting_id).first()

def get_documents_by_meeting_id(db: Session, meeting_id: int):
    return db.query(models.document_info).filter(models.document_info.meeting_id==meeting_id).all()

def get_issue_by_meeting_id(db: Session, meeting_id: int):
    return db.query(models.meeting_issues_info).filter(models.meeting_issues_info.meeting_id==meeting_id).all()

def get_meeting_issue_by_id(db: Session, meeting_issues_id: int):
    return db.query(models.meeting_issues_info).filter(models.meeting_issues_info.meeting_issues_id==meeting_issues_id).first()

def create_meeting(db: Session, meetingData: schemas.meetingInfoBase):
    print(meetingData)
    db_meeting = models.meeting_info(meeting_name=meetingData.meeting_name,meeting_agenda=meetingData.meeting_agenda,start_date_time=meetingData.start_date_time,end_date_time=meetingData.end_date_time)
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)

    response = {"message":"success","status":"OK","data":db_meeting}
    return response

def update_meeting(db: Session, meetingData:schemas.meetingInfoBase,meeting_id:int):
    print(meetingData)
    # models.meeting_info.meeting_name:meetingData.meeting_name,models.meeting_info.meeting_agenda:meetingData.meeting_agenda,models.meeting_info.start_date_time:meetingData.start_date_time,models.meeting_info.end_date_time:meetingData.end_date_time
    db_meetings = db.query(models.meeting_info).filter(models.meeting_info.meeting_id == meeting_id).first()
    db_meetings.meeting_name = meetingData.meeting_name
    db_meetings.meeting_agenda = meetingData.meeting_agenda
    db_meetings.start_date_time = meetingData.start_date_time
    db_meetings.end_date_time = meetingData.end_date_time
    db.add(db_meetings)
    db.commit()
    db.refresh(db_meetings)

    response = {"message":"success","status":"OK","data":db_meetings}
    return response

def create_meeting_issue(db: Session, meetingIssueData: schemas.meetingIssueInfo):
    print(meetingIssueData)
    db_meeting_issue = models.meeting_issues_info(issue_name=meetingIssueData.issue_name,meeting_id=meetingIssueData.meeting_id,votes=0)
    db.add(db_meeting_issue)
    db.commit()
    db.refresh(db_meeting_issue)

    response = {"message":"success","status":"OK","data":db_meeting_issue}
    return response

def up_update_meeting_vote_by_meeting_id(db: Session, meeting_issues_id: int,users_id:int):
    db_meeting = db.query(models.meeting_issues_info).filter(models.meeting_issues_info.meeting_issues_id == meeting_issues_id).first()
    print(db_meeting.votes)
    newVote = db_meeting.votes + 1 
    print(newVote)
    db_meeting_updated = db.query(models.meeting_issues_info).filter(models.meeting_issues_info.meeting_issues_id == meeting_issues_id).update({models.meeting_issues_info.votes:newVote})
    db.commit()

    db_user = db.query(models.user_info).filter(models.user_info.users_id == users_id).first()
    print(db_user)
    db_issue_participation = models.participant_voting_info(users_id=db_user.users_id,meeting_id=db_meeting.meeting_id,meeting_issues_id=meeting_issues_id,vote="Yes",hasVoted = True)
    db.add(db_issue_participation)
    db.commit()
    db.refresh(db_issue_participation)

    response = {"message":"success","status":"OK","data":db_meeting_updated}
    return response

def down_update_meeting_vote_by_meeting_id(db: Session, meeting_issues_id: int,users_id:int):
    db_meeting_issue = db.query(models.meeting_issues_info).filter(models.meeting_issues_info.meeting_issues_id == meeting_issues_id).first()
    print(db_meeting_issue)
    newVote = db_meeting_issue.votes + 1 
    print(newVote)
    db_meeting_updated = db.query(models.meeting_issues_info).filter(models.meeting_issues_info.meeting_issues_id == meeting_issues_id).update({models.meeting_issues_info.votes:newVote})
    db.commit()

    db_user = db.query(models.user_info).filter(models.user_info.users_id == users_id).first()
    print(db_user)
    db_issue_participation = models.participant_voting_info(users_id=db_user.users_id,meeting_id=db_meeting.meeting_id,meeting_issues_id=meeting_issues_id,vote="No",hasVoted = True)
    db.add(db_issue_participation)
    db.commit()
    db.refresh(db_issue_participation)

    response = {"message":"success","status":"OK","data":db_meeting_updated}
    return response

def upload_document_by_meeting_id(db: Session, meeting_id:str,document_name:str):
    db_document = models.document_info(meeting_id=meeting_id,document_name=document_name)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    response = {"message":"success","status":"OK","data":db_document}
    return response