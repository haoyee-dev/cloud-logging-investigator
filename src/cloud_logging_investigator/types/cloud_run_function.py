from typing import Optional

from .cloud_logging_base_entry import CloudLoggingBaseLogEntry


class CloudRunFunctionLogEntry(CloudLoggingBaseLogEntry):
    text_payload: str
    resource: Optional[dict] = None
    labels: Optional[dict] = None
    trace: Optional[str] = None
    span_id: Optional[str] = None
