from tempfile import mkdtemp


class Config:
    """Set Flask configuration vars from .env file."""
    # General Config
    TEMPLATES_AUTO_RELOAD = True
    SESSION_FILE_DIR = mkdtemp()
    SESSION_PERMANENT = False
    SESSION_TYPE = 'filesystem'