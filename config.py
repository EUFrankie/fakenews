from tempfile import mkdtemp
import os


class Config:
    """Set Flask configuration vars from .env file."""
    # General Config
    TEMPLATES_AUTO_RELOAD = True
    SESSION_FILE_DIR = mkdtemp()
    SESSION_PERMANENT = False
    SESSION_TYPE = 'filesystem'
    SECRET_KEY = 'this_is_our_key'
    UPLOAD_FOLDER = "data_importer/static/temp_files"

    # Database Config
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_ADDRESS', 'sqlite:///frankie.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False