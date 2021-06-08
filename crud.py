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

def get_documents_by_meeting_id(db: Session, meeting_id: int):
    return db.query(models.meeting_info).filter(models.document_info.meeting_id == meeting_id).first()

def create_meeting(db: Session, meetingData: schemas.meetingInfoBase):
    print(meetingData)
    votes = 1
    number_of_participants = 1
    db_meeting = models.meeting_info(first_name=meetingData.meeting_name,meeting_agenda=meetingData.meeting_agenda,start_date_time=meetingData.start_date_time,end_date_time=meetingData.end_date_time,votes=votes,number_of_participants=number_of_participants)
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)

    response = {"message":"success","status":"OK","data":db_meeting}
    return response

def up_update_meeting_vote_by_meeting_id(db: Session, meeting_id: int):
    db_meeting = db.query(models.meeting_info).filter(models.meeting_info.meeting_id == meeting_id).first()
    print(db_meeting)
    newVote += db_meeting.votes
    db_meeting_updated = db.query(models.meeting_info).filter(models.meeting_info.meeting_id == db_meeting.patient_id).update({models.meeting_info.votes:newVote})
    db.commit()

    response = {"message":"success","status":"OK","data":db_meeting_updated}
    return response

def down_update_meeting_vote_by_meeting_id(db: Session, meeting_id: int):
    db_meeting = db.query(models.meeting_info).filter(models.meeting_info.meeting_id == meeting_id).first()
    print(db_meeting)
    newVote -= db_meeting.votes
    db_meeting_updated = db.query(models.meeting_info).filter(models.meeting_info.meeting_id == db_meeting.patient_id).update({models.meeting_info.votes:newVote})
    db.commit()

    response = {"message":"success","status":"OK","data":db_meeting_updated}
    return response

def upload_document_by_meeting_id(db: Session, documentData: schemas.meetingDocuments):
    print(documentData)
    db_document = models.document_info(meeting_id=documentData.meeting_id,document_name=documentData.document_name,document_path=documentData.document_path)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    response = {"message":"success","status":"OK","data":db_document}
    return response