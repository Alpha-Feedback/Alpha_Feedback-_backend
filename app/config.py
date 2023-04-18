import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'dev'
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    UPLOADS_DEFAULT_DEST = 'app/static/images'
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL') or \
        'memory://'
    RATELIMIT_HEADERS_ENABLED = True
    RATELIMIT_STRATEGY = 'fixed-window-elastic-expiry'
    RATELIMIT_WINDOW_SIZE = '1 hour'
    RATELIMIT_BLOCK_DURATION = '15 minutes'
