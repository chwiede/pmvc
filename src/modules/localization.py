import os
import json
import locale


json_data = None

def localize(folder, language=None):
    global json_data

    if language is None:
        language = locale.getdefaultlocale()[0]

    jsonFile = os.path.join(folder, "locale.%s.json" % language)
    if not os.path.isfile(jsonFile):
        jsonFile = os.path.join(folder, "locale.default.json")

    json_data = json.loads(open(jsonFile).read())


def LC(key):
    global json_data

    if json_data == None:
        return key

    if '.' in key:
        data = json_data
        for item in key.split('.'):
            if item in data:
                data = data[item]
            else:
                return key

        return data

    else:
        return json_data[key]