import datetime
import json
from typing import Generator, Any

from google.cloud import logging
from google.cloud.logging_v2 import LogEntry

from .types.cloud_logging_base_entry import CloudLoggingBaseLogEntry, SeverityEnum
from .types.cloud_run_function import CloudRunFunctionLogEntry
from .util import logging as custom_logging

logger = custom_logging.get_logger(__name__)


class Investigator:
    """Retrieves the logs from Cloud Logging for further investigation

    Functions:
        get_cloud_run_function_logs: Retrieve Cloud Run Function logs

    """

    def __init__(self):
        self.client = logging.Client()

    def _get_logs(self, filter_string: str) -> Generator[Any, Any, None]:
        return self.client.list_entries(filter_=filter_string)

    def get_cloud_run_function_logs(self, function_name: str, severity: SeverityEnum = SeverityEnum.ERROR, start_date: str = "") -> Generator[CloudRunFunctionLogEntry]:
        """

        Args:
            function_name: Cloud Run Function name
            severity: Log severity to filter for
            start_date: Logs starting since the start date in YYYY-MM-DD format

        Returns:
            Generator of Cloud Run Function Log Entries
        """
        filter_string = f'resource.type="cloud_run_revision" AND resource.labels.service_name="{function_name}" AND severity>="{severity}"'
        if not start_date:
            start_date = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        filter_string += f' AND timestamp > "{start_date}"'

        logger.info(f'Cloud Logging Filter String: {filter_string}')

        log_entries =  self._get_logs(filter_string)
        return (CloudRunFunctionLogEntry.model_validate(self.log_entry_to_dict(entry)) for entry in log_entries)


    @staticmethod
    def log_entry_to_dict(entry: LogEntry) -> dict:
        """Convert a log entry to a dictionary.

        entry: Google Log Entry

        Returns:
            a dictionary representing the log entry
        """
        entry_dict = {
            "timestamp": entry.timestamp.isoformat() if entry.timestamp else None,
            "severity": entry.severity,
            "log_name": entry.log_name,
            "insert_id": entry.insert_id,
        }

        # Handle different payload types
        if hasattr(entry, 'payload') and entry.payload:
            # TextPayload
            if isinstance(entry.payload, str):
                entry_dict["text_payload"] = entry.payload
            # JsonPayload (already a dict)
            elif isinstance(entry.payload, dict):
                entry_dict["text_payload"] = json.dumps(entry.payload)
            else:
                entry_dict["text_payload"] = str(entry.payload)
        else:
            entry_dict["text_payload"] = ""
        # Add resource info
        if entry.resource:
            entry_dict["resource"] = {
                "type": entry.resource.type,
                "labels": dict(entry.resource.labels)
            }

        # Add labels
        if entry.labels:
            entry_dict["labels"] = dict(entry.labels)

        # Add trace and span if present
        if entry.trace:
            entry_dict["trace"] = entry.trace
        if entry.span_id:
            entry_dict["span_id"] = entry.span_id
        print(entry)
        return entry_dict
