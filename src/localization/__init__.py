import os
import json
import locale

# get environment
currentLocale = locale.getdefaultlocale()[0]
currentFolder = os.path.dirname(__file__)

# load locale file
jsonFile = os.path.join(currentFolder, "locale.%s.json" % currentLocale)

# check locale exists...
if not os.path.isfile(jsonFile):
    jsonFile = os.path.join(currentFolder, "locale.default.json" % currentLocale)

print(jsonFile)

# load json
json_data = None
if os.path.isfile(jsonFile):
    json_data = json.loads(open(jsonFile).read())

# -------------------------------------------

def LC(key):
    if json_data == None:
        return key
    
    if '.' in key:
        data = json_data
        for crum in key.split('.'):
            if crum in data:
                data = data[crum]
            else:
                return key
    
        return data        

    else:
        return json_data[key]