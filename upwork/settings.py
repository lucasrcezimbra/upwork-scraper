from decouple import config

BASE_URL = 'https://www.upwork.com/'
DEBUG = config('DEBUG', default=False, cast=bool)
HEADLESS = config('HEADLESS', default=True, cast=bool)
WAIT_TIMEOUT = config('WAIT_TIMEOUT', default=10, cast=int)
