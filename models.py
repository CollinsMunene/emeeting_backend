'''
/**
 * @author Collins Munene

 * @email hillarycollins@protonmail.com

 * @create date 2021-06-8 1:00:00
 * 
 * (c) Collins.
 */
'''

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, Boolean
from database import Base

# User Model


class user_info(Base):
    __tablename__ = "users"

    users_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100))
    password = Column(String(200))

# Meeting Model


class meeting_info(Base):
    __tablename__ = "all_meetings"

    meeting_id = Column(Integer, primary_key=True, index=True)
    meeting_name = Column(String(200))
    meeting_agenda = Column(String(400))
    start_date_time = Column(String(100))
    end_date_time = Column(String(100))

# Participation Model


class participant_voting_info(Base):
    __tablename__ = "participants"

    participant_id = Column(Integer, primary_key=True, index=True)
    users_id = Column(Integer, ForeignKey("users.users_id"))
    meeting_issues_id = Column(Integer, ForeignKey(
        "meeting_issues.meeting_issues_id"))
    meeting_id = Column(Integer, ForeignKey("all_meetings.meeting_id"))
    vote = Column(String(100))
    hasVoted = Column(Boolean)

# Document Model


class document_info(Base):
    __tablename__ = "meeting_documents"

    document_id = Column(Integer, primary_key=True, index=True)
    document_name = Column(String(200))
    meeting_id = Column(Integer, ForeignKey("all_meetings.meeting_id"))

# Meeting Issue Model


class meeting_issues_info(Base):
    __tablename__ = "meeting_issues"

    meeting_issues_id = Column(Integer, primary_key=True, index=True)
    issue_name = Column(String(200))
    votes = Column(Integer)
    meeting_id = Column(Integer, ForeignKey("all_meetings.meeting_id"))
