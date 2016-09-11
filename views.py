import json
import logging

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View


logger = logging.getLogger(__name__)


class CBAView(View):
    template = "cba/main.html"

    def __init__(self, **kwargs):
        super(CBAView, self).__init__(**kwargs)
        self.root = self.root("root")
        self._html = []

    def _load_components(self, root):
        """
        Loads components with values from the browser.
        """
        if hasattr(root, "components"):
            for component in root.components:
                if component.id in self.request.GET:
                    root._components[component.id].value = self.request.GET.get(component.id)
                self.load_components(component)

    def collect_refreshed_components(self, root):
        """
        Collects the html from all components which should be refreshed.
        """
        if hasattr(root, "components"):
            for component in root.components:
                if component._html:
                    self._html.append(component._html)
                self.collect_refreshed_components(component)

    def get(self, *args, **kwargs):
        if self.request.is_ajax():
            self._load_components(self.root)

            handler = self.request.GET.get("handler")
            event_id = self.request.GET.get("event_id")
            component = self.root.get_component(event_id)

            # Bubbles up the components to find the handler
            while component:
                if hasattr(component, handler):
                    component.event_id = event_id
                    getattr(component, handler)()
                    break
                component = component.parent

            self.collect_refreshed_components(self.root)

            logger.debug("Refreshed components: {}".format(self._html))

            return HttpResponse(
                json.dumps({"html": self._html}),
                content_type='application/json'
            )
        else:
            return render(self.request, self.template, {
                "content": self.root.render()
            })
