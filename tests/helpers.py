from env_setup import setup_django; setup_django()

import json

from restler.serializers import to_json


def flip(*args, **kwargs):
    return json.loads(to_json(*args, **kwargs))
