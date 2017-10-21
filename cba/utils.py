import datetime
import json
from cba import get_request
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
    logger.debug("{}: {}".format(log_message, end - start))
    return result


def get_from_session(key, default=None):
    """Gets a value from the session.

        key
            The key under which the value has been saved. When the key
            doesn't exist the method returns ``default``.

        default
            The value the method returns if key is not existing.
    """

    request = get_request()
    return request.session.get("cba", {}).get(key, default)


def set_to_session(key, value):
    """Saves a value to the session.

        key
            The key under which the value is saved.
        value
            The value to be saved.
    """
    request = get_request()
    request.session.setdefault("cba", {})[key] = value


def display_components(root):
    for component in root.components:
        print component
        display_components(component)
