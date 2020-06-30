BOT_TOKEN = ""

BOT_PROXY = ""

DATABASE_FILE = ""

SEND_TIME = ""

try:
    from local_settings import *  # noqa: F403,F401
except ImportError:
    pass
