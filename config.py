import yaml

def init_config(filename: str) -> dict:
    config = {}

    with open(filename, 'r', encoding='utf-8') as infile:
        config = yaml.load(infile, Loader=yaml.FullLoader)
    
    return config


CONFIG_FILE = "config.yaml"
CONFIG = init_config(CONFIG_FILE)

pool = CONFIG["pool"]
raw = CONFIG["raw"]
token = CONFIG["token"]

title_pseudonyms = CONFIG["title_pseudonyms"]
author_pseudonyms = CONFIG["author_pseudonyms"]
nation_pseudonyms = CONFIG["nation_pseudonyms"]
place_pseudonyms = CONFIG["place_pseudonyms"]

months = CONFIG["months"]
patches = CONFIG["patches"]
fixed_links = CONFIG["fixed_links"]
help_screen = CONFIG["help_screen"]
broken_patterns = CONFIG["broken_patterns"]