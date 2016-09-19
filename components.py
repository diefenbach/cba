from . base import Component


class Button(Component):
    """A HTML button.

        handler
            The method which is called when the button is clicked.

        value
            The value of the button.

        default_ajax
            If set to true a click to the button will be processed by the
            default cba ajax behaviour, which means the click event will be
            sent to the given handler.
    """
    template = "cba/components/button.html"

    def __init__(self, id, value="", handler=None, default_ajax=True, *args, **kwargs):
        super(Button, self).__init__(id, *args, **kwargs)
        self.value = value
        self.handler = handler
        self.default_ajax = default_ajax


class Group(Component):
    """A simple group component to arrange compontens together. For instance for
    styling reasons or for easier refresh of sub components.
    """
    template = "cba/components/group.html"


class HiddenInput(Component):
    """Renders to a HTML input hidden tag.

        value
            The value of the hidden input field.
    """
    template = "cba/components/hidden_input.html"

    def __init__(self, value="", *args, **kwargs):
        super(HiddenInput, self).__init__(*args, **kwargs)
        self.value = value


class Image(Component):
    """Renders to a HTML img tag.

        src
            The url to the image file.

        alt
            The content alt tag of the image file.

        title
            The content of the title tag of the image.

    """
    template = "cba/components/image.html"

    def __init__(self, src, alt="", title="", *args, **kwargs):
        super(Image, self).__init__(*args, **kwargs)
        self.src = src
        self.alt = alt
        self.title = title


class Link(Component):
    template = "cba/components/link.html"

    def __init__(self, handler=None, text="", default_ajax=True, *args, **kwargs):
        super(Link, self).__init__(*args, **kwargs)
        self.default_ajax = default_ajax
        self.handler = handler
        self.text = text


class Menu(Component):
    template = "cba/components/menu.html"

    def __init__(self, id=None, name="", *args, **kwargs):
        super(Menu, self).__init__(id, *args, **kwargs)
        self.name = name


class MenuItem(Component):
    template = "cba/components/menu_item.html"

    def __init__(self, id=None, handler=None, href=None, name="", default_ajax=True, *args, **kwargs):
        super(MenuItem, self).__init__(id, *args, **kwargs)
        self.default_ajax = default_ajax
        self.handler = handler
        self.href = href
        self.name = name


class Message(Component):
    template = "cba/components/message.html"

    def __init__(self, id, text, *args, **kwargs):
        super(Message, self).__init__(id, *args, **kwargs)
        self.text = text


class Modal(Component):
    template = "cba/components/modal.html"

    def __init__(self, event_id, handler, header=None, text=None, *args, **kwargs):
        super(Modal, self).__init__(*args, **kwargs)
        self.text = text
        self.event_id = event_id
        self.handler = handler
        self.header = header


class Select(Component):
    template = "cba/components/select.html"

    def __init__(self, options, *args, **kwargs):
        super(Select, self).__init__(*args, **kwargs)
        self.options = options

    def get_name(self):
        for option in self.options:
            if str(option["value"]) == self.value:
                return option["name"]


class Table(Component):
    template = "cba/components/table.html"

    def __init__(self, id, columns, data=None, *args, **kwargs):
        super(Table, self).__init__(id, *args, **kwargs)
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


class Tabs(Component):
    template = "cba/components/tabs.html"


class Tab(Component):
    def __init__(self, id, title, active=False, *args, **kwargs):
        super(Tab, self).__init__(id, *args, **kwargs)
        self.active = active
        self.title = title


class TextArea(Component):
    template = "cba/components/textarea.html"

    def __init__(self, id, label=None, value="", error=None, rows=10, *args, **kwargs):
        super(TextArea, self).__init__(id, *args, **kwargs)
        self.label = label
        self.rows = rows
        self.value = value
        self.error = error

    def clear(self):
        self.value = ""


class Text(Component):
    template = "cba/components/text.html"

    def __init__(self, id=None, value="", *args, **kwargs):
        super(Text, self).__init__(id, *args, **kwargs)
        self.value = value


class TextInput(Component):
    template = "cba/components/text_input.html"

    def __init__(self, id, value="", label=None, error=None, *args, **kwargs):
        super(TextInput, self).__init__(id, *args, **kwargs)
        self.error = error
        self.label = label
        self.value = value

    def clear(self):
        self.error = ""
        self.value = ""
