from json import load, dump
from os.path import exists
from copy import deepcopy
from hashlib import sha1


class JsonSerialization:
    ### TASK: Write a SQL Manager in the future

    def __init__(self, path):
        self.path = path
        self.config = {}

        if exists(path):
            self.load()
        else:
            self.save()

        self.default_config = {
            "disabled_commands": [],
            "image_generation_channel" : None,
            "sd_presets": {}
        }

    def save(self):
        with open(self.path, "w") as f:
            dump(self.config, f, indent=True)

    def load(self):
        with open(self.path, "r") as f:
            self.config = load(f)

    def register_new_guild(self, guild):
        guild = sha1(str(guild).encode()).hexdigest()
        self.load()
        if guild not in self.config.keys():
            self.config[guild] = deepcopy(self.default_config)
            self.save()

        else:
            for default_key, default_value in self.default_config.items():
                if default_key not in self.config[guild].keys():
                    self.config[guild][default_key] = default_value
                    self.save()

    def change_value(self, guild, key, value):
        guild = sha1(str(guild).encode()).hexdigest()
        if type(self.config[guild][key]) == list:
            self.config[guild][key].append(value)
        else:
            self.config[guild][key] = value

        self.save()

    def restore_value(self, guild, key, value):
        guild = sha1(str(guild).encode()).hexdigest()
        if type(self.config[guild][key]) == list:
            if value in self.config[guild][key]:
                self.config[guild][key].remove(value)
        else:
            self.config[guild][key] = value

        self.save()

    def get(self, guild, key):
        guild = sha1(str(guild).encode()).hexdigest()
        try:
            return self.config[guild][key]
        except KeyError:
            return None
