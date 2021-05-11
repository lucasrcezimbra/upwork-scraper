from decouple import config

BASE_URL = 'https://www.upwork.com/'
DEBUG = config('DEBUG', default=False, cast=bool)
