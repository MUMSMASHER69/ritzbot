import json
import logging
import logging.config

from os import path
logging.config.fileConfig(
    path.join(path.dirname(path.abspath(__file__)), "config/logger.ini"), disable_existing_loggers=False
)
logger = logging.getLogger(__name__)

searchList = [
    r"\$(\d+\.?[0-9]?[0-9]?)",
    r"(\d+) [Dd]ollar[s]?",
    r"(\d+) [Bb]uck[s]?"
]

def open_config():
    with open("./ritzbot/config/config.json", 'r') as f:
        config = json.load(f)
        return config

def open_token():
    with open("./ritzbot/config/token.json", 'r') as f:
        tokenfile = json.load(f)    
        return tokenfile

