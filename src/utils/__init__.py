from utils.json_serialization import JsonSerialization
from os.path import exists
from os import mkdir


if not exists("storage"):
    mkdir("storage")

JsonManager = JsonSerialization("storage\\guild_data.json")