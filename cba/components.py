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


class Checkbox(Component):
    """A HTML checkbox.

        label
            The label of the checkbox

        type
            The type of the checkbox. One of None, "toggle", "slider".
    """
    template = "cba/components/checkbox.html"

    def __init__(self, checked=False, label="", type=None, value="", *args, **kwargs):
        super(Checkbox, self).__init__(*args, **kwargs)
        self.label = label
        self.type = type
        self.checked = checked
        self.value = value


class CheckboxGroup(Component):
    """A group of checkboxes.

        label
            The label of the checkbox
    """
    template = "cba/components/checkbox_group.html"

    def __init__(self, label=None, *args, **kwargs):
        super(CheckboxGroup, self).__init__(*args, **kwargs)
        self.label = label
        self.value = None


class ConfirmModal(Component):
    """A convenient modal dialog with a ``yes`` and ``no`` button. When the
       dialog is answered with ``yes`` the handler method is called via an ajax
       request.

        event_id
            The event_id, which is passed to the backend, when the dialog has
            been answered with yes.

        handler
            The method, which is called, when the dialog has been answered with
            yes.

        header
            The header of the dialog.

        text
            The text of the dialog.
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

    Args:
        error (string)
            The current validation error of the text input.

        existing_files (list of File instances)
            A list of existing files which will be displayed for optional
            deletion. The file instances must have an ``id`` and an ``url``
            attribute.

        icon
            An optional icon of the text input, see http://semantic-ui.com/elements/icon.html
            for more.

        icon_position
            The position of the icon (one of ``left`` or ``right``).

        label
            An optional label of the text input.

        multiple
            If true multiple files can be uploaded at once.

        to_delete
            The file ids which are marked as to be deleted.

        value
            The current selected value(s) of the select box. A string  when
            ``multiple`` is False, otherwise a list.
    """
    template = "cba/components/file_input.html"

    def __init__(self, id=None, error=None, existing_files=None, icon=None,
                 icon_position="left", label=None, multiple=False, to_delete=None,
                 value="", *args, **kwargs):
        super(FileInput, self).__init__(id, *args, **kwargs)
        self.error = error
        self.existing_files = existing_files or []
        self.icon = icon
        self.icon_position = icon_position
        self.label = label
        self.multiple = multiple
        self.to_delete = to_delete or []
        self.value = value

    def clear(self):
        """Sets the value and error messages to empty strings.
        """
        self.error = None
        self.value = ""
        self.to_delete = None
        self.existing_files = []


class Group(Component):
    """A simple group component to arrange compontens together. For instance for
    styling reasons or to easier refresh its sub components.

        tag
            Optional tag, which is, when given, wrapped around every sub
            component.
    """
    template = "cba/components/group.html"

    def __init__(self, tag=None, *args, **kwargs):
        super(Group, self).__init__(*args, **kwargs)
        self.tag = tag

    def clear(self):
        """Deletes all sub components.
        """
        self._components.clear()


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

    def __init__(self, tag="div", content="", *args, **kwargs):
        super(HTML, self).__init__(*args, **kwargs)
        self.tag = tag
        self.content = content


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

        href
            The href of the link.

        target
            The target of the link.
    """
    template = "cba/components/link.html"

    def __init__(self, href=".", target=None, text="", *args, **kwargs):
        super(Link, self).__init__(*args, **kwargs)
        self.href = href
        self.target = target
        self.text = text


class List(Component):
    """The root container of a pop up menu.

        type
            The type of the list. One of ``ul`` or ``ol``.

    """
    template = "cba/components/list.html"

    def __init__(self, type="ul", *args, **kwargs):
        super(List, self).__init__(*args, **kwargs)
        self.type = type


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


class RadioCheckbox(Component):
    """A radio checkboxes.

        label
            The label of the checkbox
    """
    template = "cba/components/radio_checkbox.html"

    def __init__(self, checked=False, label="", name="", value="", *args, **kwargs):
        super(RadioCheckbox, self).__init__(*args, **kwargs)
        self.checked = checked
        self.label = label
        self.value = value


class RadioCheckboxGroup(Component):
    """A group of radio checkboxes.

        label
            The label of the checkbox
    """
    template = "cba/components/radio_checkbox_group.html"

    def __init__(self, label=None, *args, **kwargs):
        super(RadioCheckboxGroup, self).__init__(*args, **kwargs)
        self.label = label
        self.value = None


class Select(Component):
    """A HTML Select box.

    Args:
        allow_additions (boolean)
            If true, the user is allowed to add new entries.

        label (string)
            An optional label for the select box.

        multiple (boolean)
            if true multiple selections are possible.

        options (list)
            Options which can be selected.

        value (string or list)
            The current selected value(s) of the select box. A string  when
            ``multiple`` is False, otherwise a list. These can be set
            programmatically or by the browser.
    """
    template = "cba/components/select.html"

    def __init__(self, id=None, allow_additions=False, label=None, multiple=False, options=None, value=None, *args, **kwargs):
        super(Select, self).__init__(id, *args, **kwargs)
        self.allow_additions = allow_additions
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

        headers
            A list of strings which represent the header of the table.

        label
            An option label of the table.
    """
    template = "cba/components/table.html"

    def __init__(self, headers, pagination=10, page=1, label=None, selected=None, *args, **kwargs):
        self.headers = headers
        self.label = label
        self.page = page
        self.pagination = pagination
        super(Table, self).__init__(*args, **kwargs)

    def after_initial_components(self):
        range = self.get_range(1)
        self.load_data(range["start"], range["end"])

    def load_data(self, start, end):
        self.clear()
        for row in self.get_data(start=start, end=end):
            table_row = TableRow()
            for column in row:
                if isinstance(column, Component):
                    table_column = TableColumn(initial_components=[column])
                else:
                    table_column = TableColumn(content=column)
                table_row.add_component(table_column)

            self.add_component(table_row)

    def has_pagination(self):
        return (self.get_count() / self.pagination) > 1

    def set_page(self, page):
        self.page = page
        range = self.get_range(page)
        self.load_data(range["start"], range["end"])
        self.refresh()

    def clear(self):
        """Deletes all rows of the table.
        """
        self._components.clear()

    def get_pages_range(self):
        return range(1, self.get_count() / self.pagination)

    def get_range(self, page):
        start = self.pagination * (page-1)
        end = self.pagination * page + 1
        return {"start": start, "end": end}

    def has_previous(self):
        return self.page > 1

    def has_next(self):
        return self.page < ((self.get_count() / self.pagination) - 1)

    def handle_pagination(self):
        if self.component_value == "next":
            page = self.page + 1
        elif self.component_value == "previous":
            page = self.page - 1
        else:
            page = int(self.component_value)

        self.set_page(page)


class TableRow(Component):
    """A table row.
    """
    template = "cba/components/table_row.html"


class TableColumn(Component):
    """A table column.
    """
    template = "cba/components/table_column.html"

    def __init__(self, content="", *args, **kwargs):
        super(TableColumn, self).__init__(*args, **kwargs)
        self.content = content


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


class Textarea(Component):
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
        super(Textarea, self).__init__(*args, **kwargs)
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

    def __init__(self, id=None, value="", label=None, placeholder=None, error=None, icon=None, icon_position="right", *args, **kwargs):
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
