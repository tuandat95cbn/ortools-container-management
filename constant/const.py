import os
from enum import Enum
import collections

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
CONFIG_DIRECTORY_PATH = os.path.join(ROOT_PATH, 'config')
LOG_CONFIG_FILE_PATH = os.path.join(CONFIG_DIRECTORY_PATH, 'log.conf')
LOG_DIR = os.path.join(ROOT_PATH, 'logs')
UPLOAD_DIR = os.path.join(ROOT_PATH, 'uploads')
HOST_DIR='/home/ubuntu/data'

