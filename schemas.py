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

# User Request,Response model


class userInfo(BaseModel):
    email: str
    password: str

# Meeting Request,Response model


class meetingInfoBase(BaseModel):
    meeting_name: str
    meeting_agenda: str
    start_date_time: str
    end_date_time: str

# Participation Request,Response model


class participantInfo(BaseModel):
    users_id: int
    meeting_id: int
    meeting_issues_id: int
    vote: Optional[str] = None
    hasVoted: Optional[str] = None

# Meeting Documents Request,Response model


class meetingDocuments(BaseModel):
    meeting_id: int
    document_name: str

# Meeting Issue Request,Response model


class meetingIssueInfo(BaseModel):
    meeting_id: int
    issue_name: str
    votes: int
