import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://forum_db_e89m_user:ZyAxYHd3eSU8AHDbjTh591yYAO6hjs4X@dpg-d0hpuae3jp1c73bscca0-a/forum_db_e89m'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB
