import json
from bson import json_util 

class JsonHelper:
    
    def parse_json(data):
        return json.loads(json_util.dumps(data))