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
import os

#Create New User func
def create_user(db: Session, user: schemas.userInfo):
    salt = os.urandom(32) # A new salt for this user
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db_user = models.user_info(email=user.email,password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    response = {"message":"success","status":"OK","data":db_user}
    return response

# Get user by email func
def get_user_by_email(db: Session, email: str):
    return db.query(models.user_info).filter(models.user_info.email == email).first()

# Get user by id func
def get_user_by_id(db: Session, users_id: int):
    db_user = db.query(models.user_info).filter(models.user_info.users_id == users_id).first()
    return db_user

# Get all participants for a specific meeting func
def get_all_participants_by_meeting_id(db:Session,meeting_id:int):
    participants = db.query(models.participant_voting_info).filter(models.participant_voting_info.meeting_id == meeting_id).all()
    all_part = []
    for i in range(len(participants)):
        user = get_user_by_id(db,users_id=participants[i].users_id)
        issue = get_meeting_issue_by_id(db,meeting_issues_id=participants[i].meeting_issues_id)
        new_participant_info = {
            "vote":participants[i].vote,
            "user":user,
            "issue":issue
        }
        all_part.append(new_participant_info)
    return all_part

# Get participants who have participated in a specific meeting issue func
def get_participants_by_meeting_issue_user_id(db:Session,users_id:int,meeting_issues_id:int):
    participants = db.query(models.participant_voting_info).filter(models.participant_voting_info.meeting_issues_id == meeting_issues_id,models.participant_voting_info.users_id == users_id).first()
    return participants

# User Login func
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
            return "error"
    else:
        return "error"

# Get all created meetings func
def get_all_meetings(db:Session):
    return db.query(models.meeting_info).all()

# Get a specific meeting details by it's id func
def get_meeting_by_id(db:Session,meeting_id: int):
    return db.query(models.meeting_info).filter(models.meeting_info.meeting_id==meeting_id).first()

# Get all documents for a meeting func
def get_documents_by_meeting_id(db: Session, meeting_id: int):
    return db.query(models.document_info).filter(models.document_info.meeting_id==meeting_id).all()

# Get meeting issues raised for a specific meeting
def get_issue_by_meeting_id(db: Session, meeting_id: int):
    return db.query(models.meeting_issues_info).filter(models.meeting_issues_info.meeting_id==meeting_id).all()

# Get a specific meeting issue by it's id
def get_meeting_issue_by_id(db: Session, meeting_issues_id: int):
    return db.query(models.meeting_issues_info).filter(models.meeting_issues_info.meeting_issues_id==meeting_issues_id).first()

# Create a new meeting
def create_meeting(db: Session, meetingData: schemas.meetingInfoBase):
    db_meeting = models.meeting_info(meeting_name=meetingData.meeting_name,meeting_agenda=meetingData.meeting_agenda,start_date_time=meetingData.start_date_time,end_date_time=meetingData.end_date_time)
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)

    response = {"message":"success","status":"OK","data":db_meeting}
    return response

# Update an exisiting meeting details
def update_meeting(db: Session, meetingData:schemas.meetingInfoBase,meeting_id:int):
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

# Create a meeting issue that was raised during the meeting func
def create_meeting_issue(db: Session, meetingIssueData: schemas.meetingIssueInfo):
    db_meeting_issue = models.meeting_issues_info(issue_name=meetingIssueData.issue_name,meeting_id=meetingIssueData.meeting_id,votes=0)
    db.add(db_meeting_issue)
    db.commit()
    db.refresh(db_meeting_issue)

    response = {"message":"success","status":"OK","data":db_meeting_issue}
    return response

# Vote yes to a meeting issue func
def up_update_meeting_vote_by_meeting_id(db: Session, meeting_issues_id: int,users_id:int):
    db_meeting = db.query(models.meeting_issues_info).filter(models.meeting_issues_info.meeting_issues_id == meeting_issues_id).first()
    newVote = db_meeting.votes + 1 
    db_meeting_updated = db.query(models.meeting_issues_info).filter(models.meeting_issues_info.meeting_issues_id == meeting_issues_id).update({models.meeting_issues_info.votes:newVote})
    db.commit()

    db_user = db.query(models.user_info).filter(models.user_info.users_id == users_id).first()
    db_issue_participation = models.participant_voting_info(users_id=db_user.users_id,meeting_id=db_meeting.meeting_id,meeting_issues_id=meeting_issues_id,vote="Yes",hasVoted = True)
    db.add(db_issue_participation)
    db.commit()
    db.refresh(db_issue_participation)

    response = {"message":"success","status":"OK","data":db_meeting_updated}
    return response

# Vote no to a meeting issue func
def down_update_meeting_vote_by_meeting_id(db: Session, meeting_issues_id: int,users_id:int):
    db_meeting = db.query(models.meeting_issues_info).filter(models.meeting_issues_info.meeting_issues_id == meeting_issues_id).first()
    newVote = db_meeting.votes + 1 
    db_meeting_updated = db.query(models.meeting_issues_info).filter(models.meeting_issues_info.meeting_issues_id == meeting_issues_id).update({models.meeting_issues_info.votes:newVote})
    db.commit()

    db_user = db.query(models.user_info).filter(models.user_info.users_id == users_id).first()
    db_issue_participation = models.participant_voting_info(users_id=db_user.users_id,meeting_id=db_meeting.meeting_id,meeting_issues_id=meeting_issues_id,vote="No",hasVoted = True)
    db.add(db_issue_participation)
    db.commit()
    db.refresh(db_issue_participation)

    response = {"message":"success","status":"OK","data":db_meeting_updated}
    return response

# Upload meeting documents func
def upload_document_by_meeting_id(db: Session, meeting_id:str,document_name:str):
    db_document = models.document_info(meeting_id=meeting_id,document_name=document_name)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    response = {"message":"success","status":"OK","data":db_document}
    return response