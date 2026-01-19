import datetime
from enum import StrEnum

from pydantic import BaseModel


class SeverityEnum(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    NOTICE = "NOTICE"


class CloudLoggingBaseLogEntry(BaseModel):
    timestamp: datetime.datetime
    severity: SeverityEnum
    log_name: str
    insert_id: str
    text_payload: str