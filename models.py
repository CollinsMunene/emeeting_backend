'''
/**
 * @author Collins Munene

 * @email hillarycollins@protonmail.com

 * @create date 2021-06-8 1:00:00
 * 
 * (c) Collins.
 */
'''

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time,Boolean
from database import Base

class meeting_info(Base):
    __tablename__ = "all_meetings"

    meeting_id = Column(Integer, primary_key=True, index=True)
    meeting_name = Column(String(200))
    meeting_agenda = Column(String(400))
    start_date_time = Column(String(100))
    end_date_time = Column(String(100))
    votes_yes = Column(Integer)
    votes_no = Column(Integer)

class participant_info(Base):
    __tablename__ = "patricipants"

    participant_id = Column(Integer, primary_key=True, index=True)
    participant_email = Column(String(100))

class document_info(Base):
    __tablename__ = "meeting_documents"

    document_id = Column(Integer, primary_key=True, index=True)
    document_name = Column(String(200))
    meeting_id = Column(Integer, ForeignKey("all_meetings.meeting_id"))