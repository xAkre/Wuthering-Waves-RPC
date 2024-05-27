from os.path import exists
from json import loads
from src.utilities.rpc import Presence

if not exists("config/config.json"):
    raise Exception("Config file does not exist")

with open("config/config.json", "r") as f:
    config = loads(f.read())

presence = Presence(config)
presence.start()
