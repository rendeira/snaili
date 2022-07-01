import json
import os

global lang

lang = json.load(open("languages/" + os.environ['language'] + ".json"))
