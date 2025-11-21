from configparser import ConfigParser

def get_config(section, key, fallback=None):
    config = ConfigParser()
    config.read("config.ini")
    return config.get(section, key, fallback=fallback)
