BOT_TOKEN = ""

BOT_PROXY = ""

STORAGE_FILE = ""

SEND_TIME = ""

try:
    from local_settings import *  # noqa: F403,F401
except ImportError:
    pass
