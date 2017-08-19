# -*- coding: utf-8 -*-
import json

# Copied from: https://stackoverflow.com/a/16353080/539490

class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super(DatetimeEncoder, obj).default(obj)
        except TypeError:
            return str(obj)


def safe_json(obj):
    return json.dumps(obj, cls=DatetimeEncoder)
