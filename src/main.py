from dotenv import load_dotenv
import pandas as pd
import os

from cloud_logging_investigator import investigator, util
from src.cloud_logging_investigator.types.cloud_logging_base_entry import SeverityEnum

load_dotenv()

logger = util.logging.get_logger(__name__)
OUTPUT_FILENAME = os.getenv('OUTPUT_FILENAME', default='logs.csv')
CLOUD_RUN_FUNCTION_NAME = os.getenv('CLOUD_RUN_FUNCTION_NAME')

def main():
    if not CLOUD_RUN_FUNCTION_NAME:
        raise ValueError(f'CLOUD_RUN_FUNCTION_NAME cannot be empty')
    log_investigator = investigator.Investigator()
    logs = log_investigator.get_cloud_run_function_logs(CLOUD_RUN_FUNCTION_NAME, severity=SeverityEnum.ERROR, start_date='2026-01-24')
    df = pd.DataFrame([log.model_dump() for log in logs])
    logger.info(f'Found {df.shape[0]} entries')
    df.to_csv(OUTPUT_FILENAME, index=False)


if __name__ == '__main__':
    main()