# backend/app/models.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class MessageIn(BaseModel):
    msg_id: Optional[str] = None
    meta_msg_id: Optional[str] = None
    wa_id: str
    from_: str = Field(..., alias="from")  # alias for reserved word 'from'
    to: str
    text: Optional[str] = None
    timestamp: Optional[datetime] = None
    status: Optional[str] = "sent"  # sent | delivered | read
    direction: Optional[str] = "inbound"  # inbound | outbound
    name: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
