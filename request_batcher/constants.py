
import os
from dotenv import load_dotenv

# Sort out the .env file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Constants not controlled by .env
STATIC_FILE_LOC = 'static/pixel.png'

# Inbound requests
TRACKING_ID_QUERY_PARAM = os.getenv('TRACKING_ID_QUERY_PARAM', 'tracking_id')
OPEN_TRACKING_URL = os.getenv('OPEN_TRACKING_URL', '/open_tracking/')

# Outbound requests
OUTBOUND_REQUEST_USER_NAME = os.getenv('OUTBOUND_REQUEST_USER_NAME', 'user')
OUTBOUND_REQUEST_PASSWORD = os.getenv('OUTBOUND_REQUEST_PASSWORD', 'password')
EXPECTED_POST_STATUS = int(os.getenv('EXPECTED_POST_STATUS', 201))
OPEN_DATA_POST_URL = os.getenv('OPEN_DATA_POST_URL', 'http://localhost:8080/open_batch/')

# Memory-related
MAX_OPENS_ALLOWED_IN_STATE = int(os.getenv('MAX_OPENS_ALLOWED_IN_STATE', 1000000))
MAX_BATCH_TO_FLUSH = int(os.getenv('MAX_BATCH_TO_FLUSH', 10000))

# Task intervals
MONITOR_INTERVAL_SECONDS = int(os.getenv('MONITOR_INTERVAL_SECONDS', 120))
OPEN_FLUSH_INTERVAL_SECONDS = int(os.getenv('OPEN_FLUSH_INTERVAL_SECONDS', 30))
