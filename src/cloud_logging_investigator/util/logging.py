import logging

# Define the format
LOG_FORMAT = (
    '%(asctime)s - '
    '%(name)s - '
    '%(funcName)s - '
    '%(levelname)s - '
    '%(message)s'
)

# Configure the logging system
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt='%Y-%m-%d %H:%M:%S', # Optional: makes the date cleaner
    handlers=[
        logging.StreamHandler() # Outputs to console
    ]
)

def get_logger(name: str):
    return logging.getLogger(name)
