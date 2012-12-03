#-*- encoding:utf-8 -*-

import datetime
import re

from django.core.exceptions import ValidationError

def to_python(value):
    if isinstance(value, datetime.timedelta):
        return value
    match = re.match(r'(?:(\d+) days?, )?(\d+):(\d+)(?:\.(\d+))?', str(value))
    if match:
        parts = match.groups()
        # the parts in this list are as follows:
        # [days, hours, minutes, seconds, microseconds]
        # but microseconds need to be padded with zeros to work properly.
        parts[4] = parts[4].ljust(6, '0')
        parts = [part and int(part) or 0 for part in parts]
        return datetime.timedelta(parts[0], parts[3], parts[4],
                                  hours=parts[1], minutes=parts[2])

    try:
        return datetime.timedelta(seconds=float(value))
    except (TypeError, ValueError):
        raise ValidationError('This is must be a real number.')
    except OverflowError:
        raise ValidationError('The maximum allowed value is %s'
                              % datetime.timedelta.max)

