import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_KEY_NAME = os.getenv('API_KEY_NAME')
COOKIE_DOMAIN = os.getenv('COOKIE_DOMAIN')
ADMIN_KEY = os.getenv('ADMIN_KEY')
ADMIN_KEY_NAME = os.getenv('ADMIN_KEY_NAME')
