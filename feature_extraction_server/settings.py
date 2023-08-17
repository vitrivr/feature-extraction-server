
from argparse import ArgumentParser
from decouple import config


LOG_LEVEL = 'INFO'
LOG_PATH = 'default.log'
DEFAULT_TASK = 'image_captioning'

LOG_LEVEL = config('LOG_LEVEL', default=LOG_LEVEL).upper()
LOG_PATH = config('LOG_PATH', default=LOG_PATH)
DEFAULT_TASK = config('DEFAULT_TASK', default=DEFAULT_TASK)


def add_args(ap: ArgumentParser):
    ap.add_argument('--log-level', dest='log_level', type=str, help='Log level. Can be one of DEBUG, INFO, WARNING, ERROR, CRITICAL')
    ap.add_argument('--log-path', dest='log_path', type=str, help='Path to the log file')
    ap.add_argument('--default-task', dest='default_task', type=str, help='Default task to run if no task is specified in the request')
    
def adopt_args(args):
    global LOG_LEVEL, LOG_PATH, DEFAULT_TASK
    LOG_LEVEL = args.log_level or LOG_LEVEL
    LOG_PATH = args.log_path or LOG_PATH
    DEFAULT_TASK = args.default_task or DEFAULT_TASK
    check_args()


def check_args():
    VALID_LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

    if LOG_LEVEL not in VALID_LOG_LEVELS:
        raise ValueError(f"Invalid LOG_LEVEL: {LOG_LEVEL}. Must be one of {VALID_LOG_LEVELS}")
    
check_args()