'''
/**
 * @author Collins Munene

 * @email hillarycollins@protonmail.com

 * @create date 2021-06-8 1:00:00
 * 
 * (c) Collins.
 */
'''
 
from typing import List, Optional
from pydantic import BaseModel

class meetingInfoBase(BaseModel):
    meeting_name:str
    meeting_agenda:str
    start_date_time:str
    end_date_time:str
    votes_yes:Optional[int] = 0
    votes_no:Optional[int] = 0

class participantInfo(BaseModel):
    participant_email:str

class meetingDocuments(BaseModel):
    meeting_id:int
    document_name:str
