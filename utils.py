import datetime
import json
from django.template.loader import render_to_string
from django.utils.encoding import force_unicode
from django.utils.functional import Promise


class LazyEncoder(json.JSONEncoder):
    """Encodes django's lazy i18n strings.
    """
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        return obj


def time_it(func, logger, log_message, func_args=None):
    start = datetime.datetime.now()
    if func_args:
        result = func(*func_args)
    else:
        result = func()

    end = datetime.datetime.now()
    logger.debug("{}: {}".format(log_message, end-start))
    return result
