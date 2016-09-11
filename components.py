from . base import Component


class Page(Component):
    template = "cba/components/page.html"


class Text(Component):
    template = "cba/components/text.html"

    def __init__(self, id, value):
        super(Text, self).__init__(id)
        self.value = value


class TextInput(Component):
    template = "cba/components/text_input.html"

    def __init__(self, id, value="", actions=None):
        super(TextInput, self).__init__(id)
        self.actions = actions
        self.value = value


class HiddenInput(TextInput):
    template = "cba/components/hidden_input.html"

    def __init__(self, id, value="", actions=None):
        super(HiddenInput, self).__init__(id)
        self.actions = actions
        self.value = value


class Select(Component):
    template = "cba/components/select.html"

    def __init__(self, id, options, actions=None):
        super(Select, self).__init__(id)
        self.options = options

    def get_name(self):
        for option in self.options:
            if str(option["value"]) == self.value:
                return option["name"]


class Tab(Component):
    template = "cba/components/tab.html"


class TabItem(Component):
    template = "cba/components/tab_item.html"

    def __init__(self, id, title, active=False, *args, **kwargs):
        super(TabItem, self).__init__(id, *args, **kwargs)
        self.title = title
        self.active = active


class TextArea(Component):
    template = "cba/components/textarea.html"

    def __init__(self, id, value="", active=False, *args, **kwargs):
        super(TextArea, self).__init__(id, *args, **kwargs)
        self.value = value


class Button(Component):
    template = "cba/components/button.html"

    def __init__(self, handler, value="", *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
        self.handler = handler
        self.value = value


class Table(Component):
    template = "cba/components/table.html"

    def __init__(self, columns, data=None, *args, **kwargs):
        super(Table, self).__init__(*args, **kwargs)
        self.data = data or []
        self.columns = columns

    def add_data(self, data):
        temp = []
        for item in data:
            if isinstance(item, Component):
                self.add_component(item)
                temp.append(item.render())
            else:
                temp.append(item)
        self.data.append(temp)


class Image(Component):
    template = "cba/components/image.html"

    def __init__(self, src, *args, **kwargs):
        super(Image, self).__init__(*args, **kwargs)
        self.src = src
