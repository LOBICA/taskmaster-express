import json
from datetime import date
from enum import Enum
from uuid import UUID


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj.hex)
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)
