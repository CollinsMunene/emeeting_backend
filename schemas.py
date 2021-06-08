'''
/**
 * @author Collins Munene

 * @email hillarycollins@protonmail.com

 * @create date 2021-06-8 1:00:00
 * 
 * (c) Collins.
 */
'''
 
from typing import List
from pydantic import BaseModel

class meetingInfoBase(BaseModel):
    meeting_name:str
    meeting_agenda:str
    start_date_time:str
    end_date_time:str
    number_of_participants:int
    votes:int

class participantInfo(BaseModel):
    participant_email:str

class meetingDocuments(BaseModel):
    meeting_id:int
    document_name:str
    document_path:str
