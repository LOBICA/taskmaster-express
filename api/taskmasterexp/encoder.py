import json
from enum import Enum
from uuid import UUID


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj.hex)
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)
