from . base import Component


class Button(Component):
    """A HTML button.

        value
            The value of the button.
    """
    template = "cba/components/button.html"

    def __init__(self, value="", *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
        self.value = value


class ConfirmModal(Component):
    """A convenient modal dialog with a yes and no button. When the dialog is
       answered with yes the handler method is called via an ajax request.

        event_id
            The event_id which is passed to the backend when the dialog has
            been approved.

        handler
            The method which is called when the dialog has been approved.

        header
            The header of the dialog which is displayed to the user.

        text
            The text of the dialog which is displayed to the user.
    """
    template = "cba/components/confirm_modal.html"
    remove_after_render = True

    def __init__(self, event_id, handler, header=None, text=None, *args, **kwargs):
        super(ConfirmModal, self).__init__(*args, **kwargs)
        self.event_id = event_id
        self.handler = handler
        self.header = header
        self.text = text


class FileInput(Component):
    """An HTML file input.

        error
            The current validation error of the text input.

        icon
            An optional icon of the text input, see http://semantic-ui.com/elements/icon.html
            for more.

        icon_position
            The position of the icon (one of ``left`` or ``right``).

        label
            An optional label of the text input.

        placeholder
            The optional placeholder of the text input. If given it is
            displayed within the input field.

        value
            The current value of the text input.
    """
    template = "cba/components/file_input.html"

    def __init__(self, id=None, value="", label=None, placeholder=None, error=None, icon=None, icon_position="left", *args, **kwargs):
        super(FileInput, self).__init__(id, *args, **kwargs)
        self.error = error
        self.icon = icon
        self.icon_position = icon_position
        self.label = label
        self.placeholder = placeholder
        self.value = value

    def clear(self):
        """Sets the value and error messages to empty strings.
        """
        self.error = ""
        self.value = ""


class Group(Component):
    """A simple group component to arrange compontens together. For instance for
    styling reasons or to easier refresh its sub components.
    """
    template = "cba/components/group.html"


class HiddenInput(Component):
    """A HTML hidden input field.

        value
            The value of the hidden input field.
    """
    template = "cba/components/hidden_input.html"

    def __init__(self, value="", *args, **kwargs):
        super(HiddenInput, self).__init__(*args, **kwargs)
        self.value = value


class HTML(Component):
    """A HTML tag.

        tag
            The outer tag of the component.

        text
            The text of the component. Will be rendered within the outer tag.
    """
    template = "cba/components/html.html"

    def __init__(self, tag="div", text="", *args, **kwargs):
        super(HTML, self).__init__(*args, **kwargs)
        self.tag = tag
        self.text = text


class Image(Component):
    """A HTML image component.

        alt
            The content alt tag of the image file.

        src
            The url to the image file.

        title
            The content of the title tag of the image.

    """
    template = "cba/components/image.html"

    def __init__(self, alt="", src="", title="", *args, **kwargs):
        super(Image, self).__init__(*args, **kwargs)
        self.alt = alt
        self.src = src
        self.title = title


class Link(Component):
    """A HTML link.

        text
            The content of the HTML tag.
    """
    template = "cba/components/link.html"

    def __init__(self, text="", *args, **kwargs):
        super(Link, self).__init__(*args, **kwargs)
        self.text = text


class Menu(Component):
    """The root container of a pop up menu.

        direction
            The direction of the menu. One of ``vertical`` or ``horizonal``.

    """
    template = "cba/components/menu.html"

    def __init__(self, direction="horizonal", *args, **kwargs):
        super(Menu, self).__init__(*args, **kwargs)
        self.direction = direction


class MenuItem(Component):
    """An item a menu.

        handler
            The method which is called when the button is clicked.

        href
            Optional URL the item links to.

        label
            Optional label of the menu item.

        name
            The name of the menu item. This is displayed to the user.
    """
    template = "cba/components/menu_item.html"

    def __init__(self, href=None, label=None, name="", *args, **kwargs):
        super(MenuItem, self).__init__(*args, **kwargs)
        self.href = href
        self.label = label
        self.name = name


class Modal(Component):
    """A modal dialog.

        header
            The header of the dialog which is displayed to the user.

        close_button
            When set to True a close button is displayed.
    """
    template = "cba/components/modal.html"
    remove_after_render = True

    def __init__(self, header=None, close_button=True, *args, **kwargs):
        super(Modal, self).__init__(*args, **kwargs)
        self.header = header
        self.close_button = close_button


class Select(Component):
    """A HTML Select box.

        label
            An optional label for the select box.

        options
            Options which can be selected by the user.

        The current value (selected values) of the select box.
    """
    template = "cba/components/select.html"

    def __init__(self, id, label=None, value=None, options=None, multiple=False, *args, **kwargs):
        super(Select, self).__init__(id, *args, **kwargs)
        self.label = label
        self.multiple = multiple
        self.options = options or []
        self.value = value

    def get_names(self):
        """Returns the names of all selected options as a list.
        """
        names = []
        for option in self.options:
            if str(option["value"]) in self.values:
                self.names.append(option["name"])
        return names

    def clear(self):
        self.value = None


class Table(Component):
    """A HTML table

        columns
            A list of strings which represent the header of the table.

        data
            A list of list which represents the rows and columns of the table.
    """
    template = "cba/components/table.html"

    def __init__(self, columns, label=None, selected=None, *args, **kwargs):
        super(Table, self).__init__(*args, **kwargs)
        self.columns = columns
        self.label = label

    def clear(self):
        """Deletes all rows of the table.
        """
        self._components.clear()


class TableRow(Component):
    """A table row.
    """
    template = "cba/components/table_row.html"


class TableColumn(Component):
    """A table column.
    """
    template = "cba/components/table_column.html"


class Tab(Component):
    """The container component for tab item.
    """
    template = "cba/components/tab.html"


class TabItem(Component):
    """A tab item.

        active
            If true the tab item is displayed.

        title
            The title of the tab item.
    """
    def __init__(self, title="", active=False, *args, **kwargs):
        super(TabItem, self).__init__(*args, **kwargs)
        self.active = active
        self.title = title


class TextArea(Component):
    """A HTML Textarea

        error
            The current validation error of the text area.

        label
            An optional label of the text area.

        rows
            The amount of rows of the text area.
.
        value
            The current value of the text area.
    """
    template = "cba/components/textarea.html"

    def __init__(self, label=None, value="", error=None, rows=10, *args, **kwargs):
        super(TextArea, self).__init__(*args, **kwargs)
        self.error = error
        self.label = label
        self.rows = rows
        self.value = value

    def clear(self):
        """Sets the value an error to empty strings..
        """
        self.value = ""
        self.error = ""


class TextInput(Component):
    """An HTML text input.

        error
            The current validation error of the text input.

        icon
            An optional icon of the text input, see http://semantic-ui.com/elements/icon.html
            for more.

        icon_position
            The position of the icon (one of ``left`` or ``right``).

        label
            An optional label of the text input.

        placeholder
            The optional placeholder of the text input. If given it is
            displayed within the input field.

        value
            The current value of the text input.
    """
    template = "cba/components/text_input.html"

    def __init__(self, id=None, value="", label=None, placeholder=None, error=None, icon=None, icon_position="left", *args, **kwargs):
        super(TextInput, self).__init__(id, *args, **kwargs)
        self.error = error
        self.icon = icon
        self.icon_position = icon_position
        self.label = label
        self.placeholder = placeholder
        self.value = value

    def clear(self):
        """Sets the value and error messages to empty strings.
        """
        self.error = ""
        self.value = ""
