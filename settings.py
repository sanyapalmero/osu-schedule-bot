BOT_TOKEN = ""

DATABASE_FILE = ""

try:
    from local_settings import *  # noqa: F403,F401
except ImportError:
    pass
