import json
import os

global lang

lang = json.load(open("languages/" + os.environ['language'] + ".json", 'r', encoding="UTF-8"))
