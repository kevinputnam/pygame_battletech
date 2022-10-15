import json
from os.path import isfile

def save(path,settings):
    with open(path,'w') as outfile:
        json.dump(settings, outfile, indent=4)

def load(path):
    settings = {}
    if isfile(path):
        with open(path) as jsonFile:
            settings = json.load(jsonFile)
    return settings