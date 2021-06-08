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

def get_all_meetings(db:Session):
    return db.query(models.meeting_info).all()

def get_meeting_by_id(db:Session,meeting_id: int):
    return db.query(models.meeting_info).filter(models.meeting_info.meeting_id==meeting_id).first()

def get_documents_by_meeting_id(db: Session, meeting_id: int):
    return db.query(models.document_info).filter(models.document_info.meeting_id==meeting_id).first()

def create_meeting(db: Session, meetingData: schemas.meetingInfoBase):
    print(meetingData)
    votes = 0
    db_meeting = models.meeting_info(meeting_name=meetingData.meeting_name,meeting_agenda=meetingData.meeting_agenda,start_date_time=meetingData.start_date_time,end_date_time=meetingData.end_date_time,votes_yes=votes,votes_no=votes)
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)

    response = {"message":"success","status":"OK","data":db_meeting}
    return response

def up_update_meeting_vote_by_meeting_id(db: Session, meeting_id: int):
    db_meeting = db.query(models.meeting_info).filter(models.meeting_info.meeting_id == meeting_id).first()
    print(db_meeting)
    newVote = db_meeting.votes_yes + 1 
    print(newVote)
    db_meeting_updated = db.query(models.meeting_info).filter(models.meeting_info.meeting_id == db_meeting.meeting_id).update({models.meeting_info.votes_yes:newVote})
    db.commit()

    response = {"message":"success","status":"OK","data":db_meeting_updated}
    return response

def down_update_meeting_vote_by_meeting_id(db: Session, meeting_id: int):
    db_meeting = db.query(models.meeting_info).filter(models.meeting_info.meeting_id == meeting_id).first()
    print(db_meeting)
    newVote = db_meeting.votes_no + 1
    db_meeting_updated = db.query(models.meeting_info).filter(models.meeting_info.meeting_id == db_meeting.meeting_id).update({models.meeting_info.votes_no:newVote})
    db.commit()

    response = {"message":"success","status":"OK","data":db_meeting_updated}
    return response

def upload_document_by_meeting_id(db: Session, meeting_id:str,document_name:str):
    db_document = models.document_info(meeting_id=meeting_id,document_name=document_name)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    response = {"message":"success","status":"OK","data":db_document}
    return response