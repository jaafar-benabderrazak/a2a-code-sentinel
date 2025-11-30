"""Message structures for code review communication"""

from pydantic import BaseModel, ConfigDict
from typing import List, Dict
from datetime import datetime


class CodeReviewMessage(BaseModel):
    """Message passed between review agents"""
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})
    
    id: str
    from_agent: str
    to_agent: str
    code_snippet: str
    language: str
    findings: List[Dict] = []
    severity_score: int = 0  # 0-10, higher = more issues
    timestamp: datetime = datetime.now()


