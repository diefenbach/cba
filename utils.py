import datetime
from django.template.loader import render_to_string


class JSCreator(object):
    def __init__(self, component, actions):
        self.actions = actions
        self.component = component

    def create_update(self, action):
        return render_to_string("cba/js/frontend_update.js", {
            "action": action,
            "component": self.component,
        })

    def create_backend_update(self, action):
        return render_to_string("cba/js/backend_update.js", {
            "action": action,
            "component": self.component,
        })

    def create_backend_update_simple(self):
        return render_to_string("cba/js/backend_update.js", {
            "component": self.component,
        })

    def create(self):
        return ""
        if self.component.id.find("note") != -1:
            return self.create_backend_update_simple()
        if self.actions:
            for action in self.actions:
                if action["type"] == "frontend":
                    return self.create_update(action)
                else:
                    return self.create_backend_update(action)
        else:
            return ""


def time_it(func, logger, log_message, func_args=None):
    start = datetime.datetime.now()
    if func_args:
        result = func(*func_args)
    else:
        result = func()

    end = datetime.datetime.now()
    logger.debug("{}: {}".format(log_message, end-start))
    return result
