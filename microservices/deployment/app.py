
import json
from jinja2 import Environment, FileSystemLoader

# ...existing code...

def fromjson(value):
    return json.loads(value)

env = Environment(loader=FileSystemLoader('templates'))
env.filters['fromjson'] = fromjson

# ...existing code...